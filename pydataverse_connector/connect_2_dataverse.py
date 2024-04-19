import msal
import requests
import json

MS_BASE_LOGIN_URL = 'https://login.microsoftonline.com/'


class ConnectDataverse:

    def __init__(self, environment_uri: str, client_id: str, tenant_id: str, scope: str = 'user_impersonation'):
        """

        :param environment_uri:
        :param client_id:
        :param tenant_id:
        :param scope:
        """

        # MS Auth params
        self.__environment_uri = environment_uri
        self.__client_id = client_id
        self.__authority = MS_BASE_LOGIN_URL + tenant_id
        self.__scope = [f'{environment_uri}/{scope}']
        self.__api_url = f'{self.__environment_uri}/api/data/v9.2/'

        # Session
        self.__app = msal.PublicClientApplication(client_id=self.__client_id, authority=self.__authority)
        self.__result = self.__app.acquire_token_interactive(scopes=self.__scope)

        if 'access_token' in self.__result:

            print('Token generated...')

            auth_token = self.__result['access_token']

            dataverse_api_headers = {
                'OData-MaxVersion': '4.0',
                'OData-Version': '4.0',
                'If-None-Match': 'null',
                'Accept': 'application/json'
            }

            self.__session = requests.Session()
            self.__session.headers.update(dict(Authorization=f'Bearer {auth_token}'))
            self.__session.headers.update(dataverse_api_headers)

        else:
            raise self.__session.get('error')

    def get_session(self):
        """

        :return:
        """
        return self.__session.get(self.__api_url)

    def get_session_content(self):
        """

        :return:
        """
        return self.get_session().content.decode('utf-8')

    def get_data(self, entity: str, top: int = None):
        """

        :param entity:
        :param top:
        :return:
        """
        top_data = f'?$top={top}' if top else ''
        query = f'{self.__api_url}{entity}{top_data}'.strip()

        return json.loads(self.__session.get(query).content.decode('utf-8'))
