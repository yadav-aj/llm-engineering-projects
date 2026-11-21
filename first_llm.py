from openai import OpenAI

client = OpenAI(
  base_url="http://localhost:11434/v1",
  api_key="ollama"
)

response = client.chat.completions.create(
  model="qwen2.5:1.5b",
  messages=[
    {
      "role": "system",
      "content": "You are a Python teacher who explains in Hinglish."
    },
    {
      "role": "user",
      "content": "What is a Python function? Explain with one example."
    }
  ]
)

print(response.choices[0].message.content)