from base.Scrape import get_html_data


URL = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByAllContributions.aspx"


def contribution_search(first_name, last_name):
    search_url = URL + f"?txtLastOnlyName={last_name}&txtFirstName={first_name}"
    soup = get_html_data(search_url, verify=False)
    table = soup.find("table", id="ContentPlaceHolder1_gvContributions")
    if table is None:
        return None
    # Split table breaks
    for br in table.find_all("br"):
        br.replace_with("|")
    return table.prettify()
