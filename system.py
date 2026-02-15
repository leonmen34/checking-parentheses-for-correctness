from dataclasses import dataclass

@dataclass
class systemInformation:

    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Если объекта еще нет, создаем его через базовый класс object
            cls._instance = super().__new__(cls)
        return cls._instance
    
    # Множество скобок
    _brackets = [
        ['(', ')'], 
        ['[', ']'], 
        ['{', '}'], 
        ['<', '>'],
        ["A", "a"],
        ["B", "b"],
        ["C", "c"],
        ["D", "d"],
        ["E", "e"],
        ["F", "f"]]