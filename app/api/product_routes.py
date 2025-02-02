from flask import Blueprint, jsonify, session, request
from flask_login import login_required
from app.models import Product, User, db
from app.forms import ProductForm
from datetime import date
from .aws_helpers import get_unique_filename, upload_file_to_s3, remove_file_from_s3

product_routes = Blueprint('products', __name__)

@product_routes.route('/')
def get_all_products():
    """"
    Query for all products route that returns all of the products from the db.
    """
    all_products = Product.query.all()
    response = [one_product.to_dict() for one_product in all_products]

    # Adds owner username to product
    for product in response:
        owner_id = product['owner_id']
        owner = User.query.get(owner_id)
        product_owner = owner.to_dict()
        product['owner_info'] = product_owner['username']
    return response


@product_routes.route('/<int:id>')
def get_product_by_id(id):
    """"
    Query for single product route that retuns a single product from the db.
    """
    # print(id)
    one_product = Product.query.get(id)
    product = one_product.to_dict()

    # Adds owner username to product
    owner_id = product['owner_id']
    owner = User.query.get(owner_id)
    product_owner = owner.to_dict()
    product['owner_info'] = product_owner['username']
    # print("PRODUCTTTTTTTTTTTTTTTTTTT:", product)

    return product


# create a new product

@product_routes.route('/new', methods=['POST'])
@login_required
def post_new_product():
    form = ProductForm()
    print('FORM DATA:',form.data)
    owner_id = session.get('_user_id')
    form['csrf_token'].data = request.cookies["csrf_token"]

    image = form.data['preview_img']
    image.filename = get_unique_filename(image.filename)
    upload = upload_file_to_s3(image)

    if 'url' not in upload:
        return {'error': 'Fix the damn upload'}

    if form.validate_on_submit():
        new_product = Product(
            owner_id = owner_id,
            name = form.data['name'],
            description = form.data['description'],
            price = form.data['price'],
            preview_img = upload['url'],
            created_at = date.today(),
            updated_at = date.today()
        )
    # print('newProduct->', new_product)
          
    return form.errors



@product_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    product = Product.query.get(id)
    print("PRODUCTTTTTTTTTTTTTTTTTTT:", product.to_dict(), product.preview_img)
    if (not product):
        return ('No Product Found'), 404

    remove_file_from_s3(product.preview_img)

    db.session.delete(product)
    db.session.commit()

    return {'Product Successfully Deleted': id}




@product_routes.route('/current')
def get_curr_user_shop():
    """
    Query for all the products that belong to the current user
    """
    owner_id = session.get('_user_id')
    products = Product.query.filter_by(owner_id=owner_id).all()
    return {"products": [product.to_dict() for product in products]}




@product_routes.route('/<int:productId>', methods=['PUT'])
def edit_product(productId):
    """
    Update a product.
    """
    product = Product.query.get(productId)
    data = request.get_json()

    print("DATAAAAAAAAAAAA", data)
    # form['csrf_token'].data = request.cookies["csrf_token"]

    # im  age = data['preview_img']
    # image.filename = get_unique_filename(image.filename)
    # upload = upload_file_to_s3(image)

    # if 'url' not in upload:
    #     return {'error': 'Fix the damn upload'}

    if product:
        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        # product.preview_img= upload["url"]

        db.session.commit()
        return product.to_dict()
    return {"MESSAGE": "this didnt work yooooooo"}
