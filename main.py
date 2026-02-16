from flask import Flask, render_template
from tools.parser import parser
from tools.getter import getter

app = Flask(__name__)

TSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTACVRwwjFfLXov6JEImpE6YK4DDuHa-41l27U9f8IUNHApRjAKi30oD5d1GdHw8RwTU_UyX0095B0C/"  # noqa: E501
    "pub?gid=0&single=true&output=tsv"
)


@app.route("/library")
def index():
    books = parser(getter(TSV_URL))

    # Выводим ВСЕ данные
    """
    for record in books:
        print(record)
    """

    return render_template("library.html", bookslistprint=books)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
