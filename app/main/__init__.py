from flask import Blueprint

main = Blueprint('main', __name__)

# Flasky does not have forms below
from . import views, errors, forms
