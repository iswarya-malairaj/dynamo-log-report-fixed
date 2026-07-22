import json
from pathlib import Path

def test_report_exists():
    """The report file must exist."""
    assert Path("/app/report.json").exists(), "report.json not found"

def test_total_requests():
    """Total requests must be correct."""
    with open("/app/report.json") as f:
        report = json.load(f)
    assert report["total_requests"] == 6, f"Expected 6, got {report['total_requests']}"

def test_unique_ips():
    """Unique IPs must be correct."""
    with open("/app/report.json") as f:
        report = json.load(f)
    assert report["unique_ips"] == 3, f"Expected 3, got {report['unique_ips']}"

def test_top_path():
    """Top path must be correct."""
    with open("/app/report.json") as f:
        report = json.load(f)
    assert report["top_path"] == "/index.html", f"Expected /index.html, got {report['top_path']}"