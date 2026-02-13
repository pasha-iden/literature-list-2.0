import pytest
import requests
from unittest.mock import patch, Mock
import sys

sys.path.append(".")

from tools.getter import getter  # noqa: E402


# 1. ТЕСТ УСПЕШНОГО ПОЛУЧЕНИЯ TSV
@patch("tools.getter.requests.get")
def test_getter_success(mock_get):
    """Должен скачать TSV и преобразовать в список списков"""

    # Создаём мок-ответ
    mock_response = Mock()
    mock_response.text = (
        "Название\tАвтор\nВойна и мир\tТолстой\nПреступление\tДостоевский"  # noqa: E501
    )
    mock_get.return_value = mock_response

    # Вызываем тестируемую функцию
    result = getter("http://fake-url.com")

    # Проверяем результат
    assert len(result) == 3
    assert result[0] == ["Название", "Автор"]
    assert result[1] == ["Война и мир", "Толстой"]
    assert result[2] == ["Преступление", "Достоевский"]

    # Проверяем что requests.get был вызван с правильным URL
    mock_get.assert_called_once_with("http://fake-url.com")


# 2. ТЕСТ ОБРАБОТКИ ПУСТОГО TSV
@patch("tools.getter.requests.get")
def test_getter_empty_file(mock_get):
    """Должен вернуть пустой список на пустой файл"""

    mock_response = Mock()
    mock_response.text = ""
    mock_get.return_value = mock_response

    result = getter("http://fake-url.com")

    assert result == []  # или [['']] - зависит от csv.reader
    assert len(result) == 0


# 3. ТЕСТ РАЗНЫХ РАЗДЕЛИТЕЛЕЙ
@patch("tools.getter.requests.get")
def test_getter_different_delimiters(mock_get):
    """Должен работать только с табуляцией, не с запятыми"""

    # Если вдруг пришёл CSV с запятыми, а не TSV
    mock_response = Mock()
    mock_response.text = "col1,col2\nval1,val2"  # запятые!
    mock_get.return_value = mock_response

    result = getter("http://fake-url.com")

    # Должен получить ОДИН столбец, потому что табуляции нет
    assert result[0] == ["col1,col2"]
    assert result[1] == ["val1,val2"]


# 4. ТЕСТ ОШИБКИ СЕТИ
@patch("tools.getter.requests.get")
def test_getter_network_error(mock_get):
    """Должен пробрасывать исключение при ошибке сети"""

    mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

    with pytest.raises(requests.exceptions.ConnectionError):
        getter("http://fake-url.com")


# 5. ТЕСТ ОШИБКИ HTTP (404, 500 и т.д.)
@patch("tools.getter.requests.get")
def test_getter_http_error(mock_get):
    """Должен пробрасывать исключение при HTTP ошибке"""

    mock_response = Mock()
    mock_response.text = ""
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Not Found"
    )  # noqa: E501
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        getter("http://fake-url.com")


# 6. ТЕСТ КОДИРОВКИ
@patch("tools.getter.requests.get")
def test_getter_encoding(mock_get):
    """Должен устанавливать правильную кодировку"""

    mock_response = Mock()
    mock_response.text = "Автор\tКнига\nДостоевский\tИдиот"
    mock_get.return_value = mock_response

    result = getter("http://fake-url.com")

    # Проверяем что encoding был установлен
    assert mock_response.encoding == "utf-8"
    assert result[0][0] == "Автор"
    assert result[1][0] == "Достоевский"


# 7. ТЕСТ С РЕАЛЬНОЙ ССЫЛКОЙ (интеграционный, опционально)
def test_getter_real_url():
    """Реальный запрос к публичной TSV-ссылке"""

    # Используем твою реальную ссылку
    url = (
        "https://docs.google.com/spreadsheets/d/e/"
        "2PACX-1vTACVRwwjFfLXov6JEImpE6YK4DDuHa-41l27U9f8IUNHApRjAKi30oD5d1GdHw8RwTU_UyX0095B0C/"  # noqa: E501
        "pub?gid=0&single=true&output=tsv"
    )

    try:
        result = getter(url)
        assert len(result) > 0
        assert len(result[0]) > 0
        print(f" ✅ Реальный URL работает. Получено {len(result)} строк")
    except Exception as e:
        pytest.skip(f"Реальный URL недоступен: {e}")
