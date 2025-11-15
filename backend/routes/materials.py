from flask import Blueprint, request,jsonify,send_file
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity
import os
from backend.models import db,Material,User
from backend.utils.decorators import token_required
from backend.config import Config
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
materials_bp = Blueprint('materials',__name__)
def allowed_file(filename):
    return '.' in filename and \
             filename.rsplit('.',1)[1].lower() in Config.ALLOWED_EXTENSIONS
@materials_bp.route('/',methods=['GET'])
def get_all_materials():
    try:
        subject = request.args.get('subject','all')
        year = request.args.get('year','all')
        search = request.args.get('search','')
        query = Material.query
        if subject !='all':
            query = query.filter_by(subject=subject)
        if year != 'all':
            query = query.filter_by(year=year)
        if search:
            query = query.filter(
                Material.title.contains(search)
            )
        materials = query.order_by(Material.created_at.desc()).all()
        return jsonify([material.to_dict() for material in materials]),200
    except Exception as e:
        return jsonify({"error":str(e)}),500
@materials_bp.route('/upload',methods = ['POST'])
@jwt_required()
def upload_material():
    try:
        user_id = get_jwt_identity()
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}),400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file is selected'}),400
        if not allowed_file(file.filename):
            return jsonify({'error': 'file type not allowed'}),400
        filename = secure_filename(file.filename)
        timestamp = str(int(datetime.now().timestamp()))
        unique_filename = f"{timestamp}_{filename}"
        # ensure upload folder exists and build full path
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        file_size_mb = f"{file_size/ (1024*1024):.2f} MB"
        materials = Material(
            title = request.form.get('title',''),
            description = request.form.get('description',''),
            subject = request.form.get('subject',''),
            file_type = request.form.get('file_type',''),
            file_path = file_path,
            file_size = file_size_mb,
            year = str(datetime.now().year),
            uploaded_by = user_id
        )
        db.session.add(materials)
        db.session.commit()
        return jsonify({
            'message':'Material uploaded successfully',
            'material': materials.to_dict()
        }),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@materials_bp.route('/<int:material_id>',methods=['DELETE'])
@jwt_required()
def delete_material(material_id):
    try:
        user_id = get_jwt_identity()
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'error':'Material not found'}),404
        if material.uploaded_by != user_id:
            return jsonify({'error':'Unauthorized'}),403
        if os.path.exists(material.file_path):
            os.remove(material.file_path)
        db.session.delete(material)
        db.session.commit()
        return jsonify({"message":'Material deleted successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),500
@materials_bp.route('/<int:material_id>/download',methods = ['POST'])
@jwt_required()
def downloaded_material(material_id):
    try:
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'error':'Material not found'}),404
        material.downloads +=1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500
@materials_bp.route('/<int:material_id>/file',methods = ['GET'])
@jwt_required()
def get_material_file(material_id):
    try:
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'error':'Material not found'}),404
        if not os.path.exists(material.file_path):
            return jsonify({'error':'File not found'}),404
        material.views +=1
        db.session.commit()
        return send_file(
            material.file_path,
            as_attachment=True,
            download_name = material.title
        )
    except Exception as e:
        return jsonify({'error':str(e)}),500
