import argparse
import os
import sys
import webbrowser

from lxml.html import fromstring
from pathlib import Path 
from requests import get

URL = "https://news.ycombinator.com"
DIR = os.path.join(Path.home(), ".cache", "hnget")
CACHE = os.path.join(DIR, "links")

os.makedirs(DIR, exist_ok=True)

class Colors:
    BOLD = "\033[1m"
    ENDC = "\033[0m"
    FAIL = "\033[91m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    UNDERLINE = "\033[4m"
    WARNING = "\033[93m"


def html_tree(url):
    content = get(url)
    tree = fromstring(content.text)
    return tree

def comments(html_tr):
    base_url = "https://news.ycombinator.com/"
    elements = html_tr.xpath("//td[@class='subtext']/a[last()]")
    elements_hrefs = [base_url + e.get("href") for e in elements]
    return elements_hrefs

def domains(html_tr):
    return html_tr.xpath("//span[@class='sitestr']")

def links(html_tr):
    links = html_tr.xpath("//a[@class='titlelink']/@href")
    # make relative links absolute 
    for x in links:
        if x.startswith("item?id="):
            x = "https://news.ycombinator.com" + x 
    return links            

def num_comments(html_tr):
    return html_tr.xpath("//td[@class='subtext']/a[last()]")

def stories(html_tr):
    return html_tr.xpath("//a[@class='titlelink']")

def print_posts(html_tr):
    c = comments(html_tr)
    d = domains(html_tr)
    l = links(html_tr)
    n = num_comments(html_tr)
    s = stories(html_tr)

    with open(CACHE, 'w') as f:
        for idx in range(30):
            # Discussion posts don't have a domain link, but they
            # all start with 'item?id=' so this detects that and
            # inserts the Hacker News domain. 
            if l[idx].startswith("item?id="):
                d.insert(idx, "news.ycombinator.com")
            else:
                d[idx] = d[idx].text_content()
            
            # Posts with no comments are displayed in the browser as 'hide'
            # Change that to '0 commnets' here
            n[idx] = n[idx].text_content()
            if n[idx] == "hide":
                n[idx] = "0 comments"

            index_col = f"{Colors.OKCYAN}[{idx+1}]{Colors.ENDC}"
            info_col = (
                f"{s[idx].text_content()}"
                f" {Colors.OKBLUE}{d[idx]}{Colors.ENDC}"
                f" {Colors.OKGREEN}{n[idx]}{Colors.ENDC}"
            )
            row = "{:<14}{}".format(index_col, info_col)
            f.write(l[idx] + " " + c[idx] + "\n")
            print(row)


def open_urls(indices, comments):
    if comments:
        col = 1
    else:
        col = 0
    with open(CACHE, 'r') as f:
        content = f.readlines()
        for idx in indices:
            # convert 1-indexed input to 0-indexed 
            idx = int(idx) - 1
            link = content[idx].split()[col]
            webbrowser.open(link)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="hnget [OPTION]",
        description="View current stories on Hacker News.",
    )
    parser.add_argument(
        "--fetch", action="store_true", help="list stories on the front page"
    )
    parser.add_argument(
        "--open", nargs="+", help="open story link(s) in default webbrowser"
    )
    parser.add_argument(
        "--comments",
        nargs="+",
        help="open comment page link(s) in default webbrowser",
    )
    parser.add_argument(
        "--best",
        action="store_true",
        help="pull from the best stories of the week",
    )

    return parser

def run_hnget(args):
    if args.best:
        global URL
        URL = URL + "/best"
        args.fetch = True 

    if args.fetch:
        html_tr = html_tree(URL)
        print_posts(html_tr)

    if args.open:
        open_urls(args.open, False)

    if args.comments:
        open_urls(args.comments, True)

def main():
    parser = init_argparse()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    run_hnget(args)

    return 0 


if __name__ == "__main__":
    sys.exit(main())
