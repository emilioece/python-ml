from os import getenv 
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = getenv('OPENAI_API_KEY')