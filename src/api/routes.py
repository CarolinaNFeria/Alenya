from flask import Blueprint, jsonify

api = Blueprint("api", __name__)


@api.route("/test")
def test():
    return jsonify({
        "message": "Alenya routes working"
    }), 200