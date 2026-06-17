import argparse
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_ENDPOINTS = [
    ("/api/cognates/universal-search/", {"q": "tangri", "limit": "3"}),
    ("/api/search/semantic/", {"q": "kitob", "topn": "5"}),
    ("/api/rag/retrieve/", {"q": "tangri", "topn": "5"}),
    ("/api/qa/ask/", {"q": "Tangri sozining turkiy tillardagi shakllari qanday?", "topk": "5"}),
]


def request_once(base_url, endpoint, params, timeout):
    url = f"{base_url.rstrip('/')}{endpoint}?{urlencode(params)}"
    started = time.perf_counter()
    try:
        with urlopen(Request(url, headers={"Accept": "application/json"}), timeout=timeout) as response:
            response.read()
            status = response.status
    except Exception as exc:
        return {"ok": False, "status": 0, "error": str(exc), "response_time_ms": (time.perf_counter() - started) * 1000}
    return {"ok": 200 <= status < 400, "status": status, "error": "", "response_time_ms": (time.perf_counter() - started) * 1000}


def run_load_test(base_url, requests, concurrency, timeout):
    started = time.perf_counter()
    results = []
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        for index in range(requests):
            endpoint, params = DEFAULT_ENDPOINTS[index % len(DEFAULT_ENDPOINTS)]
            futures.append(executor.submit(request_once, base_url, endpoint, params, timeout))
        for future in as_completed(futures):
            results.append(future.result())
    elapsed = time.perf_counter() - started
    times = [item["response_time_ms"] for item in results]
    errors = [item for item in results if not item["ok"]]
    return {
        "base_url": base_url,
        "requests": requests,
        "concurrency": concurrency,
        "total_time_seconds": round(elapsed, 3),
        "throughput_rps": round(requests / elapsed, 3) if elapsed else 0,
        "error_rate": round(len(errors) / requests * 100, 2) if requests else 0,
        "response_time_ms": {
            "min": round(min(times), 3) if times else 0,
            "avg": round(statistics.mean(times), 3) if times else 0,
            "p50": round(statistics.median(times), 3) if times else 0,
            "max": round(max(times), 3) if times else 0,
        },
        "errors": errors[:20],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic TurkicGrammarAI API load test")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    print(json.dumps(run_load_test(args.base_url, args.requests, args.concurrency, args.timeout), indent=2))
