from dotenv import load_dotenv  # For loading environment variables from a .env file.
import os  # Provides functionality to interact with the operating system.
import time  # Used to add delays between retries.
import json  # To handle JSON data structures.
import anthropic  # SDK for interacting with Anthropic's Claude models.
import openai  # SDK for interacting with OpenAI's models (e.g., GPT models).
from mistralai import Mistral  # SDK for interacting with Mistral models.

# Load environment variables from a .env file into the application's environment.
load_dotenv()

# Initialize the Anthropic API client with an API key fetched from the environment variables.
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

# Initialize OpenAI's API key for authentication.
openai.api_key = os.getenv("OPENAI_API_KEY", "")

# Initialize the Mistral API client with an API key fetched from the environment variables.
mistral = Mistral(api_key=os.getenv("MISTRAL_API_KEY", ""))

# Function to interact with OpenAI's GPT models.
def prompt_openai(prompt, model="gpt-4o", max_tokens=16384, temperature=0):
    num_retries = 3  # Maximum number of retry attempts.

    while num_retries >= 0:
        try:
            # Call OpenAI's chat completion API.
            res = openai.chat.completions.create(
                model=model,  # Specify the model.
                max_tokens=max_tokens,  # Limit on the number of tokens in the response.
                temperature=temperature,  # Controls randomness in the response.
                messages=[
                    # System message sets the role and context for the assistant.
                    {"role": "system", "content": "You are UX Copilot, a professional UX mentor specializing in solving usability issues and enhancing the overall user experience. You provide expert guidance, offer actionable insights, and help users understand the nuances of UX design. Focus on practical solutions and stay updated with the latest UX trends and best practices."},
                    # User's input message.
                    {"role": "user", "content": prompt}
                ]
            )
            
            if res != None:  # Ensure a valid response was returned.
                text = res.choices[0].message.content  # Extract the generated content.
                # Strip unnecessary formatting from the response.
                text = text.strip("```").strip("json").strip("python")
                print(text)  # Log the response for debugging.
                return text  # Return the cleaned response text.
        except Exception as e:
            # Log any exceptions that occur during the API call.
            print(f"An error occurred: {e}")
        time.sleep(0.1)  # Short delay before retrying.
        num_retries = num_retries - 1  # Decrement the retry counter.

    return None  # Return None if all retries fail.

# Function to interact with Mistral's models.
def prompt_mistral(prompt, model="mistral-large-latest", max_tokens=7900, temperature=0):
    num_retries = 3  # Maximum number of retry attempts.

    while num_retries >= 0:
        try:
            # Call Mistral's chat completion API.
            res = mistral.chat.complete(
                model=model,  # Specify the model.
                max_tokens=max_tokens,  # Limit on the number of tokens in the response.
                temperature=temperature,  # Controls randomness in the response.
                messages=[
                    {"content": prompt, "role": "user"}  # User's input message.
                ],
            )
            
            if res != None:  # Ensure a valid response was returned.
                text = res.choices[0].message.content  # Extract the generated content.
                # Strip unnecessary formatting from the response.
                text = text.strip("dm").strip("```").strip("json").strip("python")
                print(text)  # Log the response for debugging.
                return text  # Return the cleaned response text.
        except Exception as e:
            # Log any exceptions that occur during the API call.
            print(f"An error occurred: {e}")
        time.sleep(0.1)  # Short delay before retrying.
        num_retries = num_retries - 1  # Decrement the retry counter.

    return None  # Return None if all retries fail.

# Function to interact with Anthropic's Claude models.
def prompt_claude(prompt, model="claude-3-5-sonnet-20240620", max_tokens=7900, temperature=0):
    num_retries = 3  # Maximum number of retry attempts.

    while num_retries >= 0:
        try:
            # Call Claude's API to create a message.
            message = claude.messages.create(
                model=model,  # Specify the model.
                temperature=temperature,  # Controls randomness in the response.
                max_tokens=max_tokens,  # Limit on the number of tokens in the response.
                messages=[
                    {"role": "user", "content": prompt}  # User's input message.
                ]
            )
            
            if message != None:  # Ensure a valid response was returned.
                text = message.content[0].text  # Extract the generated content.
                # Strip unnecessary formatting from the response.
                text = text.strip("```").strip("json").strip("python")
                print(text)  # Log the response for debugging.
                return text  # Return the cleaned response text.
        except Exception as e:
            # Log any exceptions that occur during the API call.
            print(f"An error occurred: {e}")
        time.sleep(1.0)  # Longer delay before retrying.
        num_retries = num_retries - 1  # Decrement the retry counter.

    return None  # Return None if all retries fail.

# Main prompt function that routes requests to the appropriate LLM based on the `llm` parameter.
def prompt(instructions, llm):
    if llm == "gpt-4o":  # For OpenAI's GPT-4o model.
        return prompt_openai(instructions, model="gpt-4o")
    if llm == "gpt-4o-mini":  # For OpenAI's GPT-4o-mini model.
        return prompt_openai(instructions, model="gpt-4o-mini")
    if llm == "gpt-3.5-turbo":  # For OpenAI's GPT-3.5 model.
        return prompt_openai(instructions, model="gpt-3.5-turbo", max_tokens=4000)
    if llm == "mistral-large-latest":  # For Mistral's large model.
        return prompt_mistral(instructions, model="mistral-large-latest", max_tokens=7900)
    if llm == "mistral-small-latest":  # For Mistral's small model.
        return prompt_mistral(instructions, model="mistral-small-latest", max_tokens=4000)

def translate_util(sentence, source, destination, llm):
    num_retries = 3
    while num_retries >= 0:
        try:

            instructions = f"""
                Translate the followng sentence from {source} to {destination}: The sentence is as follows: {sentence} .
                Respond only with the translation.
            """
            instructions = instructions.strip()
                
            res = {
                "translation": prompt(instructions, llm)
            }

            if res["translation"] != None:
                print(res)
                return res
            break
        except Exception as e:
            # Print the exception
            print(f"An error occurred: {e}")
        time.sleep(1.0)
        num_retries = num_retries - 1