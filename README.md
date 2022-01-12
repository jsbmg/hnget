#  hnget - Hacker News web scraper

A commandline program for browsing [Hacker News](https://news.ycombinator.com).

![Alt text](/extras/screen.png?raw=true "hnget screenshot")

## Usage 

`hnget --fetch (--f)`

Print the top 30 posts on Hacker News, enumerated. `--fetch` takes an optional integer value to specify different pages of the results. 

`hnget --open (--o) [NUMS...]`

Open stories in default web browser. Multiple values are
accepted. Default web browser can be set with `$BROWSER`.

`hnget --comments (--o) [NUMS...]`

Like `--open`, but view the comment page(s) instead.

`hnget --fetch --best`

View the top posts for the week instead of the current front page.

## Installation

With Pypi:

`$ pip install hnget`

Manually:

$ `git clone https://github.com/jsbmg/hnget`

$ `cd hnget`

$ `pip install . pyproject.toml`
