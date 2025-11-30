"""
Database models for the application.
"""

from . import db


class Bank(db.Model):
    """
    Represents a Bank record in the database.

    Fields:
        id       - Integer primary key
        name     - Name of the bank
        location - Location of the bank
    """

    __tablename__ = "banks"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    location: str = db.Column(db.String(255), nullable=False)

    def to_dict(self) -> dict:
        """
        Convert the Bank instance into a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
        }

    def __repr__(self) -> str:
        return f"<Bank id={self.id} name={self.name!r} location={self.location!r}>"