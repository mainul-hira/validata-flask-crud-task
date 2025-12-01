"""
Tests for the REST API endpoints.

This covers:
- empty bank list
- bank list with pagination
- creating a bank
- bank details
- updating a bank
- deleting a bank
- create duplicate bank
- update duplicate bank
- update same bank
- test 400 error (custom error handler)
- test missing fields on create bank

"""

from app import db
from app.models import Bank


def test_api_get_bank_list_empty(client):
    """
    When there are no banks, the API should return an empty list
    and valid pagination metadata.
    """
    response = client.get("/api/banks")
    assert response.status_code == 200

    data = response.get_json()
    assert "data" in data
    assert data["data"] == []

    pagination = data["pagination"]
    assert pagination["total"] == 0
    assert pagination["total_pages"] == 0
    assert pagination["page"] == 1
    assert pagination["has_prev"] is False
    assert pagination["has_next"] is False


def test_api_get_bank_list_pagination_multiple_pages(client, app):
    """
    Test that the API returns correct pagination metadata and items
    when there are multiple pages.

    per_page = 5 (as in api_list_banks).
    """
    with app.app_context():
        for i in range(1, 13):  # 12 banks
            db.session.add(Bank(name=f"Bank {i}", location=f"City {i}"))
        db.session.commit()

    # Request page 2 with per_page=5
    response = client.get("/api/banks?page=2&per_page=5")
    assert response.status_code == 200
    data = response.get_json()

    items = data["data"]
    pagination = data["pagination"]

    # Should get 5 items on page 2 (banks 6..10)
    assert len(items) == 5
    assert items[0]["name"] == "Bank 6"
    assert items[-1]["name"] == "Bank 10"

    # Check pagination metadata
    assert pagination["page"] == 2
    assert pagination["per_page"] == 5
    assert pagination["total"] == 12
    assert pagination["total_pages"] == 3
    assert pagination["has_prev"] is True
    assert pagination["has_next"] is True
    assert pagination["next_page"] == 3
    assert pagination["prev_page"] == 1


def test_api_create_bank(client, app):
    """
    Test creating a bank through the API.
    """
    payload = {"name": "API Test Bank", "location": "Dhaka"}
    response = client.post("/api/banks", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "API Test Bank"
    assert data["location"] == "Dhaka"

    with app.app_context():
        bank = Bank.query.filter_by(name="API Test Bank").first()
        assert bank is not None


def test_api_get_bank_detail(client, app):
    """
    Test fetching a bank details via the API.
    """
    with app.app_context():
        bank = Bank(name="Detail Bank", location="City")
        db.session.add(bank)
        db.session.commit()
        bank_id = bank.id

    response = client.get(f"/api/banks/{bank_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == bank_id
    assert data["name"] == "Detail Bank"
    assert data["location"] == "City"


def test_api_update_bank(client, app):
    """
    Test updating a bank via the API.
    """
    with app.app_context():
        bank = Bank(name="Dhaka Bank", location="City")
        db.session.add(bank)
        db.session.commit()
        bank_id = bank.id

    payload = {"location": "New City"}
    response = client.put(f"/api/banks/{bank_id}", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["location"] == "New City"

    with app.app_context():
        updated = db.session.get(Bank, bank_id)
        assert updated.location == "New City"


def test_api_delete_bank(client, app):
    """
    Test deleting a bank via the API.
    """
    with app.app_context():
        bank = Bank(name="Dhaka Bank", location="Bangladesh")
        db.session.add(bank)
        db.session.commit()
        bank_id = bank.id

    response = client.delete(f"/api/banks/{bank_id}")
    assert response.status_code == 204

    with app.app_context():
        deleted = db.session.get(Bank, bank_id)
        assert deleted is None


def test_api_create_bank_duplicate(client, app):
    """
    When creating a bank with duplicate name and location, the API should return a
    JSON 400 error.
    """
    # Seed one bank
    with app.app_context():
        db.session.add(Bank(name="Dup Bank", location="Dhaka"))
        db.session.commit()

    # Try to create duplicate (case-insensitive)
    resp = client.post("/api/banks", json={"name": "dup bank", "location": "dhaka"})
    assert resp.status_code == 400

    data = resp.get_json()
    assert data["error"] == "Existing bank"
    assert "already exists" in data["message"].lower()


def test_api_update_bank_duplicate(client, app):
    """
    When updating a bank with duplicate name and location, the API should return a
    JSON 400 error.
    """

    with app.app_context():
        db.session.add(Bank(name="Bank 1", location="Dhaka"))
        bank = Bank(name="Bank 2", location="Chittagong")
        db.session.add(bank)
        db.session.commit()
        bank_id = bank.id

    # Try to update bank 2 with bank 1's name and location
    resp = client.put(
        f"/api/banks/{bank_id}", json={"name": "bank 1", "location": "dhaka"}
    )
    assert resp.status_code == 400

    data = resp.get_json()
    assert data["error"] == "Existing bank"
    assert "already exists" in data["message"].lower()


def test_api_update_same_bank(client, app):
    """
    When updating a bank with same name and location, the API should return a
    JSON 200 status.
    """

    with app.app_context():
        bank = Bank(name="Bank 1", location="Dhaka")
        db.session.add(bank)
        db.session.commit()
        bank_id = bank.id

    # Try to update bank 1 with same name and location
    resp = client.put(
        f"/api/banks/{bank_id}", json={"name": "bank 1", "location": "dhaka"}
    )
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["name"] == "bank 1"
    assert data["location"] == "dhaka"


def test_api_404_returns_json(client):
    """
    Requesting a non-existent bank should return a JSON error.
    """
    response = client.get("/api/banks/9999")
    assert response.status_code == 404

    data = response.get_json()
    assert data["error"] == "Not Found"
    # message is what we passed in get_or_404(description="Bank with id 9999 not found")
    assert "Bank with id 9999 not found" in data["message"]


def test_api_400_on_missing_fields(client):
    """
    When creating a bank with missing fields, the API should return a
    JSON 400 error.
    """
    response = client.post("/api/banks", json={})

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Invalid request body"
    assert "name" in data["message"].lower()
    assert "location" in data["message"].lower()
