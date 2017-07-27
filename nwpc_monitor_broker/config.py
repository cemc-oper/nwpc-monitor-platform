"""
config.py

use environment var
"""
import os
import sys
import yaml


class Config(object):
    def __init__(self, config_path):
        with open(config_path) as config_file:
            config_dict = yaml.load(config_file)
            broker_config = config_dict['broker']
            self.BROKER_CONFIG = broker_config

            if 'debug' in broker_config:
                debug_config = broker_config['debug']
                if 'flask_debug' in debug_config:
                    flask_debug = debug_config['flask_debug']
                    if flask_debug is True:
                        self.DEBUG = True
                    elif flask_debug is not True:
                        self.DEBUG = False

            if 'mysql' in broker_config:
                mysql_config = broker_config['mysql']

                mysql_host = mysql_config['host']
                mysql_ip = mysql_host['ip']
                mysql_port = mysql_host['port']
                mysql_user = mysql_config['user']
                mysql_password = mysql_config['password']
                mysql_database = mysql_config['database']
                mysql_charset = mysql_config['charset']

                pool_recycle = mysql_config['pool_recycle']

                self.SQLALCHEMY_DATABASE_URI = \
                    "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
                        user=mysql_user,
                        password=mysql_password,
                        host=mysql_ip,
                        port=mysql_port,
                        database=mysql_database,
                        charset=mysql_charset
                    )

                self.SQLALCHEMY_POOL_RECYCLE = pool_recycle


def load_config():
    if 'NWPC_MONITOR_BROKER_CONFIG' not in os.environ:
        return None

    config_file_path = os.environ['NWPC_MONITOR_BROKER_CONFIG']
    print("config file path:", config_file_path)

    config_object = Config(config_file_path)

    return config_object
