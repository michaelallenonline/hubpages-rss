import requests
from bs4 import BeautifulSoup
from datetime import datetime
from xml.sax.saxutils import escape

URL = "https://hubpages.com/@michaelallen"
FEED_FILE = "rss.xml"
RSS_LINK = "https://michaelallenonline.com/rss.xml"

def fetch_articles():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("https://discover.hubpages.com/"):
            title = a.get_text(strip=True)
            if title:
                articles.append({
                    "title": escape(title),
                    "link": escape(href),
                    "pubDate": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                    "guid": escape(href)
                })
    return articles

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
        rss.append(f"<guid>{item['guid']}</guid>")
        rss.append("</item>")

    rss.append("</channel></rss>")

    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(rss))

if __name__ == "__main__":
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles.")
    write_rss(articles)
