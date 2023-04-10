import json
from flask import Blueprint, request, jsonify
from bson import ObjectId

from babym.models.baby import Baby
from babym.app import babies_collection

baby_controller = Blueprint('baby_controller', __name__)

@baby_controller.route('/baby', methods=['POST'])
def create_baby():
    # Parse the JSON data from the request body
    data = request.get_json()

    # Create a new Baby object using the data
    baby = Baby(
        name = data['name'],
        dob = data['dob'],
        weight = data['weight'],
        height = data['height']
    )

    # Insert the Baby object into the MongoDB collection
    inserted_baby = babies_collection.insert_one(json.loads(baby.json()))
    baby_id = str(inserted_baby.inserted_id)
    response = baby.dict()
    response['_id']= baby_id

    # Return a JSON response with the new Baby object and a 201 status code
    return jsonify(response), 201

@baby_controller.route('/baby/<string:baby_id>', methods=['GET'])
def get_baby(baby_id):
    # Find the Baby object with the matching ID in the MongoDB collection
    baby_dict = babies_collection.find_one(ObjectId(baby_id))

    # If the Baby object exists, create a new Baby object from the dictionary data
    if baby_dict:
        baby = Baby(
            name=baby_dict['name'],
            dob=baby_dict['dob'],
            weight= baby_dict['weight'],
            height=baby_dict['height'],
            id=str(baby_dict['_id'])
        )

        # Return a JSON response with the Baby object or a 404 status code if not found
        return (jsonify(baby.__dict__), 200)

    # If the Baby object doesn't exist, return a 404 status code
    else:
        return '', 404

@baby_controller.route('/baby/<string:baby_id>', methods=['PUT'])
def update_baby(baby_id):
    # Find the Baby object with the matching ID in the MongoDB collection
    baby_dict = babies_collection.find_one(ObjectId(baby_id))

    # If the Baby object exists, update its properties with the new data
    if baby_dict:
        data = request.get_json()
        baby_dict['name'] = data.get('name', baby_dict['name'])
        baby_dict['dob'] = data.get('dob', baby_dict['dob'])
        baby_dict['weight'] = data.get('weight', baby_dict['weight'])
        baby_dict['height'] = data.get('height', baby_dict['height'])

        # Update the Baby object in the MongoDB collection
        babies_collection.update_one({'_id': ObjectId(baby_id)}, {'$set': baby_dict})

        # Return a JSON response with the updated Baby object and a 200 status code
        baby_dict['_id'] = str(baby_dict['_id'])
        return jsonify(baby_dict), 200

    # If the Baby object doesn't exist, return a 404 status code
    else:
        return '', 404

@baby_controller.route('/baby/<string:baby_id>', methods=['DELETE'])
def delete_baby(baby_id):
    # Delete the Baby object with the matching ID from the MongoDB collection
    result = babies_collection.delete_one({'_id': ObjectId(baby_id)})

    # If the delete operation was successful, return a 204 status code with an empty response body
    if result.deleted_count > 0:
        return '', 204

    # If the Baby object doesn't exist, return a 404 status code
    else:
        return '', 404
