from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models.patient import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Create directories
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Register blueprints
    from routes.patient_routes import patient_bp
    from routes.report_routes import report_bp
    
    app.register_blueprint(patient_bp, url_prefix='/api')
    app.register_blueprint(report_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Health check route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Medical Report PDF Generator API',
            'status':  'running',
            'version': '1.0.0'
        })
    
    return app

if __name__ == '__main__': 
    app = create_app()
    app.run(debug=True, port=5000)