from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
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
ma = Marshmallow(app)

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
    __tablename__ = 'timer'
    id = db.Column(db.Integer, primary_key = True)
    timpestamp = db.Column(db.String)

    def __init__(self, timestamp):
        self.timestamp= timestamp

    def __repr__(self):
        return '<User %r>' &self.timestamp

class Dostawca(db.Model):
    _tablename_='Dostawca'
    id = db.Column(db.Integer, primary_key=True)
    stan = db.Column(db.String(120))
    strumien_ogrzanej_wody_Fzm = db.Column(db.String(80))
    temp_wody_zasil_Tzm = db.Column(db.String(80))
    temp_zewn_To = db.Column(db.String(80))
    awaria = db.Column(db.Boolean)
    timestamp = db.Column(db.String(80))

    def __init__(self, stan, strumien_ogrzanej_wody_Fzm, temp_wody_zasil_Tzm, temp_zewn_To, awaria, timestamp):
        self.stan = stan
        self.strumien_ogrzanej_wody_Fzm = strumien_ogrzanej_wody_Fzm
        self.temp_wody_zasil_Tzm = temp_wody_zasil_Tzm
        self.temp_zewn_To = temp_zewn_To
        self.awaria = awaria
        self.timestamp = timestamp

class Regulator(db.Model):
    _tablename_='Regulator'
    id = db.Column(db.Integer, primary_key=True)
    stan = db.Column(db.String(120))
    temp_wody_wpływającej_Tzco = db.Column(db.String(80))
    temp_zadana_Tzcoref = db.Column(db.String(80))
    zawór = db.Column(db.String(20))
    timestamp = db.Column(db.String(80))

    def __init__(self, stan, temp_wody_wpływającej_Tzco, temp_zadana_Tzcoref, zawór, timestamp):
        self.stan = stan
        self.temp_wody_wpływającej_Tzco = temp_wody_wpływającej_Tzco
        self.temp_zadana_Tzcoref = temp_zadana_Tzcoref
        self.zawór = zawór
        self.timestamp = timestamp

class RegSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("stan", "temp_wody_wpływającej_Tzco", "temp_zadana_Tzcoref", "zawór", "timestamp")

reg_schema = RegSchema()
regs_schema = RegSchema(many=True)

class Wymiennik(db.Model):
    _tablename_='Wymiennik'
    id = db.Column(db.Integer, primary_key=True)
    stan = db.Column(db.String(120))
    timestamp = db.Column(db.String(80))
    
    def __init__(self, stan, timestamp):
        self.stan = stan
        self.timestamp = timestamp

class Budynek1(db.Model):
    _tablename_='Budynek1'
    id = db.Column(db.Integer, primary_key=True)
    stan = db.Column(db.String(120))
    pobór_wody_Fcob = db.Column(db.String(80))
    temp_powrotna_Tpcob = db.Column(db.String(80))
    temp_kaloryferow_Th = db.Column(db.String(80))
    temp_pomieszczen_Tr = db.Column(db.String(80))
    timestamp = db.Column(db.String(80))

    def __init__(self, stan, pobór_wody_Fcob, temp_powrotna_Tpcob, temp_kaloryferow_Th, temp_pomieszczen_Tr, timestamp):
        self.stan = stan
        self.pobór_wody_Fcob = pobór_wody_Fcob
        self.temp_powrotna_Tpcob = temp_powrotna_Tpcob
        self.temp_kaloryferow_Th = temp_kaloryferow_Th
        self.temp_pomieszczen_Tr = temp_pomieszczen_Tr
        self.timestamp = timestamp

#-----------------------------------------------------------------------
#                             ROUTING
#-----------------------------------------------------------------------
@app.route('/')
def index():
    return "<h1 style='color': red'>Database!</h1>"

#----------------------------- USER --------------------------
# @app.route('/post_user', methods=['POST'])
# def post_user():
#     username = request.json['username']
#     email = request.json['email']
#     new_user = User(username, email)
#     db.session.add(new_user)
#     db.session.commit()
#     return ("The new user was added!")

# @app.route("/user", methods=["GET"])
# def get_user():
#     all_users = User.query.all()
#     result = users_schema.dump(all_users)
#     return jsonify(result)

# @app.route("/user/<id>", methods=["GET"])
# def user_detail(id):
#     user = User.query.get(id)
#     return user_schema.dump(user)

# ----------------------- LOGGING_ALL ----------------------------------
# @app.route('/log_all', methods=['POST'])
# def log_all():
#     # service_id = request.json['service_id']
#     info_type = request.json['info_type']
#     content = request.json['content']
#     time_stamp = request.json['time_stamp']

#     new_log_all = LogsAll(info_type, content, time_stamp)
#     db.session.add(new_log_all)
#     db.session.commit()
#     return ("New log was received and worte to database")

# ----------------------- REGULATOR ----------------------------------
@app.route('/regulator/log', methods=['POST'])
def log_regulator():
    stan = request.json['stan']
    temp_wody_wpływającej_Tzco = request.json['temp_wody_wpływającej_Tzco']
    temp_zadana_Tzcoref = request.json['temp_zadana_Tzcoref']
    zawór = request.json['zawór']
    timestamp = request.json['timestamp']

    new_log_reg = Regulator(stan, temp_wody_wpływającej_Tzco, temp_zadana_Tzcoref, zawór, timestamp)
    db.session.add(new_log_reg)
    db.session.commit()
    return ("New log of regulator was received and worte to database")

@app.route("/regulator", methods=["GET"])   #get all data
def get_reg():
    all_regs = Regulator.query.all()
    result = regs_schema.dump(all_regs)
    return jsonify(result)

@app.route("/regulator/id/<id>", methods=["GET"])   #get id
def get_regId(id):
    reg = Regulator.query.get(id)
    return reg_schema.jsonify(reg)

@app.route("/regulator/last/<num>", methods=["GET"])   #get last x records
def get_regLast(num):
    records = Regulator.query.filter().order_by(Regulator.id.desc()).limit(num).all()
    result = regs_schema.dump(records)
    return jsonify(result)



if __name__ == '__main__':
    app.run()