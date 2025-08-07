import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.get_files_info import schema_get_giles_info


def main():
    is_verbose = False
    if "--verbose" in sys.argv:
        is_verbose = True
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) < 2:
        print("Prompt was not provided.")
        sys.exit(1)

    model_name = "gemini-2.0-flash-001"  # Replace with your desired model name
    user_prompt = sys.argv[1]
    system_prompt = """
    You are a helpful AI coding  agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your fucntion call as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_giles_info,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if is_verbose:
        print(f"User prompt: {user_prompt} \n")
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)
    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
