import subprocess
from typing import Literal

from pydantic import BaseModel

from llm import ask_llm, ask_llm_json          # CHANGE 1: added ask_llm
from metrics import get_health_snapshot
from rag import search

# ---------- 1. The tools ----------
SAFE_COMMANDS = ["df -h", "uptime"]


def run_safe_command(command):
    if command not in SAFE_COMMANDS:
        return f"BLOCKED: '{command}' is not allowed. Allowed: {SAFE_COMMANDS}"
    result = subprocess.run(command.split(), capture_output=True, text=True, timeout=10)
    return result.stdout


def search_runbooks(query):
    matches = search(query, n_results=2)
    return "\n\n".join(f"[{m['source']}]\n{m['text']}" for m in matches)


def run_tool(action, action_input):
    if action == "get_health":
        return str(get_health_snapshot())
    elif action == "search_runbooks":
        return search_runbooks(action_input)
    elif action == "run_safe_command":
        return run_safe_command(action_input)
    return "Unknown tool"


# ---------- 2. The menu (what the LLM is told) ----------
SYSTEM_PROMPT = (
    "You are an SRE agent investigating an alert. Work step by step. "
    "At each step choose ONE action:\n"
    "- get_health: current CPU, memory and disk percent (action_input: empty)\n"
    "- search_runbooks: search the team runbooks (action_input: a short search phrase)\n"
    "- run_safe_command: run a read-only command. Allowed: 'df -h', 'uptime'\n"
    "- final_answer: your summary and recommended steps (action_input: the answer)\n"
    # CHANGE 2: new rules telling it not to repeat, and when to finish
    "Only use information from tool results. Never repeat an action you already took. "
    "As soon as you have checked health and the runbook, give final_answer."
)


# ---------- 3. The decision format ----------
class Step(BaseModel):
    thought: str
    action: Literal["get_health", "search_runbooks", "run_safe_command", "final_answer"]
    action_input: str


# ---------- 4. The loop ----------
def run_agent(task, max_steps=5):
    history = f"Task: {task}\n"

    for step in range(1, max_steps + 1):
        raw = ask_llm_json(history, schema=Step.model_json_schema(), system_prompt=SYSTEM_PROMPT)
        decision = Step.model_validate_json(raw)

        print(f"\nStep {step}: {decision.action} ({decision.action_input})")
        print(f"   Thought: {decision.thought}")

        if decision.action == "final_answer":
            return decision.action_input

        result = run_tool(decision.action, decision.action_input)
        print(f"   Result: {result[:200]}")

        history += f"\nStep {step}: {decision.action} ({decision.action_input})\nResult: {result}\n"

    # CHANGE 3: safety net. Instead of giving up, code forces a final answer
    print("\nStep limit reached. Asking for a final answer now.")
    final = ask_llm(history + "\nGive your final answer now, using only the results above.",
                    system_prompt="You are an SRE. Summarise the findings and the recommended steps.")
    return final


if __name__ == "__main__":
    answer = run_agent("Disk usage alert on this server. Investigate and tell me what to do.")
    print("\n=== FINAL ANSWER ===")
    print(answer)