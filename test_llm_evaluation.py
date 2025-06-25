"""
Test script for the LLM-based evaluation feature.
NOTE: This script is for reference only. The LLM-based evaluation functionality
has been temporarily removed and will be reimplemented with Langfuse SDK v3.
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

def test_with_auto_eval():
    """Test the agent with automatic LLM-based evaluation enabled."""
    # NOTE: This functionality is pending implementation with Langfuse SDK v3
    
    # Sample question
    question = "What is artificial intelligence?"
    logger.info(f"Question: {question}")
    logger.info("NOTE: LLM-based evaluation is pending implementation with Langfuse SDK v3")
    
    try:
        result = process_question(question)
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Has search results: {result['has_search_results']}")
    except Exception as e:
        logger.error(f"Error processing question: {e}")

def test_without_auto_eval():
    """Test the agent with automatic LLM-based evaluation disabled."""
    # NOTE: This functionality is pending implementation with Langfuse SDK v3
    
    # Sample question
    question = "What is machine learning?"
    logger.info(f"Question: {question}")
    logger.info("NOTE: LLM-based evaluation is pending implementation with Langfuse SDK v3")
    
    try:
        result = process_question(question)
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Has search results: {result['has_search_results']}")
    except Exception as e:
        logger.error(f"Error processing question: {e}")

def test_with_both_eval_types():
    """Test the agent with both automatic and manual evaluation."""
    # NOTE: This functionality is pending implementation with Langfuse SDK v3
    
    # Sample question
    question = "What is deep learning?"
    logger.info(f"Question: {question}")
    
    # Manual toxicity score
    toxicity_score = 0.05  # Very low toxicity score
    
    try:
        result = process_question(question, toxicity=toxicity_score)
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Has search results: {result['has_search_results']}")
        logger.info(f"Toxicity score received: {toxicity_score} (will be implemented with Langfuse SDK v3)")
    except Exception as e:
        logger.error(f"Error processing question: {e}")

if __name__ == "__main__":
    logger.info("Testing Q&A agent with LLM-based evaluation")
    
    # Test with automatic evaluation enabled
    test_with_auto_eval()
    
    logger.info("\n" + "-" * 50 + "\n")
    
    # Test with automatic evaluation disabled
    test_without_auto_eval()
    
    logger.info("\n" + "-" * 50 + "\n")
    
    # Test with both evaluation types
    test_with_both_eval_types()
