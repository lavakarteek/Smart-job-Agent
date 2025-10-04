import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
GROQ_URL="https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL="llama-3.1-8b-instant"
SCRAPINGDOG_URL= "https://api.scrapingdog.com/linkedinjobs"
LINKEDIN_API_KEY=os.getenv("LINKEDIN_API_KEY")
THEIRSTACK_API_KEY=os.getenv("THEIRSTACK_API_KEY")