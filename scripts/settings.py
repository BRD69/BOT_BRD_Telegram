import re
import os.path
import configparser

from config import FILE_CONFIG


class Settings:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self.time = 'null'

    def correct_time(self):
        if self.time == 'null':
            return False
        elif self.time == '':
            return False
        else:
            return True

    def set_time(self, time):
        self.time = time

    def load(self):
        if not os.path.exists(FILE_CONFIG):
            self.save()
        self._config.read(FILE_CONFIG)
        for key, value in self._config[self.__class__.__name__].items():
            setattr(self, key, value)

    def save(self):
        dic_val = {}
        for key, item in self.__dict__.items():
            if not "_" in key:
                dic_val[key] = item

        self._config[self.__class__.__name__] = dic_val
        with open(FILE_CONFIG, 'w') as file:
            self._config.write(file)
        file.close()


def set_time_send_message(text):
    result = re.search(r'[0,2][0-9]:[0-5][0-9]', text)
    if result is None:
        result_none = re.search(r'[0-9]*:[0-9]*', text)
        if result_none is None:
            return {'status': 'error', 'text': 'Не корректное время'}
        else:
            return {'status': 'error', 'text': f"Ошибка установки времени. {result_none.group(0)}"}

    time_str = result.group(0)

    settings = Settings()
    settings.set_time(time_str)
    settings.save()

    return {'status': 'ok', 'text': time_str}
