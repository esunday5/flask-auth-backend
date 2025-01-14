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
        database="ekondo"
    )
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print(f"Database connection error: {e}")

# Create tables and seed data inside the app context
with app.app_context():
    db.create_all()  # Create all tables

    # Seed roles
    roles = [
        "admin", "officer", "approver", "reviewer", "supervisor", "super_admin", "account_officer"
    ]
    existing_roles = {role.name for role in Role.query.all()}
    for role_name in roles:
        if role_name not in existing_roles:
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()
    print("Roles added.")

    # Seed branches
    branches = [
        "Head Office", "Corporate", "Effio-Ette", "Chamley", "Ekpo-Abasi", "Etim-Edem", "Watt", "Ika Ika",
        "Ikang", "Ikot Nakanda", "Mile 8", "Oban", "Odukpani", "Uyanga", "Ugep", "Obubra", "Ikom", "Ogoja"
    ]
    existing_branches = {branch.name for branch in Branch.query.all()}
    for branch_name in branches:
        if branch_name not in existing_branches:
            branch = Branch(name=branch_name)
            db.session.add(branch)
    db.session.commit()
    print("Branches added.")

    # Seed departments
    departments = [
        "HR/Admin", "Account", "Risk/Compliance", "IT", "Audit", "Funds Transfer", "Credit",
        "Recovery", "E-Business", "Legal", "Strategic Branding / Communication",
        "Business Development", "Managing Director"
    ]
    head_office = Branch.query.filter_by(name="Head Office").first()
    existing_departments = {department.name for department in Department.query.all()}
    for department_name in departments:
        if department_name not in existing_departments and head_office:
            department = Department(name=department_name, branch_id=head_office.id)
            db.session.add(department)
    db.session.commit()
    print("Departments added.")

    # Seed users
    user_data = [
        ('Hyacinth', 'Sunday', 'hyman', 'hyacinth.sunday@ekondomfbank.com', '11229012', 'officer', 'Head Office', 'IT'),
        ('Ekuere', 'Akpan', 'ekuere', 'ekuere.akpan@ekondomfbank.com', '11223344', 'approver', 'Head Office', 'Managing Director'),
        ('Henry', 'Ikpeme', 'henzie', 'henry.etim@ekondomfbank.com', '22446688', 'reviewer', 'Head Office', 'Risk/Compliance'),
        ('Ubong', 'Wilson', 'wilson', 'ubong.wilson@ekondomfbank.com', '44556677', 'supervisor', 'Head Office', 'IT'),
        ('Emmanuel', 'Sunday', 'emmanate', 'emmyblaq3@gmail.com', 'admin@it', 'admin', 'Head Office', 'IT'),
        ('Precious', 'Pius', 'presh', 'grace.johnson@ekondomfbank.com', 'ac123456', 'account_officer', 'Head Office', 'Account')
    ]

    existing_users = {(user.username, user.email) for user in User.query.all()}
    for first_name, last_name, username, email, password, role_name, branch_name, department_name in user_data:
        if (username, email) not in existing_users:
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
