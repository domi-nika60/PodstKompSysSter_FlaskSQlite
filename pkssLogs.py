from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from json import dumps
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# ------------------- Configuration -------------------
POSTGRES = {
    'user': 'pkssAdmin',
    'pw': 'pkssAdmin1',
    'db': 'logs',
    'host': 'logs.cegwdkw512mn.us-east-2.rds.amazonaws.com',
    'port': '5432',
}
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pkssAdmin:pkssAdmin1@logs.cegwdkw512mn.us-east-2.rds.amazonaws.com/logs'
app.debug = True
db = SQLAlchemy(app)
# db.init_app(app) # dla managerów

# -------------------------- Classes with models ----------------------------------
class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class Timer(BaseModel, db.Model):
    """Model for the timers table"""
    __tablename__ = 'timer'

    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.Float)
    log = db.Column(db.Float)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __init__(self, username, email):
        self.username= username
        self.email = email

    def __repr__(self):
        return '<User %r>' &self.username

# class UserSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ('username', 'email')

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

class LogsAll(db.Model):
    _tablename_='Logs_all'
    id = db.Column(db.Integer, primary_key=True)
    info_type = db.Column(db.String(80))
    content = db.Column(db.String(200))
    time_stamp = db.Column(db.String(80))
    # service_id = db.relationship("Regulator", backref="logger")

    def __init__(self, info_type, content, time_stamp):
        # self.service_id = service_id
        self.info_type = info_type
        self.content = content
        self.time_stamp = time_stamp

class Regulator(db.Model):
    _tablename_='Regulator'
    id = db.Column(db.Integer, primary_key=True)
    temp_zewn = db.Column(db.String(80))
    zmiana_stanu = db.Column(db.String(120))
    time_stamp = db.Column(db.String(80))
    # logger_id = db.Column(db.Integer, db.ForeignKey('logsall.id'))

    def __init__(self, temp_zewn, zmiana_stanu, time_stamp):
        self.temp_zewn = temp_zewn
        self.zmiana_stanu = zmiana_stanu
        self.time_stamp = time_stamp
        # self.logger_id = logger_id

#-----------------------------------------------------------------------
#                             ROUTING
#-----------------------------------------------------------------------
@app.route('/')
def index():
    return "<h1 style='color': red'>hello flask with postgresql</h1>"

ma = Marshmallow(app)

#----------------------------- USER --------------------------
@app.route('/post_user', methods=['POST'])
def post_user():
    username = request.json['username']
    email = request.json['email']
    new_user = User(username, email)
    db.session.add(new_user)
    db.session.commit()
    return ("The new user was added!")

@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.dump(user)

# ----------------------- LOGGING_ALL ----------------------------------
@app.route('/log_all', methods=['POST'])
def log_all():
    # service_id = request.json['service_id']
    info_type = request.json['info_type']
    content = request.json['content']
    time_stamp = request.json['time_stamp']

    new_log_all = LogsAll(info_type, content, time_stamp)
    db.session.add(new_log_all)
    db.session.commit()
    return ("New log was received and worte to database")

# ----------------------- REGULATOR ----------------------------------
@app.route('/regulator/log', methods=['POST'])
def log_regulator():
    temp_zewn = request.json['temp_zewn']
    zmiana_stanu = request.json['zmiana_stanu']
    time_stamp = request.json['time_stamp']

    new_log_reg = LOGS_ALL(temp_zewn, zmiana_stanu, time_stamp)
    db.session.add(new_log_reg)
    db.session.commit()
    return ("New log of regulator was received and worte to database")

if __name__ == '__main__':
    app.run()