from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'farmer', 'transporter', 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_average_rating(self):
        """Calculate average rating for farmers"""
        if self.user_type != 'farmer':
            return None
        
        from sqlalchemy import func
        result = db.session.query(func.avg(FarmerRating.rating)).filter(
            FarmerRating.farmer_id == self.id
        ).scalar()
        
        return round(float(result), 2) if result else None
    
    def get_rating_count(self):
        """Get total number of ratings for farmers"""
        if self.user_type != 'farmer':
            return 0
        
        return FarmerRating.query.filter_by(farmer_id=self.id).count()
    
    def to_dict(self):
        """Convert user object to dictionary"""
        avg_rating = self.get_average_rating() if self.user_type == 'farmer' else None
        rating_count = self.get_rating_count() if self.user_type == 'farmer' else 0
        
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'user_type': self.user_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'average_rating': avg_rating,
            'rating_count': rating_count
        }
    
    def __repr__(self):
        return f'<User {self.username} - {self.user_type}>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # 'kg', 'ton', 'piece', etc.
    category = db.Column(db.String(100), nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_available = db.Column(db.Boolean, default=True)
    
    # Relationship
    farmer = db.relationship('User', backref='products')
    
    def to_dict(self):
        """Convert product object to dictionary"""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farmer_username': self.farmer.username if self.farmer else None,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'unit': self.unit,
            'category': self.category,
            'photo_url': f'/api/products/{self.id}/photo' if self.photo_filename else None,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_available': self.is_available
        }
    
    def __repr__(self):
        return f'<Product {self.name} by Farmer {self.farmer_id}>'


class FarmerApplication(db.Model):
    __tablename__ = 'farmer_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    farm_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    certification_filename = db.Column(db.String(255), nullable=True)  # Store certification file
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'denied'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, nullable=True)  # Admin user ID who reviewed
    denial_reason = db.Column(db.Text, nullable=True)
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert application object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'farm_name': self.farm_name,
            'location': self.location,
            'phone': self.phone,
            'description': self.description,
            'status': self.status,
            'certification_url': f'/api/farmers/applications/{self.id}/certification' if self.certification_filename else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'reviewed_by': self.reviewed_by,
            'denial_reason': self.denial_reason
        }
    
    def __repr__(self):
        return f'<FarmerApplication {self.username} - {self.status}>'


class FarmerRating(db.Model):
    __tablename__ = 'farmer_ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farmer = db.relationship('User', foreign_keys=[farmer_id], backref='ratings_received')
    user = db.relationship('User', foreign_keys=[user_id], backref='ratings_given')
    
    # Unique constraint: one user can only rate a farmer once
    __table_args__ = (db.UniqueConstraint('farmer_id', 'user_id', name='unique_farmer_user_rating'),)
    
    def to_dict(self):
        """Convert rating object to dictionary"""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farmer_username': self.farmer.username if self.farmer else None,
            'user_id': self.user_id,
            'user_username': self.user.username if self.user else None,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<FarmerRating {self.rating} stars by User {self.user_id} for Farmer {self.farmer_id}>'


class Package(db.Model):
    __tablename__ = 'packages'
    
    id = db.Column(db.Integer, primary_key=True)
    transporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    recipient_address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'picked_up', 'in_transit', 'delivered', 'failed'
    tracking_number = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    transporter = db.relationship('User', backref='packages')
    
    def to_dict(self):
        """Convert package object to dictionary"""
        return {
            'id': self.id,
            'transporter_id': self.transporter_id,
            'transporter_username': self.transporter.username if self.transporter else None,
            'recipient_name': self.recipient_name,
            'recipient_address': self.recipient_address,
            'status': self.status,
            'tracking_number': self.tracking_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Package {self.tracking_number} - {self.status}>'

