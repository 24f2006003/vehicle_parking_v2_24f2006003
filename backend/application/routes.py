from flask import current_app as app, jsonify, request, abort
from .models import User
from flask_jwt_extended import create_access_token, current_user, jwt_required


def role_required(required_role):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(message="Unauthorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.password == password:
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


# @app.route('/who_am_i', methods=['GET'])
# @jwt_required()
# def protected():
#     return jsonify(
#         id=current_user.id,
#         username=current_user.username,
#         email=current_user.email,
#         password=current_user.password,
#         role=current_user.role
#     )


@app.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        return "Welcome to the admin dashboard!"
    else:
        return "Welcome to the user dashboard!"
