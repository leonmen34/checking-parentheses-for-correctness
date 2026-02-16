# Структура данных стек
from collections import deque

from functools import wraps
import re

# Для работы с json файлами
import json
import sys

# Глобальные переменные для настроек
BRACKETS_CONFIG = []
APP_CONFIG = {}

def load_json(filename = 'settings.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки настроек: {e}")
        return None

def clean_input_decorator(func):
    @wraps(func)
    def wrapper(user_input, *args, **kwargs):
        # Очистка строки
        # Оставляем только скобки из файла settings.json supported_brackets
        allowed_chars = list()

        for pair in BRACKETS_CONFIG:
            allowed_chars.extend(pair)

        # Если в списке есть '[', re.escape превратит его в '\['
        escaped_chars = [re.escape(char) for char in allowed_chars]

        pattern_str = f"[^{''.join(escaped_chars)}]"

        cleaned_string = re.sub(pattern_str, '', user_input)

        if cleaned_string == "":
            return None
        
        # Передаем очищенную строку в основную функцию
        return func(cleaned_string, *args, **kwargs)
    
    return wrapper

@clean_input_decorator
def checking_parentheses_for_correctness(inputData: str, *args, **kwargs) -> bool:
    system_deque = deque()
    # Создаем словарь соответствий: {закрывающая: открывающая}
    system_dict = {closed: opened for opened, closed in BRACKETS_CONFIG}
    # Набор всех открывающих скобок для быстрой проверки
    opening_brackets = set(system_dict.values())

    for char in inputData:
        # 1. Если это открывающая скобка — кладем в стек
        if char in opening_brackets:
            system_deque.append(char)
        # 2. Если это закрывающая скобка (есть в ключах словаря)
        elif char in system_dict:
            # Если стек пуст, а пришла закрывающая — это сразу ошибка
            if not system_deque:
                return False
            # Достаем последнюю открытую и проверяем, подходит ли она
            last_opened = system_deque.pop()
            if last_opened != system_dict[char]:
                return False

    return len(system_deque) == 0

def main(user_input: str) -> str:
    global BRACKETS_CONFIG, APP_CONFIG

    APP_CONFIG = load_json('settings.json')
    
    if APP_CONFIG:
        # Достаем конкретно скобки по ключу "supported_brackets"
        # Если ключа нет, вернет пустой список []
        BRACKETS_CONFIG = APP_CONFIG.get("supported_brackets", [])
        
    else:
        print("Не удалось прочитать файл настроек.")
        sys.exit()

    # Проверка, что скобки загрузились
    if not BRACKETS_CONFIG:
        print("Ошибка: Список скобок пуст или не найден в JSON")
        sys.exit()

    result = checking_parentheses_for_correctness(user_input)

    return str(result)

if __name__=="__main__":

    print(main(input()))
    pass