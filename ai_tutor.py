from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

question = input("Ask your Python question: ")

response = client.chat.completions.create(
    model="qwen2.5:1.5b",
    stream=True,
    messages=[
    {
        "role": "system",
        "content": "You are a Python teacher. Answer the user's question directly."
    },
    {
        "role": "user",
        "content": question
    }
],
    temperature=0,
    max_tokens=300
)

print("\nAI TUTOR:\n")

for chunk in response:
    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)

print()