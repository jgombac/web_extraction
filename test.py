from lxml import html
import lxml
from bs4 import BeautifulSoup

test_site = '''
<html>
    <body>
        Hello
        <b>my guy</b>
        What's good
    </body>
</html>
'''

# dom = html.fromstring(test_site)
# print(lxml.etree.tostring(dom))
# for element in dom[0]:
#     print(element.tail)

dom = BeautifulSoup(test_site, features="lxml")

for i in range(len(dom.body.contents)):
    print(dom.body.contents[i])
