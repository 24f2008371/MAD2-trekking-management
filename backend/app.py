import os
from datetime import date
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import text
from werkzeug.security import generate_password_hash

from models import db, User, Trek
from controllers import api_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprint containing all routes
app.register_blueprint(api_bp)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        inspector = db.inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('users')]
        if 'experience' not in columns:
            db.session.execute(text('ALTER TABLE users ADD COLUMN experience VARCHAR(100)'))
        if 'specialization' not in columns:
            db.session.execute(text('ALTER TABLE users ADD COLUMN specialization VARCHAR(100)'))
        db.session.commit()

        if not User.query.filter_by(username='admin').first():
            db.session.add(User(username='admin', email='admin@user.com', password=generate_password_hash('1234'), phone='1234', role='admin', status='active'))
            db.session.commit()
            print("Database created and admin user added!")

        # Seed 10 staff members (staff1 to staff10) with password '12'
        seeded_any = False
        for i in range(1, 11):
            st_username = f'staff{i}'
            if not User.query.filter_by(username=st_username).first():
                db.session.add(User(
                    username=st_username, email=f'{st_username}@trekmate.com', password=generate_password_hash('12'),
                    phone=f'987654321{i-1}', role='staff', status='active', experience='5 Years', specialization='Alpine Mountain Guide'
                ))
                seeded_any = True
        if seeded_any:
            db.session.commit()
            print("Staff members staff1 - staff10 seeded successfully!")
            
        if not Trek.query.first():
            t1 = Trek(name='Everest Base Camp', location='Nepal', difficulty='Hard', duration=12, available_slots=8, price=48000, start_date=date(2026, 8, 15), end_date=date(2026, 8, 27), image='https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=600&q=80', status='Open')
            t2 = Trek(name='Roopkund Trek', location='Uttarakhand', difficulty='Moderate', duration=7, available_slots=7, price=12500, start_date=date(2026, 8, 1), end_date=date(2026, 8, 8), image='https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=600&q=80', status='Open')
            t3 = Trek(name='Hampta Pass', location='Himachal', difficulty='Moderate', duration=5, available_slots=0, price=9800, start_date=date(2026, 9, 10), end_date=date(2026, 9, 15), image='https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=80', status='Open')
            t4 = Trek(name='Valley of Flowers', location='Uttarakhand', difficulty='Easy', duration=6, available_slots=15, price=14500, start_date=date(2026, 8, 5), end_date=date(2026, 8, 11), image='https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&q=80', status='Open')
            t5 = Trek(name='Kedarkantha Trek', location='Uttarakhand', difficulty='Moderate', duration=6, available_slots=10, price=9500, start_date=date(2026, 9, 15), end_date=date(2026, 9, 21), image='https://images.unsplash.com/photo-1501555088652-021faa106b9b?w=600&q=80', status='Open')
            t6 = Trek(name='Goechala Trek', location='Sikkim', difficulty='Hard', duration=11, available_slots=4, price=22000, start_date=date(2026, 9, 1), end_date=date(2026, 9, 12), image='https://images.unsplash.com/photo-1486915309851-b0cc1f8a0084?w=600&q=80', status='Open')
            db.session.add_all([t1, t2, t3, t4, t5, t6])
            db.session.commit()
            print("Default treks seeded successfully!")
            
    app.run(debug=True)
