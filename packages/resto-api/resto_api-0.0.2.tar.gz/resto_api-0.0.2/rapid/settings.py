"""
rapid - settings.py

Default configuration connect to local docker resto endpoint 

Note that all variables can be superseeded with environnement variables with the same name

Copyright 2023 Jerome Gasperi
@author: jerome.gasperi@gmail.com
"""

config = {

    #  =======================
    #  General configuration
    #  =======================
    'RESTO_API_ENDPOINT': 'http://localhost:5252',
    'RESTO_ADMIN_AUTH_TOCKEN': 'eyJzdWIiOiIxMDAiLCJpYXQiOjE3MDIzODg1OTIsImV4cCI6MjU2NjM4ODU5Mn0.qywT1iki4QsgZdPJTO3bWU2GuWTVf6UDs1ztaBodsk8',

    #  =======================
    #  OGC API Processes
    #  =======================

    # Absolute or relative to resto root endpoint
    'RESTO_PROCESS_API_AUTH_TOKEN': 'eyJzdWIiOiIxMDAiLCJpYXQiOjE3MDIzODg1OTIsImV4cCI6MjU2NjM4ODU5Mn0.qywT1iki4QsgZdPJTO3bWU2GuWTVf6UDs1ztaBodsk8',

    # Target S3 bucket configuration to store/provide results - results is local minio
    'RESTO_PROCESS_API_S3_HOST': '',
    'RESTO_PROCESS_API_S3_BUCKET': 'process',
    'RESTO_PROCESS_API_S3_KEY': 'XXXXXXXXXXXXXXXXX',
    'RESTO_PROCESS_API_S3_SECRET': 'YYYYYYYYYYYYYY',
    'RESTO_PROCESS_API_S3_REGION': 'eu-central-1'

}

