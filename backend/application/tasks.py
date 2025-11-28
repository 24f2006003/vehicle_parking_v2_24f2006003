from celery import shared_task 
import csv
from jinja2 import Template
from .mail import send_email
from .models import User, Reservation, ParkingLot
import datetime
from sqlalchemy import func
import os

# Task 1. Scheduled Job - Daily reminders
@shared_task(ignore_result=False, name="daily_reminder")
def daily_reminder():
    users = User.query.filter_by(role="user").all()
    today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + datetime.timedelta(days=1)

    for user in users:
        # Check for ANY reservation today
        todays_reservations = Reservation.query.filter_by(user_id=user.id).filter(
            Reservation.parking_timestamp >= today_start,
            Reservation.parking_timestamp < today_end
        ).all()
        
        if todays_reservations:
            # Send Summary
            subject = "Daily Parking Summary"
            message = f"Hello {user.username},\n\nHere are your bookings for today:\n"
            for res in todays_reservations:
                status = res.status
                cost = res.parking_cost or 0
                message += f"- Lot: {res.spot.lot.prime_location_name}, Spot: {res.spot_id}, Time: {res.parking_timestamp}, Cost: {cost}, Status: {status}\n"
            
            send_email(user.email, subject, message, content="plain")
        else:
            # Send Reminder
            subject = "Daily Parking Reminder"
            message = f"Hello {user.username},\n\nYou haven't booked a parking spot today. Visit our app to book one if you need it!"
            send_email(user.email, subject, message, content="plain")
    return "Daily reminders/summaries sent"

# Task 2. Scheduled Job - Monthly Activity Report
@shared_task(ignore_result=False, name="monthly_report")
def monthly_report():
    users = User.query.filter_by(role="user").all()
    # Calculate previous month range
    today = datetime.datetime.now()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    start_date = last_month.replace(day=1)
    end_date = first
    
    month_name = last_month.strftime("%B %Y")

    for user in users:
        reservations = Reservation.query.filter_by(user_id=user.id).filter(Reservation.parking_timestamp >= start_date, Reservation.parking_timestamp < end_date).all()
        
        total_bookings = len(reservations)
        total_spent = sum(r.parking_cost for r in reservations if r.parking_cost)
        
        # Most used parking lot
        lot_counts = {}
        for r in reservations:
            lot_id = r.spot.lot_id
            lot_counts[lot_id] = lot_counts.get(lot_id, 0) + 1
        
        most_used_lot_name = "N/A"
        if lot_counts:
            most_used_lot_id = max(lot_counts, key=lot_counts.get)
            lot = ParkingLot.query.get(most_used_lot_id)
            if lot:
                most_used_lot_name = lot.prime_location_name

        html_template = """
        <html>
        <body>
            <h1>Monthly Activity Report - {{ month }}</h1>
            <p>Hello {{ username }},</p>
            <p>Here is your parking activity for {{ month }}:</p>
            <ul>
                <li>Total Bookings: {{ total_bookings }}</li>
                <li>Total Spent: Rs. {{ total_spent }}</li>
                <li>Most Used Parking Lot: {{ most_used_lot }}</li>
            </ul>
            <p>Thank you for using our service!</p>
        </body>
        </html>
        """
        template = Template(html_template)
        html_content = template.render(
            month=month_name,
            username=user.username,
            total_bookings=total_bookings,
            total_spent=total_spent,
            most_used_lot=most_used_lot_name
        )
        
        send_email(user.email, f"Monthly Report - {month_name}", html_content, content="html")
    
    return "Monthly reports sent"

# Task 3. User Triggered Async Job - Export as CSV
@shared_task(ignore_result=False, name="export_csv")
def export_csv(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found"
        
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    
    # Create CSV file in static folder
    csv_file_name = f"parking_history_{user_id}_{datetime.datetime.now().strftime('%f')}.csv"
    file_path = os.path.join('static', csv_file_name)
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Reservation ID', 'Spot ID', 'Parking Timestamp', 'Leaving Timestamp', 'Cost', 'Status'])
        for r in reservations:
            writer.writerow([r.id, r.spot_id, r.parking_timestamp, r.leaving_timestamp, r.parking_cost, r.status])
            
    # Send email with CSV content
    subject = "Your Parking Data Export"
    body = f"Hello {user.username},\n\nYour data export is ready. Please find the attached CSV file."
    
    # Send email with attachment
    send_email(user.email, subject, body, content="plain", attachment_file=file_path)
    
    return csv_file_name
