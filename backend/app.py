from flask import Flask, request, jsonify
from models import db, User, Trek, Booking
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

CORS(app)

db.init_app(app)

jwt = JWTManager(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Trekking Management Application"

@app.route("/api/test")
def test():
    return jsonify({
        "success": True,
        "message": "Backend Connected Successfully 🎉"
    })


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            "success": False,
            "message": "Username already exists"
        }), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 400
    
    user = User(
        username = data['username'],
        email = data['email'],
        phone = data['phone'],      
        password = generate_password_hash(data['password']),
        role='user'
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
    "success": True,
    "message": "Registration successful"
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login successful', 'data': {'username': user.username, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/api/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
        
    if request.method == 'GET':
        return jsonify({
            "success": True,
            "data": {
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role
            }
        }), 200
        
    elif request.method == 'PUT':
        data = request.get_json()
        if not data.get('username') or not data.get('email') or not data.get('phone'):
            return jsonify({"success": False, "message": "Username, email, and phone are required"}), 400
            
        existing_email_user = User.query.filter(User.email == data['email'], User.id != user_id).first()
        if existing_email_user:
            return jsonify({"success": False, "message": "Email already exists"}), 400
            
        existing_username_user = User.query.filter(User.username == data['username'], User.id != user_id).first()
        if existing_username_user:
            return jsonify({"success": False, "message": "Username already taken"}), 400
            
        user.username = data['username']
        user.email = data['email']
        user.phone = data['phone']
        
        if data.get('password'):
            user.password = generate_password_hash(data['password'])
            
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "  Profile updated successfully",
            "data": {
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role
            }
        }), 200



if __name__ == "__main__":
    app.run(debug = True)
