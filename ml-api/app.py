# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import pipeline
# import spacy

# app = Flask(__name__)
# CORS(app)  # Enable CORS to allow requests from your frontend

# # Load a pre-trained sentiment analysis model from Hugging Face Transformers
# emotion_analyzer = pipeline('sentiment-analysis')

# # Load the SpaCy model for dependency parsing and semantic similarity
# nlp = spacy.load("en_core_web_md")

# # Define a set of keywords for the "adventurous" mood
# adventurous_keywords = [
#     "adventure", "exciting", "explore", "thrilling", "bold", "daring", "risk"
# ]

# # Function to check if a keyword is negated in the user's text
# def is_keyword_negated(text, keyword):
#     doc = nlp(text)
#     for token in doc:
#         if token.text.lower() == keyword.lower():
#             for child in token.children:
#                 if child.dep_ == "neg":  # Dependency label "neg" indicates negation
#                     return True
#     return False

# @app.route('/', methods=['GET'])
# def home():
#     return "Welcome to the Mood Analysis API! The server is running."



# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.get_json()
#     user_text = data.get('text')
    
#     if not user_text:
#         return jsonify({'error': 'No text provided'}), 400

#     # Perform sentiment analysis on the input text
#     analysis = emotion_analyzer(user_text)
#     sentiment = analysis[0]['label'].lower()
#     score = analysis[0]['score']

#     # Initialize the mood as neutral
#     mood = 'neutral'

#     # Map the sentiment to one of the predefined moods
#     if sentiment == 'positive':
#         mood = 'happy'
#     elif sentiment == 'negative':
#         mood = 'sad'
#     elif sentiment == 'neutral':
#         mood = 'calm'

#     # Use SpaCy for further mood detection
#     user_doc = nlp(user_text.lower())

#     # Check for "adventurous" mood using keyword matching and dependency parsing
#     adventurous_detected = False
#     for keyword in adventurous_keywords:
#         if keyword in user_text.lower():
#             if not is_keyword_negated(user_text, keyword):  # Check for negation
#                 adventurous_detected = True
#                 break

#     # If no negation was found and a keyword matched, or if semantic similarity is high
#     if adventurous_detected:
#         mood = "adventurous"
#     else:
#         # Use semantic similarity to detect the adventurous mood if no negation is found
#         for keyword in adventurous_keywords:
#             keyword_doc = nlp(keyword)
#             if user_doc.similarity(keyword_doc) > 0.7:  # Adjust threshold as needed
#                 mood = "adventurous"
#                 break

#     return jsonify({'mood': mood, 'score': score})

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)  # Change the port to 5001


from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import spacy

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your frontend

# Load a pre-trained sentiment analysis model from Hugging Face Transformers
emotion_analyzer = pipeline('sentiment-analysis')

# Load the SpaCy model for dependency parsing and semantic similarity
nlp = spacy.load("en_core_web_md")

# Define a set of keywords for the "adventurous" mood
adventurous_keywords = [
    "adventure", "exciting", "explore", "thrilling", "bold", "daring", "risk"
]

# Function to check if a keyword is negated in the user's text
def is_keyword_negated(text, keyword):
    doc = nlp(text)
    for token in doc:
        if token.text.lower() == keyword.lower():
            for child in token.children:
                if child.dep_ == "neg":  # Dependency label "neg" indicates negation
                    return True
    return False

# Add a simple home route
@app.route('/')
def home():
    return "Welcome to the Mood Analysis API! Use the /analyze endpoint to analyze moods."

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_text = data.get('text')
    
    if not user_text:
        return jsonify({'error': 'No text provided'}), 400

    # Perform sentiment analysis on the input text
    analysis = emotion_analyzer(user_text)
    sentiment = analysis[0]['label'].lower()
    score = analysis[0]['score']

    # Initialize the mood as neutral
    mood = 'neutral'

    # Map the sentiment to one of the predefined moods
    if sentiment == 'positive':
        mood = 'happy'
    elif sentiment == 'negative':
        mood = 'sad'
    elif sentiment == 'neutral':
        mood = 'calm'

    # Use SpaCy for further mood detection
    user_doc = nlp(user_text.lower())

    # Check for "adventurous" mood using keyword matching and dependency parsing
    adventurous_detected = False
    for keyword in adventurous_keywords:
        if keyword in user_text.lower():
            if not is_keyword_negated(user_text, keyword):  # Check for negation
                adventurous_detected = True
                break

    # If no negation was found and a keyword matched, or if semantic similarity is high
    if adventurous_detected:
        mood = "adventurous"
    else:
        # Use semantic similarity to detect the adventurous mood if no negation is found
        for keyword in adventurous_keywords:
            keyword_doc = nlp(keyword)
            if user_doc.similarity(keyword_doc) > 0.7:  # Adjust threshold as needed
                mood = "adventurous"
                break

    return jsonify({'mood': mood, 'score': score})

if __name__ == '__main__':
    app.run(debug=True, port=5001)