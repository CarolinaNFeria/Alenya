from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from api.models import db
from api.routes import api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alenya.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "alenya_secret_key"

CORS(app)

db.init_app(app)
Migrate(app, db)
JWTManager(app)

app.register_blueprint(api, url_prefix="/api")


@app.route("/")
def home():
    return {
        "message": "Alenya API running"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)