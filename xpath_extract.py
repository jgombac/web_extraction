from utils import *


def extract_rtvslo(dom):
    author = dom.xpath("//div[@class='author-name']/text()")[0].strip()

    time = dom.xpath("//div[@class='publish-meta']/text()")[0].strip().replace(".", "").split()
    published_time = "{}-{}-{} {}".format(time[2], get_month(time[1]), time[0], time[-1])

    title = dom.xpath("//h1/text()")[0].strip()
    subtitle = dom.xpath("//div[@class='subtitle']/text()")[0].strip()
    lead = dom.xpath("//p[@class='lead']/text()")[0].strip()
    content = "".join(
        map(lambda x: x.strip(),
            dom.xpath("//div[@class='article-body']//text()[not(ancestor::figure)]")))

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
    rows = dom.xpath("//table[@border='0' and @cellpadding='0' and @cellspacing='0' and @width='100%']//tr[@bgcolor]")

    all_data = []

    for row in rows:

        try:
            el = row.xpath("./td")[-1]

            title = el.xpath("./a/b/text()")[0]

            prices = el.xpath("./table/tbody/tr/td/table/tbody/tr/td//text()")
            list_price = prices[1]
            price = prices[3]
            saving = prices[-1].split(" ")[0]
            saving_percent = prices[-1].split(" ")[-1].replace("(", "").replace(")", "")

            content = el.xpath("./table/tbody/tr/td/span/text()")[0].strip().replace("\n", " ")

            data = {
                "title": title,
                "list_price": list_price,
                "price": price,
                "saving": saving,
                "saving_percent": saving_percent,
                "content": content
            }

            all_data.append(data)
        except Exception as e:
            pass

    return get_json(data)


def extract_imdb(dom):
    name = dom.xpath("//td[@class='name-overview-widget__section']/h1/span[@class='itemprop']/text()")[0]

    description = "".join(
        dom.xpath("//div[@class='name-trivia-bio-text']/div[@class='inline']//text()[not(ancestor::span)]")).strip()

    filmography = dom.xpath("//div[contains(@class, 'filmo-row')]")

    films = []

    for film in filmography:
        title = film.xpath("./b//text()")[0]
        year = film.xpath("./span[@class='year_column']/text()")[0].strip()
        role = film.xpath("./text()")
        if len(role) >= 4:
            role = role[3]
            if not isinstance(role, str):
                role = ""
        else:
            role = ""
        role = role.strip()
        if len(role) == 1:
            if not role[0].isalpha():
                role = ""
        films.append({
            "title": title,
            "year": year,
            "role": role.strip()
        })

    data = {
        "name": name,
        "description": description,
        "filmography": films
    }

    return get_json(data)


def run_all():
    save_dir = "results/A/"

    filename = "pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html"
    dom = get_dom(get_file(filename, "utf-8"))
    res = extract_rtvslo(dom)
    save_file(save_dir + "rtvslo_1.json", res)

    filename = "pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    dom = get_dom(get_file(filename, "utf-8"))
    res = extract_rtvslo(dom)
    save_file(save_dir + "rtvslo_2.json", res)

    filename = "pages/overstock.com/jewelry01.html"
    dom = get_dom(get_file(filename, "iso-8859-1"))
    res = extract_overstock(dom)
    save_file(save_dir + "overstock_1.json", res)

    filename = "pages/overstock.com/jewelry02.html"
    dom = get_dom(get_file(filename, "iso-8859-1"))
    res = extract_overstock(dom)
    save_file(save_dir + "overstock_2.json", res)

    filename = "pages/imdb.com/Morgan Freeman - IMDb.html"
    dom = get_dom(get_file(filename, "utf-8"))
    res = extract_imdb(dom)
    save_file(save_dir + "imdb_1.json", res)

    filename = "pages/imdb.com/Tim Robbins - IMDb.html"
    dom = get_dom(get_file(filename, "utf-8"))
    res = extract_imdb(dom)
    save_file(save_dir + "imdb_2.json", res)




