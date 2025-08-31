import os
import logging
from flask import Flask
from models.db import init_db
from routes.main import main_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    
    # Set secret key for session management
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Google Analytics configuration
    # Get the analytics ID from environment variables
    # analytics_id = os.environ.get('GOOGLE_ANALYTICS_ID')
    analytics_id = "G-XJ97NGS36D" 
    
    # Debug: Print environment info to help troubleshoot (only in development)
    if os.environ.get('FLASK_ENV') != 'production':
        app.logger.info(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")
        app.logger.info(f"GOOGLE_ANALYTICS_ID from env: {analytics_id}")
    
    # Set the config - make sure it's not None
    if analytics_id:
        app.config['GOOGLE_ANALYTICS_ID'] = analytics_id
    else:
        app.config['GOOGLE_ANALYTICS_ID'] = None
    
    # Configure logging for production
    if os.environ.get('FLASK_ENV') == 'production':
        # Google Cloud Logging
        try:
            import google.cloud.logging
            client = google.cloud.logging.Client()
            client.setup_logging()
        except ImportError:
            # Fallback to standard logging if Google Cloud Logging is not available
            logging.basicConfig(level=logging.INFO)
        
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.DEBUG)
    
    # Initialize database
    try:
        init_db()
        app.logger.info("Database initialized successfully")
    except Exception as e:
        app.logger.error(f"Database initialization failed: {e}")
        raise
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    
    # Add error handlers
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f"404 error: {error}")
        return "Page not found", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 error: {error}")
        return "Internal server error", 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
