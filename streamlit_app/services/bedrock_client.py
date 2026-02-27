"""
DataScout — Amazon Bedrock Agent Client.

Wraps the Bedrock Agent Runtime API for query processing with
streaming response parsing and structured output extraction.
Compatible with any Bedrock-supported model (Nova Pro, Claude, etc.).
"""

import logging
import re
from typing import Dict, List

import boto3
import botocore.config

from config import Config

logger = logging.getLogger('datascout.bedrock')


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
        session_state = {
            'sessionAttributes': {
                'dataset_format': 'csv'
            }
        }

        # Nova Pro requires the exact S3 Bucket name that the Bedrock agent has permissions for
        if dataset_uri:
            # Enforce that the bucket name is the one the Bedrock agent role is configured for
            # The DataScoutAgentS3Access role specifically grants access to 'datascout-storage-use2'
            if 'datascout-storage-use2' not in dataset_uri:
                logger.warning(f"Original URI {dataset_uri} doesn't match agent role bucket. Replacing...")
                file_name = dataset_uri.split('/')[-1]
                dataset_uri = f"s3://datascout-storage-use2/datasets/{session_id}/original/{file_name}"
                
            session_state['sessionAttributes']['dataset_uri'] = dataset_uri
            session_state['files'] = [
                {
                    'name': dataset_uri.split('/')[-1],
                    'source': {
                        'sourceType': 'S3',
                        's3Location': {
                            'uri': dataset_uri
                        }
                    },
                    'useCase': 'CODE_INTERPRETER'
                }
            ]

        response = self.client.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias_id,
            sessionId=session_id,
            inputText=query,
            enableTrace=True,
            sessionState=session_state
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

        # Log raw response for debugging — critical when switching models
        logger.debug("Raw agent response length: %d chars", len(full_text))
        logger.debug("Raw agent response:\n%s", full_text)

        if not full_text.strip():
            logger.warning("Agent returned an empty response")
            return {
                'explanation': 'The agent returned an empty response. '
                               'Please try rephrasing your question.',
                'code': '',
                'results': '',
                'visualizations': [],
                'next_steps': []
            }

        return self._extract_components(full_text)

    def _extract_components(self, text: str) -> Dict:
        """Extract structured components from the agent's text response.

        Model-agnostic parser that handles multiple code block formats
        (```python, ```py, bare ```) and provides a fallback when no
        structured sections are found.

        Args:
            text: Full text response from the agent.

        Returns:
            Dict with keys: explanation, code, results, visualizations,
            next_steps.
        """
        components = {
            'explanation': '',
            'code': '',
            'results': '',
            'visualizations': [],
            'next_steps': []
        }

        # ── Extract code blocks (supports ```python, ```py, and bare ```)
        # Try language-tagged blocks first, then fall back to bare blocks
        code_blocks = re.findall(
            r'```(?:python|py)\s*\n(.*?)```', text, re.DOTALL
        )
        if not code_blocks:
            # Try bare code blocks (``` without language tag)
            code_blocks = re.findall(
                r'```\s*\n(.*?)```', text, re.DOTALL
            )

        if code_blocks:
            components['code'] = code_blocks[-1].strip()

        # ── Extract S3 visualization URIs
        # Nova Pro might omit the file extension or use markdown formats like ![chart](s3://...)
        s3_uris = re.findall(r's3://[^\s\>\"\'\]\)]+', text)
        components['visualizations'] = s3_uris

        # ── Split text around ALL code blocks for explanation and results
        # Use a broad pattern that matches any fenced code block
        parts = re.split(r'```(?:\w*)\s*\n.*?```', text, flags=re.DOTALL)

        if len(parts) >= 1 and parts[0].strip():
            components['explanation'] = parts[0].strip()
        if len(parts) >= 2:
            # Combine all parts after the first code block as results
            results_text = '\n'.join(p.strip() for p in parts[1:] if p.strip())
            components['results'] = results_text

        # ── Extract next steps / suggestions
        next_steps_match = re.search(
            r'(?:next\s*steps?|suggestions?|you\s*(?:can|could|might)\s*(?:also|try))[:\s]*\n'
            r'((?:\s*[-•*\d.]+\s*.+\n?)+)',
            text, re.IGNORECASE
        )
        if next_steps_match:
            steps_text = next_steps_match.group(1)
            steps = re.findall(r'[-•*\d.]+\s*(.+)', steps_text)
            components['next_steps'] = [s.strip() for s in steps if s.strip()]

        # ── Fallback: if nothing was extracted, put the entire text as
        # explanation so the user always sees the agent's response
        if (not components['explanation'] and
                not components['code'] and
                not components['results']):
            logger.info("No structured components found; using raw text as explanation")
            components['explanation'] = text.strip()

        return components
