#!/usr/bin/env python3
"""Demo runner for LogMasker — triggers TypeError captured by Sentry."""
import sys
sys.path.insert(0, ".")

import sentry_sdk
from log_masker import LogMasker

SENTRY_DSN = "https://e993e35c4dac473cb8e2bf332e91e650@o4511426244640768.ingest.us.sentry.io/4511427264315392"

sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0,
                environment="production", release="log-masker@1.0.0")

masker = LogMasker()

samples = [
    "User john@example.com logged in from 192.168.1.100",
    "Card: 4111-1111-1111-1111 charged $99",
    "password=hunter2 api_key=sk-abcdef123456",
    "JWT: eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIn0.abc123def456",
    "Call from +1 (555) 867-5309",
]

print("=== LogMasker results ===")
for s in samples:
    print(f"IN : {s}")
    print(f"OUT: {masker.mask(s)}\n")

# Intentional error — captured by Sentry (event b3c1232ce5184e4499769ed687b5916c)
try:
    masker.mask(None)
except TypeError as e:
    sentry_sdk.capture_exception(e)
    print(f"TypeError captured by Sentry: {e}")
    raise
