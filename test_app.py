import pytest
from application import app
from application import db 
from bson import ObjectId
from datetime import datetime


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Setup (clear the database)
            db.todo_flask.delete_many({})
        yield client
        # Teardown (clear the database after tests)
        db.todo_flask.delete_many({})

def test_get_todo_with_data(client):
    # Mock data insert for testing
    db.todo_flask.insert_one({
        "name": "Test Todo",
        "description": "This is a test todo",
        "completed": "NO",
        "date_created": datetime.utcnow()
    })

    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Todo' in response.data  # Check if your test todo is displayed




def test_add_todo(client):
    response = client.post('/add_todo', data={
        'name': 'Test Todo',
        'description': 'This is a test todo',
        'completed': False
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Todo successfully added" in response.data  # Flash message check

    # Check if the todo was added to the database
    todos = list(db.todo_flask.find())
    assert len(todos) == 1
    assert todos[0]['name'] == 'Test Todo'

def test_delete_todo(client):
    # Add a todo to be deleted
    todo_id = db.todo_flask.insert_one({
        'name': 'Delete Me',
        'description': 'Delete this todo',
        'completed': False,
        'date_created': datetime.utcnow()
    }).inserted_id

    response = client.get(f'/delete_todo/{str(todo_id)}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Todo successfully deleted" in response.data  # Flash message check

    # Check if the todo was deleted from the database
    todos = list(db.todo_flask.find())
    assert len(todos) == 0

def test_delete_all_todos(client):
    # Add multiple todos
    db.todo_flask.insert_many([
        {'name': 'Todo 1', 'description': 'First todo', 'completed': False, 'date_created': datetime.utcnow()},
        {'name': 'Todo 2', 'description': 'Second todo', 'completed': False, 'date_created': datetime.utcnow()}
    ])

    response = client.post('/delete_all_todos', follow_redirects=True)
    assert response.status_code == 200
    assert b"All Todos successfully deleted" in response.data  # Flash message check

    # Check if all todos were deleted from the database
    todos = list(db.todo_flask.find())
    assert len(todos) == 0

def test_update_todo(client):
    todo_id = db.todo_flask.insert_one({
        'name': 'Update Me',
        'description': 'Update this todo',
        'completed': False,
        'date_created': datetime.utcnow()
    }).inserted_id

    response = client.post(f'/update_todo/{str(todo_id)}', data={
        'name': 'Updated Todo',
        'description': 'Updated description',
        'completed': True  # Send a boolean value
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Todo successfully updated" in response.data

    updated_todo = db.todo_flask.find_one({'_id': ObjectId(todo_id)})
    assert updated_todo['name'] == 'Updated Todo'
    assert updated_todo['description'] == 'Updated description'
    # Check that 'completed' is stored as a boolean
    assert updated_todo['completed'] is True or updated_todo['completed'] == 'True'
