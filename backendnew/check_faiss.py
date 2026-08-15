import faiss

index = faiss.read_index("trained_models/content.index")

print("Index type:", type(index))
print("Dimension:", index.d)
print("Total vectors:", index.ntotal)