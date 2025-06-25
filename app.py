from flask import Flask, render_template, request, jsonify, make_response
from agent import process_question
import os
import uuid
from dotenv import load_dotenv
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Check if OpenAI API key is set
if not os.environ.get("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY is not set. Please set it in the .env file.")

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Process a question and return the answer"""
    # Get the question from the form
    question = request.form.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Get user ID from cookie or generate a new one
        user_id = request.cookies.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
        
        # Check if toxicity score is provided (optional)
        toxicity = None
        if 'toxicity' in request.form:
            try:
                toxicity = float(request.form.get('toxicity'))
            except (ValueError, TypeError):
                logger.warning("Invalid toxicity value provided, ignoring")
        
        # Process the question using our agent
        result = process_question(question, user_id, toxicity)
        
        # Create response with answer and metadata
        response = jsonify({
            'answer': result['answer'],
            'has_citations': result.get('has_search_results', False) or any(term in result['answer'].lower() for term in 
                           ['source', 'according to', 'research', 'found', 'search'])
        })
        
        # Set user_id cookie if it doesn't exist
        if not request.cookies.get('user_id'):
            response = make_response(response)
            response.set_cookie('user_id', user_id, max_age=60*60*24*30)  # 30 days
        
        return response
    except Exception as e:
        # Handle any errors
        return jsonify({'error': str(e)}), 500

@app.route('/score', methods=['POST'])
def score():
    """Add a toxicity score to a previous answer"""
    try:
        # Get required parameters
        data = request.get_json() if request.is_json else request.form
        
        question = data.get('question')
        toxicity = data.get('toxicity')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        if toxicity is None:
            return jsonify({'error': 'Toxicity score is required'}), 400
            
        try:
            toxicity_value = float(toxicity)
            if not (0 <= toxicity_value <= 1):
                return jsonify({'error': 'Toxicity must be between 0 and 1'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Toxicity must be a number between 0 and 1'}), 400
        
        # Get user ID from cookie or generate a new one
        user_id = request.cookies.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
        
        # Process the question again, but this time with the toxicity score
        # This will trigger both user feedback scoring and automated LLM evaluation
        result = process_question(question, user_id, toxicity_value)
        
        return jsonify({
            'success': True,
            'message': f'Expert feedback score of {toxicity_value} received and applied. Automated toxicity evaluation also performed.'
        })
        
    except Exception as e:
        logger.error(f"Error adding toxicity score: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True)
