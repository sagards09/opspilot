from llm import ask_llm
from metrics import get_health_snapshot

SYSTEM_PROMPT = (
    "You are a senior Linux SRE explaining system health to an on-call engineer. "
    "Each metric already has a status decided by the monitoring system. "
    "Never change a status. Only explain it in plain English."
)


def get_status(value):
    if value < 70:
        return "HEALTHY"
    elif value <= 90:
        return "WARNING"
    else:
        return "CRITICAL"


def explain_health():
    snapshot = get_health_snapshot()

    cpu_status = get_status(snapshot["cpu_percent"])
    memory_status = get_status(snapshot["memory_percent"])
    disk_status = get_status(snapshot["disk_percent"])

    statuses = [cpu_status, memory_status, disk_status]
    if "CRITICAL" in statuses:
        overall = "CRITICAL"
    elif "WARNING" in statuses:
        overall = "WARNING"
    else:
        overall = "HEALTHY"

    print("Snapshot:", snapshot)
    print("Decided by code:", cpu_status, memory_status, disk_status, "| overall:", overall)

    question = (
        "Current system health:\n"
        f"- CPU used: {snapshot['cpu_percent']}% (status: {cpu_status})\n"
        f"- Memory used: {snapshot['memory_percent']}% (status: {memory_status})\n"
        f"- Disk used: {snapshot['disk_percent']}% (status: {disk_status})\n"
        f"Overall status: {overall}\n\n"
        "Explain each metric in one short sentence, then repeat the overall status."
    )
    return ask_llm(question, system_prompt=SYSTEM_PROMPT, temperature=0)


if __name__ == "__main__":
    print(explain_health())