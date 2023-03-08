from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/@me')
def get_current_user():
    return {}


@app.route('/login', methods=["POST"])
def login():
    # login user from db
    return {}


@app.route('/register', methods=["POST"])
def register():
    # register user here in db
    return {}


@app.route("/logout", methods=["POST"])
def logout_user():
    return ""


if __name__ == '__main__':
    app.run(debug=True)
