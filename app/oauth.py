from flask import current_app
from rauth import OAuth2Service


class ProviderFabric:
    __providers = None

    @classmethod
    def __create_providers(cls):
        for providerClass in Provider.__subclasses__():
            provider = providerClass()
            cls.__providers[provider.get_provider_name()] = provider

    @classmethod
    def get_provider_by_name(cls, provider_name):
        if provider_name not in current_app.config['OAUTHS']:
            return None

        if cls.__providers is None:
            cls.__providers = {}
            cls.__create_providers()

        return cls.__providers.get(provider_name)


class Provider:
    def authorize(self):
        pass

    def callback(self, code):
        pass

    def get_provider_name(self):
        pass


class GitHubProvider(Provider):
    def __init__(self):
        super().__init__()
        self.__provider_name = 'github'
        self.__settings = current_app.config['OAUTHS']['github']
        self.__service = OAuth2Service(
            client_id=self.__settings['client_id'],
            client_secret=self.__settings['client_secret'],
            authorize_url=self.__settings['authorize_url'],
            access_token_url=self.__settings['access_token_url']
        )

    def authorize(self):
        return self.__service.get_authorize_url()

    def callback(self, code):
        def new_decoder(payload):
            return dict(tuple(data.split('=')) for data in payload.decode('utf-8').split('&'))

        if code is None:
            return None

        oauth_session = self.__service.get_auth_session(
            data={'code': code},
            decoder=new_decoder
        )

        return oauth_session

    def get_user_information_by_session(self, oauth_session):
        return oauth_session.get(self.__settings['request_url'] + '/user').json()

    def get_provider_name(self):
        return self.__provider_name
