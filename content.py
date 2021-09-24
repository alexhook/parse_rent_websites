API_KEY = 'YOUR_API_KEY'

headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
}

users = [] #list_of_users_to_send_new_posts

url_avito = 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?district=762-763-765-766-772-773-774-776-778-779&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgkkFmSWQFFxpoMFXsiZnJvbSI6MCwidG8iOjM1MDAwfQ&s=104'
url_cian = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice=35000&offer_type=flat&region=2&room2=1&room3=1&type=4'
url_yandex = 'https://realty.yandex.ru/sankt-peterburg/snyat/kvartira/2,3-komnatnie/?priceMax=35000'
urls_vk = [
    'https://vk.com/yuytnoe_gnezdishko',
    'https://vk.com/free_live_in_spb',
    'https://vk.com/piterent',
    'https://vk.com/komnatki1',
    'https://vk.com/arenduem_spb',
    'https://vk.com/vpoiske_piter'
]

bad_words = (
    'ищу',
    'ищем',
    'сниму',
    'снимем',
    'сосед',
    'соседку',
    'сдам комнату',
    'сдаю комнату',
    'сдаем комнату',
    'сдаём комнату',
    'сдадим комнату',
    'сдавать комнату',
    'сдается комната',
    'сдаётся комната',
    'сдаётся место',
    'сдается место',
    'сдам место',
    'сдадим место',
    'студия',
    'студии',
    'студию',
    'доверител',
    'мошенник',
    'отзыв',
    'однушка',
    'однокомнатная',
    'однокомнатную',
    'однокомнатные',
    'одно комнатная',
    'одно комнатную',
    'одно комнатные',
    '1к.',
    '4к.',
    '1 к.',
    '4 к.',
    'оферист',
    '1-комнатную',
    '1-комнатная',
    '1 комнатную',
    '1 комнатная',
    '1-комнатные',
    '4-комнатную',
    '4-комнатная',
    '4-комнатные',
    '1-комн',
    '4-комн',
    'кировск',
    'коттедж',
    'продажа',
    'продам',
    'продается',
    'продаётся',
)
