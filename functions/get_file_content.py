import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Read the file, truncate if necessary, and return the content or an error message if any issues occur.
    try:
        with open(target_file, 'r') as f:
            content = f.read()
            if len(content) > MAX_CHARS:
                #if the file exceeds the maximum character limit, truncate it and append message to the end
                content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f'Error: reading file: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the specified directory and truncates it if it exceeds the maximum character limit, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
    ),
)