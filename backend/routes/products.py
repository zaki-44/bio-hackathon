"""Product routes"""
from flask import Blueprint, jsonify, request, session, send_from_directory
from models import db, User, Product
from config import Config
from utils import allowed_file, generate_unique_filename, get_mime_type, ensure_directory_exists
from uuid import uuid4
import os

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

@products_bp.route("", methods=["POST"])
def create_product():
    """Create a new product (farmer only)"""
    try:
        # Check if user is logged in via session
        logged_in = session.get('logged_in', False)
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        
        if not logged_in:
            return jsonify({
                "error": "Not authenticated",
                "message": "Please login first"
            }), 401
        
        # Check if user is a farmer
        if user_type != 'farmer':
            return jsonify({
                "error": "Unauthorized",
                "message": "Only farmers can post products"
            }), 403
        
        # Verify user still exists in database
        farmer = User.query.get(user_id)
        if not farmer or farmer.user_type != 'farmer':
            return jsonify({
                "error": "Invalid session",
                "message": "Farmer account not found or invalid"
            }), 403
        
        farmer_id = farmer.id
        
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description', '')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        unit = request.form.get('unit', 'kg')
        category = request.form.get('category', '')
        location = request.form.get('location', '')
        
        # Validate required fields
        if not name or not price or not quantity:
            return jsonify({
                "error": "Missing required fields",
                "message": "Name, price, and quantity are required"
            }), 400
        
        try:
            price = float(price)
            quantity = float(quantity)
        except ValueError:
            return jsonify({
                "error": "Invalid data",
                "message": "Price and quantity must be numbers"
            }), 400
        
        # Handle photo upload
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
                photo_filename = generate_unique_filename(file.filename)
                file_path = os.path.join(Config.UPLOAD_FOLDER, photo_filename)
                ensure_directory_exists(Config.UPLOAD_FOLDER)
                file.save(file_path)
        
        # Create product
        new_product = Product(
            farmer_id=farmer_id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            unit=unit,
            category=category,
            location=location,
            photo_filename=photo_filename
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Product created successfully",
            "product": new_product.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to create product",
            "message": str(e)
        }), 500

@products_bp.route("/<int:product_id>/photo", methods=["GET"])
def get_product_photo(product_id):
    """Get product photo by product ID"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({
                "error": "Product not found"
            }), 404
        
        if not product.photo_filename:
            return jsonify({
                "error": "Product has no photo"
            }), 404
        
        photo_path = os.path.join(Config.UPLOAD_FOLDER, product.photo_filename)
        
        if not os.path.exists(photo_path):
            print(f"Photo file not found: {photo_path}")
            return jsonify({
                "error": "Photo file not found on server",
                "path": photo_path
            }), 404
        
        mimetype = get_mime_type(product.photo_filename)
        
        response = send_from_directory(
            Config.UPLOAD_FOLDER,
            product.photo_filename,
            as_attachment=False,
            mimetype=mimetype
        )
        
        # Add CORS headers for image requests
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        
        return response
    
    except Exception as e:
        print(f"Error serving photo: {e}")
        return jsonify({
            "error": "Failed to retrieve photo",
            "message": str(e)
        }), 500

@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get product details by ID with farmer rating information"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({
                "error": "Product not found"
            }), 404
        
        if not product.is_available:
            return jsonify({
                "error": "Product not available"
            }), 404
        
        # Get product data
        product_data = product.to_dict()
        
        # Get farmer information with rating
        farmer = User.query.get(product.farmer_id)
        if farmer:
            farmer_data = farmer.to_dict()
            product_data['farmer'] = farmer_data
        
        return jsonify({
            "success": True,
            "product": product_data
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch product",
            "message": str(e)
        }), 500

@products_bp.route("/search", methods=["GET"])
def search_products():
    """Search for products by name"""
    try:
        search_query = request.args.get('q', '').strip()
        
        if not search_query:
            return jsonify({
                "error": "Missing search query",
                "message": "Please provide a search query parameter 'q'"
            }), 400
        
        # Search products by name (case-insensitive partial match)
        products = Product.query.filter(
            Product.name.ilike(f'%{search_query}%'),
            Product.is_available == True
        ).all()
        
        return jsonify({
            "success": True,
            "query": search_query,
            "count": len(products),
            "products": [product.to_dict() for product in products]
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Search failed",
            "message": str(e)
        }), 500

