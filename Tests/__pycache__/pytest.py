import app.pytest as pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


def test_health(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {'status': 'up', 'version': None}


def test_chat(test_client):
    response = test_client.post("/chat", json={"history": [], "text": "Hello"})
    assert response.status_code == 200
    assert "Hello" in response.json()["output"]


def test_recommend(test_client):
    # 1. Test without required fields
    response = test_client.post("/recommend", json={
        "text": ""})
    assert response.status_code == 200
    assert "please provide the following details" in response.json()["output"].lower()

    response = test_client.post("/recommend", json={
        "text": "Name: John"})
    assert response.status_code == 200
    assert "please provide the following details" in response.json()["output"].lower()

    # 2. Test with required fields (city, budget, guest count, etc.)
    response = test_client.post("/recommend", json={
        "text": "I would like to book a room in Los Angeles for 2 guests, from April 1 to April 5, with a budget of $1000."})
    assert response.status_code == 200
    assert "Here are some recommendations for you" in response.json()["output"].lower()

    # 3. Test with confirmation of recommendation
    response = test_client.post("/recommend", json={
        "text": "I want to book the first one."})
    assert response.status_code == 200
    assert "The link for final confirmation for your booking" in response.json()["output"].lower()

    # 4. Test with already booked accomodation
    response = test_client.post("/recommend", json={
        "text": "I want to book the first one."})
    assert response.status_code == 200
    assert "Your apartment was booked already. Your listing overview" in response.json()["output"].lower()
