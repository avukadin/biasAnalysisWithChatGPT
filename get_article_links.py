import os
import parameters
from pkg.GoogleRSSParser import GoogleRSSParser

if __name__ == "__main__":
    for query in parameters.TERMS:
        data = GoogleRSSParser().query_stories(
            start_date=parameters.START_DATE, 
            end_date=parameters.END_DATE, 
            query=query, 
            source=parameters.SOURCE)

        start = str(parameters.START_DATE)[0:10]
        end = str(parameters.END_DATE)[0:10]
        query_name = query.replace(' ', '_')
        file_name = f"./story_links_{start}_to_{end}_{query_name}.csv"

        # Make Directories
        if not os.path.isdir("./data"):
            os.mkdir("./data")
        if not os.path.isdir("./data/links"):
            os.mkdir("./data/links")

        # Save links
        path = os.path.join("./data/links", file_name)
        data.to_csv(path, index=False)
