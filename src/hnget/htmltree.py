from requests import get
from lxml.html import fromstring

def html_tree(url):
    content = get(url)
    tree = fromstring(content.text)
    return tree
