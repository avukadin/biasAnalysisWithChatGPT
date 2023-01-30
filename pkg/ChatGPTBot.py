import time
from datetime import datetime, timedelta

import numpy as np
import openai


class ChatGPTBot():

    MAX_FAILS = 3
    ANSWERS = {"positive", "negative", "neutral"}

    query_delay:int
    _last_query:datetime

    def __init__(self, api_key:str, query_delay:int):
        openai.api_key = api_key 

        self.query_delay = query_delay
        self._last_query = datetime.now() - timedelta(seconds=query_delay)

    def _query(self, text:str):
        time_since_last = (datetime.now() - self._last_query).seconds

        for i in range(1, self.MAX_FAILS+1):
            if time_since_last<self.query_delay:
                time.sleep(self.query_delay - time_since_last)
            try:
                response = openai.Completion.create(
                  model="text-davinci-003",
                  prompt=text,
                  temperature=0,
                  max_tokens=1,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0,
                  logprobs=5
                ) 
                self._last_query = datetime.now()
                break
            except openai.error.OpenAIError as e:
                print(f"Query error: {e}")
                if i>=self.MAX_FAILS:
                    raise
                print(f"Retry {i}/{self.MAX_FAILS} in {self.query_delay}s.")

        return response

    def query(self, text:str):
        response = self._query(text)
        return self.extract_answers(response)

    def extract_answers(self, response):
        log_probs = response["choices"][0]["logprobs"]["top_logprobs"][0]

        # Extract logprobs
        answers = []
        answers_certainty = []
        for k, v in log_probs.items():
            choice = k.lower().strip()
            if choice in self.ANSWERS:
                answers.append(choice)
                answers_certainty.append(v)

        answers_certainty = np.exp(answers_certainty)/(np.sum(np.exp(answers_certainty)))

        # Combine any duplicates
        answers_map = {a:0 for a in self.ANSWERS}
        for a,c in zip(answers, answers_certainty):
            answers_map[a] += c

        # Sort
        answers_map = {k: v for k, v in sorted(answers_map.items(), key=lambda item: -item[1])}
        answers = [a for a in answers_map.keys()]
        answers_certainty = [str(round(100*c,1)) + "%" for c in answers_map.values()]

        return answers, answers_certainty