from openai import OpenAI

client = OpenAI(
  base_url="http://localhost:11434/v1",
  api_key="ollama"
)

messages = [
  {
    "role": "system",
    "content": (
       "You are a helpful conversational assistant. "
            "Remember facts stated by the user in the conversation history. "
            "If the user tells you their favorite programming language, "
            "answer that language when asked. "
            "Answer directly and briefly."
    )
  }
]

while True:
  user_input = input("\nYou: ")

  if user_input.lower() == "exit":
    break

  messages.append({
    "role": "user",
    "content": user_input
  })

  print("\n--- CONVERSATION HISTORY ---")

  for message in messages:
      print(message["role"], ":", message["content"])

  print("----------------------------\n")

  response = client.chat.completions.create(
    model="qwen2.5:1.5b",
    messages=messages,
    temperature=0
  )

  answer = response.choices[0].message.content or ""

  print("AI:", answer)

  messages.append({
    "role" : "assistant",
    "content" : answer
  })