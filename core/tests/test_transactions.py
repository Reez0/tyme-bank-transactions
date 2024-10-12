import requests
import pytest

BASE_URL = "http://localhost:5000/transactions"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    clear_database()
    yield
    clear_database()


def clear_database():
    pass


def test_retrieve_all_transactions():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json()['data'], list)


def test_create_transaction():
    new_transaction = {
        "amount": 100,
        "type": "credit",
        "description": "Test transaction",
        "date": "2024-10-12"
    }
    response = requests.post(BASE_URL, json=new_transaction)
    assert response.status_code == 201
    assert response.json()['message'] == "Transaction created successfully"


def test_integration_transaction_flow():
    new_transaction = {
        "amount": 100,
        "type": "credit",
        "description": "Test transaction",
        "date": "2024-10-12"
    }

    response = requests.post(BASE_URL, json=new_transaction)
    assert response.status_code == 201

    response = requests.get(BASE_URL)
    assert response.status_code == 200
    transactions = response.json()['data']
    latest = transactions[-1]
    updated_transaction = {
        "amount": 150,
        "type": "debit",
        "description": "Updated transaction",
        "date": "2024-10-12"
    }
    transaction_id = latest['id']
    response = requests.put(
        f"{BASE_URL}/{transaction_id}", json=updated_transaction)
    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/{transaction_id}")
    assert response.status_code == 200

    response = requests.delete(f"{BASE_URL}/{transaction_id}")
    assert response.status_code == 200
    assert response.json()['message'] == "Transaction deleted successfully"

    response = requests.get(f"{BASE_URL}/{transaction_id}")
    assert response.status_code == 404
