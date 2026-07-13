import os
import datetime
import csv
import requests
import json
from celery_config import celery_app
from models import db, User, Booking, Trek
from utils import format_report
from mail import send_email

@celery_app.task(name="download_csv_report")
def csv_report():
    bookings = Booking.query.all()
    csv_file_name = f"booking_{datetime.datetime.now().strftime('%f')}.csv"
    
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    
    with open(f'static/{csv_file_name}', 'w', newline="", encoding='utf-8') as csvfile:
        sr_no = 1
        trans_csv = csv.writer(csvfile, delimiter=',')
        trans_csv.writerow([
            'Sr No.', 'Booking ID', 'User ID', 'Username', 'Email', 
            'Trek Name', 'Booking Date', 'Status', 'Payment Status', 'Price'
        ])
        for b in bookings:
            this_trans = [
                sr_no, 
                f"TM-{b.id}", 
                b.user_id, 
                b.user.username if b.user else 'N/A', 
                b.user.email if b.user else 'N/A', 
                b.trek.name if b.trek else 'N/A', 
                b.booking_date.strftime('%Y-%m-%d') if b.booking_date else 'N/A', 
                b.status, 
                b.payment_status or 'Pending', 
                b.trek.price if b.trek else 0.0
            ]
            trans_csv.writerow(this_trans)
            sr_no += 1

    return csv_file_name

@celery_app.task(name="monthly_report")
def monthly_report():
    # 1. Send aggregated summary to Admin
    admin = User.query.filter_by(role='admin').first()
    admin_email = admin.email if admin else "admin@user.com"

    bookings = Booking.query.all()
    bookings_data = []
    for b in bookings:
        bookings_data.append({
            "username": b.user.username if b.user else "N/A",
            "email": b.user.email if b.user else "N/A",
            "trek_name": b.trek.name if b.trek else "N/A",
            "status": b.status,
            "price": b.trek.price if b.trek else 0.0
        })

    admin_message = format_report('templates/admin_monthly_report.html', {"bookings": bookings_data})
    send_email(admin_email, subject="Monthly Trekking Management Summary - Admin", message=admin_message)

    # 2. Send individual summary report to each User
    users = User.query.all()
    for user in users:
        if user.role != 'user':
            continue
        user_data = {}
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_trans = []
        for booking in user.bookings:
            this_trans = {}
            this_trans["id"] = booking.id
            this_trans["name"] = booking.trek.name if booking.trek else 'N/A'
            this_trans["type"] = booking.status
            this_trans["source"] = booking.trek.location if booking.trek else 'N/A'
            this_trans["destination"] = booking.trek.name if booking.trek else 'N/A'
            this_trans["delivery"] = booking.trek.start_date.strftime('%Y-%m-%d') if (booking.trek and booking.trek.start_date) else ''
            this_trans["amount"] = booking.trek.price if booking.trek else 0.0
            this_trans["user"] = user.username
            user_trans.append(this_trans)
        user_data['transactions'] = user_trans
        user_message = format_report('templates/mail_details.html', user_data)
        send_email(user.email, subject="Your Monthly Trekking Summary - TrekMate", message=user_message)

    return "Admin and User monthly reports sent successfully"

@celery_app.task(name="delivery_update")
def delivery_report(username, trek_name="", booking_id="", status=""):
    status_emoji = {
        'Confirmed': '✅',
        'Booked': '✅',
        'Cancelled': '❌',
        'Pending': '⏳'
    }
    emoji = status_emoji.get(status, '🔔')

    card_message = {
        "cardsV2": [{
            "cardId": f"booking-{booking_id}",
            "card": {
                "header": {
                    "title": "🏔️ TrekMate Booking Update",
                    "subtitle": f"Booking {booking_id}",
                    "imageUrl": "https://img.icons8.com/color/96/trekking.png",
                    "imageType": "CIRCLE"
                },
                "sections": [{
                    "header": "Booking Details",
                    "widgets": [
                        {
                            "decoratedText": {
                                "topLabel": "Trekker",
                                "text": f"👤 {username}"
                            }
                        },
                        {
                            "decoratedText": {
                                "topLabel": "Trek",
                                "text": f"⛰️ {trek_name}"
                            }
                        },
                        {
                            "decoratedText": {
                                "topLabel": "Booking ID",
                                "text": f"🎫 {booking_id}"
                            }
                        },
                        {
                            "decoratedText": {
                                "topLabel": "Status",
                                "text": f"{emoji} {status}"
                            }
                        }
                    ]
                }]
            }
        }]
    }

    webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAEfQM7D4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Wpt1jyRYvxRzl0kcPQY4x9PD47oHKeHtSotWmOO7fD4"
    response = requests.post(webhook_url, json=card_message)
    print(f"Webhook response: {response.status_code}")
    return "The delivery status is updated"

