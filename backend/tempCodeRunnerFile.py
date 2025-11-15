from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import send_from_directory
from backend.config import Config
from backend.models import db
from datetime import datetime

# Import blueprints
from backend.routes.auth import auth_bp
from backend.routes.materials import materials_bp
from backend.routes.contributions import contributions_bp
from backend.routes.forums import forums_bp
from backend.routes.notifications import notifications_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(materials_bp, url_prefix='/api/materials')
    app.register_blueprint(contributions_bp, url_prefix='/api/contributions')
    app.register_blueprint(forums_bp, url_prefix='/api/forum')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    from flask import render_template

# Serve login.html at the root URL
    @app.route('/')
    @app.route('/login.html')
    def serve_login():
        return render_template('login.html')

# Serve index.html at /index
    @app.route('/index')
    @app.route('/index.html')
    def serve_index():
       return render_template('index.html')
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the app
    app.run(debug=True, port=3000)