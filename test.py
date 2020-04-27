import bs4


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
        elif len(element.contents) > 0:
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
                print(f"match a {match_a}")
                print(f"match b {match_b}")
                break
                # TODO add all skipped elements as optional elements => convert them to HtmlElement form bs4.tag
        # TODO if the index of a tree has not exceeded the content length add those as optional elements to the end

        # TODO go through entire wrapper and check for repeating elements. Mark those as repeating
        return wrap

    return traverse(a, b, wrap)


a = create_dom("pages/test/a.html")
c = create_dom("pages/test/c.html")
clean_newlines(a)
clean_newlines(c)

# print(compare_element(a.body.contents[1], b.body.contents[1]))
# print(generate_wrapper(a.body, b.body).tag)

w = generate_wrapper(a.body, c.body)
print("end")
#print(a.prettify())