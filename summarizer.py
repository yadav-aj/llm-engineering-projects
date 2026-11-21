from openai import OpenAI
from scraper import fetch_website_contents

client = OpenAI(
  base_url="http://localhost:11434/v1",
  api_key="ollama"
)

def summarizer_website(url):
  website_content = fetch_website_contents(url)
  print("\nCLEANED WEBSITE CONTENT:\n")
  print(website_content[:1000])

  response = client.chat.completions.create(
    model="qwen2.5:1.5b",
    messages=[
      {
        "role": "system",
        "content": (
          "Summarize the website in exactly 3 bullet points. "
                "Each bullet must start with '- '. "
                "Keep each bullet under 20 words. "
                "Do not add headings or extra text."
        )
      },
      {
        "role": "user",
        "content": "Summarize this website:\n\n" + website_content[:3000]
      }
    ],
    temperature=0,
    max_tokens=180
  )

  return response.choices[0].message.content

url = input("Enter the website URL to summarize: ")
summary = summarizer_website(url)

lines = summary.splitlines()

bullet_points = [
  line for line in lines
  if line.strip().startswith("-")
]

print("Total bullet points:", len(bullet_points))
if len(bullet_points) == 3:
  print("PASS: Exactly 3 bullet points")
else:
  print("FALL: Expected 3 bullets, got", len(bullet_points))

print("\nAI SUMMARY:\n")
print("url:", url)
print(summary)