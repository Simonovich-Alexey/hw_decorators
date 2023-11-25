import os
from datetime import datetime
import requests


def logger_one(old_function):
    def new_function(*args, **kwargs):
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        function_name = old_function.__name__
        arguments = f"args: {args}, kwargs: {kwargs}"

        result = old_function(*args, **kwargs)
        return_value = f"return: {result}"

        with open('main.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"{current_time} - {function_name} - {arguments} - {return_value}\n")

        return result

    return new_function


def logger_two(path):
    def logger(old_function):
        def new_function(*args, **kwargs):
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            function_name = old_function.__name__

            # Записываем аргументы, с которыми вызвалась функция
            arguments = ", ".join([str(arg) for arg in args])
            arguments += ", ".join([f", {value}" for value in kwargs.values()])

            result = old_function(*args, **kwargs)

            log_entry = f"{current_datetime} - {function_name}({arguments}) - {result}\n"

            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)

            return result

        return new_function

    return logger


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_one
    def hello_world():
        return 'Hello World'

    @logger_one
    def summator(a, b=0):
        return a + b

    @logger_one
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_two(path)
        def hello_world():
            return 'Hello World'

        @logger_two(path)
        def summator(a, b=0):
            return a + b

        @logger_two(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


@logger_one
def search_superhero(url_super, *superheroes_search):
    response_super = requests.get(url_super)
    if 200 <= response_super.status_code <= 300:
        data = response_super.json()
        superheroes = []
        for i in data:
            if i['name'] in superheroes_search:
                name_superheroes = i['name']
                intelligence_superheroes = i['powerstats']['intelligence']
                superheroes.append({'name': name_superheroes, 'intelligence': intelligence_superheroes})
        superheroes_sorted = sorted(superheroes, key=lambda x: x['intelligence'], reverse=True)
        return f"Самый умный супергерой: {superheroes_sorted[0]['name']}"


if __name__ == '__main__':
    test_1()
    test_2()

    search_superhero("https://akabab.github.io/superhero-api/api/all.json", "Hulk", "Captain America")
