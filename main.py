from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from flask_restful import Api, Resource
from bson.json_util import dumps
from json import loads
from datetime import datetime
from flask_mail import Mail, Message
from Keys import Passwords
from flask_cors import CORS
from urllib.parse import quote_plus

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb+srv://{quote_plus('kkhafflick13')}:{quote_plus(Passwords['MongoDB1'])}@cluster0.cv8aemp.mongodb.net/LOM?retryWrites=true&w=majority"
mongo = PyMongo(app)

CORS(app)
api = Api(app)

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '7460570c1050da'
app.config['MAIL_PASSWORD'] = 'd43d3458a02500'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route("/")
def index():
    msg = Message('Hello from the other side!', sender =   'kkhafflick@hotmail.com', recipients = ['kkhafflick@hotmail.com'])
    msg.body = "Testing...."
    mail.send(msg)
    return "Message sent!"


class DataSchema(Schema): #setting up mongoDB model 
    Temperature = fields.Float(required=True) 
    pH = fields.Float(required=True)
    Viscosity = fields.Integer(required=True)
    Opacity = fields.Integer(required=True)
    last_updated = fields.String(required=True)
    Time = fields.Float(required=True)


class ThresholdSchema(Schema):
    tempMin = fields.Integer(required=True)
    tempMax = fields.Integer(required=True)
    opacityMin = fields.Integer(required=True)
    opacityMax = fields.Integer(required=True)
    viscosityMin = fields.Integer(required=True)
    viscosityMax = fields.Integer(required=True)
    pHMin = fields.Float(required=True)
    pHMax = fields.Float(required=True)




@app.route("/Home", )
def home_page():
    record = mongo.db.parameters.find({"pH": 8})
    return dumps(list(record))

# def compare(post_data):
#     Threshold = mongo.db.thresholds.find_one({"setting":"thresholds"})
#     comparison = {}

#     if (post_data["pH"] > Threshold["pHMax"]):
#         comparison["HIGHpH"] = True
#     if (post_data["pH"] < Threshold["pHMin"]):
#         comparison["LOWpH"] = True

#     if (post_data["Temperature"] > Threshold["TempMax"]):
#         comparison["HIGHTemp"] = True
#     if (post_data["Temperature"] < Threshold["TempMin"]):
#         comparison["LOWTemp"] = True
        
#     if (post_data["Opacity"] > Threshold["opacityMax"]):
#         comparison["HIGHOpacity"] = True
#     if (post_data["Opacity"] < Threshold["opacityMin"]):
#         comparison["LOWOpacity"] = True

#     if (post_data["Viscosity"] > Threshold["viscosityMax"]):
#         comparison["HIGHViscosity"] = True
#     if (post_data["Viscosity"] < Threshold["viscosityMin"]):
#         comparison["LOWViscosity"] = True
    
#     msg = Message('Threshold Exceeded', sender='sender@example.com', recipients=['recipient@example.com'])
#     msg.body = ""

#     if (comparison.get("HIGHTemp") or comparison.get("LOWTemp")):
#         msg.body += f'Check temp'

#     if (comparison.get("HIGHpH") or comparison.get("LOWpH")):
#         msg.body += f'Check pH'

#     if (comparison.get("HIGHOpacity") or comparison.get("LOWOpacity")):
#         msg.body += f'Check Opacity'
    
#     if (comparison.get("HIGHViscosity") or comparison.get("LOWViscosity")):
#         msg.body += f'Check Viscosity'

#     if not (msg.body == ""):    
#         mail.send(msg)


class Data(Resource): 
    def post(self):
        try:
            temperature = request.json["Temp"]
            ph = request.json['pH']
            viscosity = request.json['viscosity']
            opacity = request.json['opacity']
            last_updated = datetime.now().strftime("%c")
            time = datetime.now().strftime("%H:%M:%S")

            newData = {
                'Temperature': temperature,
                'pH': ph,
                'Viscosity': viscosity,
                'Opacity': opacity,
                'last_updated': last_updated,
                'Time': time
            }
            mongo.db.data.insert_one(newData)

            # compare(newData)

            return {"success": True}
        except ValidationError as err:
            return err.message, 400

    def get(self):
        data = mongo.db.data.find()
        return jsonify(loads(dumps(data)))


class Thresholds(Resource): 
    def post(self):
        try:
            tempMin = request.json["tempMin"]
            tempMax = request.json["tempMax"]
            opacityMin = request.json["opacityMin"]
            opacityMax = request.json["opacityMax"]
            viscosityMin = request.json["viscosityMin"]
            viscosityMax = request.json["viscosityMax"]
            pHMin = request.json["pHMin"]
            pHMax = request.json["pHMax"]

            newThresholds = {
                "setting": "threshold",
                "tempMin": tempMin,
                "tempMax": tempMax,
                "viscosityMin": viscosityMin,
                "viscosityMax": viscosityMax,
                "opacityMin": opacityMin,
                "opacityMax": opacityMax,
                "pHMin": pHMin,
                "pHMax": pHMax,
            }
            mongo.db.thresholds.update_one({"setting": "threshold"}, {"$set": newThresholds})
            return {"success": True}
        except ValidationError as err:
            return err.message, 400
        
    def get(self):
        thresholds = mongo.db.thresholds.find()
        return jsonify(loads(dumps(thresholds)))

api.add_resource(Data, '/data')
api.add_resource(Thresholds, '/thresholds')




if __name__ == '__main__':
    app.run(
        debug=False,
        port=10000,
        host="0.0.0.0"
    )