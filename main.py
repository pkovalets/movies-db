"""База данных для хранения фильмов"""
from uuid import uuid4
from typing import TypedDict, Optional

from helpers import required_input, wait_for_input, load_from_json, \
    save_to_json, file_name_input
from config import DEFAULT_FILE_NAME, MENU_OPTIONS, YEAR_RANGE, DURATION_RANGE

Movie = TypedDict('Movie', {
    'id': str,
    'title': str,
    'director': str,
    'screenwriter': str,
    'duration': int,
    'year_released': int
})
Filters = TypedDict('Filters', {
    'query': str,
    'year_released': Optional[int],
    'duration': Optional[int]
})


def get_menu_option_idx() -> int:
    """Показывает меню, предлагает выбор опции из него и возвращает индекс
    выбранного элемента"""
    print('*----------- ФИЛЬМЫ -----------*')
    for num, option in enumerate(MENU_OPTIONS, start=1):
        print(f'{num}) {option}')
    print('*------------------------------*')
    return required_input('Выберите действие: ', int,
                          value_range=(1, len(MENU_OPTIONS))) - 1


def load_movies_from_file(movies: list[Movie], default_file_name: str) \
        -> tuple[list[Movie], str]:
    """Загружает фильмы из файла, который задает пользователь, и возвращает
    данные вместе с именем последнего файла"""
    file_name = file_name_input('json',
                                f'Введите имя файла ({default_file_name}): ',
                                default_file_name)
    loaded_movies = load_from_json(file_name)

    if not loaded_movies:
        print('Файл пустой или не существует! Фильмы не были загружены.')
        return movies, file_name

    print('Фильмы успешно загружены из файла!')
    return loaded_movies, file_name


def save_movies_to_file(movies: list[Movie], default_file_name: str) -> str:
    """Сохраняет фильмы в файл, который задает пользователь, и возвращает
    имя последнего файла"""
    file_name = file_name_input('json',
                                f'Введите имя файла ({default_file_name}): ',
                                default_file_name)
    save_to_json(movies, file_name)
    print('Фильмы успешно сохранены в файл!')
    return file_name


def find_movies(movies: list[Movie], filters: Filters) -> list[Movie]:
    """Ищет фильмы на основе заданных параметров и возвращает их"""
    query = filters['query'].lower().strip()
    return [
        movie for movie in movies
        if (
                (query in movie['title'].lower()) and
                (filters['year_released'] is None or
                 filters['year_released'] == movie['year_released']) and
                (filters['duration'] is None or
                 filters['duration'] == movie['duration'])
        )
    ]


def print_movies(movies: list[Movie]) -> None:
    """Выводит фильмы на экран в красивом формате, если они существуют"""
    if not movies:
        print('Не найдено ни одного фильма!')
        return

    print()
    for number, movie in enumerate(movies, start=1):
        hours = movie['duration'] // 60
        minutes = movie['duration'] % 60

        print(f'-------- {movie['title']} --------',
              f'Фильм №{number}',
              f'Режиссер: {movie['director']}',
              f'Сценарист: {movie['screenwriter']}',
              f'Длительность: {hours} часов, {minutes} минут',
              f'Год выпуска: {movie['year_released']}',
              (len(movie['title']) + 18) * '-',
              '\n', sep='\n', end='')


def change_search_query(filters: Filters) -> None:
    """Меняет запрос в параметрах поиска с клавиатуры"""
    filters['query'] = input('Найти (ничего для сброса): ')


def change_search_filters(filters: Filters) -> None:
    """Меняет фильтры в параметрах поиска с клавиатуры"""
    options = (
        ('год выхода', 'year_released', int, YEAR_RANGE),
        ('продолжительность (минуты)', 'duration', int, DURATION_RANGE)
    )
    print('1) Изменить фильтр по году',
          '2) Изменить фильтр по продолжительности',
          '3) Удалить фильтр по году',
          '4) Удалить фильтр по продолжительности',
          '5) Удалить все фильтры',
          '6) Выход', sep='\n')
    option_idx = required_input('Выберите действие: ', int,
                            value_range=(1, 6)) - 1

    if option_idx in (0, 1):
        prompt, attr, var_type, value_range = options[option_idx]
        value = required_input(f'Введите {prompt}: ', var_type,
                               value_range=value_range)
        filters[attr] = value
    elif option_idx == 2:
        filters['year_released'] = None
    elif option_idx == 3:
        filters['duration'] = None
    elif option_idx == 4:
        filters['year_released'] = None
        filters['duration'] = None
    elif option_idx == 5:
        return
    print('Фильтры успешно изменены!')


def add_new_movie(movies: list[Movie]) -> None:
    """Запрашивает у пользователя ввод данных о новом фильме с
    клавиатуры и добавляет результат в список"""
    title = required_input('Введите название: ').strip()
    director = required_input('Введите режиссера: ').strip()
    screenwriter = required_input('Введите сценариста: ').strip()
    duration = required_input('Введите длительность (в минутах): ', int,
                              value_range=DURATION_RANGE)
    year_released = required_input('Введите год выхода: ', int,
                                   value_range=YEAR_RANGE)

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


def remove_movie(movies: list[Movie], founded_movies: list[Movie]) -> None:
    """Позволяет пользователю удалить определенный элемент из списка
    найденных фильмов, модифицируя основной список"""
    print_movies(founded_movies)
    if not founded_movies:
        return

    delete_num = required_input('Введите номер удаляемого элемента (0 для '
                                'выхода): ', int,
                                value_range=(0, len(founded_movies)))
    if delete_num == 0:
        return

    movie_to_delete = founded_movies[delete_num - 1]
    movies.remove(movie_to_delete)
    print(f'Фильм {movie_to_delete['title']} успешно удален!')


def start(movies: list[Movie], filters: Filters, file_name: str) \
        -> tuple[bool, list[Movie], str]:
    """Функция, отвечающая за вызов функций меню, выход из программы и
    синхронизацию данных"""
    founded_movies = find_movies(movies, filters)

    menu_actions = (lambda: load_movies_from_file(movies, file_name),
                    lambda: print_movies(founded_movies),
                    lambda: change_search_query(filters),
                    lambda: change_search_filters(filters),
                    lambda: add_new_movie(movies),
                    lambda: remove_movie(movies, founded_movies),
                    lambda: save_movies_to_file(movies, file_name))

    menu_option_idx = get_menu_option_idx()
    if menu_option_idx == len(MENU_OPTIONS) - 1:
        return False, movies, file_name

    action = menu_actions[menu_option_idx]
    result = action()

    if isinstance(result, tuple):
        movies, file_name = result
    elif isinstance(result, str):
        file_name = result

    wait_for_input()
    return True, movies, file_name


def main() -> None:
    """Главная функция, зацикливающая работу программы"""
    movies: list[Movie] = []
    file_name = DEFAULT_FILE_NAME
    is_running = True
    filters: Filters = {
        'query': '',
        'year_released': None,
        'duration': None
    }

    while is_running:
        is_running, movies, file_name = start(movies, filters, file_name)


if __name__ == '__main__':
    main()
