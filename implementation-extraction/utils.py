from lxml import html
from json import dumps
import re


def get_file(filename, encoding):
    with open(filename, 'r', encoding=encoding) as f:
        return f.read()


def save_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(data)


def get_dom(content_str):
    return html.fromstring(content_str)


def get_json(dictionary):
    return dumps(dictionary, indent=2, ensure_ascii=False)


def extract_text(html_string):
    return re.compile('<.*?>').sub("", html_string)


def get_month(month):
    months = {
        "januar": 1,
        "februar": 2,
        "marec": 3,
        "april": 4,
        "maj": 5,
        "junij": 6,
        "julij": 7,
        "august": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "december": 12
    }
    return months[month]
