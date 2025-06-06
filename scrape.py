import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://hubpages.com/@michaelallen"
FEED_FILE = "rss.xml"
RSS_LINK = "https://raw.githubusercontent.com/michaelallenonline/hubpages-rss/main/rss.xml"

def fetch_articles():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    anchors = soup.select("a._2DqGg")  # update if HubPages changes structure

    items = []
    for a in anchors[:10]:
        title = a.get_text(strip=True)
        link = "https://hubpages.com" + a.get("href", "")
        pubDate = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        items.append({
            "title": title,
            "link": link,
            "pubDate": pubDate
        })

    return items

def write_rss(items):
    rss = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '<channel>',
        '<title>Michael Allen HubPages Feed</title>',
        f'<link>{URL}</link>',
        f'<atom:link href="{RSS_LINK}" rel="self" type="application/rss+xml" />',
        '<description>Latest articles by Michael Allen</description>'
    ]

    for item in items:
        rss.append("<item>")
        rss.append(f"<title>{item['title']}</title>")
        rss.append(f"<link>{item['link']}</link>")
        rss.append(f"<pubDate>{item['pubDate']}</pubDate>")
        rss.append(f"<guid>{item['link']}</guid>")
        rss.append("</item>")

    rss.append("</channel></rss>")

    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(rss))

if __name__ == "__main__":
    items = fetch_articles()
    write_rss(items)
