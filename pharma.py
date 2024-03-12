import json
import time
from datetime import datetime, timedelta

import requests
from tokensSecrets import pharmaBot_data


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

# sender()
# updetter()
# answering_machine()
