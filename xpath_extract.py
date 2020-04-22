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

    print(get_json(data))


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

    print(get_json(all_data))



if __name__ == '__main__':
    # filename = "pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html"
    # dom = get_dom(get_file(filename, "utf-8"))
    # extract_rtvslo(dom)
    #
    # filename = "pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html"
    # dom = get_dom(get_file(filename, "utf-8"))
    # extract_rtvslo(dom)

    filename = "pages/overstock.com/jewelry01.html"
    dom = get_dom(get_file(filename, "iso-8859-1"))
    extract_overstock(dom)

    # filename = "pages/overstock.com/jewelry02.html"
    # dom = get_dom(get_file(filename, "iso-8859-1"))
    # extract_overstock(dom)




