from app_config import create_app
from routes import auth, main
import os

app = create_app()

# Register blueprints
app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(main, url_prefix='/api/main')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
