import pandas as pd

import parameters

if __name__ == "__main__":
    df = pd.read_csv("./data/articles.csv").dropna()

    def find_value(text:str, value:str, found:list, start=0):
        ndx = text[start:].find(value)
        if ndx==-1:
            return
        found.append(ndx+start)
        find_value(text, value, found, ndx+start+1) 

    data = {"links":[], "terms":[], "articles":[], "snippets":[]}
    for row in df.iterrows():
        article, link = row[1]["articles"], row[1]["links"]

        for term in parameters.TERMS:
            found:list[int] = []
            find_value(article, term, found)
            for i in found:
                before, after = article[0:i].split(" "), article[i+len(term):].split(" ")
                before, after = before[max(0,len(before)-parameters.CONTEXT_WORDS):], after[0:parameters.CONTEXT_WORDS]
                if len(before)<parameters.CONTEXT_WORDS:
                    to_add = parameters.CONTEXT_WORDS - len(before)
                    after = article[i+len(term):].split(" ")[0:parameters.CONTEXT_WORDS+to_add]
                elif len(after)<parameters.CONTEXT_WORDS:
                    to_add = parameters.CONTEXT_WORDS - len(after)
                    before = article[0:i].split(" ")
                    before = article[0:i].split(" ")[max(0,len(before)-parameters.CONTEXT_WORDS-to_add):]

                snippet = ' '.join(before) + term + ' '.join(after)

                # Append Data
                data['links'].append(link)
                data['terms'].append(term)
                data['articles'].append(article)
                data['snippets'].append(snippet)

    pd.DataFrame(data).to_csv("./data/articles_snippets.csv", index=False)


                    


 
