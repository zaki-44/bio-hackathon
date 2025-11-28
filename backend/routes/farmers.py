"""Farmer application routes"""
from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required
from auth import user_type_required
from models import db, FarmerApplication
from config import Config
import os

farmers_bp = Blueprint('farmers', __name__, url_prefix='/api/farmers')

@farmers_bp.route("/applications/<int:application_id>/certification", methods=["GET"])
@jwt_required()
@user_type_required('admin')
def get_farmer_certification(application_id):
    """Get certification file for a farmer application"""
    try:
        application = FarmerApplication.query.get(application_id)
        
        if not application:
            return jsonify({
                "error": "Application not found"
            }), 404
        
        if not application.certification_filename:
            return jsonify({
                "error": "No certification file found"
            }), 404
        
        cert_path = os.path.join(Config.UPLOAD_FOLDER, 'certifications', application.certification_filename)
        
        if not os.path.exists(cert_path):
            return jsonify({
                "error": "Certification file not found on server"
            }), 404
        
        return send_from_directory(
            os.path.dirname(cert_path),
            os.path.basename(cert_path),
            as_attachment=False,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve certification",
            "message": str(e)
        }), 500

