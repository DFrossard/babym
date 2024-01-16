import os
import json
import pytest

from babym.app import app
from babym.models.parent import Parent
from babym.mongo import BabymMongoClient
from babym.environments import Environments

babym_mongo_client = BabymMongoClient()
parents_collection = babym_mongo_client.parents_collection

@pytest.fixture
def client():
    if os.environ.get('BABYM_ENV') != Environments.test:
        raise Exception("BABYM_ENV should be set to TEST")
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    parents_collection.delete_many({})
    


def test_create_parent(client):
    name = 'Ana'
    date_of_birth = '2000-01-01'
    email = 'ana_email@email.com'
    data = {
        'name': name,
        'dob': date_of_birth,
        'email': email
    }

    response = client.post('/parent', json=data)
    assert response.status_code == 201

    created_parent_dict = json.loads(response.data)
    created_parent_id = created_parent_dict['_id']
    created_parent = Parent.parse_obj(created_parent_dict)

    # Check that the created Parent has the correct properties
    assert created_parent_id
    assert created_parent.name == name
    assert created_parent.dob.strftime("%Y-%m-%d") == date_of_birth
    assert created_parent.email == email


def test_get_parent(client):
    # Create a new Parent object and insert it into the MongoDB collection
    name = 'Bob'
    date_of_birth = '2000-02-01'
    email = 'bob_email@email.com'
    test_parent = Parent(name=name, dob=date_of_birth, email=email)
    insert_test_result = parents_collection.insert_one(json.loads(test_parent.json()))
    inserted_id = str(insert_test_result.inserted_id)

    # Retrieve the Parent object using its ID
    response = client.get(f'/parent/{inserted_id}')
    assert response.status_code == 200

    retrieved_parent_dict = json.loads(response.data)
    retrieved_parent = Parent.parse_obj(retrieved_parent_dict)

    # Check that the retrieved Parent has the correct properties
    assert retrieved_parent.name == name
    assert retrieved_parent.dob.strftime("%Y-%m-%d") == date_of_birth
    assert retrieved_parent.email == email


def test_update_parent(client):
    # Create a new Parent object and insert it into the MongoDB collection
    name = 'Charlie'
    date_of_birth = '2000-03-01'
    email = 'charlie_email@email.com'
    test_parent = Parent(name=name, dob=date_of_birth, email=email)
    insert_test_result = parents_collection.insert_one(json.loads(test_parent.json()))
    inserted_id = str(insert_test_result.inserted_id)

    # Update the Parent object with new data
    new_date_of_birth = '1999-03-01'
    new_data = {
        'dob': new_date_of_birth
    }

    response = client.put(f'/parent/{inserted_id}', json=new_data)
    assert response.status_code == 200

    updated_parent_dict = json.loads(response.data)
    updated_parent = Parent.parse_obj(updated_parent_dict)

    # Check that the updated Parent has the correct properties
    assert updated_parent.name == name
    assert updated_parent.dob.strftime("%Y-%m-%d") == new_date_of_birth
    assert updated_parent.email == email


def test_delete_parent(client):
    # Create a new Parent object and insert it into the MongoDB collection
    name = 'Eve'
    date_of_birth = '2000-05-01'
    email = 'eve_email@email.com'
    test_parent = Parent(name=name, dob=date_of_birth, email=email)
    insert_test_result = parents_collection.insert_one(json.loads(test_parent.json()))
    inserted_id = str(insert_test_result.inserted_id)

    # Delete the Parent object using its ID
    response = client.delete(f'/parent/{inserted_id}')
    assert response.status_code == 204

    # Try to retrieve the deleted Parent object
    response = client.get(f'/parent/{inserted_id}')
    assert response.status_code == 404


