from flask import Flask, render_template
from . import todo
from . import auth

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev'
    )

    # Registrar el blueprint
    app.register_blueprint(todo.bp)

    app.register_blueprint(auth.bp)
    
    @app.route("/")
    def index():
        return render_template('index.html')
    
    return app