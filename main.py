"""База данных для хранения фильмов"""
from uuid import uuid4
from typing import TypedDict, NotRequired
from helpers import required_input, wait_for_input, load_from_json, \
    save_to_json

DB_PATH = 'data.json'

Movie = TypedDict('Movie', {
    'id': str,
    'title': str,
    'director': str,
    'screenwriter': str,
    'duration': int,
    'year_released': int
})
type MovieList = list[Movie]
Filters = TypedDict('Filters', {
    'year_released': NotRequired[int],
    'duration': NotRequired[int]
})
SearchOptions = TypedDict('SearchOptions', {
    'query': str,
    'filters': Filters
})


def get_main_menu_option() -> int:
    """Показывает меню и предлагает выбор опции из него

    Returns:
        int: Номер опции из меню
    """
    print('*----------- ФИЛЬМЫ -----------*',
          '1) Вывести найденные фильмы',
          '2) Поиск по наименованию',
          '3) Фильтровать по году выхода и продолжительности',
          '4) Добавить фильм',
          '5) Удалить фильм',
          '6) Выход', sep='\n')

    return required_input('Выберите действие: ', int, value_range=(1, 6))


def find_movies(movies: MovieList, founded_movies: MovieList,
                search_options: SearchOptions):
    """Ищет фильмы на основе заданных параметров

    Args:
        movies (MovieList): Список фильмов
        founded_movies (MovieList): Найденные фильмы, будет изменено
        search_options (SearchOptions): Параметры поиска
    """
    query = search_options['query']
    year_released = search_options['filters'].get('year_released')
    duration = search_options['filters'].get('duration')

    founded_movies.clear()
    for movie in movies:
        if (query.lower().strip() in movie['title'].lower().strip()) and \
                (not duration or duration == movie['duration']) and \
                (not year_released or year_released == movie['year_released']):
            founded_movies.append(movie)


def print_movies(movies: MovieList, numerate: bool = False):
    """Выводит фильмы на экран в красивом формате, если они существуют

    Args:
        movies (MovieList): Список фильмов
        numerate (bool, optional): Булево значение, отвечающее за то,
        будет ли список фильмов нумерован
    """
    if len(movies) == 0:
        print('Не найдено ни одного фильма!')
        return

    print()
    for number, movie in enumerate(movies, start=1):
        hours = movie['duration'] // 60
        minutes = movie['duration'] % 60

        print(f'-------- {movie['title']} --------',
              f'Фильм №{number}' if numerate else None,
              f'Режиссер: {movie['director']}',
              f'Сценарист: {movie['screenwriter']}',
              f'Длительность: {hours} часов, {minutes} минут',
              f'Год выпуска: {movie['year_released']}',
              (len(movie['title']) + 18) * '-',
              '\n', sep='\n', end='')


def change_search_query(search_options: SearchOptions):
    """Меняет запрос в параметрах поиска с клавиатуры

    Args:
        search_options (SearchOptions): Параметры поиска
    """
    query = input('Найти (ничего для сброса): ')
    search_options['query'] = query


def change_search_filters(search_options: SearchOptions):
    """Меняет фильтры в параметрах поиска с клавиатуры

    Args:
        search_options (SearchOptions): Параметры поиска
    """
    filter_keys = ('year_released', 'duration')
    new_filters = {}

    print('1) Изменить фильтр по году',
          '2) Изменить фильтр по продолжительности',
          '3) Удалить фильтр по году',
          '4) Удалить фильтр по продолжительности',
          '5) Удалить все фильтры', sep='\n')
    menu_option = required_input('Выберите действие: ', int,
                                 value_range=(1, 5))
    filter_name = filter_keys[menu_option % 2 - 1]

    if menu_option == 1:
        year_released = required_input('Введите год выхода: ', int,
                                       value_range=(1902, 2024))
        new_filters[filter_name] = year_released
    elif menu_option == 2:
        hours = required_input('Введите количество часов: ', int,
                               value_range=(0, 14))
        minutes = required_input('Введите количество минут: ', int,
                                 value_range=(0, 59))
        duration = hours * 60 + minutes
        new_filters[filter_name] = duration
    elif menu_option in (3, 4):
        for key, value in search_options['filters'].items():
            if key != filter_name:
                new_filters[key] = value

    search_options['filters'] = new_filters
    print('Фильтры успешно изменены!')


def add_new_movie(movies: MovieList):
    """Запрашивает у пользователя ввод данных о новом фильме с
    клавиатуры и добавляет результат в список

    Args:
        movies (MovieList): Список фильмов
    """
    title = required_input('Введите название: ').strip()
    director = required_input('Введите режиссера: ').strip()
    screenwriter = required_input('Введите сценариста: ').strip()
    duration = required_input('Введите длительность (в минутах): ', int,
                              value_range=(3, 873))
    year_released = required_input('Введите год выхода: ', int,
                                   value_range=(1902, 2024))
    new_movie: Movie = {
        'id': str(uuid4()),
        'title': title,
        'director': director,
        'screenwriter': screenwriter,
        'duration': duration,
        'year_released': year_released
    }
    movies.append(new_movie)
    print(f'Фильм "{new_movie['title']}" был успешно создан!')


def remove_movie(movies: MovieList, founded_movies: MovieList):
    """Позволяет пользователю удалить определенный элемент из списка
    найденных фильмов, модифицируя основной список

    Args:
        movies (MovieList): Список фильмов
        founded_movies (MovieList): Список найденных фильмов
    """
    print_movies(founded_movies, numerate=True)

    if not founded_movies:
        return

    delete_num = required_input('Введите номер удаляемого элемента (0 для '
                                'выхода): ', int,
                                value_range=(0, len(founded_movies)))

    if delete_num == 0:
        return

    for idx, movie in enumerate(movies):
        if movie['id'] == founded_movies[delete_num - 1]['id']:
            del movies[idx]
            print(f'Фильм {movie['title']} успешно удален!')


def start(search_options: SearchOptions) -> bool:
    """Функция, отвечающая за вызов функций меню, выход из программы и
    синхронизацию данных

    Args:
        search_options (SearchOptions): Параметры поиска

    Returns:
        bool: Булево значение, означающее надо ли выходить из программы
    """
    movies = load_from_json(DB_PATH) or []
    founded_movies = []
    find_movies(movies, founded_movies, search_options)
    menu = (
        (print_movies, founded_movies),
        (change_search_query, search_options),
        (change_search_filters, search_options),
        (add_new_movie, movies),
        (remove_movie, (movies, founded_movies))
    )
    menu_option = get_main_menu_option()

    if menu_option == 6:
        return False

    menu_func = menu[menu_option - 1][0]
    menu_value = menu[menu_option - 1][1]
    if isinstance(menu_value, tuple):
        menu_func(*menu_value)
    else:
        menu_func(menu_value)

    save_to_json(movies, DB_PATH)
    wait_for_input()
    return True


def main():
    """Главная функция, зацикливающая работу программы"""
    should_run = True
    search_options: SearchOptions = {
        'query': '',
        'filters': {}
    }

    while should_run:
        should_run = start(search_options)


if __name__ == '__main__':
    main()
