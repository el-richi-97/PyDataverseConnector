from pydataverse_connector.connect_2_dataverse import ConnectDataverse
import os
from dotenv import load_dotenv

# You need to create a .env file in the /tests folder
load_dotenv()

TEST_CLIENT_ID = os.environ.get('TEST_CLIENT_ID')
TEST_TENANT_ID = os.environ.get('TEST_TENANT_ID')
TEST_ENVIRONMENT_URI = os.environ.get('TEST_ENVIRONMENT_URI')


if __name__ == '__main__':

    dataverse = ConnectDataverse(
        client_id=TEST_CLIENT_ID,
        tenant_id=TEST_TENANT_ID,
        environment_uri=TEST_ENVIRONMENT_URI
    )

    # Obtaining session
    session = dataverse.get_session()
    print('Connected' if session.status_code == 200 else 'Connection failed')

    # Obtaining session content
    session_content = dataverse.get_session_content()
    print(f'len: {len(session_content)} // type: {type(session_content)}')

    # Making a query
    query = dataverse.get_data(entity='cr181_anexosdatas', top=50)
    print(query['value'])
