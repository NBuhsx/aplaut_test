import json
import logging
import uuid
from urllib import parse
from curl_cffi import requests
from cfg import Cfg
from loggs import ParserLogger

class BanExc(Exception):
    pass

class Ozon:
    base_url = 'https://api.ozon.ru'
    reviews_url = '/composer-api.bx/page/json/v2?url=/products/{}/review/list'

    def __init__(self, config: Cfg):
        self.config = config
        self.log = logging.getLogger(__name__)
        self.set_session()

    def set_session(self):
        try:
            self.session = requests.Session()
            self.session.headers.update(self.config['requests']['headers'])
            self.session.headers.update({'MOBILE-GAID': str(uuid.uuid4())})
            self.log.info('Пробую установить сессию')
            r = self.session.post('https://api.ozon.ru/composer-api.bx/_action/initAuth',
                                       json={"clientId": "androidapp"})
            if r.status_code == 200:
                jsn = None
                try:
                    self.log.info('Получены токены при установки сессии ' + str(r.json()['authToken']))
                    jsn = r.json()
                    self.session.headers['Authorization'] = 'Bearer ' + jsn['authToken']["accessToken"]
                except:
                    self.log.error('Неудачная установка сессии при инициализации и получении токенов,'
                                   ' код ответа {} текст {} json {}'.format(str(r.status_code), r.text, jsn))
                    raise BanExc
            else:
                self.log.error('Неудачная установка сессии при инициализации и получении токенов,'
                               ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                raise BanExc
            r = self.session.get('https://api.ozon.ru/composer-api.bx/_action/getMobileConfigs')
            if r.status_code == 200:
                self.log.info('Получена мобильная конфигурация при установки сессии ' + str(r.status_code))
            else:
                self.log.error('Неудачная установка сессии при получении мобильной конфигурации,'
                               ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                raise BanExc
            r = self.session.get('https://api.ozon.ru/composer-api.bx/_action/get3rdPartyConfig')
            if r.status_code == 200:
                self.log.info('Получен 3rdPartyConfig при установки сессии ' + str(r.status_code))
            else:
                self.log.error('Неудачная получение 3rdPartyConfig,'
                               ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                raise BanExc
            r = self.session.get('https://api.ozon.ru/composer-api.bx/page/json/v2?url=warmup')
            if r.status_code == 200:
                self.log.info('Успешный разогрев при установки сессии ' + str(r.status_code))
            else:
                self.log.error('Неудачная попытка разогрева при установки сессии,'
                               ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                raise BanExc
            r = self.session.get('https://api.ozon.ru/composer-api.bx/_action/getPreferredCDNs')
            if r.status_code == 200:
                self.log.info('Успешный получение PreferredCDNs при установки сессии' + str(r.status_code))
            else:
                self.log.error('Неудачная получение PreferredCDNs при установки сессии,'
                               ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                raise BanExc
            r = self.session.post('https://api.ozon.ru/composer-api.bx/_action/getTabBarConfig',
                                       json={"miniapp": "main"})
            if r.status_code == 200:
                self.log.info('Успешный получение TabBarConfig при установки сессии' + str(r.status_code))
            else:
                self.log.error('Неудачная получение TabBarConfig при установки сессии,'
                               ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                raise BanExc
            r = self.session.get('https://api.ozon.ru/composer-api.bx/_action/summary')
            if r.status_code == 200:
                self.log.info('Успешный получение summary при установки сессии' + str(r.status_code))
            else:
                self.log.error('Неудачная получение summary при установки сессии,'
                               ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                raise BanExc
            r = self.session.get('https://api.ozon.ru/composer-api.bx/page/json/v2?url=/home?anchor=true')
            if r.status_code == 200:
                try:
                    self.log.info('При переходе на стартовую страницу параметры ' + str(r.json()['browser']))
                    self.log.info('Внешний IP ' + r.json()['browser']['ip'])
                except:
                    self.log.error('Неудачная установка сессии при переходе на стартовую страницу,'
                                   ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                    raise BanExc
            else:
                self.log.error('Неудачная установка сессии при переходе на стартовую страницу,'
                               ' код ответа {} текст {}'.format(str(r.status_code), r.text))
                raise BanExc
            r = self.session.post('https://api.ozon.ru/composer-api.bx/_action/setBirthdate',
                                       json={"link": "/", "birthdate": "1994-01-01"})
            if r.status_code == 200:
                self.log.info('Установлен возраст 18+ ' + str(r.status_code))
            else:
                self.log.error('Неудачная установка возраста')
                raise BanExc
            self.log.info('Сессия успешно установлена')
        except Exception as e:
            raise e

    def parse_url(self, url):
        r = self.session.get(parse.urljoin(self.base_url, self.reviews_url.format(self.url)))
        if r and r.status_code == 200:
            response = r.json()
            if response.get('widgetStates'):
                reviews_key = [_ for _ in response['widgetStates'] if 'listReviews' in _]
                if reviews_key:
                    reviews = json.loads(response['widgetStates'][reviews_key[0]])
                    if reviews:
                        for review in reviews.get('reviews', []):
                            rve = Review(review)
    def get_rewiew(self):
        pass

class Review():
    def __init__(self, review: dict):
        pass

if __name__ == '__main__':
    ParserLogger()
    o = Ozon(url='1256117487', config=Cfg().load())
    o.parse()
