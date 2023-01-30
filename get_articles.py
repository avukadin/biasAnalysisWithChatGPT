import os

from pkg.CBCNewsScraper import CBCNewsScraper

if __name__ == "__main__":

    link_files = [os.path.join("./data/links", f) for f in os.listdir("./data/links") if f.endswith(".csv")]
    cbcns = CBCNewsScraper(link_files)
    cbcns.run()