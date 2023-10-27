import json
from functools import wraps
from flask import Flask, render_template, redirect, session

import auth
from auth import auth_bp

app = Flask(__name__)

app.config.from_file("config.json", load=json.load)

# Core blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")


# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in", False):
            return auth.login()
        else:
            return f(*args, **kwargs)
    return decorated_function


# Routes
@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/private')
@login_required
def private():
    return render_template("private.html")


if __name__ == '__main__':
    app.run()
