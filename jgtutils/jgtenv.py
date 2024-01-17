import os
import sys
from dotenv import load_dotenv


def get_openai_key():
    """Reads the OpenAI API key from the environment or a .env file."""
    
    dotenv_path = os.path.join(os.path.expanduser("~"), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables or .env file."
        )
    return api_key
