import json

def load_report():
    with open("/app/report.json") as f:
        return json.load(f)

def test_total_requests():
    """Success criterion 1"""
    report = load_report()
    assert report["total_requests"] == 6

def test_unique_ips():
    """Success criterion 2"""
    report = load_report()
    assert report["unique_ips"] == 3

def test_top_path():
    """Success criterion 3"""
    report = load_report()
    assert report["top_path"] == "/index.html"