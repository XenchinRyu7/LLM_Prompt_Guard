import re
from detect_secrets.plugins.base import RegexBasedDetector

class GCloudApiKeyDetector(RegexBasedDetector):
    """Scans for Google Cloud API Keys."""

    @property
    def secret_type(self) -> str:
        return "Google Cloud API Key"

    @property
    def denylist(self) -> list[re.Pattern]:
        return [
            # For Google Cloud API Key (AIza prefix, followed by 35 alphanumeric characters)
            re.compile(r"(?i)AIza[0-9A-Za-z\\-_]{35}"),
        ]
