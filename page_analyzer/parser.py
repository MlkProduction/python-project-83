
from bs4 import BeautifulSoup


def parse_html(text):
    soup = BeautifulSoup(text, "html.parser")

    h1 = soup.h1.text.strip() if soup.h1 else ""
    title = soup.title.text.strip() if soup.title else ""

    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc.get("content", "").strip() if meta_desc else ""

    return h1, title, description