from flask import current_app as app, jsonify, request, abort
from .models import *
from .database import db
from flask_jwt_extended import create_access_token, current_user, jwt_required
from functools import wraps
from datetime import datetime
from application.cache import cache

def calculate_invoice_amount(reservation):
    return reservation.parking_cost or 0

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(message="Unauthorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


@app.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).one_or_none()
    if not user or not user.password == password:
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token, role=user.role, username=user.username), 200


@app.route("/api/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify("User already exists"), 400

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify("User created successfully"), 201

@cache.cached(timeout=60, key_prefix='admin_dashboard_stats')
def get_admin_dashboard_stats():
    users = User.query.filter_by(role="user").all()
    reservations = Reservation.query.all()
    parking_lots = ParkingLot.query.all()
    total_users = len(users)
    parking_spots_json = []
    for lot in parking_lots:
        total = len(lot.spots)
        available = sum(1 for s in lot.spots if s.status == 'A')
        occupied = total - available
        spots_dict = {
            'id': lot.id,
            'total_spots': total or lot.number_of_spots,
            'available_spots': available,
            'occupied_spots': occupied
        }
        parking_spots_json.append(spots_dict)

    return {
        "message": "Welcome to the admin dashboard!",
        "total_users": total_users,
        "total_reservations": len(reservations),
        "total_parking_lots": len(parking_lots),
        "parking_lots": parking_spots_json
    }

@app.route("/api/dashboard")
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        stats = get_admin_dashboard_stats()
        return jsonify(stats), 200
    else:
        user = User.query.get(current_user.id)
        if not user:
            return jsonify("User not found"), 404
        reservations = Reservation.query.filter_by(user_id=current_user.id).all()
        res_json = []
        for res in reservations:
            res_dict = {}
            res_dict['reservation_id'] = res.id
            res_dict['spot_id'] = res.spot_id
            res_dict['parking_timestamp'] = res.parking_timestamp
            res_dict['leaving_timestamp'] = res.leaving_timestamp
            res_dict['parking_cost'] = res.parking_cost
            res_dict['status'] = res.status
            res_json.append(res_dict)
            
        return jsonify(reservations=res_json), 200

# User and Admin Endpoints

@app.route("/api/admin_home")
@jwt_required()
def admin_home():
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403
    return jsonify(message="Welcome to the admin home page!"), 200


@app.route("/api/user_home")
@jwt_required()
#@role_required("user")
def user_home():
    return jsonify(message="Welcome to the user home page!"), 200

@app.route("/api/lots", methods=["GET"])
def get_parking_lots():
    lots = ParkingLot.query.all()
    lots_json = []
    for lot in lots:
        total = len(lot.spots) or lot.number_of_spots
        available = sum(1 for s in lot.spots if s.status == 'A')
        lot_dict = {
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'price': lot.price,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'number_of_spots': total,
            'available_spots': available
        }
        lots_json.append(lot_dict)
    return jsonify(lots_json), 200

@app.route("/api/lots", methods=["POST"])
@jwt_required()
def create_parking_lot():
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    data = request.json
    prime_location_name = data.get("prime_location_name")
    price = data.get("price")
    address = data.get("address")
    pin_code = data.get("pin_code")
    number_of_spots = data.get("number_of_spots")

    if not all([prime_location_name, price, address, pin_code, number_of_spots]):
        return jsonify(message="Missing required fields"), 400

    lot = ParkingLot(
        prime_location_name=prime_location_name,
        price=price,
        address=address,
        pin_code=pin_code,
        number_of_spots=number_of_spots,
        available_spots=number_of_spots
    )
    db.session.add(lot)
    db.session.flush()

    for _ in range(number_of_spots):
        spot = ParkingSpot(lot_id=lot.id, status='A')
        db.session.add(spot)

    db.session.commit()
    return jsonify(message="Parking lot created successfully", lot_id=lot.id), 201

@app.route("/api/lot/<int:lot_id>")
def get_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    total = len(lot.spots) or lot.number_of_spots
    available = sum(1 for s in lot.spots if s.status == 'A')
    lot_dict = {
        'lot_id': lot.id,
        'prime_location_name': lot.prime_location_name,
        'price': lot.price,
        'address': lot.address,
        'pin_code': lot.pin_code,
        'number_of_spots': total,
        'available_spots': available
    }
    return jsonify(lot_dict), 200

@app.route("/api/lots/<int:lot_id>", methods=["PATCH"])
@jwt_required()
def update_parking_lot(lot_id):
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.json

    lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
    lot.price = data.get("price", lot.price)
    lot.address = data.get("address", lot.address)
    lot.pin_code = data.get("pin_code", lot.pin_code)

    new_total_spots = data.get("number_of_spots")
    if new_total_spots is not None and new_total_spots != lot.number_of_spots:
        current_spots = len(lot.spots)
        diff = new_total_spots - current_spots

        if diff > 0:
            # Add new spots
            for _ in range(diff):
                db.session.add(ParkingSpot(lot_id=lot.id, status='A'))
        elif diff < 0:
            # Remove available spots
            spots_to_remove = abs(diff)
            available_spots = [s for s in lot.spots if s.status == 'A']
            if len(available_spots) < spots_to_remove:
                return jsonify(message=f"Cannot reduce spots by {spots_to_remove}. Only {len(available_spots)} available spots."), 400
            
            for i in range(spots_to_remove):
                db.session.delete(available_spots[i])

        lot.number_of_spots = new_total_spots
        # Recalculate available spots
        db.session.flush()
        lot.available_spots = sum(1 for s in lot.spots if s.status == 'A')

    db.session.commit()
    # Refresh to get accurate count
    lot.available_spots = sum(1 for s in lot.spots if s.status == 'A')
    db.session.commit()
    
    return jsonify(message="Parking lot updated successfully"), 200

@app.route("/api/lots/<int:lot_id>", methods=["DELETE"])
@jwt_required()
def delete_parking_lot(lot_id):
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    lot = ParkingLot.query.get_or_404(lot_id)
    
    # Check if any spot is occupied
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()
    if occupied_spots > 0:
        return jsonify(message="Cannot delete parking lot with occupied spots"), 400

    # Delete all spots first
    ParkingSpot.query.filter_by(lot_id=lot_id).delete()
    db.session.delete(lot)
    db.session.commit()
    return jsonify(message="Parking lot deleted successfully"), 200

@app.route("/api/lots/<int:lot_id>/spots")
def get_parking_spots(lot_id):
    status = request.args.get('status', None)
    query = ParkingSpot.query.filter_by(lot_id=lot_id)
    if status in ['A', 'O']:
        query = query.filter_by(status=status)
    spots = query.all()
    spots_json = []
    for spot in spots:
        spot_dict = {
            'spot_id': spot.id,
            'lot_id': spot.lot_id,
            'status': spot.status
        }
        if spot.status == 'O':
            # Fetch active reservation details
            active_res = Reservation.query.filter_by(spot_id=spot.id, status='active').first()
            if active_res:
                spot_dict['reservation_id'] = active_res.id
                spot_dict['user_id'] = active_res.user_id
                spot_dict['username'] = active_res.user.username
                spot_dict['parking_timestamp'] = active_res.parking_timestamp
        spots_json.append(spot_dict)
    return jsonify(spots_json), 200


@app.route("/api/reservations", methods=["POST"])
@jwt_required()
def create_reservation():
    lot_id = request.json.get("lot_id", None)
    parking_timestamp_str = request.json.get("parking_timestamp", None)
    leaving_timestamp_str = request.json.get("leaving_timestamp", None)
    parking_cost = request.json.get("parking_cost", None)

    if parking_timestamp_str:
        parking_timestamp = datetime.fromisoformat(parking_timestamp_str)
    else:
        parking_timestamp = datetime.now()
        
    if leaving_timestamp_str:
        leaving_timestamp = datetime.fromisoformat(leaving_timestamp_str)
    else:
        leaving_timestamp = None

    # Auto-allocation logic
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    
    if not spot:
        return jsonify("No available spots in this lot"), 400

    spot_id = spot.id
    
    reservation = Reservation(spot_id=spot_id, user_id=current_user.id, parking_timestamp=parking_timestamp, leaving_timestamp=leaving_timestamp, parking_cost=parking_cost)
    db.session.add(reservation)
    spot.status = 'O'
    # Recalculate available spots for the lot
    spot.lot.available_spots = sum(1 for s in spot.lot.spots if s.status == 'A')
    db.session.commit()
    return jsonify("Reservation created successfully"), 201

@app.route("/api/reservations")
@jwt_required()
def get_reservations():
    # If admin, return all. If user, return own.
    if current_user.role == "admin":
        reservations = Reservation.query.all()
        reservation_list = [{
            'id': reservation.id,
            'lot_id': reservation.spot.lot_id,
            'spot_id': reservation.spot_id,
            'status': reservation.status
        } for reservation in reservations]
        return jsonify(reservations=reservation_list), 200
    else:
        user = User.query.get(current_user.id)
        reservations = Reservation.query.filter_by(user_id=user.id).all()
        reservations_json = []
        for res in reservations:
            res_dict = {
                'reservation_id': res.id,
                'spot_id': res.spot_id,
                'parking_timestamp': res.parking_timestamp,
                'leaving_timestamp': res.leaving_timestamp,
                'parking_cost': res.parking_cost,
                'status': res.status
            }
            reservations_json.append(res_dict)
        return jsonify(reservations_json), 200

@app.route("/api/reservations/<int:reservation_id>")
@jwt_required()
def get_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation_dict = {
        'reservation_id': reservation.id,
        'spot_id': reservation.spot_id,
        'parking_timestamp': reservation.parking_timestamp,
        'leaving_timestamp': reservation.leaving_timestamp,
        'parking_cost': reservation.parking_cost,
        'status': reservation.status
    }
    return jsonify(reservation_dict), 200

@app.route("/api/reservations/<int:reservation_id>", methods=["PATCH"])
@jwt_required()
def update_reservation(reservation_id):
    # Users: allowed actions via { action: "leave"|"complete" } only on their own reservations.
    # Admins: can update fields: spot_id, status, parking_timestamp, leaving_timestamp, parking_cost.

    reservation = Reservation.query.get_or_404(reservation_id)
    data = request.json or {}

    if current_user.role == "admin":
        # Admin can update full details (validate spot if provided)
        new_spot_id = data.get("spot_id")
        if new_spot_id is not None:
            spot = ParkingSpot.query.get_or_404(new_spot_id)
            reservation.spot_id = spot.id
        if "status" in data:
            reservation.status = data.get("status", reservation.status)
        if "parking_timestamp" in data:
            reservation.parking_timestamp = data.get("parking_timestamp", reservation.parking_timestamp)
        if "leaving_timestamp" in data:
            reservation.leaving_timestamp = data.get("leaving_timestamp", reservation.leaving_timestamp)
        if "parking_cost" in data:
            reservation.parking_cost = data.get("parking_cost", reservation.parking_cost)
        
        db.session.commit()
        return jsonify(message="Reservation updated successfully"), 200

    # User path: can only act on own reservation
    if reservation.user_id != current_user.id:
        return jsonify(message="Unauthorized"), 403

    action = data.get("action")
    if action == "leave":
        reservation.status = "L"
        reservation.spot.status = 'A'
        reservation.spot.lot.available_spots = sum(1 for s in reservation.spot.lot.spots if s.status == 'A')
    elif action == "complete":
        reservation.status = "C"
        reservation.spot.status = 'A'
        reservation.spot.lot.available_spots = sum(1 for s in reservation.spot.lot.spots if s.status == 'A')
        
        now = datetime.now()
        reservation.leaving_timestamp = now
        
        if reservation.parking_timestamp:
            duration = now - reservation.parking_timestamp
            hours = duration.total_seconds() / 3600
            price_per_hour = reservation.spot.lot.price
            reservation.parking_cost = max(0, round(hours * price_per_hour, 2))
            
    else:
        return jsonify(message="Invalid action"), 400

    db.session.commit()
    return jsonify(message="Reservation updated successfully"), 200

@app.route("/api/reservations/<int:reservation_id>", methods=["DELETE"])
@jwt_required()
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    try:
        reservation.spot.status = 'A'
        reservation.spot.lot.available_spots = sum(1 for s in reservation.spot.lot.spots if s.status == 'A')
    except Exception:
        pass
    db.session.delete(reservation)
    db.session.commit()
    return jsonify(message="Reservation canceled successfully"), 204

@app.route("/api/spots/<int:spot_id>", methods=["PATCH"])
@jwt_required()
def update_parking_spot(spot_id):
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    spot = ParkingSpot.query.get_or_404(spot_id)
    data = request.json

    spot.lot_id = data.get("lot_id", spot.lot_id)
    spot.status = data.get("status", spot.status)

    db.session.commit()
    return jsonify(message="Parking spot updated successfully"), 200

@app.route("/api/users")
@jwt_required()
def get_users():
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    users = User.query.all()
    user_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    } for user in users]

    return jsonify(users=user_list), 200

@app.route("/api/users/<int:user_id>")
@jwt_required()
def get_user(user_id):
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    user = User.query.get_or_404(user_id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }
    return jsonify(user=user_data), 200

@app.route("/api/users/<int:user_id>/reservations")
@jwt_required()
def get_user_reservations(user_id):
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    user = User.query.get_or_404(user_id)
    reservations = Reservation.query.filter_by(user_id=user.id).all()
    reservation_list = [{
        'id': reservation.id,
        'lot_id': reservation.spot.lot_id,
        'spot_id': reservation.spot_id,
        'status': reservation.status
    } for reservation in reservations]

    return jsonify(reservations=reservation_list), 200

@app.route("/api/reservations/<int:reservation_id>/invoice", methods=["GET", "POST"])
@jwt_required()
def create_reservation_invoice(reservation_id):
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    reservation = Reservation.query.get_or_404(reservation_id)

    invoice = {
        'id': reservation.id,
        'lot_id': reservation.spot.lot_id,
        'spot_id': reservation.spot_id,
        'status': reservation.status,
        'amount': calculate_invoice_amount(reservation)
    }

    return jsonify(invoice=invoice), 200


# Backend Jobs Triggers

@app.route("/api/export_csv", methods=["POST"])
@jwt_required()
def trigger_export_csv():
    from application.tasks import export_csv
    export_csv.delay(current_user.id)
    return jsonify(message="CSV export started. You will receive an email when it is ready."), 202

@app.route("/api/daily_reminder", methods=["POST"])
@jwt_required()
def trigger_daily_reminder():
    from application.tasks import daily_reminder
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403
    daily_reminder.delay()
    return jsonify(message="Daily reminder job started."), 202

@app.route("/api/monthly_report", methods=["POST"])
@jwt_required()
def trigger_monthly_report():
    from application.tasks import monthly_report
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403
    monthly_report.delay()
    return jsonify(message="Monthly report job started."), 202

@app.route('/api/send_mail')
def send_mail():
    from application.tasks import monthly_report
    res = monthly_report.delay()
    return{
        "message": str(res)
    }