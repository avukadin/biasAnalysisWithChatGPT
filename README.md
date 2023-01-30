This code accompanies the white paper "Is the CBC a Neutral Voice in Canadian Politics?".

The final results used in the paper are in the `data/results.csv` file.

### Code Outline
Below is an explination of the main files. Note that mose code is written in python, except for `get_chat_gpt_response.js` which is javascript. At time of writting, OpenAI does not have a API for ChatGPT the most convenient workaround was to use a javascript library. There is also the option of using `text-davinci-003` which produces very similar results to ChatGPT.

1) `get_article_links.py` will grab article links from Google News RSS feed for articles published on cbc.ca/news and save them to `data/links` folder
2) `get_articles.py` will scrape cbc.ca/news site for the full articles and save them to `data/articles.csv`
3) `extract_snippets.py` will extract the article excerpts used for feeding into ChatGPT
4) `classify_articles.py` will query `text-davinci-003` for classifying articles and save results to `data/results.csv`. To query ChatGPT instead, use node to run `get_chat_gpt_response.js`, this is not 100% complete as it will nto save to csv, instead print responses to console. This will be updated once an official API is released for ChatGPT.


[White Papre- Is the CBC a neutral voice in Canadian politics? - Alex Vukadinovic.pdf](https://github.com/avukadin/biasAnalysisWithChatGPT/files/10538751/White.Papre-.Is.the.CBC.a.neutral.voice.in.Canadian.politics.-.Alex.Vukadinovic.pdf)
