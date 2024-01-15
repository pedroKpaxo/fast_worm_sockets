from app.lib.mongo.mongo_client import get_db_handle

database_name = 'users'
users_collection_name = 'users'

# TODO Develop a betterway to mock or interact with the db
client = get_db_handle()
db = client[database_name]
users_collection = db[users_collection_name]


def test_create_user(test_client):
    users_collection.find_one_and_delete({'email': 'testuser@test.com'})
    data = {
        "name": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword",
        "password_confirm": "testpassword",
    }
    response = test_client.post(
        "/register",
        json=data
    )

    assert response.status_code == 201
    assert data.get("name") == response.json().get("name")
    users_collection.find_one_and_delete({'email': 'testuser@test.com'})


def test_login_user(test_client):
    users_collection.find_one_and_delete({'email': 'testuser@test.com'})
    data = {
        "name": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword",
        "password_confirm": "testpassword",
    }
    response = test_client.post(
        "/register",
        json=data
    )

    assert response.status_code == 201
    assert data.get("name") == response.json().get("name")
    data = {
        "email": "testuser@test.com",
        "password": "testpassword"
    }
    response = test_client.post(
        "/login",
        json=data
    )
    assert response.status_code == 200
    users_collection.find_one_and_delete({'email': 'testuser@test.com'})
