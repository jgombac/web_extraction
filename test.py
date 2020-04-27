import bs4
import math

class HtmlNode:
    def __init__(self, tag, attrs=list(), optional=False, repeating=False):
        self.tag = tag
        self.attrs = attrs
        self.optional = False
        self.repeating = False
        self.children = None
        self.value = None

    def add_child(self, child):
        if self.children is None:
            self.children = list()
        self.children.append(child)


def create_dom(filename):
    with open(filename, 'r') as file:
        return bs4.BeautifulSoup(file.read(), features="lxml")


def clean_newlines(dom):
    for i in range(len(dom.contents)-1, -1, -1):
        element = dom.contents[i]
        if type(element) is bs4.NavigableString:
            if str(element.string) == "\n":
                element.extract()
        elif type(element) is bs4.Tag:
            if len(element.contents) > 0:
                clean_newlines(element)


def compare_element(a, b):
    if type(a) is type(b):
        if type(a) is bs4.element.NavigableString:
            return True
        if a.name == b.name:
            if a.attrs.get("id", "") == b.attrs.get("id", ""):
                return True
    return False


def find_next_match(a, b, a_index, b_index):
    a_element = a.contents[a_index]
    for i in range(b_index, len(b.contents)):
        b_element = b.contents[i]
        if compare_element(a_element, b_element):
            return i
    return None


def generate_wrapper(a, b):
    wrap = HtmlNode(a.name)

    def traverse(a, b, wrap):
        a_index = 0
        b_index = 0
        while a_index < len(a.contents) and b_index < len(b.contents):
            a_element = a.contents[a_index]
            b_element = b.contents[b_index]
            if compare_element(a_element, b_element):
                # the elements are strings
                if type(a_element) is bs4.element.NavigableString:
                    text_element = HtmlNode("text")
                    if str(a_element.string) == str(b_element.string):
                        text_element.value = str(a_element.string)
                    else:
                        text_element.value = "#Text"
                    wrap.add_child(text_element)
                    a_index += 1
                    b_index += 1
                # elements are tags. Their content needs to be compared at a deeper level
                else:
                    tag_element = HtmlNode(a_element.name, a_element.attrs)
                    wrap.add_child(tag_element)
                    if len(a_element.contents) > 0:
                        # go deeper
                        traverse(a_element, b_element, tag_element)
                    a_index += 1
                    b_index += 1
            else:
                # element mismatch, find the index of next matching elements
                print(f"Mismatch {a_element} and {b_element}")
                match_b = find_next_match(a, b, a_index, b_index)
                match_a = find_next_match(b, a, b_index, a_index)
                skip_a = math.inf if match_a is None else match_a - a_index
                skip_b = math.inf if match_b is None else match_b - b_index
                print(f"skip a {skip_a}")
                print(f"skip b {skip_b}")
                if match_a is None and match_b is None:
                    a_index += 1
                    b_index += 1
                    continue
                if skip_a > skip_b:
                    b_index = match_b
                    continue
                else:
                    a_index = match_a
                    continue
                # TODO add all skipped elements as optional elements => convert them to HtmlElement form bs4.tag
        # TODO if the index of a tree has not exceeded the content length add those as optional elements to the end

        # TODO go through entire wrapper and check for repeating elements. Mark those as repeating
        # Maybe check repeating on mismatch
        return wrap

    return traverse(a, b, wrap)


a = create_dom("pages/test/a.html")
b = create_dom("pages/test/b.html")
# a = create_dom("pages/overstock.com/jewelry01.html")
# b = create_dom("pages/overstock.com/jewelry02.html")
clean_newlines(a)
clean_newlines(b)
# TODO real html pages contain types other than Tag and NavigateableString these currently crash the script, fix that
# print(compare_element(a.body.contents[1], b.body.contents[1]))
# print(generate_wrapper(a.body, b.body).tag)

w = generate_wrapper(a.body, b.body)
print("end")
#print(a.prettify())