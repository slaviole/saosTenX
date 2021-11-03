from flask import Flask, render_template, session, redirect, url_for, flash # Last 5 not in Flasky?
from flask_bootstrap import Bootstrap
#from flask_wtf import FlaskForm
#from wtforms import IntegerField, StringField, SubmitField, SelectField, PasswordField
#from wtforms.validators import DataRequired, IPAddress, Length, NumberRange
#import os
from flask_sqlalchemy import SQLAlchemy
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

