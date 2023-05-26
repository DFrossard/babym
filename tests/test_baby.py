import os
import json
import pytest

from babym.app import app
from babym.models.baby import Baby
from babym.mongo import BabymMongoClient
from babym.environments import Environments

babym_mongo_client = BabymMongoClient()
babies_collection = babym_mongo_client.babies_collection

@pytest.fixture
def client():
    if os.environ.get('BABYM_ENV') != Environments.test:
        raise Exception("BABYM_ENV should be set to TEST")
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    babies_collection.delete_many({})
    


def test_create_baby(client):
    data = {
        'name': 'Alice',
        'dob': '2022-01-01',
        'weight': 3.2,
        'height': 50.0
    }

    response = client.post('/baby', json=data)
    assert response.status_code == 201

    created_baby_dict = json.loads(response.data)
    created_baby_id = created_baby_dict['_id']
    created_baby = Baby.parse_obj(created_baby_dict)

    # Check that the created Baby has the correct properties
    assert created_baby_id
    assert created_baby.name == 'Alice'
    assert created_baby.dob.strftime("%Y-%m-%d") == '2022-01-01'
    assert created_baby.weight == 3.2
    assert created_baby.height == 50.0


def test_get_baby(client):
    # Create a new Baby object and insert it into the MongoDB collection
    test_baby = Baby(name='Bob', dob='2022-02-01', weight=4.5, height=60.0)
    insert_test_result = babies_collection.insert_one(json.loads(test_baby.json()))
    inserted_id = str(insert_test_result.inserted_id)

    # Retrieve the Baby object using its ID
    response = client.get(f'/baby/{inserted_id}')
    assert response.status_code == 200

    retrieved_baby_dict = json.loads(response.data)
    retrieved_baby = Baby.parse_obj(retrieved_baby_dict)

    # Check that the retrieved Baby has the correct properties
    assert retrieved_baby.name == 'Bob'
    assert retrieved_baby.dob.strftime("%Y-%m-%d") == '2022-02-01'
    assert retrieved_baby.weight == 4.5
    assert retrieved_baby.height == 60.0


def test_update_baby(client):
    # Create a new Baby object and insert it into the MongoDB collection
    test_baby = Baby(name='Charlie', dob= '2022-03-01', weight= 5.5, height= 70.0)
    insert_test_result = babies_collection.insert_one(json.loads(test_baby.json()))
    inserted_id = str(insert_test_result.inserted_id)

    # Update the Baby object with new data
    new_data = {
        'name': 'David',
        'dob': '2022-04-01',
        'weight': 6.5,
        'height': 80.0
    }

    response = client.put(f'/baby/{inserted_id}', json=new_data)
    assert response.status_code == 200

    updated_baby_dict = json.loads(response.data)
    updated_baby = Baby.parse_obj(updated_baby_dict)

    # Check that the updated Baby has the correct properties
    assert updated_baby.name == 'David'
    assert updated_baby.dob.strftime("%Y-%m-%d") == '2022-04-01'
    assert updated_baby.weight == 6.5
    assert updated_baby.height == 80.0


def test_delete_baby(client):
    # Create a new Baby object and insert it into the MongoDB collection
    test_baby = Baby(name='Eve', dob='2022-05-01', weight=7.5, height=90.0)
    insert_test_result = babies_collection.insert_one(json.loads(test_baby.json()))
    inserted_id = str(insert_test_result.inserted_id)

    # Delete the Baby object using its ID
    response = client.delete(f'/baby/{inserted_id}')
    assert response.status_code == 204

    # Try to retrieve the deleted Baby object
    response = client.get(f'/baby/{inserted_id}')
    assert response.status_code == 404


