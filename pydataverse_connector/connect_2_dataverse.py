import msal
import requests
import json
import urllib.parse


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
                'If-Match': '*',
                'Content-Type':  'application/json',
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
        return self.__session.get(url=self.__api_url)

    def get_session_content(self) -> json:
        """

        :return:
        """
        return json.loads(self.get_session().content.decode('utf-8'))

    def get_data(self, entity: str, top: int = None, columns: list = None, filters: dict = None) -> json:
        """

        :param entity:
        :param top:
        :param columns:
        :param filters:
        :return:
        """

        top_data = f'?$top={top}' if top else ''
        columns_data = f"{('&' if top else '?')}$select={''.join([f'{col},' for col in columns])[:-1]}" if columns \
            else ''

        if filters:
            if not all(isinstance(value, tuple) for value in filters.values()):
                raise ValueError("All values in filters dicionary needs to be tuples")

            filter_list = []
            allowed_operators = {"eq", "ne", "gt", "ge", "lt", "le"}

            for column, (operator, value) in filters.items():
                operator = operator if operator in allowed_operators else "eq"
                filter_ = f"{column} {operator} {urllib.parse.quote(str(value))}"
                filter_list.append(filter_)

            filter_data = f"{('&' if top or columns else '?')}$filter=" + " and ".join(filter_list)

        else:
            filter_data = ''

        query = f'{self.__api_url}{entity}{top_data}{columns_data}{filter_data}'.strip()

        print(f'"{query}"', '\n\n')

        return json.loads(self.__session.get(url=query).content.decode('utf-8'))

    def update_data(self, entity: str, filter_value: str, update_data: dict, filter_name: str = None, **kwargs):
        """

        :param entity:
        :param filter_name:
        :param filter_value:
        :param update_data:
        :return:
        """
        name = f'{filter_name}=' if filter_name else ''
        query = f'{self.__api_url}{entity}({name}{filter_value})'.strip()

        if update_data:
            print(f'updating element ({name}{filter_value}) from {entity} with data:\n{update_data}'.strip())

            return self.__session.patch(url=query, json=update_data, **kwargs)

        else:
            raise ValueError("Update data cannot be empty!")
