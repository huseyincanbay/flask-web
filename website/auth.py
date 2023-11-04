from flask import Blueprint


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'My Login Page'

@auth.route('/register')
def register():
    return 'my register page'