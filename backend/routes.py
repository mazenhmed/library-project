from flask import Blueprint, jsonify, request
from .database import db
from .models import Product, Category, Ad, Offer, Admin, Order

api_bp = Blueprint('api', __name__)

# --- Products ---
@api_bp.route('/products', methods=['GET'])
def get_products():
    category_name = request.args.get('category')
    if category_name and category_name != 'الكل':
        category = Category.query.filter_by(name=category_name).first()
        if category:
            products = Product.query.filter_by(category_id=category.id).all()
        else:
            products = []
    else:
        products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@api_bp.route('/products', methods=['POST'])
def add_product():
    data = request.json
    category_name = data.get('category')
    category = Category.query.filter_by(name=category_name).first()
    
    if not category:
        return jsonify({'error': 'Category not found'}), 400

    new_product = Product(
        name=data['name'],
        price=data['price'],
        category_id=category.id,
        image=data.get('image'),
        rating=data.get('rating', 0.0)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@api_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    
    if 'category' in data:
        category_name = data['category']
        category = Category.query.filter_by(name=category_name).first()
        if category:
            product.category_id = category.id
            
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.image = data.get('image', product.image)
    db.session.commit()
    return jsonify(product.to_dict())

@api_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

# --- Categories ---
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@api_bp.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category already exists'}), 400
        
    new_category = Category(name=data['name'], icon=data.get('icon'))
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

@api_bp.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.json
    category.name = data.get('name', category.name)
    category.icon = data.get('icon', category.icon)
    db.session.commit()
    return jsonify(category.to_dict())

@api_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return '', 204

# --- Ads ---
@api_bp.route('/ads', methods=['GET'])
def get_ads():
    ads = Ad.query.all()
    return jsonify([a.to_dict() for a in ads])

@api_bp.route('/ads', methods=['POST'])
def add_ad():
    data = request.json
    new_ad = Ad(title=data['title'], description=data['description'], icon=data.get('icon'))
    db.session.add(new_ad)
    db.session.commit()
    return jsonify(new_ad.to_dict()), 201

@api_bp.route('/ads/<int:id>', methods=['PUT'])
def update_ad(id):
    ad = Ad.query.get_or_404(id)
    data = request.json
    ad.title = data.get('title', ad.title)
    ad.description = data.get('description', ad.description)
    ad.icon = data.get('icon', ad.icon)
    db.session.commit()
    return jsonify(ad.to_dict())

@api_bp.route('/ads/<int:id>', methods=['DELETE'])
def delete_ad(id):
    ad = Ad.query.get_or_404(id)
    db.session.delete(ad)
    db.session.commit()
    return '', 204

# --- Offers ---
@api_bp.route('/offers', methods=['GET'])
def get_offers():
    offers = Offer.query.all()
    return jsonify([o.to_dict() for o in offers])

@api_bp.route('/offers', methods=['POST'])
def add_offer():
    data = request.json
    new_offer = Offer(title=data['title'], discount=data['discount'], icon=data.get('icon'))
    db.session.add(new_offer)
    db.session.commit()
    return jsonify(new_offer.to_dict()), 201

@api_bp.route('/offers/<int:id>', methods=['PUT'])
def update_offer(id):
    offer = Offer.query.get_or_404(id)
    data = request.json
    offer.title = data.get('title', offer.title)
    offer.discount = data.get('discount', offer.discount)
    offer.icon = data.get('icon', offer.icon)
    db.session.commit()
    return jsonify(offer.to_dict())

@api_bp.route('/offers/<int:id>', methods=['DELETE'])
def delete_offer(id):
    offer = Offer.query.get_or_404(id)
    db.session.delete(offer)
    db.session.commit()
    return '', 204

# --- Admin Auth ---
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and admin.check_password(password):
        return jsonify({'isLoggedIn': True, 'username': admin.username})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# --- Orders ---
@api_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@api_bp.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    new_order = Order(
        total_amount=data['total_amount'],
        items_count=data['items_count']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

# --- Stats ---
@api_bp.route('/stats', methods=['GET'])
def get_stats():
    stats = {
        'categories_count': Category.query.count(),
        'products_count': Product.query.count(),
        'orders_count': Order.query.count(),
        'ads_count': Ad.query.count(),
        'offers_count': Offer.query.count(),
        'products_per_category': []
    }
    
    # Calculate products per category
    categories = Category.query.all()
    for cat in categories:
        count = Product.query.filter_by(category_id=cat.id).count()
        stats['products_per_category'].append((cat.name, count))
        
    return jsonify(stats)
