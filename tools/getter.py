import csv
import requests
from io import StringIO


def getter(TSV_URL: str):

    # Скачиваем и декодируем
    response = requests.get(TSV_URL)
    response.encoding = "utf-8"
    response.raise_for_status()
    tsv_data = list(csv.reader(StringIO(response.text), delimiter="\t"))

    return tsv_data


if __name__ == "__main__":
    pass
