from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
import pg8000
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    load_dotenv()

    # Set up logging
    if not app.debug:
        handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.ERROR)
        app.logger.addHandler(handler)

    # Test database connection
    try:
        connection = pg8000.connect(
            database="ekondo",
            user="admin",
            password="aZ2ryQ9DACsQNFDY1tQouCigbOO8N2ib",
            host="dpg-ctpbp40gph6c73dcjppg-a.oregon-postgres.render.com",
            port=5432
        )
        app.logger.info("Database connection successful!")
        connection.close()
    except Exception as e:
        app.logger.error(f"Database connection error: {e}")

    # Register blueprints
    from routes import auth, main
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(main, url_prefix='/main')

    # Middleware to log errors globally
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        return jsonify({"message": "Internal server error"}), 500

    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f"Not Found: {error}")
        return jsonify({"message": "Not found"}), 404

    return app
