"""
DataScout — Centralized Application Configuration.

Loads configuration from environment variables with sensible defaults.
All required variables are validated on startup.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Centralized application configuration from environment variables."""

    # ── AWS ───────────────────────────────────────────────────────────────────
    AWS_REGION: str = os.getenv('AWS_REGION', 'us-east-1')
    S3_BUCKET: str = os.getenv('S3_BUCKET', 'datascout-storage')
    BEDROCK_AGENT_ID: str = os.getenv('BEDROCK_AGENT_ID', '')
    BEDROCK_AGENT_ALIAS_ID: str = os.getenv('BEDROCK_AGENT_ALIAS_ID', 'PRODUCTION')

    # ── Application Limits ────────────────────────────────────────────────────
    MAX_FILE_SIZE_MB: int = int(os.getenv('MAX_FILE_SIZE_MB', '100'))
    SUPPORTED_FORMATS: set = {'.csv', '.xlsx', '.xls', '.json'}
    SESSION_TIMEOUT_SECONDS: int = int(os.getenv('SESSION_TIMEOUT_MINUTES', '30')) * 60
    CODE_EXECUTION_TIMEOUT: int = 30  # seconds
    MAX_CONCURRENT_QUERIES: int = int(os.getenv('MAX_CONCURRENT_QUERIES', '5'))

    # ── Feature Flags ─────────────────────────────────────────────────────────
    ENABLE_VISUALIZATIONS: bool = True
    ENABLE_ADVANCED_STATS: bool = True
    DEBUG_MODE: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def validate(cls) -> bool:
        """Validate all required configuration variables are set.

        Raises:
            EnvironmentError: If any required variable is missing.

        Returns:
            True if all required variables are present.
        """
        required = {
            'BEDROCK_AGENT_ID': cls.BEDROCK_AGENT_ID,
            'S3_BUCKET': cls.S3_BUCKET,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        return True
