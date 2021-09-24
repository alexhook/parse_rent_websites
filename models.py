import asyncio, requests, time
from bs4 import BeautifulSoup
from dbase import DataBaseFunctions
from sqlite3.dbapi2 import IntegrityError
from datetime import datetime
from content import urls_vk, url_cian, url_yandex, url_avito, bad_words, headers

dbase = DataBaseFunctions()

class SendNewPosts:
    def __init__(self, bot, users):
        self.bot = bot
        self.users = users
    
    async def send_new_posts(self):
        while True:
            new_posts = dbase.select('id, text', 'posts', 'new=1')
            print(f'[{datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")}] Рассылаю новые посты. Кол-во: {len(new_posts)}.')
            for post in new_posts:
                for user in self.users:
                    await self.bot.send_message(
                            user,
                            f'{post[0]}\n\n'
                            f'{post[1]}'
                        )
                dbase.update('new=0', 'posts', f'id="{post[0]}"')
                await asyncio.sleep(1)
            await asyncio.sleep(60)
        

class Update:
    @classmethod
    def __skip_error(cls, func):
        try:
            return func()
        except:
            return ''

    @classmethod
    def __is_relevant_post(cls, text):
        for i in bad_words:
            if i in text: return 0
        return 1

    @classmethod
    async def update_vk_posts(cls):
        while True:
            for url in urls_vk:
                print(f'[{datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")}] Обновляем базу данных. URL: {url}')
                try:
                    response = requests.get(url, headers=headers)
                except Exception as ex:
                    print(ex)
                else:
                    print(f'Статус запроса: {response.status_code}')
                    soup = BeautifulSoup(response.text, 'lxml')
                    posts = soup.find_all('div', class_='post--with-likes')
                    for i in posts:
                        try:
                            text = i.find('div', class_='wall_post_text').text
                            post_url = i.find('div', class_='PostHeaderInfo').find('a', class_='post_link').get('href')
                        except AttributeError:
                            pass
                        else:
                            try:
                                dbase.insert([url + '?w=' + post_url[1:], text, cls.__is_relevant_post(text)], 'posts')
                            except IntegrityError:
                                pass
                time.sleep(2)
            await asyncio.sleep(60)

    @classmethod
    async def update_yandex_posts(cls):
        while True:
            print(f'[{datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")}] Обновляем базу данных. URL: {url_yandex.split("/")[2]}')
            try:
                response = requests.get(url_yandex, headers=headers)
            except Exception as ex:
                print(ex)
            else:
                print(f'Статус запроса: {response.status_code}')
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'lxml')
                posts = soup.find_all('li', class_='OffersSerpItem_view_desktop')
                for i in posts:
                    title = cls.__skip_error(lambda: i.find('h3', class_='OffersSerpItem__title').text)
                    subway = cls.__skip_error(lambda: i.find('span', class_='MetroStation__title').text)
                    subway_time = cls.__skip_error(lambda: i.find('span', class_='MetroWithTime__distance'))
                    subway_time_text = cls.__skip_error(lambda: subway_time.text)
                    try:
                        subway_time_method = subway_time.find_all('i', class_='Icon_type_small-bus')[0]
                    except:
                        subway_time_method = ' пешком'
                    else:
                        subway_time_method = ' на транспорте'
                    address_text = cls.__skip_error(lambda: i.find('div', class_='OffersSerpItem__address').text)
                    main_price = cls.__skip_error(lambda: i.find('div', class_='OffersSerpItem__price').find('span', class_='price').text)
                    price_info = cls.__skip_error(lambda: i.find('div', class_='OffersSerpItem__paymentsInfo').text)
                    description = cls.__skip_error(lambda: i.find('p', class_='OffersSerpItem__description').text)
                    post_url = 'https://realty.yandex.ru' + i.find('a', class_='OffersSerpItem__link').get('href')
                    try:
                        dbase.insert(
                            [
                                post_url,
                                str(f'{title}\n' +
                                f'Метро {subway} ' +
                                f'{subway_time_text}{subway_time_method}\n\n' +
                                f'{address_text}\n\n' +
                                f'{main_price}\n' +
                                f'{price_info}\n\n' +
                                f'{description}\n').replace('\n\n\n', '\n\n'),
                                1
                            ],
                            'posts'
                        )
                    except IntegrityError:
                        pass
            await asyncio.sleep(60)
    
    @classmethod
    async def update_avito_posts(cls):
        while True:
            print(f'[{datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")}] Обновляем базу данных. URL: {url_avito.split("/")[2]}')
            try:
                response = requests.get(url_avito, headers=headers)
            except Exception as ex:
                print(ex)
            else:
                print(f'Статус запроса: {response.status_code}')
                soup = BeautifulSoup(response.text, 'lxml')
                posts = soup.find('div', attrs={'data-marker': 'catalog-serp'}).find_all('div', attrs={'data-marker': 'item'})
                for i in posts:
                    title = cls.__skip_error(lambda: i.find('h3', attrs={'itemprop': 'name'}).text)
                    geo = cls.__skip_error(lambda: i.find('div', class_='geo-root-H3eWU'))
                    subway = cls.__skip_error(lambda: " ".join(x.text for x in geo.find('div', class_='geo-georeferences-Yd_m5').find_all('span')[-2:]))
                    address_text = cls.__skip_error(lambda: geo.find('span', class_='geo-address-QTv9k').find('span').text)
                    main_price = cls.__skip_error(lambda: i.find('span', class_='price-text-E1Y7h').text)
                    description = cls.__skip_error(lambda: i.find('meta', attrs={'itemprop': 'description'}).get_attribute_list('content')[0])
                    post_url = 'https://www.avito.ru' + i.find('a').get('href')
                    try:
                        dbase.insert(
                            [
                                post_url,
                                str(f'{title}\n' +
                                f'{main_price}\n' +
                                f'Метро {subway}\n' +
                                f'{address_text}\n\n' +
                                f'{description}\n').replace('\n\n\n', '\n\n'),
                                1
                            ],
                            'posts'
                        )
                    except IntegrityError:
                        pass
            
            await asyncio.sleep(60)
