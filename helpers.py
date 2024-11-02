"""Модуль со вспомогательными функциями"""
from typing import Type, Any
from json import load, dump


def wait_for_input():
    """Создаёт задержку, чтобы пользователь успел прочитать текст выше"""
    input('Нажмите Enter чтобы продолжить...')


def required_input(prompt: str = '', var_type: Type = str, **kwargs) -> Any:
    """Обязательный для ввода input с расширенными опциями

    Args:
        prompt (str): Текст, который видит пользователь
        var_type (Type, optional): Тип, который будет иметь значение функции.
        По умолчанию str.

    Returns:
        Any: значение, введенное пользователем
    """
    result = None
    value_range = kwargs.get('value_range')
    should_run = True

    while should_run:
        try:
            result = var_type(input(prompt))

            if var_type == str and result.strip() == '':
                should_run = True
            elif var_type in (int, float) and value_range:
                start = value_range[0]
                end = value_range[1]
                should_run = not start <= result <= end
            else:
                should_run = False
        except ValueError:
            print(f'Элемент должен соответствовать типу {var_type.__name__}!')

    return result


def load_from_json(file_path: str) -> Any | None:
    """Загружает данные из JSON файла

    Args:
        file_path (str): Путь к файлу

    Returns:
        Any | None: Содержимое файла, если оно существует
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            return load(file)
    except FileNotFoundError:
        return None


def save_to_json(obj: Any, file_path: str):
    """Сохраняет данные в JSON файл

    Args:
        obj (Any): Объект для сохранения
        file_path (str): Путь к файлу
    """
    with open(file_path, mode='w', encoding='utf-8') as file:
        dump(obj, file)
