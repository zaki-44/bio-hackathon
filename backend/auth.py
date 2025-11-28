from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def user_type_required(*allowed_types):
    """
    Decorator to restrict access to specific user types.
    Usage: @user_type_required('farmer', 'transporter')
    Note: Must be used after @jwt_required()
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            
            # Handle both dict and string identity formats
            if isinstance(current_user, dict):
                user_type = current_user.get('user_type')
            else:
                # If identity is just an ID, we'd need to look it up
                # For now, assume it's a dict
                return jsonify({
                    'error': 'Invalid token format',
                    'message': 'Token identity must be a dictionary with user_type'
                }), 401
            
            if user_type not in allowed_types:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'This endpoint requires one of the following user types: {", ".join(allowed_types)}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

