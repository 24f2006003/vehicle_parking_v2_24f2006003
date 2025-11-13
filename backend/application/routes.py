from flask import current_app as app, jsonify, request, abort
from .models import *
from .database import db
from flask_jwt_extended import create_access_token, current_user, jwt_required
from functools import wraps
from datetime import datetime

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
    return jsonify(access_token=access_token), 200


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

@app.route("/api/dashboard")
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        users = User.query.filter_by(role="user").all()
        reservations = Reservation.query.all()
        parking_lots = ParkingLot.query.all()
        total_users = len(users)
        parking_spots_json = []
        for lot in parking_lots:
            spots_dict = {}
            spots_dict['id'] = lot.id
            spots_dict['total_spots'] = lot.number_of_spots
            spots_dict['available_spots'] = lot.available_spots
            spots_dict['occupied_spots'] = lot.occupied_spots
            parking_spots_json.append(spots_dict)

        return jsonify(
            message="Welcome to the admin dashboard!",
            total_users=total_users,
            total_reservations=len(reservations),
            total_parking_lots=len(parking_lots),
            parking_lots=parking_spots_json
        ), 200
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
            
        return jsonify(
            message="Welcome to the user dashboard!",
            reservations=res_json
        ), 200


# User Endpoints

@app.route("/api/user_home")
@jwt_required()
#@role_required("user")
def user_home():
    user = User.query.get(current_user.id)
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    user_reg_json = []
    for res in user_reservations:
        res_dict = {}
        res_dict['reservation_id'] = res.id
        res_dict['spot_id'] = res.spot_id
        res_dict['parking_timestamp'] = res.parking_timestamp
        res_dict['leaving_timestamp'] = res.leaving_timestamp
        res_dict['parking_cost'] = res.parking_cost
        res_dict['status'] = res.status
        user_reg_json.append(res_dict)
    return jsonify(user_reg_json), 200


@app.route("/api/lots")
def get_parking_lots():
    parking_lots = ParkingLot.query.all()
    parking_lots_json = []
    for lot in parking_lots:
        lot_dict = {}
        lot_dict['lot_id'] = lot.id
        lot_dict['prime_location_name'] = lot.prime_location_name
        lot_dict['price'] = lot.price
        lot_dict['address'] = lot.address
        lot_dict['pin_code'] = lot.pin_code
        lot_dict['number_of_spots'] = lot.number_of_spots
        lot_dict['available_spots'] = lot.available_spots
        parking_lots_json.append(lot_dict)
    return jsonify(parking_lots_json), 200

@app.route("/api/lot/<int:lot_id>")
def get_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    lot_dict = {
        'lot_id': lot.id,
        'prime_location_name': lot.prime_location_name,
        'price': lot.price,
        'address': lot.address,
        'pin_code': lot.pin_code,
        'number_of_spots': lot.number_of_spots,
        'available_spots': lot.available_spots
    }
    return jsonify(lot_dict), 200

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
        spots_json.append(spot_dict)
    return jsonify(spots_json), 200


@app.route("/api/reservations", methods=["POST"])
@jwt_required()
def create_reservation():
    spot_id = request.json.get("spot_id", None)
    parking_timestamp = request.json.get("parking_timestamp", None)
    leaving_timestamp = request.json.get("leaving_timestamp", None)
    parking_cost = request.json.get("parking_cost", None)

    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status != 'A':
        return jsonify("Spot is not available"), 400

    reservation = Reservation(spot_id=spot_id, user_id=current_user.id, parking_timestamp=parking_timestamp, leaving_timestamp=leaving_timestamp, parking_cost=parking_cost)
    db.session.add(reservation)
    spot.status = 'O'
    spot.lot.available_spots -= 1
    db.session.commit()
    return jsonify("Reservation created successfully"), 201

@app.route("/api/reservations")
@jwt_required()
def get_my_reservations():
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
def update_reservation(reservation_id):\
    # - Users: allowed actions via { action: "leave"|"complete" } only on their own reservations.
    # - Admins: can update fields: spot_id, status, parking_timestamp, leaving_timestamp, parking_cost.

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
    elif action == "complete":
        reservation.status = "C"
    else:
        return jsonify(message="Invalid action"), 400

    db.session.commit()
    return jsonify(message="Reservation updated successfully"), 200

@app.route("/api/reservations/<int:reservation_id>", methods=["DELETE"])
@jwt_required()
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify(message="Reservation canceled successfully"), 204


# Admin Endpoints

@app.route("/api/admin_home")
@jwt_required()
def admin_home():
    if current_user.role == "admin":
        return "Welcome to the admin home page!", 200
    else:
        return jsonify(message="Unauthorized"), 403

@app.route("/api/lots", methods=["POST"])
@jwt_required()
def create_parking_lot():
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    data = request.json
    new_lot = ParkingLot(
        name=data.get("name"),
        location=data.get("location"),
        total_spots=data.get("total_spots"),
        available_spots=data.get("available_spots")
    )
    db.session.add(new_lot)
    db.session.commit()
    return jsonify(message="Parking lot created successfully"), 201

@app.route("/api/lots/<int:lot_id>", methods=["PATCH"])
@jwt_required()
def update_parking_lot(lot_id):
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.json

    lot.name = data.get("name", lot.name)
    lot.location = data.get("location", lot.location)
    lot.total_spots = data.get("total_spots", lot.total_spots)
    lot.available_spots = data.get("available_spots", lot.available_spots)

    db.session.commit()
    return jsonify(message="Parking lot updated successfully"), 200

@app.route("/api/lots/<int:lot_id>", methods=["DELETE"])
@jwt_required()
def delete_parking_lot(lot_id):
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    return jsonify(message="Parking lot deleted successfully"), 200

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

@app.route("/api/reservations")
@jwt_required()
def get_reservations():
    if current_user.role != "admin":
        return jsonify(message="Unauthorized"), 403

    reservations = Reservation.query.all()
    reservation_list = [{
        'id': reservation.id,
        'lot_id': reservation.spot.lot_id,
        'spot_id': reservation.spot_id,
        'status': reservation.status
    } for reservation in reservations]

    return jsonify(reservations=reservation_list), 200

@app.route("/api/reservations/<int:reservation_id>/invoice")
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