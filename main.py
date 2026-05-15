"""
===========================================================
Parallel Programming Assignment
Title:
Performance Comparison of Concurrent and Parallel
Data Processing Techniques Using Python

Techniques Used:
1. asyncio          (Concurrent)
2. threading        (Concurrent)
3. multiprocessing  (Parallel)

Test Types:
1. Execution Time Comparison
2. Throughput Test
3. Scalability Test
===========================================================
"""

import asyncio
import aiohttp
import multiprocessing
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import requests

README_FILE = "README.md"
README_RESULTS_START = "<!-- AUTO_BENCHMARK_RESULTS_START -->"
README_RESULTS_END = "<!-- AUTO_BENCHMARK_RESULTS_END -->"

# =========================================================
# TARGET API
# =========================================================

TARGET_URL = "https://jsonplaceholder.typicode.com/posts"

# Different workload sizes for scalability testing
TEST_SIZES = [50, 200, 500]

# =========================================================
# ASYNCIO (CONCURRENT)
# =========================================================

async def fetch_async(session, post_id):
    url = f"{TARGET_URL}/{post_id}"

    try:
        async with session.get(url) as response:
            await response.json()
            return response.status
    except:
        return 0


async def run_asyncio_test(total_requests):

    start_time = time.perf_counter()

    connector = aiohttp.TCPConnector(limit=0)

    async with aiohttp.ClientSession(connector=connector) as session:

        tasks = []

        for i in range(total_requests):
            post_id = (i % 100) + 1
            tasks.append(fetch_async(session, post_id))

        results = await asyncio.gather(*tasks)

    end_time = time.perf_counter()

    success = sum(1 for r in results if r == 200)

    duration = end_time - start_time

    throughput = total_requests / duration

    return {
        "Technique": "asyncio",
        "Requests": total_requests,
        "Success": success,
        "Duration": round(duration, 2),
        "Throughput": round(throughput, 2)
    }


# =========================================================
# THREADING (CONCURRENT)
# =========================================================

def fetch_thread(post_id):

    url = f"{TARGET_URL}/{post_id}"

    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except:
        return 0


def run_threading_test(total_requests):

    start_time = time.perf_counter()

    results = []

    with ThreadPoolExecutor(max_workers=50) as executor:

        futures = []

        for i in range(total_requests):
            post_id = (i % 100) + 1
            futures.append(executor.submit(fetch_thread, post_id))

        for future in futures:
            results.append(future.result())

    end_time = time.perf_counter()

    success = sum(1 for r in results if r == 200)

    duration = end_time - start_time

    throughput = total_requests / duration

    return {
        "Technique": "threading",
        "Requests": total_requests,
        "Success": success,
        "Duration": round(duration, 2),
        "Throughput": round(throughput, 2)
    }


# =========================================================
# MULTIPROCESSING (PARALLEL)
# =========================================================

def fetch_process(post_id):

    url = f"{TARGET_URL}/{post_id}"

    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except:
        return 0


def run_multiprocessing_test(total_requests):

    start_time = time.perf_counter()

    post_ids = []

    for i in range(total_requests):
        post_id = (i % 100) + 1
        post_ids.append(post_id)

    with ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count()
    ) as executor:

        results = list(executor.map(fetch_process, post_ids))

    end_time = time.perf_counter()

    success = sum(1 for r in results if r == 200)

    duration = end_time - start_time

    throughput = total_requests / duration

    return {
        "Technique": "multiprocessing",
        "Requests": total_requests,
        "Success": success,
        "Duration": round(duration, 2),
        "Throughput": round(throughput, 2)
    }


# =========================================================
# DISPLAY RESULTS
# =========================================================

def print_result(result):

    print("\n========================================")
    print(f"Technique   : {result['Technique']}")
    print(f"Requests    : {result['Requests']}")
    print(f"Success     : {result['Success']}")
    print(f"Duration    : {result['Duration']} seconds")
    print(f"Throughput  : {result['Throughput']} req/sec")
    print("========================================")


# =========================================================
# README RESULTS & GIT COMMIT
# =========================================================

def _project_root() -> Path:
    return Path(__file__).resolve().parent


def _format_results_markdown(all_results: list) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    cores = multiprocessing.cpu_count()
    lines = [
        f"*Generated {stamp} · CPU cores: {cores}*",
        "",
        "| Technique | Requests | Success | Duration | Throughput |",
        "|-----------|----------|---------|----------|------------|",
    ]
    for row in all_results:
        lines.append(
            f"| {row['Technique']} | {row['Requests']} | {row['Success']} | "
            f"{row['Duration']} sec | {row['Throughput']} req/sec |"
        )
    return "\n".join(lines)


def update_readme_results(all_results: list) -> Path:
    root = _project_root()
    path = root / README_FILE
    text = path.read_text(encoding="utf-8")
    start = text.find(README_RESULTS_START)
    end = text.find(README_RESULTS_END)
    if start == -1 or end == -1 or end < start:
        raise RuntimeError(
            f"{README_FILE} must contain {README_RESULTS_START} and "
            f"{README_RESULTS_END} markers around the results section."
        )
    start_cut = start + len(README_RESULTS_START)
    block = _format_results_markdown(all_results)
    new_text = text[:start_cut] + "\n\n" + block + "\n\n" + text[end:]
    path.write_text(new_text, encoding="utf-8")
    return path


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def try_commit_readme(readme_path: Path) -> None:
    if os.environ.get("ITT_NO_GIT", "").strip().lower() in ("1", "true", "yes"):
        return

    cwd = readme_path.parent
    probe = _git(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
    if probe.returncode != 0 or probe.stdout.strip().lower() != "true":
        return

    _git(["add", "--", readme_path.name], cwd=cwd)
    diff = _git(["diff", "--cached", "--quiet"], cwd=cwd)
    if diff.returncode == 0:
        return

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commit = _git(
        ["commit", "-m", f"Update benchmark results in README ({stamp})"],
        cwd=cwd,
    )
    if commit.returncode != 0:
        return

    _git(["push"], cwd=cwd)


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    print("\n================================================")
    print(" PARALLEL PROGRAMMING PERFORMANCE COMPARISON")
    print("================================================")

    print(f"CPU Cores Available: {multiprocessing.cpu_count()}")

    all_results: list = []

    for size in TEST_SIZES:

        print(f"\n\n########## TEST SIZE: {size} REQUESTS ##########")

        # -------------------------------------------------
        # ASYNCIO
        # -------------------------------------------------

        asyncio_result = asyncio.run(
            run_asyncio_test(size)
        )

        print_result(asyncio_result)
        all_results.append(asyncio_result)

        # -------------------------------------------------
        # THREADING
        # -------------------------------------------------

        threading_result = run_threading_test(size)

        print_result(threading_result)
        all_results.append(threading_result)

        # -------------------------------------------------
        # MULTIPROCESSING
        # -------------------------------------------------

        multiprocessing_result = run_multiprocessing_test(size)

        print_result(multiprocessing_result)
        all_results.append(multiprocessing_result)

    readme_path = update_readme_results(all_results)
    try_commit_readme(readme_path)


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    multiprocessing.freeze_support()

    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)