import os
from datetime import datetime

from dotenv import load_dotenv

TERMS = ["Pierre Poilievre", "Justin Trudeau", "Jagmeet Singh"]
QUESTIONS = [
        "Does this news show {term} in a positive, negative or neutral way? Answer in one word."]
FULL_INPUT = '''
{question}

NEWS SNIPPET: {snippet}
ANSWER:'''

SOURCE = "cbc.ca/news"

START_DATE = datetime(2022,1,1)
END_DATE = datetime(2023,1,14)
QUERY_DAYS = 7
CONTEXT_WORDS = 50

load_dotenv()
API_KEY = os.environ.get("API_KEY")
print(API_KEY)

