"""
REST API endpoints for Bank resources.

These endpoints return JSON.
"""

from flask import Blueprint, jsonify, request
from http import HTTPStatus

from . import db
from .models import Bank

api_bp = Blueprint("api", __name__)


@api_bp.route("/banks", methods=["GET"])
def get_bank_list() -> tuple[dict, int]:
    """
    GET /api/banks

    Return a JSON list of all banks.
    """
    banks: list[Bank] = Bank.query.all()
    bank_list: list[dict] = [bank.to_dict() for bank in banks]
    return jsonify(bank_list), HTTPStatus.OK


@api_bp.route("/banks", methods=["POST"])
def create_bank():
    """
    POST /api/banks

    Create a new bank. Expects JSON body with 'name' and 'location'.
    """
    data: dict = request.get_json() or {}
    if not data:
        return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST
    name: str = data.get("name")
    location: str = data.get("location")

    if not name or not location:
        return jsonify({"error": "name and location are required"}), HTTPStatus.BAD_REQUEST

    bank: Bank = Bank(name=name, location=location)
    db.session.add(bank)
    db.session.commit()

    return jsonify(bank.to_dict()), HTTPStatus.CREATED