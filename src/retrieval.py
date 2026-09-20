import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"


def load_documents():
    documents = []

    for path in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):
        documents.append(
            {
                "source": path.name,
                "text": path.read_text(encoding="utf-8"),
            }
        )

    return documents


def split_into_chunks(text, chunk_size=500, overlap=100):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    return response.embeddings[0].values


def build_knowledge_base():
    documents = load_documents()
    chunks = []

    for document in documents:
        document_chunks = split_into_chunks(document["text"])

        for chunk in document_chunks:
            chunks.append(
                {
                    "source": document["source"],
                    "text": chunk,
                    "embedding": create_embedding(chunk),
                }
            )

    return chunks


def cosine_similarity(vector_a, vector_b):
    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    denominator = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)

    if denominator == 0:
        return 0.0

    return float(np.dot(vector_a, vector_b) / denominator)


def retrieve_relevant_chunks(ticket_message, knowledge_base, top_k=3):
    ticket_embedding = create_embedding(ticket_message)

    scored_chunks = []

    for chunk in knowledge_base:
        score = cosine_similarity(
            ticket_embedding,
            chunk["embedding"],
        )

        scored_chunks.append(
            {
                "source": chunk["source"],
                "text": chunk["text"],
                "score": score,
            }
        )

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_chunks[:top_k]

def load_saved_knowledge_base():
    file_path = BASE_DIR / "data" / "knowledge_base_embeddings.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

if __name__ == "__main__":
    knowledge_base = load_saved_knowledge_base()

    results = retrieve_relevant_chunks(
        "My ₹3,500 order arrived damaged yesterday.",
        knowledge_base,
    )

    for result in results:
        print(result["source"], "-", round(result["score"], 4))