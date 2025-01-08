# init_db.py
from app_config import create_app, db
from models import User, Role, Branch, Department
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
    if not Role.query.first():
        admin_role = Role(name="admin")
        officer_role = Role(name="officer")
        approver_role = Role(name="approver")
        reviewer_role = Role(name="reviewer")
        supervisor_role = Role(name="supervisor")
        db.session.add(admin_role)
        db.session.add(officer_role)
        db.session.add(approver_role)
        db.session.add(reviewer_role)
        db.session.add(supervisor_role)
        db.session.commit()
        print("Roles added.")

    if not Branch.query.first():
        head_office = Branch(name="Head Office")
        db.session.add(head_office)
        db.session.commit()
        print("Branches added.")

    if not Department.query.first():
        it_department = Department(name="IT")
        md_department = Department(name="Managing Director")
        risk_compliance_department = Department(name="Risk/Compliance")
        db.session.add(it_department)
        db.session.add(md_department)
        db.session.add(risk_compliance_department)
        db.session.commit()
        print("Departments added.")

    if not User.query.first():
        # Create users with the reference provided
        user_data = [
            ('Hyacinth', 'Sunday', 'hyman', 'hyacinth.sunday@ekondomfbank.com', '11229012', 'officer', 'Head Office', 'IT'),
            ('Ekuere', 'Akpan', 'ekuere', 'ekuere.akpan@ekondomfbank.com', '11223344', 'approver', 'Head Office', 'Managing Director'),
            ('Henry', 'Ikpeme', 'henzie', 'henry.etim@ekondomfbank.com', '22446688', 'reviewer', 'Head Office', 'Risk/Compliance'),
            ('Ubong', 'Wilson', 'wilson', 'ubong.wilson@ekondomfbank.com', '44556677', 'supervisor', 'Head Office', 'IT'),
            ('Emmanuel', 'Sunday', 'emmanate', 'emmyblaq3@gmail.com', 'admin@it', 'admin', 'Head Office', 'IT')
        ]

        for first_name, last_name, username, email, password, role_name, branch_name, department_name in user_data:
            role = Role.query.filter_by(name=role_name).first()
            branch = Branch.query.filter_by(name=branch_name).first()
            department = Department.query.filter_by(name=department_name).first()
            if role and branch and department:
                user = User(
                    first_name=first_name, 
                    last_name=last_name, 
                    username=username, 
                    email=email, 
                    password=password, 
                    role_id=role.id, 
                    branch_id=branch.id, 
                    department_id=department.id
                )
                user.set_password(password)  # Ensure password is hashed
                db.session.add(user)

        db.session.commit()
        print("Users added.")

with app.app_context():
    db.create_all()  # Creates the database tables
    print("Database initialized!")
