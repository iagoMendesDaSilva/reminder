import os
import datetime
from modelsDao import dao
from random import randint
from flask_mail import Message
from app.token import create_token
from models.user import user_schema,User
from itsdangerous import SignatureExpired
from app.applications import mail, urlSafe
from werkzeug.exceptions import BadRequest
from app.exceptions import MailException, ObjectInvalid, UserExists
from flask import abort, make_response, jsonify, url_for
from werkzeug.security import check_password_hash, generate_password_hash

class UserController:
    def __init__(self):
        pass

    def login(self, data):
        try:
            user = dao.get_by_key('email',data['email'], User)
            password = check_password_hash(user.password,data['password'])
            if password and user.verified == True:
                token =  create_token(user)
                dao.update(user.id,'token',token,User)
                return user_schema.dump(user)
            else:
                raise ObjectInvalid
        except ObjectInvalid as err:
            abort(make_response(jsonify({"response":"Invalid User."}), 404))
        except Exception as err:
            abort(make_response(jsonify({"response":"Internal problem."}), 500))

    def logout(self, id):
        try:
            update_data ={"token": None}
            dao.update_many(id,update_data,User)
        except Exception as err:
            abort(make_response(jsonify({"response":"Internal problem."}), 500))

    def edit_player_id(self, data, id):
        try:
            user = dao.get_by_id(id, User)
            dao.update(id, 'onesignal_playerID',data['onesignal_playerID'], User)
        except ObjectInvalid as err:
            abort(make_response(jsonify({"response":"User not found."}), 404))
        except Exception as err:
            abort(make_response(jsonify({"response":"Internal problem."}), 500)) 

    def register(self, data):
        try:
            user_db = dao.exist_by_key('email', data['email'], User)
            password =generate_password_hash(data['password'])
            user = User(
            token=None,
            onesignal_playerID=None,
            verified=False,
            email=data['email'],
            password=password
            )
            if user_db is not None:
                if user_db.verified==True:
                    raise UserExists
                else:
                   dao.update(user_db.id, 'password', password, User)
                   self.send_email_verify_acccount(data['email'])
            else:
                dao.add(user)
                self.send_email_verify_acccount(data['email'])
        except UserExists as err:
            abort(make_response(jsonify({"response":"User already registered."}), 404))
        except BadRequest as err:
            abort(make_response(jsonify({"response":"  Invalid parameters."}), 400))
        except MailException as err:
            abort(make_response(jsonify({"response":"Fail to send email."}), 500))
        except Exception as err:
            abort(make_response(jsonify({"response":"Internal problem"}), 500))


    def send_email_verify_acccount(self, email):
        try:
            token = urlSafe.dumps(email, salt='email-confirm')
            msg = Message('Reminder app confirm email', sender = os.getenv("REMINDER_EMAIL"), recipients = [email])
            link = url_for('verify_account', token=token, _external=True)
            msg.body = 'Your link is {}'.format(link)
            mail.send(msg)
        except:
            raise MailException 

    def send_email_recovery_password(self, email, code):
        try:
            msg = Message('Reminder recovery password', sender = os.getenv("REMINDER_EMAIL"), recipients = [email])
            msg.body = 'Your code is {}'.format(code)
            mail.send(msg)
        except Exception as err:
            raise MailException 

    def verify_email(self, data):
        try:
            user = dao.get_by_key('email',data['email'],User)
            if user.verified == True:
                return user.id
            else:
                raise ObjectInvalid
        except ObjectInvalid as err:
            abort(make_response(jsonify({"response":"Invalid Email."}), 404))
        except Exception as err:
            abort(make_response(jsonify({"response":"Internal problem."}), 500))  
        
    def confirm_email(self,data):
        try:
            user =  dao.get_by_key('email',data['email'],User)
            recovery = randint(10000, 99999)
            recovery_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
            data = {"recovery":recovery,"recovery_time":recovery_time}
            dao.update_many(user.id,data,User)
            self.send_email_recovery_password(user.email, str(recovery))
            return user.id
        except ObjectInvalid as err:
            abort(make_response(jsonify({"response":"Invalid User."}), 404))
        except Exception as err:
            abort(make_response(jsonify({"response":"Internal problem."}), 500))

    def recovery(self,id,data):
        try:
            user = dao.get_by_id(id, User)
            new_password =generate_password_hash(data['password'])
            update_data ={"password": new_password, "recovery":None, "recovery_time":None}
            dao.update_many(id,update_data,User)
            return user_schema.dump(user)
        except ObjectInvalid as err:
            abort(make_response(jsonify({"response":"Invalid User."}), 404))
        except Exception as err:
            abort(make_response(jsonify({"response":"Internal problem."}), 500))

    def confirm_verification_code(self,id,data):
        try:
            user = dao.get_by_id(id,User)
            time = datetime.datetime.now() - datetime.timedelta(minutes=15)
            if str(user.recovery)==data['verification_code'] and user.recovery_time>time:
                token =  create_token(user)
                dao.update(user.id,'token',token,User)
                return user
            else:
                raise ObjectInvalid
        except ObjectInvalid as err:
            abort(make_response(jsonify({"response":"Invalid User or Code."}), 404))
        except Exception as err:
            abort(make_response(jsonify({"response":"Internal problem."}), 500))

    def create_account(self, token):
        try:
            email = urlSafe.loads(token, salt='email-confirm', max_age=900)
            user = dao.get_by_key('email', email, User)
            dao.update(user.id, 'verified', True, User)
            return '<h1>Your account has been activated.</h1>'
        except ObjectInvalid as err:
            abort(make_response(jsonify({"response":"User not found."}), 404))
        except SignatureExpired:
            return '<h1>The link is expired!</h1>'

userController = UserController()