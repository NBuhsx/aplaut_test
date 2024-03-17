import uuid
import asyncio
import logging
from curl_cffi import requests



class Base:
    url = 'https://api.ozon.ru'

    def __init__(self, config: Cfg):
        self.config = config
        self.log = logging.getLogger(__name__)


    def msg(self, status, message):
        return {
            "info": self.log.info,
            "erro": self.log.error
        }[status](message)

    async def request(self, session: request.AsyncSession, kwargs):
        return await session.request(**kwargs)


class Session(Base):
    def __init__(self, config: Cfg):
        super().__init__(config)

        self.session = requests.AsyncSession(
            headers=self.config.get('requests', {}).get('headers', {}).update({
                'MOBILE-GAID': str(uuid.uuid4())})
        )

    def check():
        return r.status_code == 200

    def step_request_1(self):
        self.log.info('Пробую установить сессию')
        return 

    def step_response_1(self, response):
        try:
            self.log.info('Получены токены при установки сессии ' +
                          str(r.json()['authToken']))
            jsn = response.json()
            self.session.headers['Authorization'] = 'Bearer ' + \
                jsn['authToken']["accessToken"]
        except:
            self.log.error(
                'Неудачная установка сессии при инициализации и получении токенов,'
                ' код ответа {} текст {} json {}'.format(response.status_code, response.text, jsn))



    def steps(self):
        return [
            dict(
                request=dict(
                    ulr='https://api.ozon.ru/composer-api.bx/_action/initAuth',
                    json={"clientId": "androidapp"}
                ),
                log=dict(
                    status="info",
                    message="Пробую установить сессию"
                ),
                error='Неудачная установка сессии при инициализации и получении токенов'
            ),
            dict(
                request=dict(
                    url='https://api.ozon.ru/composer-api.bx/_action/getMobileConfigs'
                ),
                log=dict(
                    status="info",
                    message="Что-то получаем"
                ),
                error='Неудачная установка сессии при инициализации и получении токенов'
            )
        ]


    async def get_session(self):
        try: 
            await self.auth()
        except Exception as error:
            self.msg("error", error)
            await asyncio.sleep(30)
        
    async def auth(self):
        try:
            if response := await self.request(self.session, self.step_request_1()):
                self.step_response_1(response)
                for step in self.steps[1:]:
                    self.msg(step.get("log"))
                    if self.check(
                        (await self.request(self.session, step.get('request')))):
                    else:
                        self.msg(step.get("error", step.get("error")))
                        return
                self.msg("info", "Сессия готова") 
        except:
            self.msg("error", step.get('error'))


class Review():
    def __init__(self, review: dict):
        pass
