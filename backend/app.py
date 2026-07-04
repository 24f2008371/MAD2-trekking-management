from flask import Flask, request, jsonify
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Trekking Management Application"

if __name__ == "__main__":
    app.run(debug = True)