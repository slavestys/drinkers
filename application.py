import os

from lib.yaml_extended import YamlExtended


class Application:
    root_path = os.path.dirname(__file__) + '/'
    config_path = root_path + 'config/'
    conf = None

    @staticmethod
    def conf_path_by_name(name):
        return Application.config_path + name

    @staticmethod
    def load_config():
        conf_name = '{0}.yml'.format(os.environ.get('APP_ENV') or 'application')
        Application.config = YamlExtended.load(conf_name, Application.config_path)

    @staticmethod
    def port():
        return Application.config['port']