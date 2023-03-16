from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from exts import db
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, get_jwt, get_jwt_identity
from datetime import datetime, timedelta, timezone
from config import current_config
from models import User, TokenBlocklist
from resources import ns


def create_app(config=None):
    app = Flask(__name__)
    cors = CORS(app, supports_credentials=True, origins=["http://localhost:3000", "https://localhost:3000"])
    app.config.from_object(current_config if config is None else config)
    db.init_app(app)
    # migrate=Migrate(app,db)

    # initializing a JWTManager with this app
    jwt = JWTManager(app)
    api = Api(app, doc='/docs')

    api.add_namespace(ns, '')

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(user_id=identity).one_or_none()

    @jwt.token_in_blocklist_loader
    def check_if_token_blocked(jwt_header, jwt_payload: dict) -> bool:
        # Checks if token is in blocked list
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            if response.json.get('logout', False):
                # Do nothing if logging out
                return response

            # Update JWT close to expiring
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError, AttributeError):
            # Invalid JWT, return unchanged response
            return response

    return app


def run_app():
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run()
    # app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("certificate/cert.pem", "certificate/key.pem"))


if __name__ == '__main__':
    run_app()
