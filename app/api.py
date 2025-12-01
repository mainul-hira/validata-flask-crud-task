"""
REST API endpoints for Bank resources.

These endpoints return JSON.
"""

from flask import Blueprint, jsonify, request, current_app
from http import HTTPStatus
from werkzeug.exceptions import HTTPException
from sqlalchemy import func

from . import db
from .models import Bank

api_bp = Blueprint("api", __name__)

"""
Error Handlers (JSON only for API blueprint) are defined below.
"""


@api_bp.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException) -> tuple[dict, int]:
    """
    Handle HTTP errors (404, 400, 403, etc.) for API routes.

    Flask / Werkzeug raises HTTPException for typical HTTP errors.
    By default, Flask renders an HTML error page. For API routes
    we want to return a JSON payload instead.
    """
    response = {
        "error": e.name,
        "message": e.description,
    }
    return jsonify(response), e.code


@api_bp.errorhandler(Exception)
def handle_unexpected_exception(e: Exception) -> tuple[dict, int]:
    """
    Catch-all handler for unhandled exceptions in API routes.

    This prevents exposing internal errors to the client.
    We log the error and return a generic JSON 500 response.
    """
    # Log full stack trace in the app logger for debugging
    current_app.logger.exception(f"Unhandled exception in API: {e}")

    response = {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred. Please try again later.",
    }
    return jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR


"""
API endpoints below.
"""


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
        return (
            jsonify(
                {
                    "error": "Invalid request body",
                    "message": "Both name and location must be provided",
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    # Check if another bank with the same name and location already exists
    if Bank.query.filter(
        func.lower(Bank.name) == func.lower(name),
        func.lower(Bank.location) == func.lower(location),
    ).first():
        return jsonify(
            {
                "error": "Existing bank",
                "message": "Another bank with this name and location already exists",
            }
        ), HTTPStatus.BAD_REQUEST

    bank: Bank = Bank(name=name, location=location)
    db.session.add(bank)
    db.session.commit()

    return jsonify(bank.to_dict()), HTTPStatus.CREATED


@api_bp.route("/banks/<int:bank_id>", methods=["GET"])
def get_bank_details(bank_id: int) -> tuple[dict, int]:
    """
    GET /api/banks/<bank_id>

    Return JSON for a single bank or 404 if not found.
    """
    bank: Bank = Bank.query.get_or_404(bank_id, f"Bank with id {bank_id} not found")
    return jsonify(bank.to_dict()), HTTPStatus.OK


@api_bp.route("/banks/<int:bank_id>", methods=["PUT", "PATCH"])
def update_bank(bank_id):
    """
    PUT/PATCH /api/banks/<bank_id>

    Update an existing bank. Expects JSON with 'name' and/or 'location'.
    """
    bank: Bank = Bank.query.get_or_404(bank_id, f"Bank with id {bank_id} not found")
    data: dict = request.get_json() or {}

    name: str | None = data.get("name")
    location: str | None = data.get("location")

    if not (name or location):
        return (
            jsonify(
                {
                    "error": "Invalid request body",
                    "message": "Either name or location must be provided",
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    # Check if another bank with the same name and location already exists except the current bank
    if Bank.query.filter(
        Bank.id != bank_id,
        func.lower(Bank.name) == func.lower(name),
        func.lower(Bank.location) == func.lower(location),
    ).first():
        return jsonify(
            {
                "error": "Existing bank",
                "message": "Another bank with this name and location already exists",
            }
        ), HTTPStatus.BAD_REQUEST

    if name:
        bank.name = name
    if location:
        bank.location = location

    db.session.commit()

    return jsonify(bank.to_dict()), HTTPStatus.OK


@api_bp.route("/banks/<int:bank_id>", methods=["DELETE"])
def delete_bank(bank_id: int) -> tuple[str, int]:
    """
    DELETE /api/banks/<bank_id>

    Delete an existing bank.
    """
    bank: Bank = Bank.query.get_or_404(bank_id, f"Bank with id {bank_id} not found")
    db.session.delete(bank)
    db.session.commit()
    # 204 No Content indicates success with no response body
    return "", HTTPStatus.NO_CONTENT
