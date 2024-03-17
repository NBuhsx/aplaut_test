import os
import json


class ConfigFileError(Exception):
    pass


class Cfg:
    """ Работает с файлом конфигурации в формате JSON"""

    def __init__(self, filepath='config.json'):
        if os.path.isfile(filepath):
            self.filepath = filepath
        else:
            raise ConfigFileError(f'{filepath} отсутствует либо не является файлом!')

    def load(self):
        """ Загружает файл конфигурации """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigFileError(f'{self.filepath} не является json-файлом!')
