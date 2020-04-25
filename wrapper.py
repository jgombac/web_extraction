from utils import *


def generate(pages: list) -> str:
    if len(pages) < 2:
        raise Exception("Need at least 2 pages, given: " + str(len(pages)))

    start_page = pages[0]
    for page in pages[1:]:
        pass
    
    return ""


def run():
    files_rtvslo = [
        "pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
        "pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    ]
    files_overstock = [
        "pages/overstock.com/jewelry01.html",
        "pages/overstock.com/jewelry02.html"
    ]
    files_imdb = [
        "pages/imdb.com/Morgan Freeman - IMDb.html",
        "pages/imdb.com/Tim Robbins - IMDb.html"
    ]

    pages_rtvslo = [get_dom(get_file(x, "utf-8")) for x in files_rtvslo]
    pages_overstock = [get_dom(get_file(x, "iso-8859-1")) for x in files_overstock]
    pages_imdb = [get_dom(get_file(x, "utf-8")) for x in files_imdb]

    generate(pages_rtvslo)
    # generate(pages_overstock)
    # generate(pages_imdb)


if __name__ == '__main__':
    run()
