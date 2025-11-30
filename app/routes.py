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
    List all banks.

    This function queries all Bank records and passes them to the template
    which displays them in a table.
    """
    banks = Bank.query.all()
    return render_template("bank_list.html", banks=banks)


@bank_bp.route("/banks/<int:bank_id>")
def get_bank_detail(bank_id):
    """
    Show details for a single bank.

    :param bank_id: ID of the bank to display
    """
    bank = Bank.query.get_or_404(bank_id)
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

        new_bank = Bank(name=name, location=location)
        db.session.add(new_bank)
        db.session.commit()
        flash("Bank created successfully!", "success")
        return redirect(url_for("bank.get_bank_list"))

    # GET request: render the form
    return render_template("bank_form.html", mode="create")