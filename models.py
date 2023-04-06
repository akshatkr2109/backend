from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(30), nullable=False)

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f"Student('{self.employee_id}', '{self.name}', '{self.email}', {self.role})"
