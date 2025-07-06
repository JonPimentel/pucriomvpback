from flask import Flask
from config import Config
from database import db
from flasgger import Swagger
from routes import routes

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
Swagger(app)

CORS(app)

app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
