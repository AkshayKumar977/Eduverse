from flask import Blueprint, request,jsonify
from flask_jwt_extended import get_jwt_identity
from backend.models import db, ForumThread, ForumComment
from backend.utils.decorators import token_required
from flask_jwt_extended import jwt_required, get_jwt_identity
forums_bp = Blueprint('forums',__name__)
@forums_bp.route('/threads',methods = ['GET'])
def get_all_threads():
    try:
        threads = ForumThread.query.order_by(ForumThread.created_at.desc())
        return jsonify([thread.to_dict() for thread in threads]),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
@forums_bp.route('/threads',methods = ['POST'])
@jwt_required()
def create_thread():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        thread = ForumThread(
            title = data['title'],
            content = data['content'],
            tags = data.get('tags',""),
            author_id = user_id
        )
        db.session.add(thread)
        db.session.commit()
        return jsonify({
            'message': 'Thread created successfully',
            'thread': thread.to_dict()
        }),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500
@forums_bp.route('/threads/<int:thread_id>/comments',methods = ['POST'])
@jwt_required()
def add_comment(thread_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        thread = ForumThread.query.get(thread_id)
        if not thread:
            return jsonify({'error':'Thread not found'}), 404
        comment = ForumComment(
            thread_id = thread_id,
            author_id = user_id,
            content = data['content']
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify({
            'message': 'Comment added successfully',
            'comment': comment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500