from pydantic import ValidationError

from llm import ask_llm_json
from logs import read_log, build_evidence
from schemas import IncidentSummary

SYSTEM_PROMPT = (
    "You are a senior Linux SRE investigating a production incident. "
    "Base your analysis only on the evidence provided. "
    "Do not invent commands, IP addresses or numbers. "
    "If something is unclear, write 'unknown'."
)


def build_prompt(evidence, context):
    return (
        f"Context: these are {context}.\n\n"
        "Task: identify the main incident in the evidence below.\n\n"
        f"Evidence:\n{evidence}\n\n"
        "Reply in JSON with exactly these fields: "
        "severity (low, medium, high or critical), summary, likely_cause, affected_service."
    )


def analyse_logs(filename, context, max_attempts=2, simulate_bad_first=False):
    lines = read_log(filename)
    evidence = build_evidence(lines)
    prompt = build_prompt(evidence, context)
    schema = IncidentSummary.model_json_schema()

    for attempt in range(1, max_attempts + 1):
        try:
            if simulate_bad_first and attempt == 1:
                raw = '{"severity": "very bad", "summary": "SSH attack"}'
            else:
                raw = ask_llm_json(prompt, schema=schema, system_prompt=SYSTEM_PROMPT)

            incident = IncidentSummary.model_validate_json(raw)
            print(f"Attempt {attempt}: valid output")
            return incident

        except ValidationError as error:
            print(f"Attempt {attempt}: invalid output ({error.error_count()} errors)")
            prompt = (
                build_prompt(evidence, context)
                + "\n\nYour previous reply was invalid:\n"
                + str(error)
                + "\nReply again with valid JSON only."
            )

        except Exception as error:
            print(f"Attempt {attempt}: could not reach the LLM ({error})")

    print(f"Could not analyse {filename} after {max_attempts} attempts. Check the logs manually.")
    return None


if __name__ == "__main__":
    tests = [
        ("OpenSSH_2k.log", "SSH server logs from a production Linux host"),
        ("Linux_2k.log", "system logs from a production Linux host"),
    ]

    for filename, context in tests:
        print(f"\n=== {filename} ===")
        incident = analyse_logs(filename, context)
        if incident:
            print(incident.model_dump_json(indent=2))