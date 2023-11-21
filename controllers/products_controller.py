from flask import jsonify

from db import db
from util.reflection import populate_object
from util.validate_uuid4 import validate_uuid4
from models.products import Products, product_schema, products_schema
from models.categories import Categories
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate_return_auth
def product_add(req, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "must be an administrator to complete this action"}), 403

    post_data = req.form if req.form else req.json

    new_product = Products.get_new_product()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "product added", "product": product_schema.dump(new_product)}), 201


@authenticate
def products_get_all(req):
    products_query = db.session.query(Products).all()

    return jsonify({"message": "products found", "products": products_schema.dump(products_query)}), 200


@authenticate
def product_get_by_id(req, product_id):
    if not validate_uuid4(product_id):
        return jsonify({"message": "invalid product id"}), 400

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    else:
        return jsonify({"message": "product found", "product": product_schema.dump(product_query)}), 200


@authenticate_return_auth
def product_update_by_id(req, product_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "must be an administrator to complete this action"}), 403

    if not validate_uuid4(product_id):
        return jsonify({"message": "invalid product id"}), 400

    post_data = req.form if req.form else req.json
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    populate_object(product_query, post_data)
    db.session.commit()

    return jsonify({"message": "product updated", "product": product_schema.dump(product_query)}), 200


@authenticate_return_auth
def product_activity(req, product_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "must be an administrator to complete this action"}), 403

    if not validate_uuid4(product_id):
        return jsonify({"message": "invalid product id"}), 400

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    product_query.active = not product_query.active
    db.session.commit()

    if product_query.active:
        return jsonify({"message": "product activated", "product": product_schema.dump(product_query)}), 200

    else:
        return jsonify({"message": "product deactivated", "product": product_schema.dump(product_query)}), 200


@authenticate_return_auth
def product_delete_by_id(req, product_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "must be an administrator to complete this action"}), 403

    if not validate_uuid4(product_id):
        return jsonify({"message": "invalid product id"}), 400

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    db.session.delete(product_query)
    db.session.commit()

    return jsonify({"message": "product deleted"}), 200


@authenticate_return_auth
def product_add_category(req, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "must be an administrator to complete this action"}), 403

    post_data = req.form if req.form else req.json

    product_id = post_data.get("product_id")
    if not product_id:
        return jsonify({"message": "product id not found"}), 404

    if not validate_uuid4(product_id):
        return jsonify({"message": "invalid product id"}), 400

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not product_query:
        return jsonify({"message": "product not found"}), 404

    category_id = post_data.get("category_id")
    if not category_id:
        return jsonify({"message": "category id not found"}), 404

    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not category_query:
        return jsonify({"message": "category not found"}), 404

    product_query.categories.append(category_query)

    try:
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to add category to product"}), 400

    return jsonify({"message": "category added", "product": product_schema.dump(product_query)}), 200
