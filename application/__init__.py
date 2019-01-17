from flask import Flask
from application.routes.route import user_blueprint
from application.routes.auth import auth_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(auth_blueprint)