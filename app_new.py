from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# MongoDB Atlas connection using environment variable
client = MongoClient(os.getenv('MONGO_URI'))
db = client.recruitmentdb1

# Set up logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Utility function to convert ObjectId to string
def convert_objectid_to_str(documents):
    for document in documents:
        document['_id'] = str(document['_id'])
    return documents

# Utility function to validate required fields
def validate_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    return missing_fields

# Routes for Questions
@app.route('/questions', methods=['GET'])
def get_questions():
    questions = list(db.questions.find())
    questions = convert_objectid_to_str(questions)
    return jsonify(questions), 200

@app.route('/questions', methods=['POST'])
def add_question():
    data = request.json
    required_fields = ["created_at", "created_by", "modified_at", "modified_by", "question", "question_id"]
    missing_fields = validate_fields(data, required_fields)
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    result = db.questions.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/questions/many', methods=['POST'])
def add_many_questions():
    data = request.json
    required_fields = ["created_at", "created_by", "modified_at", "modified_by", "question", "question_id"]
    for item in data:
        missing_fields = validate_fields(item, required_fields)
        if missing_fields:
            return jsonify({'error': f'Missing fields in one or more items: {", ".join(missing_fields)}'}), 400
    result = db.questions.insert_many(data)
    return jsonify({'inserted_ids': [str(id) for id in result.inserted_ids]}), 201

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

@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    data = request.json
    result = db.questions.update_one({'question_id': question_id}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Question updated successfully'}), 200
    else:
        return jsonify({'error': 'Question not found'}), 404

@app.route('/questions/update_many', methods=['PUT'])
def update_many_questions():
    filter_criteria = request.json.get('filter', {})
    update_data = request.json.get('update', {})
    result = db.questions.update_many(filter_criteria, {'$set': update_data})
    return jsonify({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    result = db.questions.delete_one({'question_id': question_id})
    if result.deleted_count:
        return jsonify({'message': 'Question deleted successfully'}), 200
    else:
        return jsonify({'error': 'Question not found'}), 404

@app.route('/questions/delete_many', methods=['DELETE'])
def delete_many_questions():
    filter_criteria = request.json
    result = db.questions.delete_many(filter_criteria)
    return jsonify({'deleted_count': result.deleted_count}), 200

@app.route('/questions/delete_all', methods=['DELETE'])
def delete_all_questions():
    result = db.questions.delete_many({})
    return jsonify({'deleted_count': result.deleted_count}), 200

# Routes for Tags
@app.route('/tags', methods=['GET'])
def get_tags():
    tags = list(db.tags.find())
    tags = convert_objectid_to_str(tags)
    return jsonify(tags), 200

@app.route('/tags', methods=['POST'])
def add_tag():
    data = request.json
    required_fields = ["created_at", "created_by", "modified_at", "modified_by", "level", "tag", "tag_id"]
    missing_fields = validate_fields(data, required_fields)
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    result = db.tags.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/tags/many', methods=['POST'])
def add_many_tags():
    data = request.json
    required_fields = ["created_at", "created_by", "modified_at", "modified_by", "level", "tag", "tag_id"]
    for item in data:
        missing_fields = validate_fields(item, required_fields)
        if missing_fields:
            return jsonify({'error': f'Missing fields in one or more items: {", ".join(missing_fields)}'}), 400
    result = db.tags.insert_many(data)
    return jsonify({'inserted_ids': [str(id) for id in result.inserted_ids]}), 201

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

@app.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    data = request.json
    result = db.tags.update_one({'tag_id': tag_id}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Tag updated successfully'}), 200
    else:
        return jsonify({'error': 'Tag not found'}), 404

@app.route('/tags/update_many', methods=['PUT'])
def update_many_tags():
    filter_criteria = request.json.get('filter', {})
    update_data = request.json.get('update', {})
    result = db.tags.update_many(filter_criteria, {'$set': update_data})
    return jsonify({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@app.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    result = db.tags.delete_one({'tag_id': tag_id})
    if result.deleted_count:
        return jsonify({'message': 'Tag deleted successfully'}), 200
    else:
        return jsonify({'error': 'Tag not found'}), 404

@app.route('/tags/delete_many', methods=['DELETE'])
def delete_many_tags():
    filter_criteria = request.json
    result = db.tags.delete_many(filter_criteria)
    return jsonify({'deleted_count': result.deleted_count}), 200

@app.route('/tags/delete_all', methods=['DELETE'])
def delete_all_tags():
    result = db.tags.delete_many({})
    return jsonify({'deleted_count': result.deleted_count}), 200

# Routes for Mappings
@app.route('/mappings', methods=['GET'])
def get_mappings():
    mappings = list(db.mappings.find())
    mappings = convert_objectid_to_str(mappings)
    return jsonify(mappings), 200

@app.route('/mappings', methods=['POST'])
def add_mapping():
    data = request.json
    required_fields = ["created_at", "created_by", "is_mandatory", "mappings_id", "modified_at", "modified_by", "question_id", "tag_id"]
    missing_fields = validate_fields(data, required_fields)
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    result = db.mappings.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/mappings/many', methods=['POST'])
def add_many_mappings():
    data = request.json
    required_fields = ["created_at", "created_by", "is_mandatory", "mappings_id", "modified_at", "modified_by", "question_id", "tag_id"]
    for item in data:
        missing_fields = validate_fields(item, required_fields)
        if missing_fields:
            return jsonify({'error': f'Missing fields in one or more items: {", ".join(missing_fields)}'}), 400
    result = db.mappings.insert_many(data)
    return jsonify({'inserted_ids': [str(id) for id in result.inserted_ids]}), 201

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

@app.route('/mappings/<int:mappings_id>', methods=['PUT'])
def update_mapping(mappings_id):
    data = request.json
    result = db.mappings.update_one({'mappings_id': mappings_id}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Mapping updated successfully'}), 200
    else:
        return jsonify({'error': 'Mapping not found'}), 404

@app.route('/mappings/update_many', methods=['PUT'])
def update_many_mappings():
    filter_criteria = request.json.get('filter', {})
    update_data = request.json.get('update', {})
    result = db.mappings.update_many(filter_criteria, {'$set': update_data})
    return jsonify({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@app.route('/mappings/<int:mappings_id>', methods=['DELETE'])
def delete_mapping(mappings_id):
    result = db.mappings.delete_one({'mappings_id': mappings_id})
    if result.deleted_count:
        return jsonify({'message': 'Mapping deleted successfully'}), 200
    else:
        return jsonify({'error': 'Mapping not found'}), 404

@app.route('/mappings/delete_many', methods=['DELETE'])
def delete_many_mappings():
    filter_criteria = request.json
    result = db.mappings.delete_many(filter_criteria)
    return jsonify({'deleted_count': result.deleted_count}), 200

@app.route('/mappings/delete_all', methods=['DELETE'])
def delete_all_mappings():
    result = db.mappings.delete_many({})
    return jsonify({'deleted_count': result.deleted_count}), 200

if __name__ == '__main__':
    app.run(debug=True)
