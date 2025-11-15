from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
from backend.models import db, Notification
from backend.utils.decorators import token_required
from flask_jwt_extended import jwt_required, get_jwt_identity
notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        user_id = get_jwt_identity()
        
        notifications = Notification.query.filter_by(user_id=user_id)\
            .order_by(Notification.created_at.desc())\
            .limit(10).all()
        
        return jsonify([notif.to_dict() for notif in notifications]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notifications_bp.route('/<int:notif_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notif_id):
    try:
        user_id = get_jwt_identity()
        
        notification = Notification.query.filter_by(
            id=notif_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'message': 'Notification marked as read'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500