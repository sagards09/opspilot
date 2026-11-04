import numpy as np
import ollama

EMBED_MODEL = "nomic-embed-text"


def embed(text):
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return np.array(response["embeddings"][0])


def similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


if __name__ == "__main__":
    sentences = [
        "disk is full",
        "server is out of space",
        "user cannot log in",
    ]

    vectors = [embed(s) for s in sentences]
    print("Numbers in one embedding:", len(vectors[0]))
    print("First 5 numbers:", vectors[0][:5])
    print()
    print(f"'{sentences[0]}' vs '{sentences[1]}': {similarity(vectors[0], vectors[1]):.2f}")
    print(f"'{sentences[0]}' vs '{sentences[2]}': {similarity(vectors[0], vectors[2]):.2f}")
    print(f"'{sentences[1]}' vs '{sentences[2]}': {similarity(vectors[1], vectors[2]):.2f}")