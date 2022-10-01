import os
import socket

"""
This file hosts db acccess information for the test und prod environment
"""

config = 'dev' if socket.gethostname().lower() == 'liestal' else 'prod'
db_config_dict = {
    "dev": {
        "DB_USER": "postgres",
        "DB_PASS": 'password',
        "DB_HOST": 'localhost',
        "DB_PORT": 5432,
        "DATABASE": 'opendata'
    },

    "prod": {
        "DB_USER": os.environ.get('DB_USER'),
        "DB_PASS": os.environ.get('DB_PASS'),
        "DB_HOST": os.environ.get('DB_HOST'),
        "DB_PORT": os.environ.get('DB_PORT'),
        "DATABASE": os.environ.get('DATABASE'),
    }
}

dbcn = db_config_dict[config]
