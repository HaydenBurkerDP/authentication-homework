import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.products_categories_xref import products_categories_association_table


class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    price = db.Column(db.Float())
    active = db.Column(db.Boolean(), default=True)

    categories = db.relationship("Categories", secondary=products_categories_association_table, back_populates="products")

    def __init__(self, name, description, price, active):
        self.name = name
        self.description = description
        self.price = price
        self.active = active

    def get_new_product():
        return Products("", "", 0.0, True)


class ProductsSchema(ma.Schema):
    class Meta:
        fields = ["product_id", "name", "description", "price", "active", "categories"]

    categories = ma.fields.Nested("CategoriesSchema", exclude=["products"], many=True)


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
