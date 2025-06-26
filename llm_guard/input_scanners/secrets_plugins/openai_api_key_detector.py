import re
from detect_secrets.plugins.base import RegexBasedDetector

class OpenAIKeyDetector(RegexBasedDetector):
    """Scans for OpenAI API Keys."""

    @property
    def secret_type(self) -> str:
        return "OpenAI API Key"

    @property
    def denylist(self) -> list[re.Pattern]:
        return [
            re.compile(r"(?i)sk-[A-Za-z0-9]{32}")
        ]

    def _scan(self, file_contents: str):
        print("Scanning for OpenAI API Keys...")
        # Custom scanning logic can be implemented here if needed
        print("Custom scanning logic for OpenAI API Keys.")
