import json
from typing import Literal

from pydantic import BaseModel, ValidationError


class IncidentSummary(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    summary: str
    likely_cause: str
    affected_service: str


if __name__ == "__main__":
    print("=== The schema we will give Ollama ===")
    print(json.dumps(IncidentSummary.model_json_schema(), indent=2))

    print("\n=== Test 1: good data ===")
    good = '{"severity": "high", "summary": "SSH attack", "likely_cause": "brute force", "affected_service": "sshd"}'
    incident = IncidentSummary.model_validate_json(good)
    print("Valid! severity =", incident.severity)

    print("\n=== Test 2: bad data ===")
    bad = '{"severity": "very bad", "summary": "SSH attack"}'
    try:
        IncidentSummary.model_validate_json(bad)
    except ValidationError as error:
        print(error)