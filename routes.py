from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user
from app import app, db
from models import User

bcrypt = Bcrypt(app)

# Register User (POST /api/register)
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    
    new_user = User(username=data["username"], password=hashed_password, role=data["role"])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Done"}), 201

# Login User (POST /api/login)
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity={"username": user.username, "role": user.role})
        return jsonify({"token": access_token, "role": user.role}), 200
    
    return jsonify({"message": "Invalid"}), 401

# Logout User (POST /api/logout)
@app.route("/api/logout", methods=["POST"])
@jwt_required()
def logout():
    logout_user()
    return jsonify({"message": "Done"}), 200

# Dashboard with Role-Based Access (GET /api/dashboard)
@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    role = current_user["role"]
    
    if role == "Professor" or role == "Student" or role == "Assistant":
        return jsonify({"role": role}), 200
    else:
        return jsonify({"role": "Unauthorized"}), 403
