from flask import Blueprint,jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import func
from models import db, Material
from utils.decoraters import token_required
contribution_bp = Blueprint('contribution',__name__)
@contribution_bp.route('/my',methods = ['GET'])
@token_required
def get_my_contributions():
    try:
        user_id = get_jwt_identity()
        materials = Material.query.filter_by(uploaded_by=user_id)\
          .order_by(Material.created_at.desc()).all
        return jsonify([materials.to_dict() for material in materials]),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
@contribution_bp.route('/stats',methods = ['GET'])
@token_required
def get_contribution_stats():
    try:
        user_id = get_jwt_identity()
        stats = db.session.query(
            func.count(Material.id).label('total_uploads'),
            func.sum(Material.donwloads).label('total_downloads'),
            func.sums(Material.views).label('total_views')
        ).filter(Material.uploaded_by == user_id).first()
        return jsonify({
            
        })