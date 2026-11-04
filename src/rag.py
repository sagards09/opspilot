from pathlib import Path

import chromadb
import ollama

RUNBOOK_DIR = Path("data/runbooks")
DB_DIR = "chroma_db"
COLLECTION = "runbooks"
EMBED_MODEL = "nomic-embed-text"


def embed(texts):
    response = ollama.embed(model=EMBED_MODEL, input=texts)
    return response["embeddings"]


def chunk_runbook(path):
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    chunks = []
    for section in text.split("\n## ")[1:]:
        heading = section.splitlines()[0].strip()
        chunks.append({
            "id": f"{path.stem}-{heading.lower()}",
            "text": f"{title} - {heading}\n{section}",
            "metadata": {"source": path.name, "section": heading},
        })
    return chunks


def build_index():
    chunks = []
    for path in sorted(RUNBOOK_DIR.glob("*.md")):
        chunks.extend(chunk_runbook(path))

    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})

    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embed([c["text"] for c in chunks]),
        metadatas=[c["metadata"] for c in chunks],
    )
    print(f"Indexed {len(chunks)} chunks from {RUNBOOK_DIR}")


def search(question, n_results=3):
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION)

    results = collection.query(
        query_embeddings=embed([question]),
        n_results=n_results,
    )

    matches = []
    for text, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        matches.append({"text": text, "source": meta["source"],
                        "section": meta["section"], "distance": round(distance, 3)})
    return matches


if __name__ == "__main__":
    build_index()

    questions = [
        "server is out of space",
        "someone keeps trying to guess our passwords",
        "browser says the website is not secure",
        "the application keeps getting killed",
        "the time on the server is wrong",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        for m in search(q):
            print(f"   {m['distance']}  {m['source']} → {m['section']}")