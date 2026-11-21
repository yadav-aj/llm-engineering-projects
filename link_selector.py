
from openai import OpenAI
from scraper import fetch_website_links
from urllib.parse import urljoin
from scraper import fetch_website_contents
import json


# 1. Connect to local Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# 2. Fetch website links
url = "https://www.python.org"
links = fetch_website_links(url)

clean_links = []

# 3. Remove invalid links
for link in links:
    if link.startswith(("#", "javascript:", "mailto:", "tel:")):
        continue

    full_url = urljoin(url, link)

    if full_url.startswith(("http://", "https://")):
        clean_links.append(full_url)

# 4. Remove duplicates
unique_links = list(dict.fromkeys(clean_links))

print("Original links:", len(links))
print("Clean links:", len(clean_links))
print("Unique links:", len(unique_links))

# 5. Shortlist relevant website pages
candidate_links = [
    link for link in unique_links
    if link.startswith("https://www.python.org/")
    and any(
        word in link.lower()
        for word in ["about", "psf", "jobs", "community"]
    )
]

print("\nCandidate links:", len(candidate_links))

for link in candidate_links[:10]:
    print(link)

if not candidate_links:
    raise SystemExit("No candidate links found.")

# 6. Ask Qwen to select relevant links
response = client.chat.completions.create(
    model="qwen2.5:1.5b",
    messages=[
        {
            "role": "system",
            "content": (
                "You select useful links for a Python.org brochure. "
                "Select at most 3 URLs from the provided list. "
                "Copy URLs exactly. Do not invent URLs. "
                'Return only JSON: {"links": ["url1", "url2"]}'
            )
        },
        {
            "role": "user",
            "content": "\n".join(candidate_links)
        }
    ],
    temperature=0,
    max_tokens=300
)

# 7. Clean LLM response
raw_output = response.choices[0].message.content or ""

print("\nRaw AI output:")
print(raw_output)

raw_output = raw_output.replace("```json", "")
raw_output = raw_output.replace("```", "")
raw_output = raw_output.strip()

# 8. Parse and validate JSON
try:
    data = json.loads(raw_output)

    selected_links = data["links"]

    if not isinstance(selected_links, list):
        raise ValueError("links must be a list")

    # Normalize URLs while preserving original links
    normalized_links = {
        link.rstrip("/"): link
        for link in candidate_links
    }

    valid_links = []

    for link in selected_links[:3]:
        if not isinstance(link, str):
            print("Rejected non-string URL:", link)
            continue

        normalized = link.rstrip("/")

        if normalized in normalized_links:
            original_url = normalized_links[normalized]

            if original_url not in valid_links:
                valid_links.append(original_url)
                print("Accepted:", original_url)
        else:
            print("Rejected hallucinated URL:", link)

    print("\nValid selected links:", valid_links)

except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
    print("Invalid AI response:", e)


# Fetch content from selected pages
all_page_contents = []

for page_url in valid_links:
    print("\nFetching:", page_url)

    try:
        page_content = fetch_website_contents(page_url)

        all_page_contents.append(page_content[:2000])

        print("Characters fetched:", len(page_content))

    except Exception as e:
        print("Failed to fetch page:", e)

combined_content = "\n\n--- NEXT PAGE ---\n\n".join(all_page_contents)

print("\nTotal combined characters:", len(combined_content))

# Generate final multi-page brochure

print("\nGenerating company brochure...\n")

brochure_response = client.chat.completions.create(
    model="qwen2.5:1.5b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a professional company brochure writer. "
                "Use only the supplied website content. "
                "Do not invent information. "
                "Write a concise brochure in Markdown with "
                "these sections: Introduction, Offerings, "
                "Community and Highlights. "
                "Use bullet points where appropriate. "
                "If information is missing, do not invent it."
            )
        },
        {
            "role": "user",
            "content": (
                "Create a brochure for Python.org based on "
                "the following website content:\n\n"
                + combined_content
            )
        }
    ],
    temperature=0,
    max_tokens=650,
    stream=True
)
brochure = ""

print("\nFINAL BROCHURE:\n")

for chunk in brochure_response:
    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)
        brochure += content

print()

with open("company_brochure.md", "w", encoding="utf-8") as file:
    file.write(brochure)

print("\nBrochure saved successfully!")

print("Finish reason:", brochure_response.choices[0].finish_reason)
print("\nFINAL BROCHURE:\n")
print(brochure)
