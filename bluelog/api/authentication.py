# by sunnyseed
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import Admin #ss: for bluelog
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username,password):
    if password == '':
        return False
    # 只有一个admin
    admin = Admin.query.first()
    g.current_user = admin
    return admin.validate_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

"""
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')
"""