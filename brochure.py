from openai import OpenAI
from scraper import fetch_website_contents
from scraper import fetch_website_links

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def check_source(keyword, website_content):
    if keyword.lower() in website_content.lower():
        return True
    else:
        return False

def generate_brochure(website_content):
    response = client.chat.completions.create(
        model="qwen2.5:1.5b",
        messages=[
            {
    "role": "system",
    "content": (
        "You create concise company brochures using only supplied website text. "
        "Write in Markdown with exactly three sections: "
        "Introduction (maximum 40 words), "
        "Offerings (maximum 3 bullet points), "
        "Highlights (maximum 3 bullet points). "
        "Do not repeat information. "
        "Do not mention products or technologies absent from the source. "
        "If information is missing, say 'Not specified'."
    )
},
            {
                "role": "user",
                "content": "Create a brochure from this website:\n\n"
                           + website_content[:3000]
            }
        ],
        temperature=0,
        max_tokens=400
    )
    print("\nFinish reason:", response.choices[0].finish_reason)
    return response.choices[0].message.content

url = input("Enter company website URL: ")
website_content = fetch_website_contents(url)
summary = generate_brochure(website_content)

with open("company_brochure.md", "w", encoding="utf-8") as file:
    file.write(summary)

print("Brochure saved successfully!")

keyword = "NumPy"

if keyword.lower() in website_content.lower():
    print("Found in source")
else:
    print("Not found in source")

print("Website content fetched!")
print("Characters:", len(website_content))
print("\nSOURCE WEBSITE TEXT:\n")
print(website_content)
print("NumPy:", check_source("NumPy", website_content))
print("Django:", check_source("Django", website_content))
print("TensorFlow:", check_source("TensorFlow", website_content))
print(summary)

url = "https://www.python.org"

links = fetch_website_links(url)

print("Total links:", len(links))

for link in links[:10]:
    print(link)