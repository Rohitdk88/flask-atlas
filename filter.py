from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# MongoDB Atlas connection using environment variable
client = MongoClient(os.getenv('MONGO_URI'))
db = client.recruitmentdb1

# Set up logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Route for getting all questions
@app.route('/questions', methods=['GET'])
def get_questions():
    questions = list(db.questions.find())
    for question in questions:
        question['_id'] = str(question['_id'])
    return jsonify(questions), 200

# Route for adding a question
@app.route('/questions', methods=['POST'])
def add_question():
    data = request.json
    result = db.questions.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# Route for getting a question by question_id
@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    try:
        question = db.questions.find_one({'question_id': question_id})
        if question:
            question['_id'] = str(question['_id'])
            return jsonify(question), 200
        else:
            return jsonify({'error': 'Question not found'}), 404
    except Exception as e:
        app.logger.error(f"Error retrieving question: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Route for updating a question by question_id
@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    data = request.json
    result = db.questions.update_one({'question_id': question_id}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Question updated successfully'}), 200
    else:
        return jsonify({'error': 'Question not found'}), 404

# Route for deleting a question by question_id
@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    result = db.questions.delete_one({'question_id': question_id})
    if result.deleted_count:
        return jsonify({'message': 'Question deleted successfully'}), 200
    else:
        return jsonify({'error': 'Question not found'}), 404

# Route for getting all tags
@app.route('/tags', methods=['GET'])
def get_tags():
    tags = list(db.tags.find())
    for tag in tags:
        tag['_id'] = str(tag['_id'])
    return jsonify(tags), 200

# Route for adding a tag
@app.route('/tags', methods=['POST'])
def add_tag():
    data = request.json
    result = db.tags.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# Route for getting a tag by tag_id
@app.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    try:
        tag = db.tags.find_one({'tag_id': tag_id})
        if tag:
            tag['_id'] = str(tag['_id'])
            return jsonify(tag), 200
        else:
            return jsonify({'error': 'Tag not found'}), 404
    except Exception as e:
        app.logger.error(f"Error retrieving tag: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Route for updating a tag by tag_id
@app.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    data = request.json
    result = db.tags.update_one({'tag_id': tag_id}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Tag updated successfully'}), 200
    else:
        return jsonify({'error': 'Tag not found'}), 404

# Route for deleting a tag by tag_id
@app.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    result = db.tags.delete_one({'tag_id': tag_id})
    if result.deleted_count:
        return jsonify({'message': 'Tag deleted successfully'}), 200
    else:
        return jsonify({'error': 'Tag not found'}), 404

# Route for getting all mappings
@app.route('/mappings', methods=['GET'])
def get_mappings():
    mappings = list(db.mappings.find())
    for mapping in mappings:
        mapping['_id'] = str(mapping['_id'])
    return jsonify(mappings), 200

# Route for adding a mapping
@app.route('/mappings', methods=['POST'])
def add_mapping():
    data = request.json
    result = db.mappings.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# Route for getting a mapping by mappings_id
@app.route('/mappings/<int:mappings_id>', methods=['GET'])
def get_mapping(mappings_id):
    try:
        mapping = db.mappings.find_one({'mappings_id': mappings_id})
        if mapping:
            mapping['_id'] = str(mapping['_id'])
            return jsonify(mapping), 200
        else:
            return jsonify({'error': 'Mapping not found'}), 404
    except Exception as e:
        app.logger.error(f"Error retrieving mapping: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Route for updating a mapping by mappings_id
@app.route('/mappings/<int:mappings_id>', methods=['PUT'])
def update_mapping(mappings_id):
    data = request.json
    result = db.mappings.update_one({'mappings_id': mappings_id}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Mapping updated successfully'}), 200
    else:
        return jsonify({'error': 'Mapping not found'}), 404

# Route for deleting a mapping by mappings_id
@app.route('/mappings/<int:mappings_id>', methods=['DELETE'])
def delete_mapping(mappings_id):
    result = db.mappings.delete_one({'mappings_id': mappings_id})
    if result.deleted_count:
        return jsonify({'message': 'Mapping deleted successfully'}), 200
    else:
        return jsonify({'error': 'Mapping not found'}), 404

# Route for filtering questions based on tags
@app.route('/questions/filter', methods=['POST'])
def filter_questions():
    try:
        data = request.json
        tags = data.get('tags', [])
        if not tags:
            return jsonify({'error': 'No tags provided'}), 400

        query = {'$or': [{tag: "Yes"} for tag in tags]}
        mappings = db.mappings.find(query)
        questions = [mapping.get('questions') for mapping in mappings if mapping.get('questions')]

        if questions:
            return jsonify({'questions': questions}), 200
        else:
            return jsonify({'message': 'No questions found for the given tags'}), 404
    except Exception as e:
        app.logger.error(f"Error filtering questions: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)