from collections import deque
from functools import wraps
import re


from system import systemInformation

def clean_input_decorator(func):
    @wraps(func)
    def wrapper(user_input, *args, **kwargs):
        # ЛОГИКА ДО: Очистка строки
        # Оставляем только скобки из systemInformation._brackets
        allowed_chars = list()

        for pair in info._brackets:
            allowed_chars.extend(pair)

        # Если в списке есть '[', re.escape превратит его в '\['
        escaped_chars = [re.escape(char) for char in allowed_chars]

        pattern_str = f"[^{''.join(escaped_chars)}]"

        cleaned_string = re.sub(pattern_str, '', user_input)
        
        # Передаем очищенную строку в основную функцию
        return func(cleaned_string, *args, **kwargs)
    
    return wrapper

@clean_input_decorator
def checking_parentheses_for_correctness(inputData: str, *args, **kwargs) -> bool:
    system_deque = deque()
    # Создаем словарь соответствий: {закрывающая: открывающая}
    system_dict = {closed: opened for opened, closed in info._brackets}
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

if __name__=="__main__":

    info = systemInformation()
    result = None

    user_input = input()

    result = checking_parentheses_for_correctness(user_input)

    print(result)