import os
from config import MAX_CHARS

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
# os.path.abspath: Get an absolute path from a relative path
# os.path.join: Join two paths together safely (handles slashes)
# .startswith: Check if a string starts with a specific substring
# os.path.isfile: Check if a path is a file