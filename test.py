from lxml import html

test_site = '''
<html>
    <body>
        Hello
        <b>my guy</b>
        What's good
    </body>
</html>
'''

dom = html.fromstring(test_site)

print(len(dom[0]))