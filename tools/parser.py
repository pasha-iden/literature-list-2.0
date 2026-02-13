def parser(tsv_data: list):

    if not tsv_data or not tsv_data[0]:
        return []

    # Парсим
    result = []
    global_id = 0

    for col_idx in range(len(tsv_data[0])):
        column = [
            row[col_idx].strip() if col_idx < len(row) else ""
            for row in tsv_data  # noqa: E501
        ]

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
                    author_display = "еще" if idx < len(books) - 1 else author

                    result.append(
                        (global_id, title, author_display, genre, book_num)
                    )  # noqa: E501

                    global_id += 1
                    book_num += 1

            if i < len(column) and not column[i]:
                i += 1

    return result


if __name__ == "__main__":
    pass
