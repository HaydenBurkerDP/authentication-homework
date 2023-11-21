import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.products_categories_xref import products_categories_association_table


class Categories(db.Model):
    __tablename__ = "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)

    products = db.relationship("Products", secondary=products_categories_association_table, cascade="all,delete", back_populates="categories")

    def __init__(self, name):
        self.name = name

    def get_new_category():
        return Categories("")


class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ["category_id", "name", "products"]

    products = ma.fields.Nested("ProductsSchema", exclude=["categories"], many=True)


category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)
