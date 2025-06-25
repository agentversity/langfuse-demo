"""
Test script for the toxicity scoring feature.
This script demonstrates how to use the toxicity scoring feature with the Q&A agent.
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

def test_with_toxicity_score():
    """Test the agent with a toxicity score."""
    # Sample question
    question = "What is artificial intelligence?"
    logger.info(f"Question: {question}")
    
    # Process the question with a toxicity score
    toxicity_score = 0.1  # Low toxicity score (0-1 scale)
    logger.info(f"Adding toxicity score: {toxicity_score}")
    
    try:
        result = process_question(question, toxicity=toxicity_score)
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Has search results: {result['has_search_results']}")
        logger.info(f"Toxicity score {toxicity_score} received (will be implemented with Langfuse SDK v3)")
    except Exception as e:
        logger.error(f"Error processing question: {e}")

def test_without_toxicity_score():
    """Test the agent without a toxicity score."""
    # Sample question
    question = "What is machine learning?"
    logger.info(f"Question: {question}")
    
    # Process the question without a toxicity score
    try:
        result = process_question(question)
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Has search results: {result['has_search_results']}")
        logger.info("No toxicity score added")
    except Exception as e:
        logger.error(f"Error processing question: {e}")

if __name__ == "__main__":
    logger.info("Testing Q&A agent with toxicity scoring")
    
    # Test with toxicity score
    test_with_toxicity_score()
    
    logger.info("\n" + "-" * 50 + "\n")
    
    # Test without toxicity score
    test_without_toxicity_score()
