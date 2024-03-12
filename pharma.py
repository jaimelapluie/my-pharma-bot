from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import time
from datetime import datetime, timedelta

import requests
from tokensSecrets import pharmaBot_data, unsplash_com


API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
base_url_api = 'https://api.telegram.org/bot'
token = pharmaBot_data.token


# Запрос апдейтов
def updetter():
    cnt = 0
    while cnt < 20:
        cnt += 1
        api_url = f'https://api.telegram.org/bot{token}/getUpdates'
        print(f'Итерация #{cnt}')
        
        response = requests.get(api_url)  # Отправляем GET-запрос и сохраняем ответ в переменной response
        
        if response.status_code == 200:  # Если код ответа на запрос - 200, то смотрим, что пришло в ответе
            message = response.json()
            # print(json.dumps(message, separators=(',', ' : '), indent='  '))
            for i in range(len(message['result'])):
                print(type(message), message['result'][i]['message']['text'])
        else:
            print(response.status_code)  # При другом коде ответа выводим этот код
            
        print('Конец Апдейта')
        print()
        time.sleep(3)
        # print('!', message['result'][0]['message']['text'])


# Отправление сообщения
def sender():
    recipient_id = input('введи id получателя')
    text = 'Проверка связи'
    
    api_url = f'{base_url_api}{token}/sendMessage?chat_id={recipient_id}&text={text}'
    response = requests.get(api_url)  # Отправляем GET-запрос и сохраняем ответ в переменной response
    
    if response.status_code == 200:  # Если код ответа на запрос - 200, то смотрим, что пришло в ответе
        message = response.text
        print(type(message), message)
    else:
        print(response.status_code)  # При другом коде ответа выводим этот код


def answering_machine():
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=2)
    offset = -2
    cnt = 1
    
    while datetime.now() < end_time:
        print(f'Работает цикл # {cnt}')
        cnt += 1
        url_api = f'{base_url_api}{token}/getUpdates?offset={offset + 1}'
        updates = requests.get(url_api).json()
        # print(json.dumps(updates, separators=(',', ' : '), indent='  '))
        
        if updates['result']:
            for update in updates['result']:
                offset = update['update_id']
                chat_id = update['message']['from']['id']
                get_text = update['message']['text']
                requests.get(
                    f'{base_url_api}{token}/sendMessage?chat_id={chat_id}&text=Получил сообщение: {get_text}.\nВпечатлён твоим литературным слогом: пиши ещё!')
                
                # print(update)
                # print(offset)
                print(get_text)
        time.sleep(3)


def rabbit_answering_machine():
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=5)
    offset = -2
    cnt = 1
    
    while datetime.now() < end_time:
        print(f'Работает цикл # {cnt}')
        cnt += 1
        url_api = f'{base_url_api}{token}/getUpdates?offset={offset + 1}&timeout=50'
        updates = requests.get(url_api).json()
        # print(json.dumps(updates, separators=(',', ' : '), indent='  '))
        
        if updates['result']:
            rabbit_response = rabbit_image_url()
            for update in updates['result']:
                offset = update['update_id']
                chat_id = update['message']['from']['id']
                get_text = update['message']['text']
                requests.get(
                    f'{base_url_api}{token}/sendMessage?chat_id={chat_id}&text=Получил твоё сообщение: {get_text}.\n'
                    f'А сейчас ты от меня получишь сюрприз!')
                for sec in range(3, 0, -1):
                    requests.get(
                        f'{base_url_api}{token}/sendMessage?chat_id={chat_id}&text={sec}')
                    print('Уснул')
                    time.sleep(1)
                    print('Проснулся')
                requests.get(
                    f'{base_url_api}{token}/sendPhoto?chat_id={chat_id}&photo={rabbit_response}')
                
                # print(update)
                # print(offset)
                print(get_text)
        time.sleep(3)


def rabbit_image_url():
    UNSPLASH_ACCESS_KEY = unsplash_com.token
    url = 'https://api.unsplash.com/photos/random'
    params = {
        'query': 'rabbit',
        'client_id': UNSPLASH_ACCESS_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        image_url = data['urls']['regular']
        print(f"Ссылка на изображение кролика: {image_url}")
    else:
        print(f"Ошибка: {data['errors'][0]}")
    return image_url


# Создаем объекты бота и диспетчера
bot = Bot(token=token)
dp = Dispatcher()


# Эти хэндлеры будут срабатывать на команды "/pill_new" и прочие
@dp.message(Command(commands=["pill_new"]))
async def process_pill_new_command(message: Message):
    await message.answer('Привет!\nМеня зовут Pharma bot!\nНапиши мне какое лекарство нужно добавить в список')


@dp.message(Command(commands=["pill_delete"]))
async def process_pill_delete_command(message: Message):
    await message.answer('Привет!\nМеня зовут Pharma bot!\nНапиши мне какое лекарство нужно удалить из списка')


@dp.message(Command(commands=["pill_list"]))
async def process_pill_list_command(message: Message):
    await message.answer('Привет!\nМеня зовут Pharma bot!\nВот какие лекарства сейчас есть в списке')

@dp.message(Command(commands=["pill_schedule"]))
async def process_pill_schedule_command(message: Message):
    await message.answer('Привет!\nМеня зовут Pharma bot!\nНапоминаю твоё расписание приема лекарств')


@dp.message(Command(commands=["pill_buy"]))
async def process_pill_buy_command(message: Message):
    await message.answer('Привет!\nМеня зовут Pharma bot!\nНапоминаю про лекарства, которые могут закончиться'
                         ' в ближайшее время')


@dp.message(Command(commands=["pill_correction"]))
async def process_pill_correction_command(message: Message):
    await message.answer('Привет!\nМеня зовут Pharma bot!\nЯ помогу откорректировать информацию о лекарствах')


@dp.message()
async def send_echo(message: Message):
    print('Кролик1')
    print(type(message))
    print(message.text)
    if message.text == 'Кролик':
        print('Держи кролика!')
        rabbit_answering_machine()
    else:
        await message.reply(text=message.text)
    

if __name__ == '__main__':
    dp.run_polling(bot)

# sender()
# updetter()
# answering_machine()
# rabbit_answering_machine()


