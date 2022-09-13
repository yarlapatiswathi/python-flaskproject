from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)
app.config['SECRET_KEY']='firstsecretkey'
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database//cjflasksql.db'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://admin:admin@localhost:5432/flaskpostgres'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']='kabirdas64@gmail.com'
app.config['MAIL_PASSWORD']='eaxkkdmrygmrzrkf'
mail=Mail(app)
from project import route