# Parallel Programming Performance Comparison Using Python

---

## Table of Contents

1. [How It Works](#1-how-it-works)
2. [Problem Statement](#2-problem-statement)
3. [System Requirements](#3-system-requirements)
4. [Installation](#4-installation)
5. [How to Run](#5-how-to-run)
6. [Project Structure](#6-project-structure)
7. [Techniques Explained](#7-techniques-explained)
8. [Test Types](#8-test-types)
9. [Sample Output](#9-sample-output)
10. [Results & Analysis](#10-results--analysis)

---

# 1. How It Works

This project compares different execution techniques in Python for processing large numbers of API requests.

The application sends multiple requests to a public API and compares:

- Concurrent execution using **asyncio**
- Concurrent execution using **threading**
- Parallel execution using **multiprocessing**

Each technique processes the same workload:

- 50 requests
- 200 requests
- 500 requests

Execution time and throughput are measured to determine which technique performs best.

---

# 2. Problem Statement

Modern applications often need to process many tasks simultaneously such as:

- API requests
- File handling
- Data processing

Sequential execution becomes inefficient when handling large workloads.

This project investigates how concurrent and parallel programming techniques affect system performance using:

- Execution time
- Throughput
- Scalability

The goal is to identify which approach is more suitable for large-scale workloads.

---

# 3. System Requirements

| Component | Requirement |
|------------|-------------|
| Operating System | Windows 10/11 or Linux |
| Python Version | Python 3.10+ |
| RAM | Minimum 4GB |
| Processor | Multi-core CPU recommended |
| Internet | Required |

Required Python packages:

```bash
aiohttp
requests

# 4. Installation

## Step 1: Install Python

Download Python:

https://www.python.org/downloads/

During installation:

✅ Check:

```bash
Add Python to PATH
```

Verify installation:

```bash
python --version
```

Example:

```bash
Python 3.13.5
```

---

## Step 2: Install Required Packages

Open PowerShell:

```bash
pip install aiohttp requests
```

Verify installed packages:

```bash
pip list
```

---

# 5. How to Run

Open PowerShell inside project folder:

```bash
cd Desktop\itt-assignment
```

Run:

```bash
python main.py
```

The program will automatically:

1. Execute asyncio test
2. Execute threading test
3. Execute multiprocessing test
4. Measure execution duration
5. Calculate throughput
6. Display comparison result

---

# 6. Project Structure

```text
itt-assignment/
│
├── main.py
├── README.md
└── requirements.txt
```

Description:

| File | Purpose |
|-------|----------|
| main.py | Main program source code |
| README.md | Documentation |
| requirements.txt | Required Python libraries |

---

# 7. Techniques Explained

## A) asyncio

**Type:** Concurrent Programming

**Description:**

Uses a single thread with an event loop.

Suitable for:

- API requests
- Network communication
- I/O operations

Advantages:

✔ Low memory usage  
✔ Very fast for I/O operations

Disadvantages:

✘ Not suitable for CPU-heavy tasks

---

## B) Threading

**Type:** Concurrent Programming

**Description:**

Uses multiple threads within one process.

Suitable for:

- Moderate I/O operations

Advantages:

✔ Easy implementation

Disadvantages:

✘ Limited by Python Global Interpreter Lock (GIL)

---

## C) Multiprocessing

**Type:** Parallel Programming

**Description:**

Uses multiple processes and multiple CPU cores.

Suitable for:

- Heavy CPU computation

Advantages:

✔ True parallel execution

Disadvantages:

✘ High process creation overhead

---

# 8. Test Types

Three workload sizes are used.

| Test | Requests |
|--------|----------|
| Small Load | 50 |
| Medium Load | 200 |
| Large Load | 500 |

Purpose:

### Small Load
Measures basic performance.

### Medium Load
Measures scalability.

### Large Load
Measures behavior under heavy workloads.

---

# 9. Sample Output

Console output:

```text
================================================
 PARALLEL PROGRAMMING PERFORMANCE COMPARISON
================================================
CPU Cores Available: 16
```

### Test Result Summary

| Technique | Requests | Duration | Throughput |
|------------|-----------|-----------|-------------|
| asyncio | 50 | 1.08 sec | 46.29 req/sec |
| threading | 50 | 4.08 sec | 12.25 req/sec |
| multiprocessing | 50 | 10.40 sec | 4.81 req/sec |
| asyncio | 200 | 1.65 sec | 121.57 req/sec |
| threading | 200 | 16.43 sec | 12.17 req/sec |
| multiprocessing | 200 | 37.01 sec | 5.40 req/sec |
| asyncio | 500 | 8.44 sec | 59.26 req/sec |
| threading | 500 | 40.92 sec | 12.22 req/sec |
| multiprocessing | 500 | 89.30 sec | 5.60 req/sec |

---

# 10. Results & Analysis

## Performance Ranking

🥇 asyncio

🥈 threading

🥉 multiprocessing

---

## Why asyncio is Fastest

`asyncio` uses a single event loop and does not create extra threads or processes.

When one request waits for a response:

- another request immediately executes
- minimal overhead occurs

Therefore performance is higher.

---

## Why Threading is Slower

Threading creates multiple threads.

Although threads help execute tasks simultaneously:

- thread creation adds overhead
- Python GIL limits performance

Thus performance becomes lower than asyncio.

---

## Why Multiprocessing is Slowest

Multiprocessing creates separate processes.

Each process:

- has its own memory
- requires communication overhead

Since API requests are mainly I/O tasks rather than CPU-heavy tasks:

process creation cost becomes larger than performance gain.

---

## Final Conclusion

For API-based workloads:

**asyncio is the best technique**

For CPU-intensive workloads:

**multiprocessing becomes more suitable**

For moderate concurrent workloads:

**threading provides acceptable performance**