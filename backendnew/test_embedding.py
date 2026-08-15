from app.embeddings.generator import generate_embedding

text = "Artificial Intelligence is changing healthcare."

embedding = generate_embedding(text)

print(type(embedding))
print(len(embedding))
print(embedding[:10])