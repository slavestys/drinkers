import os
import logging.config

import redis

from lib.yaml_extended import YamlExtended


class Application:
    root_path = os.path.dirname(__file__) + '/'
    config_path = root_path + 'config/'
    config = None
    redis = None

    @classmethod
    def load_config(cls):
        conf_name = '{0}.yml'.format(os.environ.get('APP_ENV') or 'application')
        cls.config = YamlExtended.load(conf_name, cls.config_path)

    @classmethod
    def port(cls):
        return cls.config['port']

    @classmethod
    def init(cls):
        if cls.config:
            return
        cls.load_config()
        redis_conf = cls.config['redis']
        cls.redis = redis.StrictRedis(host=redis_conf['host'], port=redis_conf['port'], db=redis_conf['db'])
        logging.config.dictConfig(Application.config['logger'])