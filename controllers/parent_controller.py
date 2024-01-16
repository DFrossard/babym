import json
from flask import Blueprint, request, jsonify
from bson import ObjectId

from babym.models.parent import Parent
from babym.mongo import BabymMongoClient

parent_controller = Blueprint('parent_controller', __name__)
baby_mongo_client = BabymMongoClient()
parents_collection = baby_mongo_client.parents_collection

@parent_controller.route('/parent', methods=['POST'])
def create_parent():
    # Parse the JSON data from the request body
    data = request.get_json()

    # Create a new Parent object using the data
    parent = Parent(
        name = data['name'],
        dob = data['dob'],
        email = data['email']
    )

    # Insert the Parent object into the MongoDB collection
    inserted_parent = parents_collection.insert_one(json.loads(parent.json()))
    parent_id = str(inserted_parent.inserted_id)
    response = parent.dict()
    response['_id']= parent_id

    # Return a JSON response with the new Parent object and a 201 status code
    return jsonify(response), 201

@parent_controller.route('/parent/<string:parent_id>', methods=['GET'])
def get_parent(parent_id):
    # Find the Parent object with the matching ID in the MongoDB collection
    parent_dict = parents_collection.find_one(ObjectId(parent_id))

    # If the Parent object exists, create a new Parent object from the dictionary data
    if parent_dict:
        parent = Parent(
            name=parent_dict['name'],
            dob=parent_dict['dob'],
            email= parent_dict['email'],
            id=str(parent_dict['_id'])
        )

        # Return a JSON response with the Parent object or a 404 status code if not found
        return (jsonify(parent.__dict__), 200)

    # If the Parent object doesn't exist, return a 404 status code
    else:
        return '', 404
    
@parent_controller.route('/parent/<string:parent_id>', methods=['PUT'])
def update_parent(parent_id):
    # Find the Parent object with the matching ID in the MongoDB collection
    parent_dict = parents_collection.find_one(ObjectId(parent_id))

    # If the Parent object exists, update it with the new data
    if parent_dict:
        data = request.get_json()
        parent_dict['name'] = data.get('name', parent_dict['name'])
        parent_dict['dob'] = data.get('dob', parent_dict['dob'])
        parent_dict['email'] = data.get('email', parent_dict['email'])

        parents_collection.update_one(
            {'_id': ObjectId(parent_id)},
            {'$set': parent_dict}
        )

        # Return a JSON response with the updated Baby object and a 204 status code
        parent_dict['_id'] = str(parent_dict['_id'])
        return jsonify(parent_dict), 200

    # If the Parent object doesn't exist, return a 404 status code
    else:
        return '', 404

@parent_controller.route('/parent/<string:parent_id>', methods=['DELETE'])
def delete_parent(parent_id):
    # Find the Parent object with the matching ID in the MongoDB collection
    parent_dict = parents_collection.find_one(ObjectId(parent_id))

    # If the Parent object exists, delete it from the MongoDB collection
    if parent_dict:
        parents_collection.delete_one({'_id': ObjectId(parent_id)})

        # Return a 204 status code
        return '', 204

    # If the Parent object doesn't exist, return a 404 status code
    else:
        return '', 404