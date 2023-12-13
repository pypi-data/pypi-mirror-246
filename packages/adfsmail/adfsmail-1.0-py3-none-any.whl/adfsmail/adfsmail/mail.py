#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created.

@author: gp
"""
import time
import json
import threading
import re
from urllib import parse
from lxml import etree
import requests
from requests_ntlm import HttpNtlmAuth
import websocket
parser = etree.HTMLParser()


# Класс для представления вложения
class Attachment:
    '''
    Класс для взаимодействия с вложениями письма в удобной форме.
    '''

    def __init__(
            self,
            att: dict,
            sess: requests.sessions.Session,
            server: str
            ):
        """
        Объект вложения. Нужен для возможности удобно сохранять вложения.

        Parameters
        ----------
        att : dict
            Словарь с описанием вложения.
        sess : requests.sessions.Session
            Сессия, нужна, чтобы скачать файл.
        server : str
            Адрес почтового сервера.

        Returns
        -------
        None.

        """
        self.att = att
        self._id = self.att.get('AttachmentId').get('Id')
        self.sess = sess
        self.server = server

    def get_filename(self) -> str:
        """
        Метод получения названия вложения.

        Returns
        -------
        str
            Название файла.

        """
        return self.att.get('Name')

    def save(self, f_name: str):
        """
        Метод сохранения вложения.

        Parameters
        ----------
        f_name : str
            Путь, куда сохранять файл.

        Returns
        -------
        None.

        """
        cont = self.sess.get(
            f'https://mail.{self.server}/owa/service.svc/s/GetFileAttachment',
            params={
                'id': self.att.get('AttachmentId').get('Id'),
                'X-OWA-CANARY': self.sess.cookies.get_dict()['X-OWA-CANARY']
                  }
          )
        with open(f_name, 'wb') as file_to_save:
            file_to_save.write(cont.content)


# Класс для представления письма
class EmailMessage:
    '''
    Класс для взаимодействия с письмом в удобной форме.
    '''

    def __init__(
            self,
            raw_message: dict,
            sess: requests.sessions.Session,
            server: str
            ):
        """
        Объект письма. Нужен для возможности удобно работать с письмами.

        Parameters
        ----------
        raw_message : dict
            Словарь с описанием содержимого письма.
        sess : requests.sessions.Session
            Сессия, нужна, чтобы скачать файл.
        server : str
            Адрес почтового сервера.

        Returns
        -------
        None.

        """
        self.message = raw_message
        self.sess = sess
        self.server = server

    def get_from(self) -> dict:
        """
        Метод получения параметров отправителя.

        Returns
        -------
        dict
            Данные отправителя.

        """
        return self.message.get('From')

    def get_to(self) -> list:
        """
        Метод получения параметров получателей.

        Returns
        -------
        list
            Данные получателей.

        """
        return self.message.get('ToRecipients')

    def get_subject(self) -> str:
        """
        Метод получения темы письма.

        Returns
        -------
        str
            Тема письма.

        """
        return self.message.get('Subject')

    def get_body(self) -> str:
        """
        Метод получения содержимого письма.

        Returns
        -------
        str
            Содержимое письма в формате html.

        """
        return self.message.get('UniqueBody').get('Value')

    def get_datetime(self) -> str:
        """
        Метод получения времени получения письма.

        Returns
        -------
        str
            Дата и время получения письма.

        """
        return self.message.get('DateTimeReceived')

    def get_attachments(self) -> list[Attachment]:
        """
        Метод получения объектов вложений.

        Returns
        -------
        attachments : list[Attachment]
            Список объектов Attachment.

        """
        attachments = self.message.get('Attachments')
        attachments = [
            Attachment(x, self.sess, self.server)
            for x in attachments
            ]
        return attachments

    def get_attachments_count(self) -> int:
        """
        Метод получения количества вложений.

        Returns
        -------
        int
            Количество вложений.

        """
        return len(self.message.get('Attachments'))


class AdfsMail:
    '''
    Класс для чтения почты через ВПН.
    '''

    def __init__(self, login: str, password: str, server: str):
        """
        Функция залогирования.

        Parameters
        ----------
        login : str
            Почтовый адрес.
        password : str
            Пароль от почты.
        server : str
            Адрес почтового сервера.

        Returns
        -------
        None.

        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8,application"
            "/signed-exchange;v=b3;q=0.7",
            "Content-Type": "application/json",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/119.0.0.0 Safari/537.36"
            }
        self.login = login
        self.password = password
        self.server = server
        # Создаем сессию, чтобы куки обрабатывались автоматически
        self.sess = requests.Session()
        # При подключении к ВПН у нас в браузере просто надо залогиниться
        _r1 = self.sess.get(
            f'https://mail.{self.server}/owa/#path=/mail',
            # Строка ниже вводит логин и пароль во всплывающем окне браузера
            auth=HttpNtlmAuth(self.login, self.password),
            verify=False,
            headers=headers
            )
        _r1_text = etree.fromstring(_r1.text, parser)
        wresult = _r1_text.xpath('//input[@name="wresult"]/@value')[0]
        wctx = _r1_text.xpath('//input[@name="wctx"]/@value')[0]
        # Далее мы должны отправить этот запрос, чтобы сервер пустил
        _ = self.sess.post(
            f'https://mail.{self.server}/owa/',
            headers={
                "Accept": "text/html,application/xhtml+xml,application"
                "/xml;q=0.9,image/avif,image/webp,image/apng,*/*;"
                "q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Content-Length": "6888",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": f"mail.{self.server}",
                "Origin": f"https://adfs.{self.server}",
                "Referer": f"https://adfs.{self.server}/",
                'Sec-Ch-Ua':
                    '"Google Chrome";v="119", "Chromium";v="119", '
                    '"Not?A_Brand";v="24"',
                "Sec-Ch-Ua-Mobile": '?0',
                'Sec-Ch-Ua-Platform': "Windows",
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-site',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/119.0.0.0  Safari/537.36'
            },
            data={
                'wa': 'wsignin1.0',
                'wresult': wresult,
                'wctx': wctx
                }
        )
        # Это время в формате unix
        self.t_req = int(time.time() * 1000)
        # А этим запросом мы получаем первичные данные содержимого почты
        _r3 = self.sess.post(
            f'https://mail.{self.server}/owa/sessiondata.ashx',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Client-Request-Id':
                    f"{self.sess.cookies.get_dict()['ClientId']}_{self.t_req}",
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Host': f'mail.{self.server}',
                'Origin': f'https://mail.{self.server}',
                'Sec-Ch-Ua':
                    '"Google Chrome";v="119", "Chromium";v="119", '
                    '"Not?A_Brand";v="24"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': "Windows",
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/119.0.0.0 Safari/537.36',
                'X-Owa-Correlationid':
                    f"{self.sess.cookies.get_dict()['ClientId']}_{self.t_req}",
                'X-Owa-Smimeinstalled': '1'
                },
            params={'appcacheclient': '0'}
                )
        self.s_version = _r3.json()['findFolders']['Header']
        self.s_version = self.s_version['ServerVersionInfo']['Version']

    def get_mail(
            self,
            offset: int = 0,
            max_return: int = 25
            ) -> list[EmailMessage]:
        """
        Метод получения списка последних писем в виде объектов.

        Parameters
        ----------
        offset : int, optional
            Отсутп, сверху. The default is 0.
        max_return : int, optional
            Количество писем. The default is 25.

        Returns
        -------
        list[EmailMessage]
            Список объектов писем.

        """
        dic_request = {
            '__type': 'FindConversationJsonRequest:#Exchange',
            'Header': {
                '__type': 'JsonRequestHeaders:#Exchange',
                'RequestServerVersion': self.s_version,
                'TimeZoneContext': {
                    '__type': 'TimeZoneContext:#Exchange',
                    'TimeZoneDefinition': {
                        '__type': 'TimeZoneDefinitionType:#Exchange',
                        'Id': 'Russian Standard Time'
                        }
                    }
                },
            'Body': {
                '__type': 'FindConversationRequest:#Exchange',
                'ParentFolderId': {
                    '__type': 'TargetFolderId:#Exchange',
                    'BaseFolderId': {
                        '__type': 'DistinguishedFolderId:#Exchange',
                        'Id': 'inbox'
                        }
                    },
                'ConversationShape': {
                    '__type': 'ConversationResponseShape:#Exchange',
                    'BaseShape': 'IdOnly'
                    },
                'ShapeName': 'ConversationListView',
                'Paging': {
                    '__type': 'IndexedPageView:#Exchange',
                    'BasePoint': 'Beginning',
                    'Offset': offset,
                    'MaxEntriesReturned': max_return
                    },
                'ViewFilter': 'All',
                'FocusedViewFilter': -1,
                'SortOrder': [
                    {
                        '__type': 'SortResults:#Exchange',
                        'Order': 'Descending',
                        'Path': {
                            '__type': 'PropertyUri:#Exchange',
                            'FieldURI': 'ConversationLastDeliveryOrRenewTime'
                            }
                        },
                    {
                        '__type': 'SortResults:#Exchange',
                        'Order': 'Descending',
                        'Path': {
                            '__type': 'PropertyUri:#Exchange',
                            'FieldURI': 'ConversationLastDeliveryTime'
                            }
                        }
                    ]
                }
            }
        _r7 = self.sess.post(
            f'https://mail.{self.server}/owa/service.svc',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Action': 'FindConversation',
                'Client-Request-Id':
                    f"{self.sess.cookies.get_dict()['ClientId']}_{self.t_req}",
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': f'mail.{self.server}',
                'Origin': f'https://mail.{self.server}',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/119.0.0.0 Safari/537.36',
                'X-Owa-Actionid': '-38',
                'X-Owa-Actionname': 'Browse_All',
                'X-Owa-Attempt': '1',
                'X-Owa-Canary':
                    self.sess.cookies.get_dict()['X-OWA-CANARY'],
                'X-Owa-Correlationid':
                    f"{self.sess.cookies.get_dict()['ClientId']}_{self.t_req}",
                'X-Owa-Urlpostdata': json.dumps(dic_request),
                'X-Requested-With': 'XMLHttpRequest'
                },
            params={
                'action': 'FindConversation',
                'EP': '1',
                'ID': '-38',
                'AC': '1'}
        )
        messages = _r7.json()['Body']['Conversations']
        return self.get_messages(messages)

    def get_messages(self, mess: list[dict]) -> list[EmailMessage]:
        """
        Внутренний метод получения деталей писем.

        Parameters
        ----------
        mess : list[dict]
            Список словарей писем.

        Returns
        -------
        list[EmailMessage]
            Список объектов писем.

        """
        l_conv = []
        for m_i in mess:
            l_conv.append(
                {'__type': 'ConversationRequestType:#Exchange',
                 'ConversationId':
                     {'__type': 'ItemId:#Exchange',
                      'Id': m_i['ConversationId']['Id']
                      },
                     'SyncState': ''
                 }
                )
        dic_request = {
            '__type': 'GetConversationItemsJsonRequest:#Exchange',
            'Header': {'__type': 'JsonRequestHeaders:#Exchange',
                       'RequestServerVersion': self.s_version,
                       'TimeZoneContext':
                           {'__type': 'TimeZoneContext:#Exchange',
                            'TimeZoneDefinition':
                                {'__type': 'TimeZoneDefinitionType:#Exchange',
                                 'Id': 'Russian Standard Time'
                                 }
                            }
                       },
            'Body': {'__type': 'GetConversationItemsRequest:#Exchange',
                     'Conversations': l_conv,
                     'ShapeName': 'ItemPart',
                     }
            }
        _r4 = self.sess.post(
            f'https://mail.{self.server}/owa/service.svc',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Action': 'GetConversationItems',
                'Client-Request-Id':
                    f"{self.sess.cookies.get_dict()['ClientId']}_{self.t_req}",
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': f'mail.{self.server}',
                'Origin': f'https://mail.{self.server}',
                'Sec-Ch-Ua':
                    '"Google Chrome";v="119", "Chromium";v="119", '
                    '"Not?A_Brand";v="24"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': "Windows",
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/119.0.0.0 Safari/537.36',
                'X-Owa-Actionid': '-7',
                'X-Owa-Actionname': 'GetConversationItemsAction',
                'X-Owa-Attempt': '1',
                'X-Owa-Canary': self.sess.cookies.get_dict()['X-OWA-CANARY'],
                'X-Owa-Clientbegin': '2023-12-04T12:12:33.026',
                'X-Owa-Clientbuildversion': '15.2.1258.28',
                'X-Owa-Correlationid':
                    f"{self.sess.cookies.get_dict()['ClientId']}_{self.t_req}",
                'X-Owa-Urlpostdata': json.dumps(dic_request),
                'X-Requested-With': 'XMLHttpRequest'
                },
            params={
                'action': 'GetConversationItems',
                'EP': '1',
                'UA': '0',
                'ID': '-7',
                'AC': '1'}
                )
        convs = _r4.json()['Body']['ResponseMessages']['Items']
        convs = [
            conv['Conversation']["ConversationNodes"][0]['Items'][0]
            for conv in convs
            ]
        return [EmailMessage(conv, self.sess, self.server) for conv in convs]


class MFA:
    '''
    Класс для создания соединения типа вебсокет.
    '''

    def __init__(
        self,
        url: str,
        str_mfa: str,
        str_provider: str,
        str_provider_id: str,
        ws_header
    ):
        # Настраиваем логи
        self.logs = []
        self.str_mfa = str_mfa
        self.str_provider = str_provider
        self.str_provider_id = str_provider_id
        self.result = None
        # Создаем объект вебсокета, но пока не открываем канал
        self.websock = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            header=ws_header,
        )
        # Указываем, что должно отправиться при открытии вебсокета
        self.websock.on_open = self.on_open
        # Создаем объект канала для вебсокета в качестве параллельного потока
        self.websocket_thread = threading.Thread(target=self.run_websocket)
        # Открывам канал вебсокета в параллельном потоке
        self.websocket_thread.start()

    def on_message(self, _, message: str) -> None:
        """
        Метод обрабатывает входящие сообщения по вебсокету.

        Parameters
        ----------
        message : str
            Входящее сообщение по вебсокету.

        Returns
        -------
        None
            Метод ничего не возвращает.

        """
        self.logs.append(f'Received message: "{message}"')
        # Обработка входящих сообщений от сервера, чтобы канал работал
        if message == '{}\x1e':
            # Нужно, для приветственной комбинации
            self.websock.send(
                '{"arguments":["' + self.str_mfa +
                '"],"invocationId":"0","target":"Register","type":1}\x1e')
            self.logs.append(
                '{"arguments":["' + self.str_mfa +
                '"],"invocationId":"0","target":"Register","type":1}\x1e')
        elif message == '{"type":3,"invocationId":"0","result":null}\x1e':
            # Нужно, для приветственной комбинации
            self.websock.send(
                '{"arguments":["' + self.str_mfa +
                '",{"Provider":"' + self.str_provider + '","id":"' +
                self.str_provider_id +
                '"}],"invocationId":"1","target":"Auth","type":1}\x1e')
            self.logs.append(
                '{"arguments":["' + self.str_mfa + '",{"Provider":"' +
                self.str_provider + '","id":"' + self.str_provider_id +
                '"}],"invocationId":"1","target":"Auth","type":1}\x1e')
        elif message == '{"type":1,"target":"SendMessage",'\
                '"arguments":["keep alive"]}\x1e':
            # Нужно, для приветственной комбинации
            self.websock.send('{"type":6}\x1e')
            self.logs.append('{"type":6}\x1e')
        elif "AccessGranted" in f'{message}':
            # Если пришло сообщение, что подтвержден вход
            self.result = message
            self.websock.close()
            self.logs.append('Connection closed succ')

    def on_error(self, _, error: str) -> None:
        """
        Метод обрабатывает ошибки.

        Parameters
        ----------
        error : str
            Текст ошибки.

        Returns
        -------
        None
            Метод ничего не возвращает.

        """
        self.logs.append(f'Error occurred: {error}')

    def on_close(self, _) -> None:
        """
        Метод обрабатывает событие закрытия вебсокета.

        Returns
        -------
        None
            Метод ничего не возвращает.

        """
        self.logs.append('Connection closed')

    def on_open(self, _) -> None:
        """
        Метод выполняет первые действия при октрытии вебсокета.

        Returns
        -------
        None
            Метод ничего не возвращает.

        """
        # Отправляем приветственное сообщение
        self.websock.send('{"protocol":"json","version":1}\x1e')
        self.logs.append('{"protocol":"json","version":1}\x1e')

    def run_websocket(self) -> None:
        """
        Метод запускает вебсокет.

        Returns
        -------
        None.

        """
        self.websock.run_forever()


class AdfsMailMFA:
    '''
    Класс для создания соединения типа вебсокет.
    '''

    def __init__(self, login, password, server):
        """
        Функция залогирования.

        Parameters
        ----------
        login : str
            Почтовый адрес.
        password : str
            Пароль от почты.
        server : str
            Адрес почтового сервера.

        Returns
        -------
        None.

        """
        self.login = login
        self.password = password
        self.server = server
        self.sess = requests.Session()
        # Этот запрос нужнен для получения client_id
        req = self.sess.get(
            f'https://mail.{self.server}/owa/#path=/mail',
            verify=False,
            headers={
                "accept":
                    "text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,image/apng,*/*;q=0.8,application"
                    "/signed-exchange;v=b3;q=0.7",
                "content-type": "application/json",
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/119.0.0.0 Safari/537.36"
                }
            )
        str_link = re.findall(
            r'form id="options" method="post" action="(.*)">', req.text)[0]
        self.client_id = dict(
            parse.parse_qsl(parse.urlsplit(str_link).query)
            )['client-request-id']
        # Этот запрос нужен для получения контекста
        req = self.sess.post(
            f'https://adfs.{self.server}/adfs/ls/',
            verify=False,
            headers={
                "accept":
                    "text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,image/apng,*/*;q=0.8,application"
                    "/signed-exchange;v=b3;q=0.7",
                "content-type": "application/json",
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/119.0.0.0 Safari/537.36"
                },
            params={
                'wa': 'wsignin1.0',
                'wtrealm': f'https://mail.{self.server}/owa/',
                'wctx': 'rm=0&id=passive&ru=%2fowa%2f',
                'client-request-id': self.client_id
            },
            data={
                'UserName': self.login,
                'Password': self.password,
                'AuthMethod': 'FormsAuthentication'
            }
            )
        str_context = re.findall(
            r'<input id="context" type="hidden" name="Context" value="(.*)"/>',
            req.text)[0]
        sso_cookie = list(self.sess.cookies.get_dict().keys())[0]
        # Этот запрос нужен для получения первичного токена к мультифактору
        req = self.sess.get(
            f'https://adfs.{self.server}/adfs/ls/',
            verify=False,
            headers={
                "accept":
                    "text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,image/apng,*/*;q=0.8,application"
                    "/signed-exchange;v=b3;q=0.7",
                "content-type": "application/json",
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/119.0.0.0 Safari/537.36"
                },
            params={
                'wa': 'wsignin1.0',
                'wtrealm': f'https://mail.{self.server}/owa/',
                'wctx': 'rm=0&id=passive&ru=%2fowa%2f',
                'client-request-id': self.client_id,
                'ssoCookie': sso_cookie
            },
            )
        str_mfa = re.findall(
            r'var accessPageUrl = "(.*)";', req.text)[0].rsplit('/', 1)[1]
        # Этот запрос нужен для получения токена соединения от мультифактора
        req = self.sess.post(
            'https://access.multifactor.ru/broadcastHub/negotiate',
            verify=False,
            params={
                'negotiateVersion': '1',
            },
            )
        connect_tok = req.json()['connectionToken']
        # Этот запрос нужен для получения списка провайдеров
        req = self.sess.get(
            f'https://access.multifactor.ru/api/auth/{str_mfa}/providers',
            verify=False,
            params={
                'lang': 'ru',
            },
            )
        # Берем первый попавшийся провайдер, даже если это телеграм
        str_s = req.json()[0]["value"]
        # Берем первое попавшееся устройство провайдера
        req = self.sess.get(
            f'https://access.multifactor.ru/api/auth/{str_mfa}/{str_s}/items',
            verify=False,
            params={
                'lang': 'ru',
            },
            )
        str_provider_id = req.json()[0]["value"]
        # Ну а тут мы коннектимся к мультифактору и ждем подтверждения
        mfa_app = MFA(
            url=f'wss://access.multifactor.ru/broadcastHub?id={connect_tok}',
            str_mfa=str_mfa,
            str_provider=str_s,
            str_provider_id=str_provider_id,
            ws_header={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/119.0.0.0 Safari/537.36',
                }
                )
        # Ждем подтверждения
        while not mfa_app.result:
            time.sleep(5)
        # Передаем на сервер токен полученный от мультифактора
        req = self.sess.post(
            f'https://adfs.{self.server}/adfs/ls/',
            verify=False,
            params={'wa': 'wsignin1.0',
                    'wtrealm': f'https://mail.{self.server}/owa/',
                    'wctx': 'rm=0&id=passive&ru=%2fowa%2f',
                    'client-request-id': self.client_id,
                    'ssoCookie': sso_cookie
                    },
            data={
                'AuthMethod': 'MultiFactor',
                'Context': str_context,
                'accessToken': json.loads(
                    mfa_app.result[:-1]
                    )['arguments'][0]['accessToken']
            }
            )
        # Забираем из ответа сертификат подключения
        xmlns_data = etree.fromstring(req.text, parser)
        xmlns = xmlns_data.xpath('//input[@name="wresult"]/@value')[0]
        # Отправляем сертификат подключения
        req = self.sess.post(
            f'https://mail.{self.server}/owa/',
            verify=False,
            data={
                'wa': 'wsignin1.0',
                'wresult': xmlns,
                'wctx': 'rm=0&id=passive&ru=%2fowa%2f'
            },
            headers={
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image'
                '/avif,image/webp,image/apng,*/*;q=0.8,application'
                '/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Cache-Control': 'max-age=0',
                'Content-Length': '6910',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': f'https://adfs.{self.server}',
                'Referer': f'https://adfs.{self.server}/',
                'Sec-Ch-Ua':
                    '"Google Chrome";v="119", '
                    '"Chromium";v="119", '
                    '"Not?A_Brand";v="24"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': "Windows",
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-site',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/119.0.0.0 Safari/537.36'
                }
                )
        # Время в формате unix
        self.t_req = int(time.time() * 1000)
        # Получаем превью страницы почты после успешной авторизации
        req = self.sess.post(
            f'https://mail.{self.server}/owa/sessiondata.ashx',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Client-Request-Id':
                    f"{self.client_id}_{self.t_req}",
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Host': f'mail.{self.server}',
                'Origin': f'https://mail.{self.server}',
                'Sec-Ch-Ua':
                    '"Google Chrome";v="119", '
                    '"Chromium";v="119", '
                    '"Not?A_Brand";v="24"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': "Windows",
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/119.0.0.0 Safari/537.36',
                'X-Owa-Correlationid':
                    f"{self.client_id}_{self.t_req}",
                'X-Owa-Smimeinstalled': '1'
                },
            params={'appcacheclient': '0'}
            )
        self.s_version = req.json()['findFolders']['Header']
        self.s_version = self.s_version['ServerVersionInfo']['Version']

    def get_mail(
            self,
            offset: int = 0,
            max_return: int = 25
            ) -> list[EmailMessage]:
        """
        Метод получения списка последних писем в виде объектов.

        Parameters
        ----------
        offset : int, optional
            Отсутп, сверху. The default is 0.
        max_return : int, optional
            Количество писем. The default is 25.

        Returns
        -------
        list[EmailMessage]
            Список объектов писем.

        """
        dic_request = {
            '__type': 'FindConversationJsonRequest:#Exchange',
            'Header': {
                '__type': 'JsonRequestHeaders:#Exchange',
                'RequestServerVersion': self.s_version,
                'TimeZoneContext': {
                    '__type': 'TimeZoneContext:#Exchange',
                    'TimeZoneDefinition': {
                        '__type': 'TimeZoneDefinitionType:#Exchange',
                        'Id': 'Russian Standard Time'
                        }
                    }
                },
            'Body': {
                '__type': 'FindConversationRequest:#Exchange',
                'ParentFolderId': {
                    '__type': 'TargetFolderId:#Exchange',
                    'BaseFolderId': {
                        '__type': 'DistinguishedFolderId:#Exchange',
                        'Id': 'inbox'
                        }
                    },
                'ConversationShape': {
                    '__type': 'ConversationResponseShape:#Exchange',
                    'BaseShape': 'IdOnly'
                    },
                'ShapeName': 'ConversationListView',
                'Paging': {
                    '__type': 'IndexedPageView:#Exchange',
                    'BasePoint': 'Beginning',
                    'Offset': offset,
                    'MaxEntriesReturned': max_return
                    },
                'ViewFilter': 'All',
                'FocusedViewFilter': -1,
                'SortOrder': [
                    {
                        '__type': 'SortResults:#Exchange',
                        'Order': 'Descending',
                        'Path': {
                            '__type': 'PropertyUri:#Exchange',
                            'FieldURI': 'ConversationLastDeliveryOrRenewTime'
                            }
                        },
                    {
                        '__type': 'SortResults:#Exchange',
                        'Order': 'Descending',
                        'Path': {
                            '__type': 'PropertyUri:#Exchange',
                            'FieldURI': 'ConversationLastDeliveryTime'
                            }
                        }
                    ]
                }
            }
        _r12 = self.sess.post(
            f'https://mail.{self.server}/owa/service.svc',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Action': 'FindConversation',
                'Client-Request-Id':
                    f"{self.sess.cookies.get_dict()['ClientId']}_{self.t_req}",
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': f'mail.{self.server}',
                'Origin': f'https://mail.{self.server}',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/119.0.0.0 Safari/537.36',
                'X-Owa-Actionid': '-38',
                'X-Owa-Actionname': 'Browse_All',
                'X-Owa-Attempt': '1',
                'X-Owa-Canary':
                    self.sess.cookies.get_dict()['X-OWA-CANARY'],
                'X-Owa-Correlationid':
                    f"{self.client_id}_{self.t_req}",
                'X-Owa-Urlpostdata': json.dumps(dic_request),
                'X-Requested-With': 'XMLHttpRequest'
                },
            params={
                'action': 'FindConversation',
                'EP': '1',
                'ID': '-38',
                'AC': '1'}
        )
        messages = _r12.json()['Body']['Conversations']
        return self.get_messages(messages)

    def get_messages(self, mess: list[dict]) -> list[EmailMessage]:
        """
        Внутренний метод получения деталей писем.

        Parameters
        ----------
        mess : list[dict]
            Список словарей писем.

        Returns
        -------
        list[EmailMessage]
            Список объектов писем.

        """
        l_conv = []
        for m_i in mess:
            l_conv.append(
                {'__type': 'ConversationRequestType:#Exchange',
                 'ConversationId':
                     {'__type': 'ItemId:#Exchange',
                      'Id': m_i['ConversationId']['Id']
                      },
                     'SyncState': ''
                 }
                )
        dic_request = {
            '__type': 'GetConversationItemsJsonRequest:#Exchange',
            'Header': {'__type': 'JsonRequestHeaders:#Exchange',
                       'RequestServerVersion': self.s_version,
                       'TimeZoneContext':
                           {'__type': 'TimeZoneContext:#Exchange',
                            'TimeZoneDefinition':
                                {'__type': 'TimeZoneDefinitionType:#Exchange',
                                 'Id': 'Russian Standard Time'
                                 }
                            }
                       },
            'Body': {'__type': 'GetConversationItemsRequest:#Exchange',
                     'Conversations': l_conv,
                     'ShapeName': 'ItemPart',
                     }
            }
        _r13 = self.sess.post(
            f'https://mail.{self.server}/owa/service.svc',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9',
                'Action': 'GetConversationItems',
                'Client-Request-Id':
                    f"{self.sess.cookies.get_dict()['ClientId']}_{self.t_req}",
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': f'mail.{self.server}',
                'Origin': f'https://mail.{self.server}',
                'Sec-Ch-Ua':
                    '"Google Chrome";v="119", "Chromium";v="119", '
                    '"Not?A_Brand";v="24"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': "Windows",
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/119.0.0.0 Safari/537.36',
                'X-Owa-Actionid': '-7',
                'X-Owa-Actionname': 'GetConversationItemsAction',
                'X-Owa-Attempt': '1',
                'X-Owa-Canary': self.sess.cookies.get_dict()['X-OWA-CANARY'],
                'X-Owa-Clientbegin': '2023-12-04T12:12:33.026',
                'X-Owa-Clientbuildversion': '15.2.1258.28',
                'X-Owa-Correlationid':
                    f"{self.client_id}_{self.t_req}",
                'X-Owa-Urlpostdata': json.dumps(dic_request),
                'X-Requested-With': 'XMLHttpRequest'
                },
            params={
                'action': 'GetConversationItems',
                'EP': '1',
                'UA': '0',
                'ID': '-7',
                'AC': '1'}
                )
        convs = _r13.json()['Body']['ResponseMessages']['Items']
        convs = [
            conv['Conversation']["ConversationNodes"][0]['Items'][0]
            for conv in convs
            ]
        return [EmailMessage(conv, self.sess, self.server) for conv in convs]
