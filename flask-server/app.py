from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api
from exts import db
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, get_jwt, get_jwt_identity, \
    current_user, get_jti
from datetime import datetime, timedelta
from config import current_config
from models import User, Token
from resources.user import ns as user_ns
from resources.event import ns as event_ns
from resources.ticket import ns as ticket_ns

# Routes that do not fresh access token
NON_REFRESH_ROUTES = ["/user/logout", "/ticket/request_qr_data"]


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(current_config if config is None else config)
    db.init_app(app)

    # CORS
    origins = []
    for host in app.config.get("host", {}):
        origins.append(f"http://{host}")
        origins.append(f"http://{host}:3000")
        origins.append(f"https://{host}")
        origins.append(f"https://{host}:3000")
    cors = CORS(app, supports_credentials=True, origins=origins)

    # initializing a JWTManager with this app
    jwt = JWTManager(app)
    api = Api(app, doc='/docs')

    api.add_namespace(user_ns)
    api.add_namespace(event_ns)
    api.add_namespace(ticket_ns)

    if app.config.get("TEST_MODE"):
        from resources.ticket_no_sign import ns as ticket_no_sign_ns
        api.add_namespace(ticket_no_sign_ns)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(user_id=identity).scalar()

    @jwt.token_in_blocklist_loader
    def check_if_token_blocked(jwt_header, jwt_payload: dict) -> bool:
        # Checks if token is current session
        jti = jwt_payload["jti"]
        token = Token.query.filter_by(jti=jti).scalar()
        return not token or token.exp_date < datetime.now()

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            if request.path in NON_REFRESH_ROUTES:
                # Do nothing
                return response

            # Update JWT close to expiring
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now()
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            minimum_timestamp = datetime.timestamp(now + timedelta(seconds=10))
            if target_timestamp > exp_timestamp > minimum_timestamp:
                # Update old token(s)
                Token.query.filter(Token.user == current_user, Token.exp_date > now + timedelta(seconds=10))\
                    .update({Token.exp_date: now + timedelta(seconds=10)})

                # New token
                access_token = create_access_token(identity=get_jwt_identity())
                user = User.query.filter_by(user_id=current_user.user_id).one_or_none()
                user.jti = get_jti(access_token)
                token = Token(jti=user.jti, exp_date=datetime.now() + timedelta(hours=1), user_id=user.user_id)
                db.session.add(token)

                # Save changes
                db.session.commit()

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
    if app.config.get("SELF_SIGNED"):
        app.run(host="0.0.0.0", port=5000, ssl_context=("certificate/cert.pem", "certificate/key.pem"))
    else:
        app.run()


if __name__ == '__main__':
    run_app()
