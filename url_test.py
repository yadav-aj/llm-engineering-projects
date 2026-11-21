from scraper import fetch_website_links
from urllib.parse import urljoin

base_url = "https://www.python.org"

links = fetch_website_links(base_url)

clean_links = []

for link in links:
    if link.startswith("#"):
        continue

    if link.startswith("javascript:"):
        continue

    full_url = urljoin(base_url, link)

    if full_url.startswith(("http://", "https://")):
        clean_links.append(full_url)

unique_links = list(dict.fromkeys(clean_links))
print("Unique links:", len(unique_links))

print("Original links:", len(links))
print("Clean links:", len(clean_links))

for link in clean_links[:10]:
    print(link)