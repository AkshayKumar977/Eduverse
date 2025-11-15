from flask import Blueprint, request,jsonify
from flask_jwt_extended import create_access_token,get_jwt_identity
from backend.models import db,User
from backend.utils.decorators import token_required
from flask_jwt_extended import jwt_required, get_jwt_identity
auth_bp = Blueprint('auth',__name__)
@auth_bp.route('/register',methods = ['POST'])
def register():
    try:
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email alreaddy registered'}),400
        user = User(
            name = data['name'],
            email = data['email'],
            student_id = data.get('student_id'),
            department = data.get('department')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message':'User registered successfully',
            'user': user.to_dict()
        }),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'token': access_token,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404