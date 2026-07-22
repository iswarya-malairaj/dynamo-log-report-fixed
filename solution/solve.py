#!/usr/bin/env python3
import json
import re
from collections import Counter
from pathlib import Path

# Create /app directory
Path("/app").mkdir(exist_ok=True)

paths, ips, total = Counter(), set(), 0

# Read the access log
log_path = "/app/access.log"
print(f"Reading log from: {log_path}")

if not Path(log_path).exists():
    print(f"ERROR: {log_path} not found!")
    with open("/app/report.json", "w") as out:
        json.dump({
            "total_requests": 0,
            "unique_ips": 0,
            "top_path": "",
            "error": "access.log not found"
        }, out, indent=2)
    print("wrote fallback /app/report.json")
    exit(0)

with open(log_path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total += 1
        parts = line.split()
        if parts:
            ips.add(parts[0])
        m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
        if m:
            paths[m.group(1)] += 1

# Build the report
report = {
    "total_requests": total,
    "unique_ips": len(ips),
    "top_path": paths.most_common(1)[0][0] if paths else "",
}

with open("/app/report.json", "w") as out:
    json.dump(report, out, indent=2)

print(f"wrote /app/report.json with {total} requests")
print(f"Report: {report}")