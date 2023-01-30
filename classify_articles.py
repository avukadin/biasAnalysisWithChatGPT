import json
import time
from random import random

import pandas as pd

import parameters
from pkg.ChatGPTBot import ChatGPTBot

if __name__ == "__main__":
    
    df = pd.read_csv("./data/articles_snippets.csv")

    save_data = {"links":[], "terms":[], "snippets":[]}
    for i in range(len(parameters.QUESTIONS)):
        save_data[f"question {i+1}"] = []
        save_data[f"response {i+1}"] = []
        save_data[f"response confidence {i+1}"] = []
    
    cgpt = ChatGPTBot(parameters.API_KEY, query_delay=3)
    start_time  = time.time()

    count = 0
    rep = 1
    for row in df.iterrows():
        count += 1
        term = row[1]["terms"]
        snippet = row[1]["snippets"]
        link = row[1]["links"]

        save_data["terms"].append(term)
        save_data["snippets"].append(snippet)
        save_data["links"].append(link)

        for i, q in enumerate(parameters.QUESTIONS):
            question = q.format(term=term)
            input_value = parameters.FULL_INPUT.format(
                question=question,
                snippet=snippet
                )
            answers, answers_certainty = cgpt.query(input_value)

            save_data[f"question {i+1}"].append(question)
            save_data[f"response {i+1}"].append(' '.join(answers))
            save_data[f"response confidence {i+1}"].append(' '.join(answers_certainty))
        complete = round(100*count/len(df))
        if complete>=rep:
           time_elapsed = (time.time() - start_time)/60
           time_left = round((len(df)-count)*(time_elapsed/count),1)
           print(f"Completed: {complete}, minutes left: {time_left}")
           rep += 1

        
        
        pd.DataFrame(save_data).to_csv("./data/results.csv", index=False)
