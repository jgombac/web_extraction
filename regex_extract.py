from utils import *
import re

def extract_rtvslo(dom):
    author = re.findall('<div class="author-name">(.*?)</div>', dom)[0]

    time = re.findall('<div class="publish-meta">(.*?)<br>', dom, re.MULTILINE | re.DOTALL)[0].strip()\
        .replace(".", "").split()
    published_time = "{}-{}-{} {}".format(time[2], get_month(time[1]), time[0], time[-1])

    title = re.findall('<h1>(.*?)</h1>', dom, re.MULTILINE | re.DOTALL)[0].strip()
    subtitle = re.findall('<div class="subtitle">(.*?)</div>', dom, re.MULTILINE | re.DOTALL)[0].strip()
    lead = re.findall('<p class="lead">(.*?)</p>', dom, re.MULTILINE | re.DOTALL)[0].strip()

    content_dom = re.findall('<article class="article">(.*?)</article>', dom, re.MULTILINE | re.DOTALL)[0]
    remove = re.findall('<figure .*?>.*?</figure>', content_dom, re.MULTILINE | re.DOTALL)
    for x in remove:
        content_dom = content_dom.replace(x, "")
    content = extract_text(content_dom).strip()

    data = {
        "author": author,
        "published_time": published_time,
        "title": title,
        "subtitle": subtitle,
        "lead": lead,
        "content": content
    }

    return get_json(data)




def extract_overstock(dom):
    pass

def extract_imdb(dom):
    pass


def run_all():
    save_dir = "results/B/"

    filename = "pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html"
    dom = get_file(filename, "utf-8")
    res = extract_rtvslo(dom)
    save_file(save_dir + "rtvslo_1.json", res)

    filename = "pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    dom = get_file(filename, "utf-8")
    res = extract_rtvslo(dom)
    save_file(save_dir + "rtvslo_2.json", res)


if __name__ == '__main__':
    filename = "pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html"
    dom = get_file(filename, "utf-8")
    x = extract_rtvslo(dom)
    print(x)

    filename = "pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    dom = get_file(filename, "utf-8")
    x = extract_rtvslo(dom)
    print(x)

