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

    queri1 = dataverse.get_session_content()

    print(queri1)

    # Making a query
    filters = {'cr181_anexosdataid': ('eq', '693c2338-9efc-ee11-a1fe-000d3a494a6e')}
    query = dataverse.get_data(entity='cr181_anexosdatas', filters=filters)

    print('data:')
    for i, data in enumerate(query['value']):
        print(f'{i + 1} -> {data}')

    data_to_update = {'cr181_cnae': r'hello_world_from_PyDataverseConnector'}

    update = dataverse.update_data(
        entity='cr181_anexosdatas',
        filter_name='cr181_anexosdataid',
        filter_value='693c2338-9efc-ee11-a1fe-000d3a494a6e',
        update_data=data_to_update
    )

    print(update.status_code, update.content)

    query2 = dataverse.get_data(entity='cr181_anexosdatas', filters=filters)

    print('updated data:')
    for i, data in enumerate(query2['value']):
        print(f'{i + 1} -> {data}')
