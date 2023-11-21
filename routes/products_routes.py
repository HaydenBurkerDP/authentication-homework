from flask import Blueprint, request

import controllers

products = Blueprint("products", __name__)


@products.route("/product", methods=["POST"])
def product_add():
    return controllers.product_add(request)


@products.route("/products", methods=["GET"])
def products_get_all():
    return controllers.products_get_all(request)


@products.route("/product/<product_id>", methods=["GET"])
def product_get_by_id(product_id):
    return controllers.product_get_by_id(request, product_id)


@products.route("/product/<product_id>", methods=["PUT"])
def product_update_by_id(product_id):
    return controllers.product_update_by_id(request, product_id)


@products.route("/product/activity/<product_id>", methods=["PATCH"])
def product_activity(product_id):
    return controllers.product_activity(request, product_id)


@products.route("/product/delete/<product_id>", methods=["DELETE"])
def product_delete_by_id(product_id):
    return controllers.product_delete_by_id(request, product_id)


@products.route("/product/category-add", methods=["PATCH"])
def product_add_category():
    return controllers.product_add_category(request)
