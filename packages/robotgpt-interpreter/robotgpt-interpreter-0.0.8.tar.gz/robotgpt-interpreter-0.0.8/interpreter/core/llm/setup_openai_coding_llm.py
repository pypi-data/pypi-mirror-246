# RobotGPT Python bindings.
# 张圣涛 blaze.zhang
import json
import uuid
import requests
import tokentrim as tt
from typing import Callable, List, Optional, Dict
from ...terminal_interface.utils.display_markdown_message import (
    display_markdown_message,
)
from ..utils.convert_to_openai_messages import convert_to_openai_messages
from ..utils.merge_deltas import merge_deltas
from ..utils.parse_partial_json import parse_partial_json

function_schema = {
    "name": "execute",
    "description": "Executes code on the user's machine, **in the users local environment**, and returns the output",
    "parameters": {
        "type": "object",
        "properties": {
            "language": {
                "type": "string",
                "description": "The programming language (required parameter to the `execute` function)",
                "enum": [
                    # This will be filled dynamically with the languages OI has access to.
                ],
            },
            "code": {"type": "string", "description": "The code to execute (required)"},
        },
        "required": ["language", "code"],
    },
}


def setup_openai_coding_llm(interpreter):
    """
    Takes an Interpreter (which includes a ton of LLM settings),
    returns a OI Coding LLM (a generator that takes OI messages and streams deltas with `message`, `language`, and `code`).
    """

    def coding_llm(messages):
        # Convert messages
        messages = convert_to_openai_messages(
            messages, function_calling=True, vision=interpreter.vision
        )

        # Add OpenAI's recommended function message
        messages[0][
            "content"
        ] += "\n\nOnly use the function you have been provided with."

        # Seperate out the system_message from messages
        # (We expect the first message to always be a system_message)
        system_message = messages[0]["content"]
        messages = messages[1:]

        # Trim messages, preserving the system_message
        try:
            messages = tt.trim(
                messages=messages,
                system_message=system_message,
                model=interpreter.model,
            )
        except:
            if interpreter.context_window:
                messages = tt.trim(
                    messages=messages,
                    system_message=system_message,
                    max_tokens=interpreter.context_window,
                )
            else:
                if len(messages) == 1:
                    display_markdown_message(
                        """
                    **We were unable to determine the context window of this model.** Defaulting to 3000.
                    If your model can handle more, run `interpreter --context_window {token limit}` or `interpreter.context_window = {token limit}`.
                    """
                    )
                messages = tt.trim(
                    messages=messages, system_message=system_message, max_tokens=3000
                )

        if interpreter.debug_mode:
            print("Sending this to the OpenAI LLM:", messages)

        # Add languages OI has access to
        function_schema["parameters"]["properties"]["language"][
            "enum"
        ] = interpreter.languages

        if interpreter.temperature is None:
            interpreter.temperature = 0.0

        headers = {"Content-Type": "application/json"}
        headers["ApiName"] = "robotGptLLMApi"
        headers["Model"] = interpreter.model
        headers["Authorization"] = interpreter.api_key
        r_url = interpreter.api_base
        requestdata = {
            "id": str(uuid.uuid4()),
            "messages": messages,
            "temperature": interpreter.temperature,
            "max_tokens": interpreter.max_tokens,
            "stream": True,
            "functions": [function_schema],
        }
        response = requests.post(url=r_url, headers=headers, json=requestdata, stream=True)
        # Parse response

        accumulated_deltas = {}
        language = None
        code = ""
        old_str = b""
        for line in response:
            old_str += line
            if line.rfind(b"}\n\n") != -1:
                line_arr = old_str.split(b'\n\n')
                old_str = b""
                for line_new in line_arr:
                    if line_new.startswith(b"data: [DONE]"):
                        break
                    if line_new == b"" or not line_new.endswith(b'}'):
                        old_str = line_new
                        break

                    if line_new.startswith(b"data: "):
                        line_new = line_new[len(b"data: "):]

                    line_new = line_new.decode("utf-8").strip()
                    chunk = json.loads(line_new)
                    if "choices" not in chunk or len(chunk["choices"]) == 0:
                        # This happens sometimes
                        continue
                    delta = chunk["choices"][0]["message"]

                    # Accumulate deltas
                    accumulated_deltas = merge_deltas(accumulated_deltas, delta)

                    if "content" in delta and delta["content"]:
                        yield {"type": "message", "content": delta["content"]}

                    if (
                        "function_call" in accumulated_deltas
                        and "arguments" in accumulated_deltas["function_call"]
                    ):
                        if (
                            "name" in accumulated_deltas["function_call"]
                            and accumulated_deltas["function_call"]["name"] == "execute"
                        ):
                            arguments = accumulated_deltas["function_call"]["arguments"]
                            arguments = parse_partial_json(arguments)

                            if arguments:
                                if (
                                    language is None
                                    and "language" in arguments
                                    and "code"
                                    in arguments  # <- This ensures we're *finished* typing language, as opposed to partially done
                                    and arguments["language"]
                                ):
                                    language = arguments["language"]

                                if language is not None and "code" in arguments:
                                    # Calculate the delta (new characters only)
                                    code_delta = arguments["code"][len(code) :]
                                    # Update the code
                                    code = arguments["code"]
                                    # Yield the delta
                                    if code_delta:
                                        yield {
                                            "type": "code",
                                            "format": language,
                                            "content": code_delta,
                                        }
                            else:
                                if interpreter.debug_mode:
                                    print("Arguments not a dict.")

                        # Common hallucinations
                        elif "name" in accumulated_deltas["function_call"] and (
                            accumulated_deltas["function_call"]["name"] == "python"
                            or accumulated_deltas["function_call"]["name"] == "functions"
                        ):
                            if interpreter.debug_mode:
                                print("Got direct python call")
                            if language is None:
                                language = "python"

                            if language is not None:
                                # Pull the code string straight out of the "arguments" string
                                code_delta = accumulated_deltas["function_call"]["arguments"][
                                    len(code) :
                                ]
                                # Update the code
                                code = accumulated_deltas["function_call"]["arguments"]
                                # Yield the delta
                                if code_delta:
                                    yield {
                                        "type": "code",
                                        "format": language,
                                        "content": code_delta,
                                    }

                        else:
                            # If name exists and it's not "execute" or "python" or "functions", who knows what's going on.
                            if "name" in accumulated_deltas["function_call"]:
                                print(
                                    "Encountered an unexpected function call: ",
                                    accumulated_deltas["function_call"],
                                )
                            else:
                                if interpreter.debug_mode:
                                    print("No name in function_call.")
    return coding_llm

