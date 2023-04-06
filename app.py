from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from models import db, Employee
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]
db.init_app(app)


@app.before_first_request
def create_table():
    engine = create_engine(os.environ["DATABASE_URI"])
    if not database_exists(engine.url):
        create_database(engine.url)
    engine.dispose()
    db.create_all()


# Home route / Landing route
@app.route('/')
@app.route('/employee')
def home():
    return jsonify({"success": True, "message": "Welcome to the Flask server!"})


# Add an employee
@app.route('/employee/add', methods=['POST'])
def new_employee():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    role = data['role']

    employee = Employee(name, email, password, role)
    db.session.add(employee)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Employee Added Successfully"
    })


# Get a specific employee
@app.route('/employee/<string:mail>', methods=['GET'])
def get_employee(mail):
    employee = Employee.query.filter_by(email=mail).first()
    if not employee:
        return jsonify({
            "success": False,
            "message": "Employee not found!"
        })

    result = {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "password": employee.password,
            "role": employee.role,
        }
    return jsonify({
        "success": True,
        "employee": result
    })


# Get all employee
@app.route('/employee/all', methods=['GET'])
def get_employees():
    employees = Employee.query.all()

    results = []
    for employee in employees:
        temp = {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "password": employee.password,
            "role": employee.role,
        }
        results.append(temp)

    return jsonify({
        "success": True,
        "employees": results,
    })


# Update an employee
@app.route('/employee/update/<string:mail>', methods=['PUT'])
def update_employee(mail):
    employee = Employee.query.filter_by(email=mail).first()
    if not employee:
        return jsonify({
        "success": False,
        "message": "Employee not found!",
    })

    db.session.delete(employee)
    db.session.commit()
    data = request.get_json()
    print(data)
    name = data['name']
    email = data['email']
    password = data['password']
    role = data['role']
    db.session.add(Employee(name=name, email=email, password=password, role=role))
    db.session.commit()

    updated_employee = Employee.query.filter_by(email=mail).first()
    result = {
            "employee_id": updated_employee.employee_id,
            "name": updated_employee.name,
            "email": updated_employee.email,
            "password": updated_employee.password,
            "role": updated_employee.role,
        }

    return jsonify({
        "success": True,
        "message": "Updated Sucessfully",
        "updated_employee": result
    })


# Delete an employee
@app.route('/employee/delete/<string:mail>', methods=['DELETE'])
def delete_employee(mail):
    employee = Employee.query.filter_by(email=mail).first()
    if not employee:
        return jsonify({
        "success": False,
        "message": "Employee not found!"
    })

    db.session.delete(employee)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Deleted Sucessfully"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
