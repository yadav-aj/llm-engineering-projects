import tiktoken

encoding = tiktoken.get_encoding("o200k_base")

text = "Hi my name is Ajay and I like banoffee pie"

tokens = encoding.encode(text)

print("Original text:", text)
print("Total tokens:", len(tokens))
print("Token IDs:", tokens)

for token_id in tokens:
  token_text = encoding.decode([token_id])
  print(f"{token_id} = {token_text}")

decoded_text = encoding.decode(tokens)

print("\nDecoded text:", decoded_text)
print("Original matches decoded:", text == decoded_text)