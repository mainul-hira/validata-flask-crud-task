"""
HTML page routes for Bank CRUD operations.

These routes handle browser-based interactions—forms, buttons, and links—
so users can create, view, update, and delete Bank records through the web UI.
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from sqlalchemy import func

from . import db
from .models import Bank

# Blueprint for bank-related pages
bank_bp = Blueprint("bank", __name__)


@bank_bp.route("/")
def home():
    """
    Simple home route.

    We redirect users to the list of banks to make the app easy to navigate.
    """
    return redirect(url_for("bank.get_bank_list"))


@bank_bp.route("/banks")
def get_bank_list():
    """
    List all banks with pagination.

    This function queries all Bank records and passes them to the template
    which displays them in a table.
    """

    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1

    per_page = 5

    pagination = Bank.query.order_by(Bank.id).paginate(
        page=page,
        per_page=per_page,
        error_out=True,
    )

    return render_template(
        "bank_list.html", banks=pagination.items, pagination=pagination
    )


@bank_bp.route("/banks/<int:bank_id>")
def get_bank_detail(bank_id):
    """
    Show details for a single bank.

    :param bank_id: ID of the bank to display
    """
    bank = db.get_or_404(Bank, bank_id)
    return render_template("bank_detail.html", bank=bank)


@bank_bp.route("/banks/create", methods=["GET", "POST"])
def create_bank():
    """
    Create a new bank.

    - GET: render an empty form
    - POST: validate form data, insert new Bank, and redirect
    """
    if request.method == "POST":
        name: str | None = request.form.get("name")
        location: str | None = request.form.get("location")

        # Simple validation: ensure both fields are provided
        if not name or not location:
            flash("Name and location are required.", "error")
            return render_template("bank_form.html", mode="create")

        # Check if another bank with the same name and location already exists
        if Bank.query.filter(
            func.lower(Bank.name) == func.lower(name),
            func.lower(Bank.location) == func.lower(location),
        ).first():
            flash("Another bank with this name and location already exists.", "error")
            return render_template("bank_form.html", mode="create")

        new_bank: Bank = Bank(name=name, location=location)
        db.session.add(new_bank)
        db.session.commit()
        flash("Bank created successfully!", "success")
        return redirect(url_for("bank.get_bank_list"))

    # GET request: render the form
    return render_template("bank_form.html", mode="create")


@bank_bp.route("/banks/<int:bank_id>/edit", methods=["GET", "POST"])
def update_bank(bank_id):
    """
    Update an existing bank.

    - GET: render the form pre-filled with existing data.
    - POST: apply updates and save to the database.
    """
    bank: Bank = db.get_or_404(Bank, bank_id)

    if request.method == "POST":
        name: str | None = request.form.get("name")
        location: str | None = request.form.get("location")

        if not name or not location:
            flash("Name and location are required.", "error")
            return render_template("bank_form.html", mode="edit", bank=bank)

        # Check if another bank with the same name and location already exists except the current bank
        if Bank.query.filter(
            Bank.id != bank_id,
            func.lower(Bank.name) == func.lower(name),
            func.lower(Bank.location) == func.lower(location),
        ).first():
            flash("Another bank with this name and location already exists.", "error")
            return render_template("bank_form.html", mode="edit", bank=bank)

        bank.name = name
        bank.location = location
        db.session.commit()

        flash("Bank updated successfully!", "success")
        return redirect(url_for("bank.get_bank_detail", bank_id=bank.id))

    # GET request: render form with existing values
    return render_template("bank_form.html", mode="edit", bank=bank)


@bank_bp.route("/banks/<int:bank_id>/delete", methods=["GET", "POST"])
def delete_bank(bank_id: int) -> str:
    """
    Delete a bank.

    - GET: show a confirmation page.
    - POST: delete the bank and redirect to the list.

    Using POST for deletion is safer than using GET, because GET requests
    should not have side effects.
    """
    bank = db.get_or_404(Bank, bank_id)

    if request.method == "POST":
        db.session.delete(bank)
        db.session.commit()
        flash("Bank deleted successfully.", "success")
        return redirect(url_for("bank.get_bank_list"))

    # GET: show confirmation page
    return render_template("bank_confirm_delete.html", bank=bank)
