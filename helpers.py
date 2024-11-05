"""Модуль со вспомогательными функциями"""
from typing import Type, Any, Optional
from json import load, dump


def wait_for_input() -> None:
    """Создаёт задержку, чтобы пользователь успел прочитать текст выше"""
    input('Нажмите Enter чтобы продолжить...')


def required_input(prompt: str = '', var_type: Type = str, **kwargs) -> Any:
    """Обязательный для ввода input с расширенными опциями"""
    value_range = kwargs.get('value_range')

    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print('Ошибка! Ввод не может быть пустым.')
            continue

        try:
            value = var_type(user_input)
            if (value_range and
                    not value_range[0] <= value <= value_range[1]):
                print(f'Ошибка! Введите значение в диапазоне от'
                      f' {value_range[0]} до '
                      f'{value_range[1]}.')
                continue
            return value
        except ValueError:
            print(f'Ошибка! Ожидался тип {var_type.__name__}.')


def file_name_input(extension: str, prompt: str = '',
                    default_file_name: Optional[str] = None) -> str:
    """Input для ввода имени файла с необходимыми проверками"""
    while True:
        new_file_name = input(prompt).strip() or default_file_name

        if not new_file_name:
            print('Ошибка! Имя файла не может быть пустым.')
            continue
        if not new_file_name.endswith(f'.{extension}'):
            print('Ошибка! Некорректное имя файла.')
            continue
        return new_file_name


def load_from_json(file_path: str, default: Optional[Any] = None) -> Any:
    """Загружает данные из JSON файла и возвращает их"""
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            return load(file)
    except (FileNotFoundError, ValueError):
        return default


def save_to_json(obj: Any, file_path: str) -> None:
    """Сохраняет данные в JSON файл"""
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            dump(obj, file)
    except IOError as e:
        print(f'Ошибка сохранения: {e}')
