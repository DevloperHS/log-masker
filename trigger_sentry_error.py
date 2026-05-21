#!/usr/bin/env python3
"""Triggers a new Sentry error: re.error from invalid regex pattern in LogMasker."""
import re
import sys
sys.path.insert(0, ".")

import sentry_sdk
from log_masker import LogMasker

SENTRY_DSN = "https://e993e35c4dac473cb8e2bf332e91e650@o4511426244640768.ingest.us.sentry.io/4511427264315392"

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    environment="production",
    release="log-masker@1.1.0",
)

print("=== LogMasker v1.1.0 — SSN pattern demo ===")
masker = LogMasker()

samples = [
    "User john@example.com logged in from 192.168.1.100",
    "SSN: 123-45-6789 on file",
    "Card: 4111-1111-1111-1111 charged $99",
    "password=hunter2 api_key=sk-abcdef123456",
    "JWT: eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIn0.abc123def456",
    "Call from +1 (555) 867-5309",
]

for s in samples:
    print(f"IN : {s}")
    print(f"OUT: {masker.mask(s)}\n")

# Intentional error: invalid regex pattern → re.error captured by Sentry
print("Triggering re.error with invalid pattern...")
try:
    bad_masker = LogMasker(patterns={"broken": ("(unclosed_group", "[X]")})
    bad_masker.mask("test")
except re.error as e:
    sentry_sdk.capture_exception(e)
    sentry_sdk.flush()
    print(f"re.error captured by Sentry: {e}")
    sys.exit(1)
