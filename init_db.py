from app_config import create_app, db
from models import User
import pg8000  # Use pg8000 for Postgres connection

# Create app instance
app = create_app()

# Test database connection using pg8000
try:
    connection = pg8000.connect(
        user="admin",
        password="aZ2ryQ9DACsQNFDY1tQouCigbOO8N2ib",
        host="dpg-ctpbp40gph6c73dcjppg-a.oregon-postgres.render.com",
        port=5432,
        database="ekondo"  # Corrected to `database`
    )
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print(f"Database connection error: {e}")

# Create tables and seed data inside the app context
with app.app_context():
    db.create_all()  # Create all tables

    # Seed data (optional)
    if not User.query.first():
        admin = User(username="admin", email="emmyblaq3@gmail.com", password="admin@it")
        admin.set_password("admin@it")  # Ensure the password is hashed
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")

with app.app_context():
    db.create_all()  # Creates the database tables
    print("Database initialized!")