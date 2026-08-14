import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("TMDB_API_KEY"))