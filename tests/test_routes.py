"""
Tests for HTML routes (frontend CRUD) using Flask's test client.
This covers:
- listing banks
- pagination behavior on /banks
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
