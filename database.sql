-- Create roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Create branches table
CREATE TABLE branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Create departments table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    branch_id INTEGER REFERENCES branches(id)
);

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    branch_id INTEGER REFERENCES branches(id),
    department_id INTEGER REFERENCES departments(id)
);

-- Insert default roles
INSERT INTO roles (name) VALUES
    ('officer'),
    ('approver'),
    ('reviewer'),
    ('supervisor'),
    ('admin'),
    ('super_admin');

-- Insert default branches
INSERT INTO branches (name) VALUES
    ('Head Office'),
    ('Corporate'),
    ('Effio-Ette'),
    ('Chamley'),
    ('Ekpo-Abasi'),
    ('Etim-Edem'),
    ('Watt'),
    ('Ika Ika'),
    ('Ikang'),
    ('Ikot Nakanda'),
    ('Mile 8'),
    ('Oban'),
    ('Odukpani'),
    ('Uyanga'),
    ('Ugep'),
    ('Obubra'),
    ('Ikom'),
    ('Ogoja');

-- Insert default departments
INSERT INTO departments (name, branch_id) VALUES
    ('HR/Admin', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Account', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Risk/Compliance', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('IT', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Audit', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Funds Transfer', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Credit', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Recovery', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('E-Business', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Legal', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Strategic Branding / Communication', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Business Development', (SELECT id FROM branches WHERE name = 'Head Office')),
    ('Managing Director', (SELECT id FROM branches WHERE name = 'Head Office'));

-- Insert users (replace password hashes with actual hashed values)
INSERT INTO users (username, email, password, role_id, branch_id, department_id) VALUES
    ('hyman', 'hyacinth.sunday@ekondomfbank.com', '11229012', (SELECT id FROM roles WHERE name = 'officer'), (SELECT id FROM branches WHERE name = 'Head Office'), (SELECT id FROM departments WHERE name = 'IT')),
    ('ekuere', 'ekuere.akpan@ekondomfbank.com', '11223344', (SELECT id FROM roles WHERE name = 'approver'), (SELECT id FROM branches WHERE name = 'Head Office'), (SELECT id FROM departments WHERE name = 'Managing Director')),
    ('henzie', 'henry.etim@ekondomfbank.com', '22446688', (SELECT id FROM roles WHERE name = 'reviewer'), (SELECT id FROM branches WHERE name = 'Head Office'), (SELECT id FROM departments WHERE name = 'Risk/Compliance')),
    ('wilson', 'ubong.wilson@ekondomfbank.com', '44556677', (SELECT id FROM roles WHERE name = 'supervisor'), (SELECT id FROM branches WHERE name = 'Head Office'), (SELECT id FROM departments WHERE name = 'IT')),
    ('emmanate', 'emmyblaq3@gmail.com', 'admin@it', (SELECT id FROM roles WHERE name = 'admin'), (SELECT id FROM branches WHERE name = 'Head Office'), (SELECT id FROM departments WHERE name = 'IT'));

