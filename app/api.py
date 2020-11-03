import random
from threading import Event, Thread, Lock

from flask import redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

from app import app, sio, db
from app.oauth import ProviderFabric
from app.models import User


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/api/authorize/<string:provider_name>', methods=['GET'])
def oauth_authorize(provider_name):
    provider = ProviderFabric.get_provider_by_name(provider_name)
    if provider is None:
        return url_for('authorization')

    return provider.authorize()


@app.route('/api/callback/<string:provider_name>', methods=['GET', 'POST'])
def oauth_callback(provider_name):
    provider = ProviderFabric.get_provider_by_name(provider_name)
    if provider is None:
        return redirect(url_for('authorization'))

    oauth_session = provider.callback(request.args.get('code'))
    if oauth_session is None:
        return redirect(url_for('authorization'))

    user_data = provider.get_user_information_by_session(oauth_session)
    if user_data is None:
        return redirect(url_for('authorization'))

    user = User.query.filter_by(
        social_id=user_data['id'],
        social_name=provider.get_provider_name()
    ).first()
    if not user:
        user = User(
            social_id=user_data['id'],
            social_name=provider.get_provider_name(),
            email=user_data['email'],
            login=user_data['login'],
            avatar_url=user_data['avatar_url']
        )
        user.commit_to_db()

    login_user(user, remember=True)
    return redirect(url_for('index'))


lock = Lock()
thread = None
thread_stop_event = None


def get_numbers(user_id):
    user = db.session.query(User).get(user_id)
    while not thread_stop_event.isSet():
        number = random.randint(1, 100)
        user.add_number(number)
        sio.emit('new_number', number)
        sio.sleep(5)


@sio.on('connect')
def connect():
    global thread, thread_stop_event
    thread_stop_event = Event()

    with lock:
        if thread is None:
            thread = Thread(target=get_numbers, args=(current_user.id,))
            thread.daemon = True
            thread.start()


@sio.on('disconnect')
def disconnect():
    global thread, thread_stop_event
    with lock:
        thread_stop_event.set()
        thread = None
