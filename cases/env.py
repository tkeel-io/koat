# -*- coding: utf-8 -*-
''' get env config from .env '''

import os


host = os.getenv('HOST')
port = os.getenv('PORT')
admin_password = os.getenv('ADMIN_PASSWORD')


tenant_id = os.getenv('TENANT_ID')
tenant_user = os.getenv('TENANT_USER')
tenant_password = os.getenv('TENANT_PASSWORD')


url = f'http://{host}:{port}'