from llm import ask_llm

# ---------- A. Temperature ----------
print("=== A. Temperature ===")
question = "Suggest a short, catchy name for a server monitoring tool. Reply with the name only."

for temp in [0.0, 1.0]:
    print(f"\n--- temperature = {temp} ---")
    for i in range(3):
        answer = ask_llm(question, temperature=temp)
        print(f"Try {i + 1}: {answer}")

# ---------- B. System prompt ----------
print("\n=== B. System prompt ===")
question = "Why is a high load average a problem on a Linux server?"

prompts = {
    "Default": "You are a helpful Linux assistant.",
    "Senior SRE": "You are a senior SRE. Answer in exactly 2 short bullet points.",
    "Teacher": "You explain things to a complete beginner using one simple real-life analogy. Maximum 3 sentences.",
}

for name, prompt in prompts.items():
    print(f"\n--- {name} ---")
    print(ask_llm(question, system_prompt=prompt))

# ---------- C. Reducing hallucination ----------
print("\n=== C. Reducing hallucination ===")
question = "What does the Linux command diskclean --deep do?"

strict = (
    "You are a careful Linux assistant. Only describe commands you are certain exist. "
    "If a command is not a standard Linux command, reply exactly: I don't know this command."
)

print("\n--- Default prompt ---")
print(ask_llm(question))

print("\n--- Strict prompt ---")
print(ask_llm(question, system_prompt=strict))