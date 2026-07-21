There is an Apache-style access log located at /app/access.log.

Analyze the log and produce a JSON report at:

/app/report.json

The output must be valid JSON and contain exactly the following fields:

1. total_requests – total number of log entries.
2. unique_ips – number of unique client IP addresses.
3. top_path – the request path that appears most frequently.

Do not include any additional fields.