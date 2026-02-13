import sys

sys.path.append(".")

from tools.parser import parser  # noqa: E402


# 1. ТЕСТ БАЗОВОЙ СТРУКТУРЫ
def test_parser_returns_list():
    """Парсер всегда возвращает список"""
    result = parser([])
    assert isinstance(result, list)


def test_parser_empty_data():
    """Пустые данные → пустой результат"""
    result = parser([])
    assert result == []


# 2. ТЕСТ С ОДНИМ СТОЛБЦОМ (ОДИН ЖАНР)
def test_parser_one_genre_one_book():
    """Один жанр, одна книга"""
    data = [["Философия"], [""], ["Искусство войны"], ["Сунь Цзы"], [""]]

    result = parser(data)

    assert len(result) == 2  # заголовок + книга
    assert result[0] == (0, 0, 0, "Философия", 0)  # заголовок жанра
    assert result[1][1] == "Искусство войны"  # название
    assert result[1][2] == "Сунь Цзы"  # автор
    assert result[1][3] == "Философия"  # жанр
    assert result[1][4] == 1  # номер в жанре


def test_parser_one_genre_multiple_books_one_author():
    """Один автор, несколько книг"""
    data = [
        ["Философия"],
        [""],
        ["Книга 1"],
        ["Книга 2"],
        ["Книга 3"],
        ["Автор"],
        [""],
    ]  # noqa: E501

    result = parser(data)

    assert len(result) == 4  # заголовок + 3 книги

    # Первая книга
    assert result[1][1] == "Книга 1"
    assert result[1][2] == "еще"
    assert result[1][4] == 1

    # Вторая книга
    assert result[2][1] == "Книга 2"
    assert result[2][2] == "еще"
    assert result[2][4] == 2

    # Третья книга (последняя) - автор
    assert result[3][1] == "Книга 3"
    assert result[3][2] == "Автор"
    assert result[3][4] == 3


def test_parser_one_genre_multiple_authors():
    """Несколько авторов подряд"""
    data = [
        ["Философия"],
        [""],
        ["Книга А1"],
        ["Автор А"],
        [""],
        ["Книга Б1"],
        ["Книга Б2"],
        ["Автор Б"],
        [""],
    ]

    result = parser(data)

    assert len(result) == 4

    # Автор А (одна книга)
    assert result[1][1] == "Книга А1"
    assert result[1][2] == "Автор А"

    # Автор Б (две книги)
    assert result[2][1] == "Книга Б1"
    assert result[2][2] == "еще"
    assert result[3][1] == "Книга Б2"
    assert result[3][2] == "Автор Б"


# 3. ТЕСТ С НЕСКОЛЬКИМИ СТОЛБЦАМИ (НЕСКОЛЬКО ЖАНРОВ)
def test_parser_two_genres():
    """Два жанра (два столбца)"""
    data = [
        ["Философия", "Психология"],
        ["", ""],
        ["Книга Ф1", "Книга П1"],
        ["Автор Ф", "Автор П"],
        ["", ""],
    ]

    result = parser(data)

    # Первый жанр
    assert result[0] == (0, 0, 0, "Философия", 0)
    assert result[1][1] == "Книга Ф1"
    assert result[1][2] == "Автор Ф"
    assert result[1][3] == "Философия"

    # Второй жанр
    assert result[2] == (2, 0, 0, "Психология", 0)
    assert result[3][1] == "Книга П1"
    assert result[3][2] == "Автор П"
    assert result[3][3] == "Психология"


# 4. ТЕСТ ПРОПУСКА ПУСТЫХ СТОЛБЦОВ
def test_parser_skips_empty_columns():
    """Пустые столбцы игнорируются"""
    data = [
        ["Философия", "", "Психология"],
        ["", "", ""],
        ["Книга", "", "Книга"],
        ["Автор", "", "Автор"],
        ["", "", ""],
    ]

    result = parser(data)

    # Должны быть только два жанра (Философия и Психология)
    genres = []
    for record in result:
        if record[1] == 0 and record[2] == 0:
            genres.append(record[3])

    assert len(genres) == 2
    assert "Философия" in genres
    assert "Психология" in genres
    assert "Пустой столбец" not in genres


# 5. ТЕСТ КОРРЕКТНОСТИ ID
def test_parser_id_increment():
    """ID должны увеличиваться последовательно"""
    data = [["Философия"], [""], ["Книга 1"], ["Книга 2"], ["Автор"], [""]]

    result = parser(data)

    # ID: 0 - заголовок, 1 - книга1, 2 - книга2
    assert result[0][0] == 0
    assert result[1][0] == 1
    assert result[2][0] == 2


# 6. ТЕСТ РАЗНЫХ ФОРМАТОВ ДАННЫХ
def test_parser_handles_whitespace():
    """Должен обрезать пробелы в начале/конце"""
    data = [["  Философия  "], [""], ["  Искусство войны  "], ["  Сунь Цзы  "]]

    result = parser(data)

    assert result[0][3] == "Философия"  # пробелы обрезаны
    assert result[1][1] == "Искусство войны"
    assert result[1][2] == "Сунь Цзы"


# 7. ТЕСТ НА РЕАЛЬНЫХ ДАННЫХ (ИНТЕГРАЦИОННЫЙ)
def test_parser_with_real_data():
    """Проверка на данных, похожих на реальную таблицу"""
    data = [
        ["Философия", "Психология"],
        ["", ""],
        ["Искусство войны", "Введение в психоанализ"],
        ["Сунь Цзы", "Тотем и табу"],
        ["", "Я и Оно"],
        ["Бусидо", "По ту сторону принципа наслаждения"],
        ["Ямамото Цунэтомо", "Зигмунд Фрейд"],
        ["", ""],
        ["Государство", "Архетипы и коллективное бессознательное"],
        ["Платон", "Карл Юнг"],
    ]

    result = parser(data)

    # Проверяем философию (Сунь Цзы - одна книга)
    philosophy_books = [r for r in result if r[3] == "Философия" and r[1] != 0]
    assert len(philosophy_books) == 3
    assert philosophy_books[0][2] == "Сунь Цзы"  # у Сунь Цзы автор сразу

    # Проверяем психологию (Фрейд - 4 книги)
    psychology_books = [
        r for r in result if r[3] == "Психология" and r[1] != 0
    ]  # noqa: E501
    freud_books = [
        b for b in psychology_books if b[2] == "еще" or b[2] == "Зигмунд Фрейд"
    ]  # noqa: E501
    assert len(freud_books) == 4
    assert freud_books[0][2] == "еще"  # первая книга
    assert freud_books[1][2] == "еще"  # вторая
    assert freud_books[2][2] == "еще"  # третья
    assert freud_books[3][2] == "Зигмунд Фрейд"  # последняя
