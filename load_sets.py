import requests
from bs4 import BeautifulSoup

def get_all_sets():
    data = requests.get("https://yugioh.fandom.com/wiki/TCG_set_prefixes")
    soup = BeautifulSoup(data.text, "html.parser")
    links = soup.find_all("a", {"class": "mw-redirect"})
    return sorted([link["title"] for link in links if not (" " in link["title"] or "-" in link["title"])])
