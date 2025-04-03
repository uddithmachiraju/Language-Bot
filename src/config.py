import os 
from dotenv import load_dotenv 

load_dotenv()

# OpenAI API Key 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

# Database Path
DATABASE_PATH = "db/Mistakes.db"

# Logging Configuration
LOG_FILE = "logs/app.log" 