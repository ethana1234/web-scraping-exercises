from base.scrape import get_html_data


def get_rankings_table(db, URL):
    website_soup = get_html_data(URL)
    table = website_soup.find("table")
    for row in table.findAll("tr"):
        print(','.join([ele.text.strip() for ele in row.find_all('td')]))
