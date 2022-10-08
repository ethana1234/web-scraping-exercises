import pandas as pd
from isbe.IsbeScrape import contribution_search

if __name__ == "__main__":
    table_txt = contribution_search("Ron", "Johnson")
    df = pd.read_html(table_txt)[0]
    df.to_csv("./test.csv")
    print(df.head())
