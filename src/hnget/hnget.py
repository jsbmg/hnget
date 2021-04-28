'''
Store stories and URLs from Hacker News.
'''

from htmltree import html_tree
import webbrowser

URL = 'https://news.ycombinator.com/'
URL_BEST = URL + 'best'

HTML_TR = html_tree(URL)

class Colors:
    HEADER =    '\033[95m'
    OKBLUE =    '\033[94m'
    OKCYAN =    '\033[96m'
    OKGREEN =   '\033[92m'
    WARNING =   '\033[93m'
    FAIL =      '\033[91m'
    ENDC =      '\033[0m'
    BOLD =      '\033[1m'
    UNDERLINE = '\033[4m'

def links():
    return HTML_TR.xpath("//a[@class='storylink']/@href")

def stories():
    return HTML_TR.xpath("//a[@class='storylink']")

def comments():
    base_url = 'https://news.ycombinator.com/'
    elements = HTML_TR.xpath("//tr/td/a[3]")
    elements_hrefs = [base_url + e.get('href') for e in elements]
    return elements_hrefs

def domains():
    return HTML_TR.xpath("//td/span/a/span")

def print_posts():
    st, do, li = stories(), domains(), links()
    for idx, s in enumerate(st):
        spaces = " "
        if idx < 10:
            spaces = "  "
        text = f"{Colors.OKGREEN}[{idx}]{Colors.ENDC}{spaces}{s.text_content()}"
        print(f"{text}\n     {Colors.OKBLUE}[{do[idx].text_content()}]{Colors.ENDC}")

def choose_stories():
    print("Enter numbers corresponding to stories to view:")
    choices = input("> ")
    result = [int(s) for s in choices.split(' ')]
    return result

def view_story():
    choices = choose_stories()
    li = links()
    for ch in choices:
        webbrowser.open(li[ch])

def view_comments():
    choices = choose_stories()
    ur = comments()
    for ch in choices:
        webbrowser.open(ur[ch])
