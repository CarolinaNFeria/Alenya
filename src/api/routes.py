from flask import Blueprint, jsonify, request
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from api.models import db, User, BehaviorAnalysis

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
    user = get_current_user()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "message": "Private route valid",
        "user": user.serialize()
    }), 200


def get_current_user():
    current_user_email = get_jwt_identity()

    user = db.session.execute(
        select(User).where(User.email == current_user_email)
    ).scalar_one_or_none()

    return user


def analyze_behavior_text(text):
    clean_text = text.lower()

    sexual_pressure_words = [
        "manda foto", "pasa foto", "si me quisieras", "nadie se entera",
        "no le digas a nadie", "te obligo", "si no lo haces", "insistí",
        "insistir", "presioné", "presionar"
    ]

    bullying_words = [
        "gorda", "feo", "fea", "ridículo", "ridicula", "tonto", "tonta",
        "imbécil", "idiota", "humillar", "burlé", "burla", "molestar",
        "apodo", "excluir", "ignorar"
    ]

    manipulation_words = [
        "es tu culpa", "sin ti no soy nada", "te dejo si", "si no haces",
        "me debes", "eres exagerada", "solo era una broma"
    ]

    if any(word in clean_text for word in sexual_pressure_words):
        return {
            "risk_level": "rojo",
            "category": "presión sexual o falta de consentimiento",
            "feedback": "Esta conducta puede hacer que la otra persona se sienta presionada, insegura o sin libertad para decidir.",
            "recommendation": "Detente, respeta el límite de la otra persona y no insistas. El consentimiento debe ser libre, claro y sin presión."
        }

    if any(word in clean_text for word in bullying_words):
        return {
            "risk_level": "rojo",
            "category": "bullying o humillación",
            "feedback": "Esta conducta puede dañar emocionalmente a otra persona, aunque se presente como una broma.",
            "recommendation": "Reconoce el daño, deja de repetir esa conducta y busca una forma honesta de disculparte."
        }

    if any(word in clean_text for word in manipulation_words):
        return {
            "risk_level": "amarillo",
            "category": "manipulación emocional",
            "feedback": "Esta frase puede hacer que otra persona se sienta culpable o atrapada emocionalmente.",
            "recommendation": "Expresa lo que sientes sin presionar, culpar ni controlar a la otra persona."
        }

    return {
        "risk_level": "verde",
        "category": "conducta sin riesgo claro",
        "feedback": "No se detecta una señal clara de acoso o daño en el texto, pero siempre es importante revisar cómo puede sentirse la otra persona.",
        "recommendation": "Antes de actuar, pregúntate: ¿esto respeta los límites, la dignidad y la libertad de la otra persona?"
    }


@api.route("/analyze-behavior", methods=["POST"])
@jwt_required()
def analyze_behavior():
    user = get_current_user()

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data received"}), 400

    behavior_text = data.get("behavior_text")

    if not behavior_text:
        return jsonify({"message": "behavior_text is required"}), 400

    result = analyze_behavior_text(behavior_text)

    new_analysis = BehaviorAnalysis(
        behavior_text=behavior_text,
        risk_level=result["risk_level"],
        category=result["category"],
        feedback=result["feedback"],
        recommendation=result["recommendation"],
        user_id=user.id
    )

    db.session.add(new_analysis)
    db.session.commit()

    return jsonify({
        "message": "Behavior analyzed successfully",
        "analysis": new_analysis.serialize()
    }), 201


@api.route("/my-analyses", methods=["GET"])
@jwt_required()
def my_analyses():
    user = get_current_user()

    if not user:
        return jsonify({"message": "User not found"}), 404

    analyses = db.session.execute(
        select(BehaviorAnalysis)
        .where(BehaviorAnalysis.user_id == user.id)
        .order_by(BehaviorAnalysis.created_at.desc())
    ).scalars().all()

    return jsonify({
        "analyses": [analysis.serialize() for analysis in analyses]
    }), 200