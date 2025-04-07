from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import *
from professor_functions import *
from auth_functions import *
from dashboard_function import *


# Register User (POST /api/register)
@app.route("/api/register", methods=["POST"])
def register_func():
    return register()

@app.route("/api/login", methods=["POST"])
def login_func():
    return login()

# Logout User (POST /api/logout)
@app.route("/api/logout", methods=["POST"])
@jwt_required()
def logout_func():
    return logout()

# Dashboard with Role-Based Access (GET /api/dashboard)
@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard_func():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user["id"]).first()
    return dashboard(user)
    

@app.route("/api/get_professor_subjects", methods=["POST"])
@jwt_required()
def get_professor_subjects_func():
    current_user = get_jwt_identity()
    if current_user["role"]=="professor":
        professor = Professor.query.filter_by(id=current_user["id"]).first()
        return get_professor_subjects(professor)
    return jsonify({"error": "Unauthorized"}), 403

@app.route("/api/fetch_students_in_subject", methods=["POST"])
@jwt_required()
def fetch_students_in_subject_func():
    current_user = get_jwt_identity()
    if current_user["role"]=="professor":
        return fetch_students_in_subject()
    return jsonify({"error": "Unauthorized"}), 403

@app.route("/api/mark_attendance", methods=["POST"])
@jwt_required()
def mark_attendance_func():
    current_user = get_jwt_identity()
    if current_user["role"]=="professor":
        return mark_attendance()
    return jsonify({"error": "Unauthorized"}), 403

@app.route("/api/mark_attendance", methods=["POST"])
@jwt_required()
def mark_attendance_func():
    current_user = get_jwt_identity()
    if current_user["role"]=="professor":
        return mark_attendance()
    return jsonify({"error": "Unauthorized"}), 403

@app.route("/api/mark_grade", methods=["POST"])
@jwt_required()
def mark_grade_func():
    current_user = get_jwt_identity()
    if current_user["role"]=="professor":
        return mark_grade()
    return jsonify({"error": "Unauthorized"}), 403
    
