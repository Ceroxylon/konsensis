import os
from dotenv import load_dotenv
import openai
from anthropic import Anthropic

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

def get_api_key():
    """Fetches API keys for OpenAI and Anthropic from environment variables."""
    return {
        "openai": os.environ.get("OPENAI_API_KEY", ""),  # Default to empty string if not found
        "anthropic": os.environ.get("ANTHROPIC_API_KEY", "")
    }

def call_model(api_name, model, system_prompt, user_prompt):
    if api_name == 'OPENAI':
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    elif api_name == 'ANTHROPIC':
        anthropic_client = Anthropic(api_key=anthropic_api_key)
        response = anthropic_client.messages.create(
            max_tokens=1024,
            system=system_prompt,  # Set system prompt as a top-level parameter
            messages=[{"role": "user", "content": user_prompt}],
            model=model
        )
    # Check if the response contains 'content' and it's a list with at least one TextBlock
    if isinstance(response.content, list) and response.content:
        # Assuming the first item is a TextBlock object and accessing its 'text' attribute
        first_content_item = response.content[0]
        if hasattr(first_content_item, 'text'):
            return first_content_item.text.strip()  # Use attribute access for objects
        else:
            return "TextBlock does not have a 'text' attribute"
    else:
        return "Unexpected content format in response or empty content"







def is_numeric(s):
    #Checks if a string is numeric.
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_model_choice(input_str):
    # Parses user input to determine models to use.
    choices = input_str.split(',')
    models = []
    for choice in choices:
        if choice.strip() == '1':
            models.append("OPENAI")
        elif choice.strip() == '2':
            models.append("ANTHROPIC")
    return models

def main():
    api_keys = get_api_key()
    print("Available Models: 1. OpenAI 2. Anthropic")
    model_choice = input("Choose models to use (e.g., '1,2' for both): ")
    models = parse_model_choice(model_choice)
    recursive_mode = input("Enable recursive mode? (yes/no): ").lower() == 'yes'
    threshold = int(input("Enter a quality threshold (1-100): "))
    
    initial_system_prompt = input("Enter an Initial System Prompt (default is 'You are a helpful assistant'): ") or "You are a helpful assistant"
    evaluation_system_prompt = f"As an expert, thoroughly interpret this answer and grade it on a scale of 1-100. If it is above {threshold}, only return that number and no other information. Again, if the score is above the threshold, only return a single integer and no other text. If it is below that threshold, rewrite the answer to get it above {threshold}."

    user_question = input("Enter your question: ")
    last_text_response = user_question
    current_model_index = 0

    while True:
        system_prompt = initial_system_prompt if last_text_response == user_question else evaluation_system_prompt
        model_api = models[current_model_index]
        model_name = 'gpt-4-0125-preview' if model_api == 'OPENAI' else 'claude-3-opus-20240229'
        response = call_model(model_api, model_name, system_prompt, last_text_response)
        print(f"Response from {model_api}:", response)

        if is_numeric(response):
            score = float(response)
            print(f"Score received from {model_api}: {score}")  # Display the score received
            if score >= threshold:
                print(f"Final response meets threshold: {score}")
                print("Accepted answer:", last_text_response)
                break  # Exit the loop if the threshold is met
        else:
            print(f"Received text response from {model_api}, continuing interaction.")
            last_text_response = response  # Set the new response to be sent back in the next iteration

        # Switch model or keep using the same in recursive mode
        current_model_index = (current_model_index + 1) % len(models) if not recursive_mode else current_model_index


if __name__ == "__main__":
    main()