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

class Provider(db.Model):
    _tablename_='Provider'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120))
    warm_water_stream_Fzm = db.Column(db.String(80))
    incoming_water_temp_Tzm = db.Column(db.String(80))
    outside_temp_To = db.Column(db.String(80))
    failure = db.Column(db.String(20))
    timestamp = db.Column(db.String(80))

    def __init__(self, status, warm_water_stream_Fzm, incoming_water_temp_Tzm, outside_temp_To, failure, timestamp):
        self.status = status
        self.warm_water_stream_Fzm = warm_water_stream_Fzm
        self.incoming_water_temp_Tzm = incoming_water_temp_Tzm
        self.outside_temp_To = outside_temp_To
        self.failure = failure
        self.timestamp = timestamp

class ProvSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("status", "warm_water_stream_Fzm", "incoming_water_temp_Tzm", "outside_temp_To", "failure", "timestamp")

prov_schema = ProvSchema()
provs_schema = ProvSchema(many=True)

class Controler(db.Model):
    _tablename_='Controler'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120))
    incoming_water_temp_Tzco = db.Column(db.String(80))
    set_temp_Tzcoref = db.Column(db.String(80))
    valve = db.Column(db.String(20))
    timestamp = db.Column(db.String(80))

    def __init__(self, status, incoming_water_temp_Tzco, set_temp_Tzcoref, valve, timestamp):
        self.status = status
        self.incoming_water_temp_Tzco = incoming_water_temp_Tzco
        self.set_temp_Tzcoref = set_temp_Tzcoref
        self.valve = valve
        self.timestamp = timestamp

class ControlSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("status", "incoming_water_temp_Tzco", "set_temp_Tzcoref", "valve", "timestamp")

control_schema = ControlSchema()
controls_schema = ControlSchema(many=True)

class Wymiennik(db.Model):
    _tablename_='Wymiennik'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120))
    timestamp = db.Column(db.String(80))
    
    def __init__(self, status, timestamp):
        self.status = status
        self.timestamp = timestamp

class Building(db.Model):
    _tablename_='Building'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120))
    tag_name = db.Column(db.String(200))
    pobór_wody_Fcob = db.Column(db.String(80))
    temp_powrotna_Tpcob = db.Column(db.String(80))
    radiator_temp_Th = db.Column(db.String(80))
    temp_pomieszczen_Tr = db.Column(db.String(80))
    timestamp = db.Column(db.String(80))

    def __init__(self, status, tag_name, water_intake_Fcob, return_water_temp_Tpcob, radiator_temp_Th, room_temp_Tr, timestamp):
        self.status = status
        self.tag_name=tag_name
        self.water_intake_Fcob = water_intake_Fcob
        self.return_water_temp_Tpcob = return_water_temp_Tpcob
        self.radiator_temp_Th = radiator_temp_Th
        self.room_temp_Tr = room_temp_Tr
        self.timestamp = timestamp

#-----------------------------------------------------------------------
#                             ROUTING
#-----------------------------------------------------------------------
@app.route('/')
def index():
    return "<h1 style='color': red'>Database!</h1>"

# ----------------------- CONTROLER ----------------------------------
@app.route('/controler/log', methods=['POST'])
def log_controler():
    status = request.json['status']
    incoming_water_temp_Tzco = request.json['incoming_water_temp_Tzco']
    set_temp_Tzcoref = request.json['set_temp_Tzcoref']
    valve = request.json['valve']
    timestamp = request.json['timestamp']

    new_log_cont = Controler(status, incoming_water_temp_Tzco, set_temp_Tzcoref, valve, timestamp)
    db.session.add(new_log_cont)
    db.session.commit()
    return ("New log of controler was received and worte to database")

@app.route("/controler", methods=["GET"])   #get all data
def get_cont():
    all_logs = Controler.query.all()
    result = controls_schema.dump(all_logs)
    return jsonify(result)

@app.route("/controler/id/<id>", methods=["GET"])   #get id
def get_regId(id):
    log_id = Controler.query.get(id)
    return control_schema.jsonify(log_id)

@app.route("/controler/last/<num>", methods=["GET"])   #get last x records
def get_regLast(num):
    records = Controler.query.filter().order_by(Controler.id.desc()).limit(num).all()
    result = controls_schema.dump(records)
    return jsonify(result)

# ----------------------- PROVIDER ----------------------------------
@app.route('/provider/log', methods=['POST'])
def log_provider():
    status = request.json['status']
    timestamp = request.json['timestamp']
    warm_water_stream_Fzm = request.json['warm_water_stream_Fzm']
    incoming_water_temp_Tzm = request.json['incoming_water_temp_Tzm']
    outside_temp_To = request.json['outside_temp_To']
    failure = request.json['failure']

    new_log_prov = Provider(status, warm_water_stream_Fzm, incoming_water_temp_Tzm, outside_temp_To, failure, timestamp)
    db.session.add(new_log_prov)
    db.session.commit()
    return ("New log of provider was received and worte to database")

@app.route("/provider", methods=["GET"])   #get all data
def get_prov():
    all_logs = Provider.query.all()
    result = provs_schema.dump(all_logs)
    return jsonify(result)

@app.route("/provider/id/<id>", methods=["GET"])   #get id
def get_provId(id):
    log_id = Provider.query.get(id)
    return prov_schema.jsonify(log_id)

@app.route("/provider/last/<num>", methods=["GET"])   #get last x records
def get_provLast(num):
    records = Provider.query.filter().order_by(Provider.id.desc()).limit(num).all()
    result = provss_schema.dump(records)
    return jsonify(result)



if __name__ == '__main__':
    app.run()