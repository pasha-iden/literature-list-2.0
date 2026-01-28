import csv
import requests
from io import StringIO

from flask import Flask, render_template

def parser():

    TSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTACVRwwjFfLXov6JEImpE6YK4DDuHa-41l27U9f8IUNHApRjAKi30oD5d1GdHw8RwTU_UyX0095B0C/pub?gid=0&single=true&output=tsv'

    # Скачиваем и декодируем
    response = requests.get(TSV_URL)
    response.encoding = 'utf-8'
    tsv_data = list(csv.reader(StringIO(response.text), delimiter='\t'))

    # Парсим
    result = []
    global_id = 0

    for col_idx in range(len(tsv_data[0])):
        column = [row[col_idx].strip() if col_idx < len(row) else '' for row in tsv_data]

        # Жанр
        genre = next((cell for cell in column if cell), None)
        if not genre:
            continue

        # Заголовок жанра
        result.append((global_id, 0, 0, genre, 0))
        global_id += 1

        # Книги
        i = 1
        book_num = 1

        while i < len(column):
            if not column[i]:
                i += 1
                continue

            # Группа одного автора
            group = []
            while i < len(column) and column[i]:
                group.append(column[i])
                i += 1

            if group:
                author = group[-1]
                books = group[:-1]

                for idx, title in enumerate(books):
                    author_display = 'еще' if idx < len(books) - 1 else author

                    result.append((
                        global_id,
                        title,
                        author_display,
                        genre,
                        book_num
                    ))

                    global_id += 1
                    book_num += 1

            if i < len(column) and not column[i]:
                i += 1

    return result


app = Flask(__name__)

@app.route('/library')
def index ():
    books = parser()

    # Выводим ВСЕ данные
    """
    for record in books:
        print(record)
    """

    return render_template("library.html", bookslistprint=books)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=1001)