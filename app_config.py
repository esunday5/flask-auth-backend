from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
import pg8000
from dotenv import load_dotenv

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    load_dotenv()

    try:
        connection = pg8000.connect(
            database="ekondo",
            user="admin",
            password="aZ2ryQ9DACsQNFDY1tQouCigbOO8N2ib",
            host="dpg-ctpbp40gph6c73dcjppg-a.oregon-postgres.render.com",
            port=5432
        )
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print(f"Database connection error: {e}")

    # Register blueprints
    from routes import auth, main
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(main, url_prefix='/main')

    return app
