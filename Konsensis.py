import os
import click  # type: ignore
import openai  # type: ignore
from anthropic import Anthropic  # type: ignore
from dotenv import load_dotenv  # type: ignore
import cohere  # type: ignore

# Load environment variables
load_dotenv()


def get_api_key(api_name):
    """Fetches API key for a specified service from environment variables."""
    return os.getenv(api_name)


def call_model(api_name, api_key, model, system_prompt, user_prompt):
    if api_name == "OPENAI":
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            api_key=api_key,  # Pass the API key directly to the method
        )
        return response.choices[0].message["content"].strip()
    elif api_name == "ANTHROPIC":
        anthropic_client = Anthropic(api_key=api_key)
        response = anthropic_client.messages.create(
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            model=model,
        )
        if isinstance(response.content, list) and response.content:
            first_content_item = response.content[0]
            if hasattr(first_content_item, "text"):
                return first_content_item.text.strip()
            else:
                return "TextBlock does not have a 'text' attribute"
        else:
            return "Unexpected content format in response or empty content"
    elif api_name == "COHERE":
        cohere_client = cohere.Client(api_key)
        response = cohere_client.chat(
            model=model,
            chat_history=[
                {"role": "system", "message": system_prompt},
                {"role": "user", "message": user_prompt},
            ],
            message=user_prompt,
        )
        return response.text.strip()  # Correctly accessing the 'text' attribute


def is_numeric(s):
    """Checks if a string is numeric."""
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_model_choice(input_str):
    """Parses user input to determine models to use."""
    choices = input_str.split(",")
    models = []
    for choice in choices:
        if choice.strip() == "1":
            models.append("OPENAI")
        elif choice.strip() == "2":
            models.append("ANTHROPIC")
        elif choice.strip() == "3":
            models.append("COHERE")
    return models


@click.command()
@click.option(
    "--models",
    default="1,2,3",
    help='Choose models to use: OpenAI is 1, Anthropic is 2, Cohere is 3 (use "1,2,3" for all).',
)
@click.option("--recursive", is_flag=True, help="Enable recursive mode.")
@click.option(
    "--threshold", default=50, type=int, help="Enter a quality threshold (1-100)."
)
@click.option(
    "--initial_prompt",
    default="You are a helpful assistant",
    help="Enter an Initial System Prompt.",
)
@click.argument("user_question")
def main(models, recursive, threshold, initial_prompt, user_question):
    openai_api_key = get_api_key("OPENAI_API_KEY")
    anthropic_api_key = get_api_key("ANTHROPIC_API_KEY")
    cohere_api_key = get_api_key("COHERE_API_KEY")  # New API key for Cohere

    model_list = parse_model_choice(models)
    evaluation_system_prompt = f"As an expert, thoroughly interpret this answer and grade it on a scale of 1-100. If it is above {threshold}, only return that number and no other information. Again, if the score is above the threshold, only return a single integer and no other text. If it is below that threshold, rewrite the answer to get it above {threshold}."

    last_text_response = user_question
    current_model_index = 0

    while True:
        system_prompt = (
            initial_prompt
            if last_text_response == user_question
            else evaluation_system_prompt
        )
        model_api = model_list[current_model_index]
        api_key = (
            openai_api_key
            if model_api == "OPENAI"
            else (anthropic_api_key if model_api == "ANTHROPIC" else cohere_api_key)
        )
        model_name = (
            "gpt-4-0125-preview"
            if model_api == "OPENAI"
            else (
                "claude-3-opus-20240229"
                if model_api == "ANTHROPIC"
                else "command-r-plus"
            )
        )
        response = call_model(
            model_api, api_key, model_name, system_prompt, last_text_response
        )
        print(f"Response from {model_api}:", response)

        if is_numeric(response):
            score = float(response)
            if score >= threshold:
                print(f"Final response meets threshold: {score}")
                print("Accepted answer:", last_text_response)
                break
        else:
            last_text_response = response

        current_model_index = (
            (current_model_index + 1) % len(model_list)
            if not recursive
            else current_model_index
        )


if __name__ == "__main__":
    main()