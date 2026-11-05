from llm import ask_llm
from rag import search

SYSTEM_PROMPT = (
    "You are an SRE assistant. Answer ONLY using the runbook context provided. "
    "Do not use outside knowledge and do not invent commands. "
    "Keep the answer short, as numbered steps. "
    "End with 'Source:' followed by the runbook file and section you used. "
    "If the answer is not in the context, reply exactly: Not found in runbooks."
)


def ask_runbooks(question):
    # R: Retrieve the 3 closest runbook chunks
    matches = search(question, n_results=3)
    print("Retrieved:", [f"{m['source']} - {m['section']}" for m in matches])

    # A: Augment, building the context text with sources
    context = ""
    for m in matches:
        context += f"[Source: {m['source']} - {m['section']}]\n{m['text']}\n\n"

    prompt = f"Context:\n{context}Question: {question}"

    # G: Generate the answer
    return ask_llm(prompt, system_prompt=SYSTEM_PROMPT, temperature=0)


if __name__ == "__main__":
    questions = [
        "server is out of space, what should I do?",
        "how do I check when our SSL certificate expires?",
        "how do I reset a Cisco router password?",
    ]

    for q in questions:
        print(f"\n=== Q: {q} ===")
        print(ask_runbooks(q))