from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager




app = Flask(__name__)

app.secret_key = "\xbe\x10\xbf'\xb5\xdb\x9ahG\x10\xc7\xf5\x8e\xb8\xe94"

# ket noi mysql
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345678@localhost/lapdb?charset=utf8mb4"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="Laptop", template_mode="bootstrap3")

login = LoginManager(app=app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thuthaokg1999@gmail.com'
app.config['MAIL_PASSWORD'] = 'ecdmynofvenzmcgh'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



