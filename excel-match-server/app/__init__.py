from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from . import routes
    app.register_blueprint(routes.bp)
    CORS(app)

    return app
