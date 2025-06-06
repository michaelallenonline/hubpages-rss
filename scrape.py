import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://hubpages.com/@michaelallen"
FEED_FILE = "rss.xml"

def fetch_articles():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.select('a._2DqGg')  # May need updating if HubPages structure changes
    return [
        {
            "title": a.get_text(strip=True),
            "link": "https://hubpages.com" + a['href'],
            "pubDate": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        }
        for a in articles[:10]
    ]

def write_rss(items):
    rss = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0"><channel>',
           '<title>Michael Allen HubPages Feed</title>',
           f'<link>{URL}</link>',
           '<description>Latest articles by Michael Allen</description>']

    for item in items:
        rss.append("<item>")
        rss.append(f"<title>{item['title']}</title>")
        rss.append(f"<link>{item['link']}</link>")
        rss.append(f"<pubDate>{item['pubDate']}</pubDate>")
        rss.append("</item>")

    rss.append("</channel></rss>")

    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(rss))

if __name__ == "__main__":
    items = fetch_articles()
    write_rss(items)
