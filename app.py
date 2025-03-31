from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/mydatabase"
app.config["JWT_SECRET_KEY"] = "supersecretkey"  # Change this in production

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)  # Allows React to communicate with Flask

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'professor', 'student', 'assistant'

# Create tables
with app.app_context():
    db.create_all()

# ✅ Register User API
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(username=data["username"], password=hashed_password, role=data["role"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# ✅ Login User API (Returns JWT Token)
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity={"username": user.username, "role": user.role})
        return jsonify({"token": access_token, "role": user.role}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# ✅ Protected Dashboard API (Requires Token)
@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()  # Extract user info from token
    return jsonify({"message": f"Welcome {current_user['username']}!", "role": current_user["role"]})

if __name__ == "__main__":
    app.run(debug=True)
