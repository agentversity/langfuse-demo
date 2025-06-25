"""
Test script for the Q&A agent with Langfuse prompt management.
This script demonstrates how to use the agent with different prompt labels.
"""

import os
from dotenv import load_dotenv
import logging
from agent import process_question

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Test the agent with a sample question."""
    # Get the current prompt label
    prompt_label = os.getenv("PROMPT_LABEL", "development")
    logger.info(f"Using prompt label: {prompt_label}")
    
    # Sample question
    question = "What is artificial intelligence?"
    logger.info(f"Question: {question}")
    
    # Process the question
    try:
        result = process_question(question)
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Has search results: {result['has_search_results']}")
    except Exception as e:
        logger.error(f"Error processing question: {e}")

if __name__ == "__main__":
    main()
