import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    aliases = db.Column(db.String(255))


class Expense(Base):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("categories.id"))
    created_at = db.Column(db.Date, default=db.func.now())
