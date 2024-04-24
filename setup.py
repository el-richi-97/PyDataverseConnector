from setuptools import setup, find_packages

setup(
    name='pydataverse_connector',  # Nombre del proyecto
    version='0.1a1',  # Versión del proyecto
    packages=find_packages(),  # Encuentra automáticamente los paquetes a incluir
    install_requires=[
        'msal==1.28.0',  # Dependencia MSAL
        'requests==2.31.0',  # Dependencia Requests
        'python-dotenv==1.0.1',  # Dependencia python-dotenv
    ],
    author='Ricardo Quintana',  # Nombre del autor o autores
    author_email='ricardoquintana117@gmail.com',  # Email del autor o autores
    description='Una librería para conectar con Dataverse',  # Descripción del proyecto
    long_description=open('README.md').read(),  # Descripción larga del proyecto (generalmente desde README.md)
    long_description_content_type='text/markdown',  # Tipo de contenido de la descripción larga
    url='https://github.com/el-richi-97/PyDataverseConnector',  # URL del repositorio del proyecto
    license='MIT',  # Licencia del proyecto
)
