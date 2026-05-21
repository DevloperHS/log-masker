import re
from typing import Union


PATTERNS = {
    "email":       (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL]"),
    "ip":          (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[IP]"),
    "credit_card": (r"\b(?:\d{4}[\-\s]?){3}\d{4}\b", "[CARD]"),
    "phone":       (r"\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE]"),
    "api_key":     (r"(?i)(api[_-]?key|token|secret)\s*[=:]\s*\S+", r"\1=[REDACTED]"),
    "password":    (r"(?i)(password|passwd|pwd)\s*[=:]\s*\S+", r"\1=[REDACTED]"),
    "jwt":         (r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", "[JWT]"),
}


class LogMasker:
    """Masks PII and secrets from log strings using configurable regex patterns."""

    def __init__(self, patterns: dict = None):
        self.patterns = patterns or PATTERNS
        self._compiled = {
            name: (re.compile(pat, re.IGNORECASE if "(?i)" in pat else 0), repl)
            for name, (pat, repl) in self.patterns.items()
        }

    def mask(self, text: Union[str, None]) -> str:
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__!r}")
        for _name, (regex, replacement) in self._compiled.items():
            text = regex.sub(replacement, text)
        return text

    def mask_dict(self, record: dict) -> dict:
        return {k: self.mask(str(v)) if isinstance(v, str) else v
                for k, v in record.items()}

    def mask_lines(self, text: str) -> str:
        return "\n".join(self.mask(line) for line in text.splitlines())
