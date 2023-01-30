import json
import os
import time
from random import random

import pandas as pd
import requests
from bs4 import BeautifulSoup


class CBCNewsScraper():
    article_links:set[str] = set()

    def __init__(self, link_files:list[str]):
        self._load_links(link_files)

    def _load_links(self, link_files:list[str]):
        print("Loaded articles links from:")

        captured = set()
        if os.path.exists("./data/articles.csv"):
            [captured.add(v) for v in  pd.read_csv("./data/articles.csv").links] 

        for file in link_files:
            df = pd.read_csv(file)
            [self.article_links.add(v) for v in df.links if v not in captured]
            print(file)

        print(f"Total of {len(self.article_links)} unique articles.")

    @staticmethod
    def get_content(body:list, txt:list):
        for b in body:
            data = b.get('content', [])
            if type(data) == list:
                CBCNewsScraper.get_content(data, txt)
            elif type(data) == str:
                data = data.replace('\xa0', ' ')
                data = data.replace('—', '-')
                data = data.replace('&nbsp;', ' ')
                data = data.replace('\n', ' ')
                data = ' '.join(data.split())
                txt.append(data)

    def run(self):
        failed = 0
        count = 0
        rep = 1
        t0 = time.time()
        if os.path.exists("./data/articles.csv"):
            print("Collecting articles from checkpoint: ./data/articles.csv")
            df = pd.read_csv("./data/articles.csv")
        else:
            print("Collecting articles...")
            df = pd.DataFrame({'links':[], 'articles':[]})

        for link in self.article_links:
            count += 1
            time.sleep(random()*5+3) # sleep seconds to avoid being blocked
           
            for i in range(3):
                try:
                    headers = {"Content-Type": "text/html; charset=utf-8"}
                    response = requests.get(link, timeout=60, headers=headers)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    if i == 2:
                        raise
                    print(f"Error making request on {link}, will retry in 5s.")
                    print(e)
                    time.sleep(5)

            soup = BeautifulSoup(response.text, "html.parser")
            scripts = soup.find_all("script", {"id": "initialStateDom"})

            if len(scripts)!=1:
                print(f"Failed to load json data for {link}")
                failed += 1
                continue
            
            # Parse the json data returned in the script tag
            data = scripts[0].get_text()
            data = data.replace("window.__INITIAL_STATE__ = ", "")[0:-1]
            try:
                json_data = json.loads(data)
            except:
                print(f"Failed to load json data for {link}")
                failed += 1
                continue

            body = json_data.get("detail", {}).get("content", {}).get("body", [])

            txt = []
            self.get_content(body, txt)

            txt_str = ' '.join(' '.join(txt).split()) # Remove multiple white spaces
            df = pd.concat([df, pd.DataFrame({'links':[link], "articles":[txt_str]})])
            df.to_csv("./data/articles.csv", index=False)
            
            # Progress print out
            completed = round(100*count/len(self.article_links),1)
            if completed>=rep:
                seconds_left = (len(self.article_links)-count)*((time.time() - t0)/count)
                minutes_left = round(seconds_left/60,1)
                print(f"Completed: {count} of {len(self.article_links)} ({completed}%). Minutes Remaining: {minutes_left}")
                rep += 1

        print(f"Total Failed: {failed}")





            
            
