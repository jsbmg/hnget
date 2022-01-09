import argparse
import webbrowser

from lxml.html import fromstring
from requests import get


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
    return html_tr.xpath("//a[@class='titlelink']/@href")


def num_comments(html_tr):
    return html_tr.xpath("//td[@class='subtext']/a[last()]")


def stories(html_tr):
    return html_tr.xpath("//a[@class='titlelink']")


def print_posts(html_tr):
    all_stories = stories(html_tr)
    all_domains = domains(html_tr)
    all_num_comments = num_comments(html_tr)
    all_links = links(html_tr)
    for idx in range(30):
        if (
            len(all_domains) < idx + 1
        ):  # can occur if final story is a self post
            all_domains.insert(idx, "news.ycombinator.com")
        # Hacker News' "self posts" don't have a domain,  
        # so give them news.ycombinator.com 
        if all_links[idx].startswith("item?id="):
            all_domains.insert(idx, "news.ycombinator.com")
        else:
            all_domains[idx] = all_domains[idx].text_content()

        index_column = f"{Colors.OKCYAN}[{idx+1}]{Colors.ENDC}"
        info_column = (
            f"{all_stories[idx].text_content()}"
            f" {Colors.OKBLUE}{all_domains[idx]}{Colors.ENDC}"
            f" {Colors.OKGREEN}{all_num_comments[idx].text_content()}{Colors.ENDC}"
        )
        row = "{:<14}{}".format(index_column, info_column)
        print(row)


def open_url(entry, urls):
    entry = int(entry) - 1
    if urls[entry].startswith("item?id="):
        urls[entry] = "news.ycombinator.com/" + urls[entry]
    webbrowser.open(urls[entry])


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


def main():
    url = "https://news.ycombinator.com"
    parser = init_argparse()
    args = parser.parse_args()

    if args.best:
        url = url + "/best"
    html_tr = html_tree(url)

    if args.fetch:
        print_posts(html_tr)

    if args.open:
        urls = links(html_tr)
        for entry in args.open:
            open_url(entry, urls)

    if args.comments:
        urls = comments(html_tr)
        for entry in args.comments:
            open_url(entry, urls)


if __name__ == "__main__":
    main()
