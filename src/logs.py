import re
from collections import Counter
from pathlib import Path

LOG_DIR = Path("data/logs")

PROBLEM_WORDS = re.compile(
    r"fail|error|denied|invalid|refused|break-in|critical", re.IGNORECASE
)
IP_PATTERN = re.compile(r"\d+\.\d+\.\d+\.\d+")


def read_log(filename):
    path = LOG_DIR / filename
    text = path.read_text(encoding="utf-8", errors="replace")
    return text.splitlines()


def filter_problem_lines(lines):
    return [line for line in lines if PROBLEM_WORDS.search(line)]


def top_failed_ips(lines, top_n=5):
    ips = []
    for line in lines:
        if "Failed password" in line:
            match = IP_PATTERN.search(line)
            if match:
                ips.append(match.group())
    return Counter(ips).most_common(top_n)


def build_evidence(lines, sample_size=10):
    problems = filter_problem_lines(lines)
    failed = [line for line in lines if "Failed password" in line]
    invalid_users = [line for line in lines if "Invalid user" in line]
    first_time = lines[0][:15]
    last_time = lines[-1][:15]

    ip_text = "\n".join(
        f"- {ip}: {count} failed logins" for ip, count in top_failed_ips(lines)
    )
    samples = "\n".join(problems[:sample_size])

    return (
        f"Time range: {first_time} to {last_time}\n"
        f"Total log lines: {len(lines)}\n"
        f"Problem lines: {len(problems)}\n"
        f"Failed password attempts: {len(failed)}\n"
        f"Invalid user attempts: {len(invalid_users)}\n"
        f"Top attacking IPs:\n{ip_text}\n\n"
        f"Sample problem lines:\n{samples}"
    )


if __name__ == "__main__":
    lines = read_log("OpenSSH_2k.log")
    print(build_evidence(lines))
    print(f"\nApprox evidence tokens: {len(build_evidence(lines)) // 4}")