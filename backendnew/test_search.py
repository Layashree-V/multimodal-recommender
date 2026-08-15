from app.embeddings.search import SemanticSearch

search = SemanticSearch()

results = search.search("Artificial Intelligence")

print(results)