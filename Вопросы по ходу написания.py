
# тестовый фрагмент бота
api_url = 'https://api.telegram.org/bot'

start_time = datetime.now()
end_time = start_time + timedelta(minutes=2)

offset = -2
cnt = 1
while datetime.now() < end_time:  # работает пару минут для эксперимента
    print(f'Работает цикл # {cnt}')
    cnt += 1

    """Вариант 1 похож на вариант 2, но работают по разному. Почему?"""
    #  вариант 1 - НЕ работает
    api_url = f'{api_url}{token}/getUpdates?offset={offset + 1}'
    updates = requests.get(api_url).json()   

     #  вариант 2 - работает
    updates = requests.get(f'{api_url}{token}/getUpdates?offset={offset + 1}').json()
    
    if updates['result']:
        for update in updates['result']:
            offset = update['update_id']
            chat_id = update['message']['from']['id']
            get_text = update['message']['text']
            requests.get(f'{api_url}{token}/sendMessage?chat_id={chat_id}&text=Я получил твоё сообщение: "{get_text}".\nПиши ещё!')

""" Хотелось бы вернуться к этому в будущем и получше разобраться. 
Тем временем чат GPT пишет следующее:
В приведенном вами коде есть тонкость в работе с переменной api_url. Давайте рассмотрим каждый из ваших вариантов:

Вариант 1:

python
Copy code
api_url = f'{api_url}{token}/getUpdates?offset={offset + 1}'
updates = requests.get(api_url).json()
Вариант 2:

python
Copy code
updates = requests.get(f'{api_url}{token}/getUpdates?offset={offset + 1}').json()
Различия:

В варианте 1 после первой итерации цикла, api_url преобразуется из базового URL в URL с токеном и параметрами запроса. После этого каждый запрос на api_url будет отправлен на обновленный URL с токеном и параметрами.

В варианте 2 каждый запрос формируется с использованием полного URL с токеном и параметрами, и при каждой итерации цикла URL не изменяется.

Проблема:

В варианте 1, после первой итерации цикла, api_url уже не является базовым URL, и при каждой новой итерации вы добавляете токен и параметры запроса к уже сформированному URL.
Рекомендации:

Вариант 2 является более предпочтительным, поскольку каждый раз вы формируете URL с токеном и параметрами, не изменяя базовый URL. Это обеспечивает правильное формирование запросов в каждой итерации цикла.
Поэтому, если у вас нет конкретной необходимости изменять базовый URL в теле цикла, предпочтительнее использовать вариант 2."""
