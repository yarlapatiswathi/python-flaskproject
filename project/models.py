from time import time, timezone
from project import db,bcrypt,login_manager,app
from datetime import datetime,timedelta
from flask_login import UserMixin
from flask import redirect,url_for
import jwt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('register'))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image=db.Column(db.String(20),nullable=False,default='default.jpg')
    password=db.Column(db.String(60),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def generate_token(self,mints=60):
        token=jwt.encode({
                        "confirm":self.id,
                              #dt.datetime.now(dt.timezone.utc).astimezone().tzname()
                        "exp":datetime.utcnow() + timedelta(minutes=mints)},
                    app.config['SECRET_KEY'],algorithm="HS256"
                    )
        return token
    @staticmethod
    def verify_token(token):
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
            print('id=',data.get('confirm'))
            return data.get('confirm')
        except:
            return None

    def __repr__(self):
        return f'{self.username}:{self.email}:{self.date_created.strftime("%d-%m-%y,%H:%M:%S")}'