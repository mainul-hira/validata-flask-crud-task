"""
Simple Python client that interacts with the Flask REST API using 'requests'.

This script demonstrates:
- Listing banks
- Creating a new bank
- Getting details of a bank
- Updating a bank
- Deleting a bank
"""

import requests

BASE_URL = "http://127.0.0.1:5001/api/banks"


def handle_response(resp):
    try:
        data = resp.json()
    except ValueError:
        print("Status:", resp.status_code)
        print("Raw response:", resp.text)
        return

    if resp.ok:
        print("Status:", resp.status_code)
        print("Data:", data)
    else:
        print("Error status:", resp.status_code)
        print("Error:", data.get("error"))
        print("Message:", data.get("message"))


def list_banks():
    """GET /api/banks"""
    resp = requests.get(BASE_URL)
    print("\nLIST BANKS:")
    handle_response(resp)


def create_bank(name, location):
    """POST /api/banks"""
    payload = {"name": name, "location": location}
    resp = requests.post(BASE_URL, json=payload)
    print("\nCREATE BANK:")
    handle_response(resp)
    if resp.ok:
        return resp.json()
    return None


def get_bank(bank_id):
    """GET /api/banks/<id>"""
    resp = requests.get(f"{BASE_URL}/{bank_id}")
    print("\nGET BANK:")
    handle_response(resp)
    if resp.ok:
        return resp.json()
    return None


def update_bank(bank_id, name=None, location=None):
    """PUT /api/banks/<id>"""
    payload = {}
    if name is not None:
        payload["name"] = name
    if location is not None:
        payload["location"] = location
    resp = requests.put(f"{BASE_URL}/{bank_id}", json=payload)
    print("\nUPDATE BANK:")
    handle_response(resp)


def delete_bank(bank_id):
    """DELETE /api/banks/<id>"""
    resp = requests.delete(f"{BASE_URL}/{bank_id}")
    print("\nDELETE BANK:")
    handle_response(resp)


if __name__ == "__main__":
    list_banks()
    created = create_bank("API Bank", "Dhaka")
    bank_id = created["id"]
    get_bank(bank_id)
    update_bank(bank_id, location="Chattogram")
    get_bank(bank_id)
    delete_bank(bank_id)
    list_banks()
