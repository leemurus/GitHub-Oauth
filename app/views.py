from flask import render_template
from flask_login import login_required, current_user

from app import app


@app.route('/authorization', methods=['GET'])
def authorization():
    return render_template('authorization.html')


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template(
        'index.html',
        numbers=current_user.numbers[-min(len(current_user.numbers), 100):],
        email=current_user.email,
        login=current_user.login,
        avatar_url=current_user.avatar_url
    )
