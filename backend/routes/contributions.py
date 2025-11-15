from flask import Blueprint,jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import func
from backend.models import db, Material
from backend.utils.decorators import token_required
from flask_jwt_extended import jwt_required, get_jwt_identity
contributions_bp = Blueprint('contributions',__name__)
@contributions_bp.route('/my',methods = ['GET'])
@jwt_required()
def get_my_contributions():
    try:
        user_id = get_jwt_identity()
        materials = Material.query.filter_by(uploaded_by=user_id)\
          .order_by(Material.created_at.desc()).all
        return jsonify([materials.to_dict() for material in materials]),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
@contributions_bp.route('/stats',methods = ['GET'])
@jwt_required()
def get_contribution_stats():
    try:
        user_id = get_jwt_identity()
        stats = db.session.query(
            func.count(Material.id).label('total_uploads'),
            func.sum(Material.donwloads).label('total_downloads'),
            func.sum(Material.views).label('total_views')
        ).filter(Material.uploaded_by == user_id).first()
        return jsonify({
            'total_uploads': stats.total_uploads or 0,
            'total_downloads': stats.total_downloads or 0,
            'total_views': stats.total_views or 0
        }),200
    except Exception as e:
        return jsonify({'error':str(e)}),500