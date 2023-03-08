from flask import Flask, request, jsonify
from flask_restx import Api,Resource, fields
from config import DevConfig
from models import UserTable
from exts import db
#from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
#migrate=Migrate(app,db)

#initializing a JWTManager with this app
JWTManager(app)
api = Api(app, doc='/docs')



#serilizer for Sign up
signup_model = api.model(
    "SignUp",
    {
        "userId":fields.Integer(),
        "firstName":fields.String(),
        "surName":fields.String(),
        "emailAddress":fields.String(),
        "password":fields.String()
    }
)

#serilizer for Login 
login_model = api.model(
    "LogIn",
    {
        "userId":fields.Integer(),
        "password":fields.String()
    }
)






@api.route('/signup')
class SignUp(Resource):

    @api.expect(signup_model)
    def post(self):
        data = request.get_json()

        userId = data.get('userId')

        # user already exists in database?
        db_user = UserTable.query.filter_by(userId=userId).first()
        if db_user is not None:
            return jsonify({"message" : f"The user {userId} already exits."})


        new_user = UserTable(
            userId = data.get('userId'),
            firstName = data.get('firstName'),
            surName = data.get('surName'),
            emailAddress = data.get('emailAddress'),
            # We need a random salt here to mitiage offline birthday attacks
            password = generate_password_hash(data.get('password'))
        )
        new_user.save()

        return jsonify({"message" : f"User {userId} created successsfully."})





@api.route('/login')
class Login(Resource):

    @api.expect(login_model)
    def post(self):
        data = request.get_json()

        userId = data.get('userId')
        password = data.get('password')

        db_user = UserTable.query.filter_by(userId=userId).first()
        #if db_user is None:
        #    return jsonify({"message" : f"The userId {userId} does not exist"})

        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.userId)
            refresh_token = create_refresh_token(identity=db_user.userId)

            return jsonify(
                {
                "acess_token" : access_token,
                "refresh_token": refresh_token
                }
            )
        # return ? in case of failure



'''
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "UserTable": UserTable
    }

'''

if __name__ == '__main__':
    app.run()