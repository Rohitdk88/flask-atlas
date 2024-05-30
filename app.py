from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client.recruitmentdb1

# Routes for questions collection
@app.route('/questions', methods=['GET'])
def get_questions():
    questions = list(db.questions.find())
    for question in questions:
        question['_id'] = str(question['_id'])
    return jsonify(questions), 200

@app.route('/questions', methods=['POST'])
def add_question():
    data = request.json
    result = db.questions.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/questions/<id>', methods=['GET'])
def get_question(id):
    question = db.questions.find_one({'_id': ObjectId(id)})
    if question:
        question['_id'] = str(question['_id'])
        return jsonify(question), 200
    else:
        return jsonify({'error': 'Question not found'}), 404

@app.route('/questions/<id>', methods=['PUT'])
def update_question(id):
    data = request.json
    result = db.questions.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Question updated successfully'}), 200
    else:
        return jsonify({'error': 'Question not found'}), 404

@app.route('/questions/<id>', methods=['DELETE'])
def delete_question(id):
    result = db.questions.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Question deleted successfully'}), 200
    else:
        return jsonify({'error': 'Question not found'}), 404

# Routes for tags collection
@app.route('/tags', methods=['GET'])
def get_tags():
    tags = list(db.tags.find())
    for tag in tags:
        tag['_id'] = str(tag['_id'])
    return jsonify(tags), 200

@app.route('/tags', methods=['POST'])
def add_tag():
    data = request.json
    result = db.tags.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/tags/<id>', methods=['GET'])
def get_tag(id):
    tag = db.tags.find_one({'_id': ObjectId(id)})
    if tag:
        tag['_id'] = str(tag['_id'])
        return jsonify(tag), 200
    else:
        return jsonify({'error': 'Tag not found'}), 404

@app.route('/tags/<id>', methods=['PUT'])
def update_tag(id):
    data = request.json
    result = db.tags.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Tag updated successfully'}), 200
    else:
        return jsonify({'error': 'Tag not found'}), 404

@app.route('/tags/<id>', methods=['DELETE'])
def delete_tag(id):
    result = db.tags.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Tag deleted successfully'}), 200
    else:
        return jsonify({'error': 'Tag not found'}), 404

# Routes for mappings collection
@app.route('/mappings', methods=['GET'])
def get_mappings():
    mappings = list(db.mappings.find())
    for mapping in mappings:
        mapping['_id'] = str(mapping['_id'])
    return jsonify(mappings), 200

@app.route('/mappings', methods=['POST'])
def add_mapping():
    data = request.json
    result = db.mappings.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/mappings/<id>', methods=['GET'])
def get_mapping(id):
    mapping = db.mappings.find_one({'_id': ObjectId(id)})
    if mapping:
        mapping['_id'] = str(mapping['_id'])
        return jsonify(mapping), 200
    else:
        return jsonify({'error': 'Mapping not found'}), 404

@app.route('/mappings/<id>', methods=['PUT'])
def update_mapping(id):
    data = request.json
    result = db.mappings.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Mapping updated successfully'}), 200
    else:
        return jsonify({'error': 'Mapping not found'}), 404

@app.route('/mappings/<id>', methods=['DELETE'])
def delete_mapping(id):
    result = db.mappings.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Mapping deleted successfully'}), 200
    else:
        return jsonify({'error': 'Mapping not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
