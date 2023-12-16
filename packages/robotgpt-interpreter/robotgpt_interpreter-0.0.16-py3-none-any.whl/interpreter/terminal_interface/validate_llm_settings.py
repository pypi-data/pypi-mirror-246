import getpass
import os
import time

from .display_markdown_message import display_markdown_message

def validate_llm_settings(interpreter):
    """
    Interactively prompt the user for required LLM settings
    """

    # This runs in a while loop so `continue` lets us start from the top
    # after changing settings (like switching to/from local)
    while True:
        if interpreter.local:
            # We have already displayed a message.
            # (This strange behavior makes me think validate_llm_settings needs to be rethought / refactored)
            break

        else:
            # Ensure API tokens are set as environment variables

            # OpenAI
            if not os.environ.get("ROBOTGPT_API_TOKEN") and not interpreter.api_key:
                display_welcome_message_once()

                display_markdown_message(
                    """---
                > OpenAI API token not found

                To use `GPT-4` (highly recommended) please provide an OpenAI API token.

                To use another language model, consult the documentation at [docs.openinterpreter.com](https://docs.openinterpreter.com/language-model-setup/).
                
                ---
                """
                )

                response = getpass.getpass("OpenAI API token: ")
                print(f"OpenAI API token: {response[:4]}...{response[-4:]}")

                display_markdown_message(
                    """

                **Tip:** To save this key for later, run `export ROBOTGPT_API_TOKEN=your_api_token` on Mac/Linux or `setx ROBOTGPT_API_TOKEN your_api_token` on Windows.
                
                ---"""
                )

                interpreter.api_key = response
                time.sleep(2)
                break

            # This is a model we don't have checks for yet.
            break

    # If we're here, we passed all the checks.

    # Auto-run is for fast, light useage -- no messages.
    # If local, we've already displayed a message.
    if not interpreter.auto_run and not interpreter.local:
        display_markdown_message(f"> Model set to `{interpreter.model}`")
    return


def display_welcome_message_once():
    """
    Displays a welcome message only on its first call.

    (Uses an internal attribute `_displayed` to track its state.)
    """
    if not hasattr(display_welcome_message_once, "_displayed"):
        display_markdown_message(
            """
        ●

        Welcome to **RobotGPT Interpreter**.
        """
        )
        time.sleep(1.5)

        display_welcome_message_once._displayed = True
