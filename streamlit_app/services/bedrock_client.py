"""
DataScout — Amazon Bedrock Agent Client.

Wraps the Bedrock Agent Runtime API for query processing with
streaming response parsing and structured output extraction.
"""

import re
from typing import Dict, List

import boto3
import botocore.config

from config import Config


class BedrockAgentClient:
    """Amazon Bedrock Agent Runtime client wrapper.

    Handles invocation of the Bedrock Agent, streaming response parsing,
    and extraction of structured components (explanation, code, results,
    visualizations) from the agent's response.
    """

    def __init__(self):
        """Initialize the Bedrock Agent Runtime client."""
        config = botocore.config.Config(
            region_name=Config.AWS_REGION,
            retries={'max_attempts': 3, 'mode': 'adaptive'},
            read_timeout=60
        )
        self.client = boto3.client('bedrock-agent-runtime', config=config)
        self.agent_id: str = Config.BEDROCK_AGENT_ID
        self.agent_alias_id: str = Config.BEDROCK_AGENT_ALIAS_ID

    def invoke_agent(self, query: str, session_id: str,
                     dataset_uri: str) -> Dict:
        """Invoke the Bedrock Agent with a user query.

        Args:
            query: The natural language question from the user.
            session_id: Unique session identifier for conversation context.
            dataset_uri: S3 URI of the uploaded dataset.

        Returns:
            Structured dict with keys: explanation, code, results,
            visualizations, next_steps.

        Raises:
            botocore.exceptions.ClientError: On AWS API errors.
        """
        response = self.client.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias_id,
            sessionId=session_id,
            inputText=query,
            enableTrace=True,
            sessionState={
                'sessionAttributes': {
                    'dataset_uri': dataset_uri,
                    'dataset_format': 'csv'
                }
            }
        )
        return self._parse_response(response)

    def _parse_response(self, response: dict) -> Dict:
        """Parse streaming response into structured components.

        Args:
            response: Raw response from invoke_agent API.

        Returns:
            Structured dict with extracted components.
        """
        chunks: List[str] = []
        for event in response.get('completion', []):
            if 'chunk' in event:
                chunk_bytes = event['chunk'].get('bytes', b'')
                chunks.append(chunk_bytes.decode('utf-8'))

        full_text = ''.join(chunks)
        return self._extract_components(full_text)

    def _extract_components(self, text: str) -> Dict:
        """Extract structured components from the agent's text response.

        Parses the response to isolate:
        - Explanation text (before code blocks)
        - Python code (from fenced code blocks)
        - Results text (after code blocks)
        - Visualization S3 URIs (s3://...png)

        Args:
            text: Full text response from the agent.

        Returns:
            Dict with keys: explanation, code, results, visualizations, next_steps.
        """
        components = {
            'explanation': '',
            'code': '',
            'results': '',
            'visualizations': [],
            'next_steps': []
        }

        # Extract Python code blocks
        code_blocks = re.findall(r'```python\n(.*?)```', text, re.DOTALL)
        if code_blocks:
            components['code'] = code_blocks[-1].strip()

        # Extract S3 visualization URIs
        s3_uris = re.findall(r's3://[^\s\)\"\']+\.png', text)
        components['visualizations'] = s3_uris

        # Split text around code blocks for explanation and results
        parts = re.split(r'```python.*?```', text, flags=re.DOTALL)
        if len(parts) >= 1:
            components['explanation'] = parts[0].strip()
        if len(parts) >= 2:
            components['results'] = parts[-1].strip()

        return components
