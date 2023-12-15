# RobotGPT Python bindings.
# 张圣涛 blaze.zhang
import os
import traceback
import uuid
import requests
import tokentrim as tt

from ...terminal_interface.display_markdown_message import (
    display_markdown_message,
)


def setup_text_llm(interpreter):
    """
    Takes an Interpreter (which includes a ton of LLM settings),
    returns a text LLM (an RobotGPT-compatible chat LLM with baked-in settings. Only takes `messages`).
    """

    # Pass remaining parameters to RobotGPT
    def base_llm(messages):
        """
        Returns a generator
        """

        system_message = messages[0]["content"]

        messages = messages[1:]

        try:
            if interpreter.context_window and interpreter.max_tokens:
                trim_to_be_this_many_tokens = (
                    interpreter.context_window - interpreter.max_tokens - 25
                )  # arbitrary buffer
                messages = tt.trim(
                    messages,
                    system_message=system_message,
                    max_tokens=trim_to_be_this_many_tokens,
                )
            elif interpreter.context_window and not interpreter.max_tokens:
                # Just trim to the context window if max_tokens not set
                messages = tt.trim(
                    messages,
                    system_message=system_message,
                    max_tokens=interpreter.context_window,
                )
            else:
                try:
                    messages = tt.trim(
                        messages, system_message=system_message, model=interpreter.model
                    )
                except:
                    if len(messages) == 1:
                        display_markdown_message(
                            """
                        **We were unable to determine the context window of this model.** Defaulting to 3000.
                        If your model can handle more, run `interpreter --context_window {token limit}` or `interpreter.context_window = {token limit}`.
                        Also, please set max_tokens: `interpreter --max_tokens {max tokens per response}` or `interpreter.max_tokens = {max tokens per response}`
                        """
                        )
                    messages = tt.trim(
                        messages, system_message=system_message, max_tokens=3000
                    )

        except TypeError as e:
            if interpreter.vision and str(e) == "expected string or buffer":
                # There's just no way to use tokentrim on vision-enabled models yet.
                if interpreter.debug_mode:
                    print("Couldn't token trim image messages. Error:", e)

                ### DISABLED image trimming
                # To maintain the order of messages while simulating trimming, we will iterate through the messages
                # and keep only the first 2 and last 2 images, while keeping all non-image messages.
                # trimmed_messages = []
                # image_counter = 0
                # for message in messages:
                #     if (
                #         "content" in message
                #         and isinstance(message["content"], list)
                #         and len(message["content"]) > 1
                #     ):
                #         if message["content"][1]["type"] == "image":
                #             image_counter += 1
                #             if (
                #                 image_counter <= 2
                #                 or image_counter
                #                 > len(
                #                     [
                #                         m
                #                         for m in messages
                #                         if m["content"][1]["type"] == "image"
                #                     ]
                #                 )
                #                 - 2
                #             ):
                #                 # keep message normal
                #                 pass
                #             else:
                #                 message["content"].pop(1)

                #         trimmed_messages.append(message)
                # messages = trimmed_messages

                # Reunite messages with system_message
                messages = [{"role": "system", "content": system_message}] + messages
            else:
                raise

        if interpreter.debug_mode:
            print("Passing messages into LLM:", messages)

        # Create RobotGPT generator
        params = {
            "model": interpreter.model,
            "messages": messages,
            "stream": True,
        }

        # Optional inputs
        if interpreter.api_base:
            params["api_base"] = interpreter.api_base
        if interpreter.api_key:
            params["api_key"] = interpreter.api_key
        if interpreter.api_version:
            params["api_version"] = interpreter.api_version
        if interpreter.max_tokens:
            params["max_tokens"] = interpreter.max_tokens
        if interpreter.temperature is None:
            interpreter.temperature = 0.0

        headers = {"Content-Type": "application/json"}
        headers["ApiName"] = "robotGptLLMApi"
        headers["Model"] = interpreter.model
        headers["Authorization"] = interpreter.api_key
        r_url = interpreter.api_base
        if r_url is None:
            r_url = "https://dataai.harix.iamidata.com/llm/api/ask"
        requestdata = {
            "id": str(uuid.uuid4()),
            "messages": messages,
            "temperature": interpreter.temperature,
            "max_tokens": interpreter.max_tokens,
            "stream": True,
        }
        return requests.post(url=r_url, headers=headers, json=requestdata, stream=True)
    return base_llm