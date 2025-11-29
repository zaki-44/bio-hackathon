"""Delivery routes"""
from flask import Blueprint, jsonify, request, session
from models import db, User, Package
from datetime import datetime

delivery_bp = Blueprint('delivery', __name__, url_prefix='/api/delivery')

@delivery_bp.route("/packages", methods=["GET"])
def get_packages():
    """Get packages assigned to the logged-in transporter"""
    try:
        # Check authentication
        if not session.get('logged_in'):
            return jsonify({
                "error": "Not authenticated",
                "message": "Please login first"
            }), 401
        
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        
        # Verify user is a transporter (or admin/farmer if needed, but mainly transporter)
        # For now, let's restrict to transporter or admin
        if user_type not in ['transporter', 'admin']:
             return jsonify({
                "error": "Unauthorized",
                "message": "Access restricted to delivery personnel"
            }), 403

        # If admin, maybe show all packages? For now, let's stick to assigned packages for transporter
        if user_type == 'transporter':
             packages = Package.query.filter_by(transporter_id=user_id).order_by(Package.created_at.desc()).all()
        else:
             # Admin sees all
             packages = Package.query.order_by(Package.created_at.desc()).all()
        
        return jsonify({
            "success": True,
            "count": len(packages),
            "packages": [pkg.to_dict() for pkg in packages]
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch packages",
            "message": str(e)
        }), 500

@delivery_bp.route("/packages/<int:package_id>/status", methods=["PUT"])
def update_package_status(package_id):
    """Update the status of a package"""
    try:
        # Check authentication
        if not session.get('logged_in'):
            return jsonify({
                "error": "Not authenticated",
                "message": "Please login first"
            }), 401
            
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        
        if user_type not in ['transporter', 'admin']:
             return jsonify({
                "error": "Unauthorized",
                "message": "Access restricted to delivery personnel"
            }), 403
            
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({
                "error": "Missing status",
                "message": "Status is required"
            }), 400
            
        valid_statuses = ['pending', 'picked_up', 'in_transit', 'delivered', 'failed']
        if new_status not in valid_statuses:
             return jsonify({
                "error": "Invalid status",
                "message": f"Status must be one of: {', '.join(valid_statuses)}"
            }), 400

        package = Package.query.get(package_id)
        
        if not package:
            return jsonify({
                "error": "Package not found"
            }), 404
            
        # Verify ownership if transporter
        if user_type == 'transporter' and package.transporter_id != user_id:
            return jsonify({
                "error": "Unauthorized",
                "message": "You can only update packages assigned to you"
            }), 403
            
        package.status = new_status
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Package status updated",
            "package": package.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to update package status",
            "message": str(e)
        }), 500
