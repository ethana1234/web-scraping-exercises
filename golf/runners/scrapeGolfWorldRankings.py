from golf.golfScrape import get_rankings_table


if __name__ == "__main__":
    URL = "https://www.owgr.com/current-world-ranking"
    get_rankings_table(None, URL)
