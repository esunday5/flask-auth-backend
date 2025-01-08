from app_config import create_app
from routes import auth, main

app = create_app()

# Register blueprints
app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(main, url_prefix='/api/main')

if __name__ == '__main__':
    app.run(debug=True)
