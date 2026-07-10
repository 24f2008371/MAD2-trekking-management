import os
import time
from datetime import datetime, date
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Trek, Booking

api_bp = Blueprint('api', __name__)

def format_unsplash_url(url):
    if not url:
        return ''
    if 'unsplash.com/photos/' in url:
        parts = url.strip('/').split('/')
        photo_id = parts[-1].split('?')[0]
        if '-' in photo_id:
            photo_id = photo_id.split('-')[-1]
        return f"https://images.unsplash.com/photo-{photo_id}?w=600&auto=format&fit=crop&q=80"
    return url

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            u_id = int(get_jwt_identity())
            user = User.query.get(u_id)
            if not user or user.role != role:
                return jsonify({"success": False, "message": "Unauthorized"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@api_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({"success": False, "message": "Username or Email already exists"}), 400
    user = User(
        username=data['username'],
        email=data['email'],
        phone=data.get('phone'),      
        password=generate_password_hash(data['password']),
        role='user',
        status='active'
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": True, "message": "Registration successful"}), 201

@api_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        if user.status == 'blacklisted':
            return jsonify({'message': 'You cannot login as you are blacklisted'}), 403
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login successful', 'data': {'username': user.username, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@api_bp.route('/api/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    if request.method == 'GET':
        return jsonify({"success": True, "data": {"username": user.username, "email": user.email, "phone": user.phone, "role": user.role}}), 200
    
    data = request.get_json()
    if not data.get('username') or not data.get('email') or not data.get('phone'):
        return jsonify({"success": False, "message": "Username, email, and phone are required"}), 400
    if User.query.filter(User.email == data['email'], User.id != user_id).first():
        return jsonify({"success": False, "message": "Email already exists"}), 400
    if User.query.filter(User.username == data['username'], User.id != user_id).first():
        return jsonify({"success": False, "message": "Username already taken"}), 400
        
    user.username = data['username']
    user.email = data['email']
    user.phone = data['phone']
    if data.get('password'):
        user.password = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({"success": True, "message": "Profile updated successfully", "data": {"username": user.username, "email": user.email, "phone": user.phone, "role": user.role}}), 200

# ================= ADMIN ROUTES =================

@api_bp.route('/api/admin/stats', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_stats():
    return jsonify({
        "success": True,
        "data": {
            "total_treks": Trek.query.count(),
            "total_users": User.query.filter_by(role='user').count(),
            "total_staff": User.query.filter_by(role='staff').count(),
            "total_bookings": Booking.query.count()
        }
    }), 200

@api_bp.route('/api/admin/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_get_users():
    users = User.query.filter_by(role='user').all()
    return jsonify({"success": True, "data": [{"id": u.id, "username": u.username, "email": u.email, "phone": u.phone, "status": u.status} for u in users]}), 200

@api_bp.route('/api/admin/users/<int:u_id>/status', methods=['PUT'])
@jwt_required()
@role_required('admin')
def admin_update_user_status(u_id):
    user = User.query.get(u_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    new_status = request.get_json().get('status')
    if new_status not in ['active', 'blacklisted', 'suspended']:
        return jsonify({"success": False, "message": "Invalid status"}), 400
    user.status = new_status
    db.session.commit()
    return jsonify({"success": True, "message": f"User status updated to {new_status}"}), 200

@api_bp.route('/api/admin/staff', methods=['GET', 'POST'])
@jwt_required()
@role_required('admin')
def admin_staff():
    if request.method == 'GET':
        staff = User.query.filter_by(role='staff').all()
        return jsonify({"success": True, "data": [{"id": s.id, "username": s.username, "email": s.email, "phone": s.phone, "experience": s.experience, "specialization": s.specialization, "status": s.status} for s in staff]}), 200
    
    data = request.get_json()
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"success": False, "message": "Username, email, and password are required"}), 400
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({"success": False, "message": "Username or Email already exists"}), 400
        
    new_staff = User(
        username=data['username'],
        email=data['email'],
        phone=data.get('phone'),
        password=generate_password_hash(data['password']),
        experience=data.get('experience'),
        specialization=data.get('specialization'),
        status='active',
        role='staff'
    )
    db.session.add(new_staff)
    db.session.commit()
    return jsonify({"success": True, "message": "Staff member created successfully"}), 201

@api_bp.route('/api/admin/staff/<int:s_id>/status', methods=['PUT'])
@jwt_required()
@role_required('admin')
def admin_update_staff_status(s_id):
    staff = User.query.filter_by(id=s_id, role='staff').first()
    if not staff:
        return jsonify({"success": False, "message": "Staff member not found"}), 404
    new_status = request.get_json().get('status')
    if new_status not in ['active', 'blacklisted', 'suspended']:
        return jsonify({"success": False, "message": "Invalid status"}), 400
    staff.status = new_status
    db.session.commit()
    return jsonify({"success": True, "message": f"Staff status updated to {new_status}"}), 200

@api_bp.route('/api/admin/treks', methods=['GET', 'POST'])
@jwt_required()
@role_required('admin')
def admin_treks():
    if request.method == 'GET':
        treks = Trek.query.all()
        return jsonify({"success": True, "data": [{
            "id": t.id, "name": t.name, "location": t.location, "difficulty": t.difficulty,
            "duration": t.duration, "slots": t.available_slots, "price": t.price,
            "image": format_unsplash_url(t.image) or 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=600&q=80',
            "status": t.status, "start_date": t.start_date.strftime('%Y-%m-%d') if t.start_date else '',
            "end_date": t.end_date.strftime('%Y-%m-%d') if t.end_date else '',
            "staff_id": t.staff_id, "staff_name": t.staff.username if t.staff else 'Unassigned'
        } for t in treks]}), 200

    data = request.get_json()
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except Exception:
        start_date = end_date = date.today()
        
    staff_id = None
    if data.get('staff_id'):
        try:
            staff_id = int(data['staff_id'])
        except Exception:
            pass

    new_trek = Trek(
        name=data['name'], location=data['location'], difficulty=data['difficulty'],
        duration=int(data['duration']), available_slots=int(data['slots']), price=float(data['price']),
        image=format_unsplash_url(data.get('image', '')), status=data.get('status', 'Open'),
        start_date=start_date, end_date=end_date, staff_id=staff_id
    )
    db.session.add(new_trek)
    db.session.commit()
    return jsonify({"success": True, "message": "Trek created successfully"}), 201

@api_bp.route('/api/admin/treks/<int:t_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@role_required('admin')
def admin_single_trek(t_id):
    trek = Trek.query.get(t_id)
    if not trek:
        return jsonify({"success": False, "message": "Trek not found"}), 404
        
    if request.method == 'DELETE':
        Booking.query.filter_by(trek_id=t_id).delete()
        db.session.delete(trek)
        db.session.commit()
        return jsonify({"success": True, "message": "Trek deleted successfully"}), 200

    data = request.get_json()
    try:
        trek.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        trek.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except Exception:
        pass
        
    trek.name = data['name']
    trek.location = data['location']
    trek.difficulty = data['difficulty']
    trek.duration = int(data['duration'])
    trek.available_slots = int(data['slots'])
    trek.price = float(data['price'])
    trek.image = format_unsplash_url(data.get('image', trek.image))
    trek.status = data.get('status', trek.status)
    
    staff_id = None
    if data.get('staff_id'):
        try:
            staff_id = int(data['staff_id'])
        except Exception:
            pass
    trek.staff_id = staff_id
            
    db.session.commit()
    return jsonify({"success": True, "message": "Trek updated successfully"}), 200

@api_bp.route('/api/admin/upload', methods=['POST'])
@jwt_required()
@role_required('admin')
def admin_upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    if file:
        filename = f"{int(time.time())}_{secure_filename(file.filename)}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"success": True, "url": f"http://127.0.0.1:5000/static/uploads/{filename}"}), 200

@api_bp.route('/api/admin/bookings', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_get_bookings():
    bookings = Booking.query.order_by(Booking.id.desc()).all()
    return jsonify({"success": True, "data": [{
        "id": f"TM-{b.id}", "raw_id": b.id, "user": b.user.username,
        "email": b.user.email, "trek": b.trek.name,
        "date": b.booking_date.strftime('%Y-%m-%d') if b.booking_date else '', "status": b.status
    } for b in bookings]}), 200

@api_bp.route('/api/admin/bookings/<int:b_id>/status', methods=['PUT'])
@jwt_required()
@role_required('admin')
def admin_update_booking_status(b_id):
    booking = Booking.query.get(b_id)
    if not booking:
        return jsonify({"success": False, "message": "Booking not found"}), 404
        
    new_status = request.get_json().get('status')
    if new_status not in ['Pending', 'Confirmed', 'Cancelled', 'Booked']:
        return jsonify({"success": False, "message": "Invalid status"}), 400
        
    trek, old_status = booking.trek, booking.status
    if new_status in ['Confirmed', 'Booked'] and old_status not in ['Confirmed', 'Booked']:
        if trek.available_slots <= 0:
            return jsonify({"success": False, "message": "Cannot approve booking. Trek has no slots left!"}), 400
        trek.available_slots -= 1
    elif new_status == 'Cancelled' and old_status in ['Confirmed', 'Booked']:
        trek.available_slots += 1
        
    booking.status = new_status
    db.session.commit()
    return jsonify({"success": True, "message": f"Booking status updated to {new_status}"}), 200

@api_bp.route('/api/admin/search', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_global_search():
    q = request.args.get('q', '').strip().lower()
    if not q:
        return jsonify({"success": True, "data": []}), 200
        
    results = []
    # Search Users
    for u in User.query.filter((User.username.like(f'%{q}%')) | (User.email.like(f'%{q}%')) | (User.phone.like(f'%{q}%'))).all():
        type_str = 'Staff' if u.role == 'staff' else 'User'
        results.append({"key": f"u-{u.id}", "type": type_str, "title": u.username, "subtitle": u.email, "matchText": f"Matched fields in {type_str}"})
    # Search Treks
    for t in Trek.query.filter((Trek.name.like(f'%{q}%')) | (Trek.location.like(f'%{q}%')) | (Trek.difficulty.like(f'%{q}%'))).all():
        results.append({"key": f"t-{t.id}", "type": "Trek", "title": t.name, "subtitle": f"{t.location} | {t.difficulty} ({t.duration} Days)", "matchText": "Matched fields in Trek"})
    # Search Bookings
    for b in Booking.query.all():
        b_id_str = f"TM-{b.id}"
        if q in b_id_str.lower() or q in b.user.username.lower() or q in b.trek.name.lower() or q in b.status.lower():
            results.append({"key": f"b-{b.id}", "type": "Booking", "title": f"{b_id_str} — {b.user.username}", "subtitle": f"{b.trek.name} ({b.status})", "matchText": "Matched fields in Booking"})
            
    return jsonify({"success": True, "data": results}), 200

@api_bp.route('/api/admin/reports', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_reports():
    confirmed_bookings = Booking.query.filter(Booking.status.in_(['Confirmed', 'Booked', 'Completed'])).all()
    total_revenue = sum(b.trek.price for b in confirmed_bookings)
    
    total_bookings = Booking.query.count()
    avg_value = total_revenue / len(confirmed_bookings) if len(confirmed_bookings) > 0 else 0
    
    active_excursions = Trek.query.filter_by(status='Open').count()
    
    treks = Trek.query.all()
    popularity = []
    for t in treks:
        t_bookings_count = Booking.query.filter_by(trek_id=t.id).count()
        popularity.append({
            "name": t.name,
            "bookings": t_bookings_count
        })
    popularity = sorted(popularity, key=lambda x: x['bookings'], reverse=True)
    
    popularity_index = []
    for tp in popularity[:4]:
        pct = (tp['bookings'] / total_bookings * 100) if total_bookings > 0 else 0
        popularity_index.append({
            "name": tp['name'],
            "count": tp['bookings'],
            "percentage": int(round(pct))
        })
        
    confirmed_count = Booking.query.filter(Booking.status.in_(['Confirmed', 'Booked', 'Completed'])).count()
    pending_count = Booking.query.filter_by(status='Pending').count()
    cancelled_count = Booking.query.filter_by(status='Cancelled').count()
    
    dist_total = confirmed_count + pending_count + cancelled_count
    confirmed_pct = int(round(confirmed_count / dist_total * 100)) if dist_total > 0 else 0
    pending_pct = int(round(pending_count / dist_total * 100)) if dist_total > 0 else 0
    cancelled_pct = int(round(cancelled_count / dist_total * 100)) if dist_total > 0 else 0
    
    return jsonify({
        "success": True,
        "data": {
            "total_revenue": f"₹{int(total_revenue):,}",
            "avg_booking_value": f"₹{int(avg_value):,}",
            "active_excursions": f"{active_excursions} Treks",
            "popularity_index": popularity_index,
            "distribution": {
                "confirmed": confirmed_pct,
                "pending": pending_pct,
                "cancelled": cancelled_pct,
                "confirmed_count": confirmed_count,
                "pending_count": pending_count,
                "cancelled_count": cancelled_count
            }
        }
    }), 200

# ================= USER ROUTES =================

@api_bp.route('/api/treks', methods=['GET'])
def get_treks():
    treks = Trek.query.all()
    return jsonify({"success": True, "data": [{
        "id": t.id, "name": t.name, "location": t.location, "difficulty": t.difficulty,
        "duration": f"{t.duration} Days", "slots": t.available_slots,
        "total_slots": t.available_slots + Booking.query.filter(Booking.trek_id == t.id, Booking.status.in_(['Confirmed', 'Booked', 'Completed'])).count(),
        "price": f"₹{int(t.price):,}" if t.price.is_integer() else f"₹{t.price}",
        "image": format_unsplash_url(t.image) or 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=600&q=80',
        "status": t.status, "start_date": t.start_date.strftime('%Y-%m-%d') if t.start_date else '',
        "end_date": t.end_date.strftime('%Y-%m-%d') if t.end_date else '',
        "staff_name": t.staff.username if t.staff else 'Passang Sherpa'
    } for t in treks]}), 200

@api_bp.route('/api/bookings', methods=['GET', 'POST'])
@jwt_required()
def user_bookings():
    user_id = int(get_jwt_identity())
    if request.method == 'GET':
        bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.id.desc()).all()
        return jsonify({"success": True, "data": [{
            "id": f"TM-{b.id}", "trekId": b.trek_id, "trekName": b.trek.name,
            "bookingDate": b.booking_date.strftime('%d %b %Y') if b.booking_date else '',
            "trekDates": f"{b.trek.start_date.strftime('%d %b')} - {b.trek.end_date.strftime('%d %b %Y')}" if b.trek.start_date and b.trek.end_date else '',
            "startDate": b.trek.start_date.strftime('%Y-%m-%d') if b.trek.start_date else '',
            "completedOn": b.trek.end_date.strftime('%d %b %Y') if b.trek.end_date else '',
            "status": 'Completed' if (b.status in ['Confirmed', 'Booked'] and b.trek.end_date and b.trek.end_date < date.today()) else b.status
        } for b in bookings]}), 200

    data = request.get_json()
    trek_id = data.get('trek_id')
    if not trek_id:
        return jsonify({"success": False, "message": "Trek ID is required"}), 400
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"success": False, "message": "Trek not found"}), 404
        
    if Booking.query.filter_by(user_id=user_id, trek_id=trek_id).filter(Booking.status != 'Cancelled').first():
        return jsonify({"success": False, "message": "You have already booked this trek"}), 400
        
    if Booking.query.filter_by(user_id=user_id).filter(Booking.status != 'Cancelled').filter(
        Booking.trek.has(start_date=trek.start_date)
    ).first():
        return jsonify({"success": False, "message": "Cannot book this trek as it has the same start date as your other booked trek"}), 400
        
    if trek.available_slots <= 0:
        return jsonify({"success": False, "message": "No slots available for this trek"}), 400
        
    new_booking = Booking(user_id=user_id, trek_id=trek_id, booking_date=date.today(), status='Pending', payment_status='Paid')
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"success": True, "message": "Trek booked successfully 🎉", "booking": {
        "id": f"TM-{new_booking.id}", "trekName": trek.name, "bookingDate": new_booking.booking_date.strftime('%d %b %Y'),
        "trekDates": f"{trek.start_date.strftime('%d %b')} - {trek.end_date.strftime('%d %b %Y')}" if trek.start_date and trek.end_date else '', "status": new_booking.status
    }}), 201

# ================= STAFF ROUTES =================

@api_bp.route('/api/staff/stats', methods=['GET'])
@jwt_required()
@role_required('staff')
def staff_stats():
    user_id = int(get_jwt_identity())
    treks = Trek.query.filter_by(staff_id=user_id).all()
    today = date.today()
    ongoing = sum(1 for t in treks if t.start_date <= today <= t.end_date and t.status != 'Completed')
    total_participants = sum(
        Booking.query.filter(Booking.trek_id == t.id, Booking.status.in_(['Confirmed', 'Booked', 'Completed'])).count()
        for t in treks
    )
    return jsonify({"success": True, "data": {"assigned_treks": len(treks), "total_participants": total_participants, "ongoing_treks": ongoing}}), 200

@api_bp.route('/api/staff/treks', methods=['GET'])
@jwt_required()
@role_required('staff')
def staff_get_treks():
    user_id = int(get_jwt_identity())
    treks = Trek.query.filter_by(staff_id=user_id).all()
    return jsonify({"success": True, "data": [{
        "id": t.id, "name": t.name, "location": t.location, "difficulty": t.difficulty, "duration": f"{t.duration} Days",
        "slots": t.available_slots, "total_slots": t.available_slots + Booking.query.filter(Booking.trek_id == t.id, Booking.status.in_(['Confirmed', 'Booked', 'Completed'])).count(),
        "participants": Booking.query.filter(Booking.trek_id == t.id, Booking.status.in_(['Confirmed', 'Booked', 'Completed'])).count(),
        "dates": f"{t.start_date.strftime('%d %b')} - {t.end_date.strftime('%d %b %Y')}" if t.start_date and t.end_date else '',
        "start_date": t.start_date.strftime('%Y-%m-%d') if t.start_date else '', "end_date": t.end_date.strftime('%Y-%m-%d') if t.end_date else '',
        "status": t.status or 'Open', "price": f"₹{int(t.price):,}" if t.price.is_integer() else f"₹{t.price}"
    } for t in treks]}), 200

@api_bp.route('/api/staff/treks/<int:t_id>/participants', methods=['GET'])
@jwt_required()
@role_required('staff')
def staff_get_trek_participants(t_id):
    user_id = int(get_jwt_identity())
    trek = Trek.query.filter_by(id=t_id, staff_id=user_id).first()
    if not trek:
        return jsonify({"success": False, "message": "Trek not found or not assigned to you"}), 404
    bookings = Booking.query.filter_by(trek_id=t_id).all()
    return jsonify({"success": True, "data": [{"id": b.id, "name": b.user.username, "email": b.user.email, "bookingDate": b.booking_date.strftime('%d %b %Y') if b.booking_date else '', "status": b.status} for b in bookings]}), 200

@api_bp.route('/api/staff/treks/<int:t_id>/status', methods=['PUT'])
@jwt_required()
@role_required('staff')
def staff_update_trek_status(t_id):
    user_id = int(get_jwt_identity())
    trek = Trek.query.filter_by(id=t_id, staff_id=user_id).first()
    if not trek:
        return jsonify({"success": False, "message": "Trek not found or not assigned to you"}), 404
    new_status = request.get_json().get('status')
    if new_status not in ['Open', 'Closed', 'Completed']:
        return jsonify({"success": False, "message": "Invalid status"}), 400
    trek.status = new_status
    db.session.commit()
    return jsonify({"success": True, "message": f"Trek status updated to {new_status}"}), 200
