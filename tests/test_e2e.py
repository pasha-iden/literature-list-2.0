import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:1001"


def test_home_page_loads():
    """1. Главная страница загружается"""
    response = requests.get(f"{BASE_URL}/library")
    assert response.status_code == 200
    assert "Библиотека" in response.text


def test_genres_displayed():
    """2. Отображаются жанры"""
    response = requests.get(f"{BASE_URL}/library")
    soup = BeautifulSoup(response.text, "html.parser")

    genres = soup.find_all(class_="genre")
    assert len(genres) >= 3

    genres_text = [g.text.strip() for g in genres]
    assert "Философия" in genres_text


def test_books_structure():
    """3. Книги с правильной структурой"""
    response = requests.get(f"{BASE_URL}/library")
    soup = BeautifulSoup(response.text, "html.parser")

    # Найти все span с классом book
    books = soup.find_all("span", class_="book")
    assert len(books) > 0

    # Проверить что названия в кавычках
    first_book = books[0].text
    assert '"' in first_book


def test_author_grouping_simple():
    """4. Группировка авторов - упрощенная версия"""
    response = requests.get(f"{BASE_URL}/library")
    soup = BeautifulSoup(response.text, "html.parser")

    # Найти все span с книгами
    books = soup.find_all("span", class_="book")

    # Найти книги с автором (содержат имя и фамилию)
    author_books = []
    yet_books = []

    for book in books:
        text = book.get_text(strip=True)
        has_bold = book.find("b") is not None

        if has_bold:
            # Это книга с автором
            author_books.append(text)
        else:
            # Это книга без тега <b> - должна быть из серии
            yet_books.append(text)

    # Проверяем что есть оба типа
    assert len(yet_books) > 0, "Нет книг из серий"
    assert len(author_books) > 0, "Нет книг с авторами"


def test_css_loaded():
    """5. CSS файл загружается"""
    response = requests.get(f"{BASE_URL}/static/css/library.css")
    assert response.status_code == 200
    assert "genre" in response.text or "book" in response.text
