import json

from retrieval import build_knowledge_base


OUTPUT_FILE = "data/knowledge_base_embeddings.json"


knowledge_base = build_knowledge_base()

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(knowledge_base, file)

print(f"Saved {len(knowledge_base)} embedded chunks")
print(f"File: {OUTPUT_FILE}")