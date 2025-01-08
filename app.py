from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from app_config import Config, app  # Import `app` from `app_config`
from routes import register_routes  # Assuming you have a `register_routes` function

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    """Factory function to create the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Import models after initializing db to avoid circular imports
    from models import User

    return app

# Register routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
