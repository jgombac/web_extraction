import bs4
import math
import chardet
from utils import list_to_str


class HtmlNode:
    def __init__(self, tag, attrs=None, optional=False, repeating=False):
        if attrs is None:
            attrs = dict()
        self.tag = tag
        self.attrs = attrs
        self.optional = optional
        self.repeating = repeating
        # Was it removed due to being a repeated element
        self.removed = False
        self.children = []
        self.value = None

    def __repr__(self):
        return self.stringify()

    def __eq__(self, other):
        if self.tag != other.tag:
            return False

        if len(self.children) != len(other.children):
            return False

        if len(self.attrs) != len(other.attrs):
            return False

        # If we got to here, we know that they have the same number of attributes
        for key in self.attrs:
            if key not in other.attrs:
                return False

            if self.attrs[key] != other.attrs[key]:
                return False

        # If we got to here, we know that they have the same amount of children
        for i in range(len(self.children)):
            if self.children[i] != other.children[i]:
                return False

        return self.value == other.value

    def add_child(self, child):
        self.children.append(child)

    def is_empty_text(self):
        return self.tag == "text" and self.value is None

    def stringify(self, depth=0):
        tabs = ""
        for i in range(depth):
            tabs += "\t"

        if self.tag == "text":
            if self.value is None:
                return ""
            string = self.value
            for c in self.children:
                if c.removed or c.is_empty_text():
                    continue
                string += c.stringify(depth + 1)

            regex_bl = ""
            regex_br = ""
            regex_symbol = ""
            if self.optional:
                regex_bl = "("
                regex_br = ")"
                regex_symbol = "?"
            if self.repeating:
                regex_bl = "("
                regex_br = ")"
                regex_symbol = "+"
            string = f"{tabs}{regex_bl}{string}{regex_br}{regex_symbol}"

        else:
            attrs_list = ""
            for attr_name in self.attrs:
                if type(self.attrs[attr_name]) is list:
                    attr_string = list_to_str(self.attrs[attr_name])
                else:
                    attr_string = self.attrs[attr_name]
                attrs_list += f' {attr_name}="{attr_string}"'
            opening_tag = f"<{self.tag}{attrs_list}>"
            closing_tag = f"</{self.tag}>"
            children_string = ""
            regex_bl = ""
            regex_br = ""
            regex_symbol = ""
            if self.optional:
                regex_bl = "("
                regex_br = ")"
                regex_symbol = "?"
            if self.repeating:
                regex_bl = "("
                regex_br = ")"
                regex_symbol = "+"

            if len(self.children) > 0:
                if len(self.children) == 1 and self.children[0].tag == "text" and not self.children[0].is_empty_text():
                    string = f"{tabs}{regex_bl}{opening_tag}{self.children[0].stringify()}{closing_tag}{regex_br}{regex_symbol}"
                else:
                    for c in self.children:
                        if c.removed or c.is_empty_text():
                            continue
                        children_string += c.stringify(depth + 1) + "\n"
                    string = f"{tabs}{regex_bl}{opening_tag}\n{children_string}{tabs}{closing_tag}{regex_br}{regex_symbol}"
            else:
                string = f"{tabs}{regex_bl}{opening_tag}{closing_tag}{regex_br}{regex_symbol}"

        return string


def create_dom(filename):
    with open(filename, 'rb') as f:
        charset = chardet.detect(f.read())
        print(charset)
    with open(filename, 'r', encoding=charset['encoding']) as file:
        print(file.encoding)
        return bs4.BeautifulSoup(file.read(), features="lxml")


# removes any non Tag or Text elements. Also removes empty Text elements that just contain a newline
def clean_dom(dom):
    for i in range(len(dom.contents)-1, -1, -1):
        element = dom.contents[i]
        if type(element) is not bs4.Tag and type(element) is not bs4.NavigableString:
            element.extract()
            continue
        if type(element) is bs4.NavigableString:
            if str(element.string) == "\n":
                element.extract()
        elif type(element) is bs4.Tag:
            if len(element.contents) > 0:
                clean_dom(element)


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


def find_repeating(wrapper: HtmlNode):
    if len(wrapper.children) < 2:
        return

    current = wrapper.children[0]
    for child in wrapper.children[1:]:
        if current == child:
            current.repeating = True
            child.repeating = True
            child.removed = True

        find_repeating(child)
        current = child

    print("done")


def add_optional_child(wrap, child):
    # TODO: Add depth checking
    if type(child) is bs4.element.NavigableString:
        wrap.add_child(HtmlNode("text", optional=True))
    else:
        wrap.add_child(HtmlNode(child.name, child.attrs, optional=True))


def generate_wrapper(a, b):
    wrap = HtmlNode(a.name)
    matches = 0
    mismatches = 0
    interesting_data = 0

    def traverse(a, b, wrap):
        nonlocal matches
        nonlocal mismatches
        nonlocal interesting_data
        a_index = 0
        b_index = 0
        while a_index < len(a.contents) and b_index < len(b.contents):
            a_element = a.contents[a_index]
            b_element = b.contents[b_index]
            if compare_element(a_element, b_element):
                matches += 1
                # the elements are strings
                if type(a_element) is bs4.element.NavigableString:
                    text_element = HtmlNode("text")
                    if str(a_element.string) == str(b_element.string):
                        text_element.value = str(a_element.string)
                    else:
                        text_element.value = "#Text"
                        interesting_data += 1
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
                mismatches += 1
                # element mismatch, find the index of next matching elements
                print(f"Mismatch {a_element} and {b_element}")
                match_b = find_next_match(a, b, a_index, b_index)
                match_a = find_next_match(b, a, b_index, a_index)
                skip_a = math.inf if match_a is None else match_a - a_index
                skip_b = math.inf if match_b is None else match_b - b_index
                print(f"skip a {skip_a}")
                print(f"skip b {skip_b}")
                if match_a is None and match_b is None:
                    add_optional_child(wrap, a.contents[a_index])
                    add_optional_child(wrap, b.contents[b_index])
                    a_index += 1
                    b_index += 1
                    continue
                if skip_a > skip_b:
                    for i in range(b_index, match_b):
                        add_optional_child(wrap, b.contents[i])
                    b_index = match_b
                    continue
                else:
                    for i in range(a_index, match_a):
                        add_optional_child(wrap, a.contents[i])
                    a_index = match_a
                    continue

        # TODO if the index of a tree has not exceeded the content length add those as optional elements to the end
        if a_index < len(a.contents) - 1:
            for i in range(a_index, len(a.contents)):
                add_optional_child(wrap, a.contents[i])

        if b_index < len(b.contents) - 1:
            for i in range(b_index, len(b.contents)):
                add_optional_child(wrap, b.contents[i])

        find_repeating(wrap)
        return wrap
    traverse(a, b, wrap)
    print(f"Matches: {matches}")
    print(f"Mismatches: {mismatches}")
    print(f"Interesting data: {interesting_data}")
    return wrap


a = create_dom("pages/test/a.html")
b = create_dom("pages/test/b.html")
# a = create_dom("pages/overstock.com/jewelry01.html")
# b = create_dom("pages/overstock.com/jewelry02.html")
# a = create_dom("pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
# b = create_dom("pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")
clean_dom(a)
clean_dom(b)
print(compare_element(a.body.contents[1], b.body.contents[1]))
print(generate_wrapper(a.body, b.body).tag)

w = generate_wrapper(a.body, b.body)
print("end")
# TODO output the wrapper w
print(w.stringify())
