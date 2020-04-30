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
    regex = '''<tr bgcolor=.*?> 
<td valign="top" align="center"> 
<table><tbody><tr><td><a href=.*?><img src=.*? border="0" width="80" height="80"></a></td></tr> 
<tr><td><a href=.*?>More Info...</a></td></tr> 
</tbody></table></td><td valign="top"> 
<a href=.*?><b>(.*?)</b></a><br> 
<table><tbody><tr><td valign="top"><table> 
<tbody><tr><td align="right" nowrap="nowrap"><b>List Price:</b></td><td align="left" nowrap="nowrap"><s>(.*?)</s></td></tr> 
<tr><td align="right" nowrap="nowrap"><b>Price:</b></td><td align="left" nowrap="nowrap"><span class="bigred"><b>(.*?)</b></span></td></tr> 
<tr><td align="right" nowrap="nowrap"><b>You Save:</b></td><td align="left" nowrap="nowrap"><span class="littleorange">(.*?)</span></td></tr> 
</tbody></table> 
</td><td valign="top"><span class="normal">(.*?)<br><a href=.*?><span class="tiny"><b>Click here to purchase.</b></span></a></span><br>'''

    items = re.findall(regex, dom, re.MULTILINE | re.DOTALL)

    all_data = []
    for item in items:
        all_data.append({
            "title": item[0].strip(),
            "list_price": item[1].strip(),
            "price": item[2].strip(),
            "saving": item[3].split(" ")[0].strip(),
            "saving_percent": item[3].split(" ")[1].replace("(", "").replace(")", "").strip(),
            "content": item[4].replace("\n", " ").strip()
        })

    return get_json(all_data)


def extract_imdb(dom):
    name = re.findall('<td class="name-overview-widget__section">.*?'
                      '<h1 class="header"> <span class="itemprop">(.*?)</span>', dom,
                      re.MULTILINE | re.DOTALL)[0].strip()

    description = re.findall('<div class="name-trivia-bio-text">.*?<div class="inline">(.*?)<span', dom,
                             re.MULTILINE | re.DOTALL)[0].strip()
    description = extract_text(description)

    film_regex = '''<div class="filmo-row .*?>
<span class="year_column">
&nbsp;(.*?)
</span>
<b><a href=.*?
>(.*?)</a></b>(.*?)</?div'''
    filmography = re.findall(film_regex, dom, re.MULTILINE | re.DOTALL)

    films = []
    for film in filmography:
        roles = film[-1].split("<br/>")
        role = ""
        if len(roles) > 1:
            role = roles[-1]

        films.append({
            "title": extract_text(film[1]).strip(),
            "year": extract_text(film[0]).strip(),
            "role": extract_text(role).strip().split("\n")[-1]
        })

    data = {
        "name": name,
        "description": description,
        "filmography": films
    }

    return get_json(data)


def run_all():
    save_dir = "../results/B/"

    filename = "../input-extraction/pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html"
    dom = get_file(filename, "utf-8")
    res = extract_rtvslo(dom)
    save_file(save_dir + "rtvslo_1.json", res)

    filename = "../input-extraction/pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    dom = get_file(filename, "utf-8")
    res = extract_rtvslo(dom)
    save_file(save_dir + "rtvslo_2.json", res)

    filename = "../input-extraction/pages/overstock.com/jewelry01.html"
    dom = get_file(filename, "iso-8859-1")
    res = extract_overstock(dom)
    save_file(save_dir + "overstock_1.json", res)

    filename = "../input-extraction/pages/overstock.com/jewelry02.html"
    dom = get_file(filename, "iso-8859-1")
    res = extract_overstock(dom)
    save_file(save_dir + "overstock_2.json", res)

    filename = "../input-extraction/pages/imdb.com/Morgan Freeman - IMDb.html"
    dom = get_file(filename, "utf-8")
    res = extract_imdb(dom)
    save_file(save_dir + "imdb_1.json", res)

    filename = "../input-extraction/pages/imdb.com/Tim Robbins - IMDb.html"
    dom = get_file(filename, "utf-8")
    res = extract_imdb(dom)
    save_file(save_dir + "imdb_2.json", res)

