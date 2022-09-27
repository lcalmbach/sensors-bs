"""
This file hosts db acccess information for the test und prod environment
"""
config = 'dev'
db_config_dict = {
    "dev": {
        "DB_USER": "postgres",
        "DB_PASS": 'password',
        "DB_HOST": 'localhost',
        "DB_PORT": 3306,
        "DATABASE": 'opendata'
    },

    "prod": {
        "DB_USER": "root",
        "DB_PASS": 'password',
        "DB_HOST": 'terra-2.cxudpg3pe6ie.us-east-2.rds.amazonaws.com',
        "DB_PORT": 3306,
        "DATABASE": 'traffic'
    }
}

dbcn = db_config_dict[config]
