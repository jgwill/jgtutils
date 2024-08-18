import os
import sys

from dotenv import load_dotenv

from jgtcliconstants import JGT_ENV_EXPORT_NAME, JGT_SUBDIR_NAME



def get_jgt_env_export_path(in_jgt_subdir=False):
    
    if in_jgt_subdir:
      jgt_export_directory = os.path.join(os.getcwd(),JGT_SUBDIR_NAME)
      os.makedirs(jgt_export_directory, exist_ok=True)#|print(f"Directory {subdir} created")
    else :
      jgt_export_directory = os.getcwd()
      
    batch_file_path = os.path.join(jgt_export_directory,JGT_ENV_EXPORT_NAME)
    return batch_file_path
  
def get_openai_key():
    """Reads the OpenAI API key from the environment or a .env file."""

    # Define the possible locations for the .env file
    dotenv_paths = [
      os.path.join(os.path.dirname(__file__), '..', '.env'),  # Parent directory
      os.path.join(os.path.dirname(__file__), '..', '..', '.env'),  # Grandparent directory
      os.path.join(os.path.expanduser("~"), ".env"),  # Home directory
    ]

    # Try to load the .env file from the possible locations
    for dotenv_path in dotenv_paths:
      if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        break

    # Get the API key from the environment variables
    api_key = os.getenv("OPENAI_API_KEY")

    # Raise an error if the API key is not found
    if api_key is None:
      raise ValueError(
        "OPENAI_API_KEY not found in environment variables or .env file."
      )
    return api_key
