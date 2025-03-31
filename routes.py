from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_bcrypt import Bcrypt
from app import app, db
from models import User
from forms import RegisterForm, LoginForm

bcrypt = Bcrypt(app)

# Register User (POST /api/register)
@app.route("/api/register", methods=["POST"])
def register():
    form = RegisterForm(data=request.json)  # Ensure we pass JSON data

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            return jsonify({"message": "Username already taken"}), 400  # Bad Request

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, password=hashed_password, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "Registration successful"}), 201
    else:
        return jsonify({"errors": form.errors}), 400  # Return validation errors

@app.route("/api/login", methods=["POST"])
def login():
    form = LoginForm(data=request.json)  # Pass JSON data to Flask-WTF form

    if form.validate_on_submit():  # Validate input fields
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            access_token = create_access_token(identity={"username": user.username, "role": user.role})
            return jsonify({"token": access_token}), 200  # Successful login

        return jsonify({"message": "Invalid username or password"}), 401  # Unauthorized
    else:
        return jsonify({"errors": form.errors}), 400  # Return validation errors

# Logout User (POST /api/logout)
@app.route("/api/logout", methods=["POST"])
@jwt_required()
def logout():
    #"Delete the JWT token in Frontend"
    return jsonify({"message": "Done"}), 200

# Dashboard with Role-Based Access (GET /api/dashboard)
@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    role = current_user["role"]
    return jsonify({"role": role}), 200
