import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = '3mpc3o48nc3m*(Y#N8c20873nx82374xn2339b&'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OAUTHS = {
        'github': {
            'client_id': '58a2b5337775fd6cf570',  # The client secret received from GitHub
            'client_secret': 'fc64261b062e0be2fbd57d82293e8ae64f921717',  # The client ID received from GitHub
            'authorize_url': 'https://github.com/login/oauth/authorize',  # Url for getting authorization code
            'access_token_url': 'https://github.com/login/oauth/access_token',  # Get access token using auth code
            'request_url': 'https://api.github.com'  # Url for api requests
        }
    }
