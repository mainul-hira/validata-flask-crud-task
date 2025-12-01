"""
Tests for HTML routes (frontend CRUD) using Flask's test client.
This covers:
- listing banks
- pagination behavior on /banks
- creating a bank
- editing a bank
- deleting a bank
- bank detail page
"""

from app import db
from app.models import Bank


def test_get_bank_list_page_empty(client):
    """
    When no banks exist, the /banks page should show a helpful message.
    """
    response = client.get("/banks")
    assert response.status_code == 200
    assert b"No banks found" in response.data
    assert b"Create one" in response.data


def test_bank_list_pagination_first_page_html(client, app):
    """
    Test that /banks shows only the first page of results when paginated.

    We set per_page=5 in the route code.
    """
    with app.app_context():
        # Create 12 banks to force multiple pages
        for i in range(1, 13):
            db.session.add(Bank(name=f"Bank {i}", location=f"City {i}"))
        db.session.commit()

    # Request first page
    response = client.get("/banks?page=1")
    assert response.status_code == 200

    html_text = response.get_data(as_text=True)

    # Page 1 should contain Bank 1..5
    for i in range(1, 6):
        assert f">Bank {i}<" in html_text

    # But should NOT contain Bank 6+
    assert ">Bank 6<" not in html_text
    assert ">Bank 12<" not in html_text

    # Should show pagination controls if more than 1 page
    assert 'class="pagination"' in html_text
    # Current page '1' should appear as current
    assert '<span class="current">1</span>' in html_text


def test_bank_list_pagination_second_page_html(client, app):
    """
    Test that /banks?page=2 shows the second page of results.

    We set per_page=5 in the route code.
    """
    with app.app_context():
        for i in range(1, 13):
            db.session.add(Bank(name=f"Bank {i}", location=f"City {i}"))
        db.session.commit()

    # Request second page
    response = client.get("/banks?page=2")
    assert response.status_code == 200

    html_text = response.get_data(as_text=True)

    # Page 2 should contain Bank 6..10
    for i in range(6, 11):
        assert f">Bank {i}<" in html_text

    # Should not contain Bank 1..5
    assert ">Bank 1<" not in html_text
    assert ">Bank 5<" not in html_text

    # Check pagination current page 2
    assert '<span class="current">2</span>' in html_text


def test_create_bank_via_form(client, app):
    """
    Test creating a bank via the HTML form.
    """
    response = client.post(
        "/banks/create",
        data={"name": "Test Bank", "location": "Dhaka"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Bank created successfully" in response.data
    assert b"Test Bank" in response.data

    # Ensure it's saved in the DB also
    with app.app_context():
        bank = Bank.query.filter_by(name="Test Bank").first()
        assert bank is not None
        assert bank.location == "Dhaka"


def test_update_bank_via_form(client, app):
    """
    Test updating a bank via the HTML form.
    """
    with app.app_context():
        bank = Bank(name="Dhaka Bank", location="City")
        db.session.add(bank)
        db.session.commit()
        bank_id = bank.id

    response = client.post(
        f"/banks/{bank_id}/edit",
        data={"name": "Eastern Bank Ltd.", "location": "Chittagong"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Bank updated successfully" in response.data
    assert b"Eastern Bank Ltd." in response.data

    with app.app_context():
        updated = db.session.get(Bank, bank_id)
        assert updated.name == "Eastern Bank Ltd."
        assert updated.location == "Chittagong"


def test_delete_bank_via_form(client, app):
    """
    Test deleting a bank via the HTML delete route.
    """
    with app.app_context():
        bank = Bank(name="Dhaka Bank", location="Bangladesh")
        db.session.add(bank)
        db.session.commit()
        bank_id = bank.id

    # First show confirmation page
    response = client.get(f"/banks/{bank_id}/delete")
    assert response.status_code == 200
    assert (
        b"Are you sure you want to delete bank <strong>Dhaka Bank</strong>"
        in response.data
    )

    # Then POST to actually delete
    response = client.post(f"/banks/{bank_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Bank deleted successfully" in response.data

    with app.app_context():
        deleted = db.session.get(Bank, bank_id)
        assert deleted is None


def test_bank_detail_page(client, app):
    """
    Test the detail page shows correct bank info.
    """
    with app.app_context():
        bank = Bank(name="Dhaka Bank", location="Dhaka")
        db.session.add(bank)
        db.session.commit()
        bank_id = bank.id

    response = client.get(f"/banks/{bank_id}")
    assert response.status_code == 200
    assert b"Dhaka Bank" in response.data
    assert b"Dhaka" in response.data
