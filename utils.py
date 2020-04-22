from lxml import html
from json import dumps


def get_file(filename, encoding):
    with open (filename, 'r', encoding=encoding) as f:
        return f.read()


def get_dom(content_str):
    return html.fromstring(content_str)


def get_json(dictionary):
    return dumps(dictionary, indent=2, ensure_ascii=False)


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
