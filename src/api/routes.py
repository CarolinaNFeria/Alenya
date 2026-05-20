from flask import Blueprint, jsonify, request
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from api.models import db, User

api = Blueprint("api", __name__)


@api.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Alenya routes working"}), 200


@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data received"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    age = data.get("age")

    if not username or not email or not password or age is None:
        return jsonify({"message": "username, email, password and age are required"}), 400

    existing_user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if existing_user:
        return jsonify({"message": "Email already registered"}), 409

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        age=age
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": new_user.serialize()
    }), 201


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data received"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=user.email)

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": user.serialize()
    }), 200


@api.route("/private", methods=["GET"])
@jwt_required()
def private():
    current_user_email = get_jwt_identity()

    user = db.session.execute(
        select(User).where(User.email == current_user_email)
    ).scalar_one_or_none()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "message": "Private route valid",
        "user": user.serialize()
    }), 200