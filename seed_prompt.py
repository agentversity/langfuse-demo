"""
Script to seed or update the Langfuse prompt for the Q&A agent.
Run this script to create or update the prompt in Langfuse.
"""

from langfuse import get_client
from dotenv import load_dotenv
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Create or update the Langfuse prompt."""
    try:
        # Initialize Langfuse client
        client = get_client()
        
        # Get prompt label from environment or default to "development"
        prompt_label = os.getenv("PROMPT_LABEL", "development")
        
        # Create or update the prompt
        prompt = client.create_prompt(
            name="qa-system-prompt-dev",
            prompt=(
                "You are a helpful assistant that provides clear and concise answers. "
                "When you use information from search results, cite your sources. "
                "{{search_context}}"
            ),
            config={
                "model": "gpt-4o-mini", 
                "temperature": 0
            },
            labels=[prompt_label]
        )
        
        logger.info(f"Successfully created/updated prompt 'qa-system-prompt-dev' with label '{prompt_label}' and version {prompt.version}")
        
    except Exception as e:
        logger.error(f"Error creating/updating Langfuse prompt: {e}")
        raise e

if __name__ == "__main__":
    main()
