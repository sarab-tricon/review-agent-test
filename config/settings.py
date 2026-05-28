import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "qwen/qwen3-32b"
MAX_ITERATIONS = 10  # Max loop iterations before stopping
TIMEOUT = 30  # Max wait time in seconds
