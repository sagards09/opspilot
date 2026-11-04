import requests

PROMETHEUS_URL = "http://localhost:9090"

QUERIES = {
    "cpu_percent": '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)',
    "memory_percent": "(node_memory_active_bytes + node_memory_wired_bytes + node_memory_compressed_bytes) / node_memory_total_bytes * 100",
    "disk_percent": '100 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"} * 100)',
}


def query_prometheus(promql):
    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": promql},
        timeout=5,
    )
    response.raise_for_status()
    data = response.json()

    results = data["data"]["result"]
    if not results:
        return None
    return float(results[0]["value"][1])


def get_health_snapshot():
    snapshot = {}
    for name, promql in QUERIES.items():
        value = query_prometheus(promql)
        if value is None:
            snapshot[name] = None
        else:
            snapshot[name] = round(value, 1)
    return snapshot


if __name__ == "__main__":
    snapshot = get_health_snapshot()
    print(snapshot)