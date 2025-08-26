import os
from flask import Flask
from models.db import init_db
from routes.main import main_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    
    # Set secret key for session management
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
