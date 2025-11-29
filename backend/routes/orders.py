"""Order routes"""
from flask import Blueprint, jsonify, request, session
from models import db, User, Product, Order, OrderItem
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@orders_bp.route("", methods=["POST"])
def create_order():
    """Create a new order from cart items"""
    try:
        # Check authentication
        if not session.get('logged_in'):
            return jsonify({
                "error": "Not authenticated",
                "message": "Please login first"
            }), 401
        
        user_id = session.get('user_id')
        data = request.get_json()
        cart_items = data.get('items', [])
        
        if not cart_items:
            return jsonify({
                "error": "Empty cart",
                "message": "Cannot create order with empty cart"
            }), 400
            
        # Calculate total and verify items
        total_amount = 0
        order_items = []
        
        for item in cart_items:
            product_id = item.get('id')
            quantity = item.get('quantity')
            
            if not product_id or not quantity:
                continue
                
            product = Product.query.get(product_id)
            if not product:
                continue
                
            # Check availability
            if not product.is_available or product.quantity < quantity:
                return jsonify({
                    "error": "Product unavailable",
                    "message": f"Product {product.name} is not available in requested quantity"
                }), 400
                
            # Update product quantity
            product.quantity -= quantity
            if product.quantity <= 0:
                product.is_available = False
                
            total_amount += product.price * quantity
            
            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })
            
        # Create Order
        new_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status='pending'
        )
        db.session.add(new_order)
        db.session.flush() # Get ID
        
        # Create OrderItems
        for item in order_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
            
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Order created successfully",
            "order": new_order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to create order",
            "message": str(e)
        }), 500

@orders_bp.route("", methods=["GET"])
def get_orders():
    """Get user's orders"""
    try:
        if not session.get('logged_in'):
            return jsonify({
                "error": "Not authenticated",
                "message": "Please login first"
            }), 401
            
        user_id = session.get('user_id')
        
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            "success": True,
            "count": len(orders),
            "orders": [order.to_dict() for order in orders]
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch orders",
            "message": str(e)
        }), 500
