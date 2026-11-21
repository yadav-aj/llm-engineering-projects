import requests
from bs4 import BeautifulSoup


def fetch_website_contents(url):
  response = requests.get(url, timeout=15)
  response.raise_for_status()

  soup = BeautifulSoup(response.text, "html.parser")

  title = soup.title.get_text(strip=True) if soup.title else "No title"
  for tag in soup.select(
    "script, style, nav, footer, header, "
    "aside, form, noscript"
  ):
    tag.decompose()
  body = soup.body.get_text(separator="\n", strip=True) if soup.body else ""

  website_content = title + "\n\n" + body

  return website_content

def fetch_website_links(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    links = []

    for link in soup.find_all("a"):
        href = link.get("href")

        if href:
            links.append(href)

    return links

if __name__ == "__main__":
  url = "https://www.python.org"
  result = fetch_website_contents(url)
  print(result)
