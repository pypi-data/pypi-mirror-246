from setuptools import setup, find_packages

setup(
    name='azucar_web_driver',  # Nombre de tu paquete
    version='0.1',      # Versión inicial del paquete
    packages=find_packages(),  # Encuentra automáticamente todos los paquetes
    description='Automatización de navegadores con Selenium',  # Una breve descripción
    long_description=open('README.md').read(),  # Descripción larga, típicamente de un README
    long_description_content_type='text/markdown',  # Tipo de contenido de la descripción larga
    install_requires=[   # Lista de dependencias necesarias para usar tu paquete
        'attrs==23.1.0',
        'certifi==2023.11.17',
        'cffi==1.16.0',
        'charset-normalizer==3.3.2',
        'exceptiongroup==1.2.0',
        'h11==0.14.0',
        'idna==3.6',
        'outcome==1.3.0.post0',
        'packaging==23.2',
        'pycparser==2.21',
        'PySocks==1.7.1',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'selenium==4.16.0',
        'sniffio==1.3.0',
        'sortedcontainers==2.4.0',
        'trio==0.23.2',
        'trio-websocket==0.11.1',
        'urllib3==2.1.0',
        'webdriver-manager==4.0.1',
        'wsproto==1.2.0'
    ],
    # Incluye cualquier otro parámetro relevante como author, author_email, url, etc.
)
