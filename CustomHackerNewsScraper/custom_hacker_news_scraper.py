# Imports
import sys
import pprint
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Please make sure to install requests and beautifulsoup4 libraries first: use 'pip install requests' and 'pip install beautifulsoup4' commands")
    sys.exit()


# Functions
def get_hacker_news_pages(number_of_pages):
    all_links = []
    all_subtexts = []
    url = "https://news.ycombinator.com/news"

    for i in range(1, number_of_pages + 1):
        if i != 1:
            url = "https://news.ycombinator.com/news" + f"?p={i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select(".storylink")
        subtexts = soup.select(".subtext") # To avoid articles without votes
        all_links += links
        all_subtexts += subtexts

    return all_links, all_subtexts


def create_custom_hacker_news(links, subtexts, minimum_score):
    wanted_hacker_news = []
    for i in range(len(links)):
        title = links[i].getText()
        href = links[i].get("href", None) # Get the link, else None
        vote = subtexts.select(".score")
        if len(vote): # Not an empty list
            points = int(vote[0].getText().replace(" points", "")) # Replace the suffix to make the string numeric
            if points >= minimum_score:
                wanted_hacker_news.append({"title": title, "link": href, "votes": points})

    return sort_stories_by_votes(wanted_hacker_news)


def sort_stories_by_votes(wanted_hacker_news):
    return sorted(wanted_hacker_news, key = lambda story: story["votes"], reverse = True) # Sorting the dicts


# Validations
try:
    if len(sys.argv) > 3:
        raise IOError(f"Arguments Error - too much arguments:\n{sys.argv[0]} [Minimum Count Of Votes (score of an articles to select)] [Number of pages]")
    if len(sys.argv) < 3:
        raise IOError(f"Arguments Error - not enough arguments:\n{sys.argv[0]} [Minimum Count Of Votes (score of an articles to select)] [Number of pages]")

    try:
        minimum_score = int(sys.argv[1])
        number_of_pages = int(sys.argv[2])
    except TypeError as e:
        raise TypeError(f"Arguments Type Error - not an integer: Minimum Count Of Votes and Number Of Pages must be an unsigned integers")

    if minimum_score < 0 or number_of_pages < 0:
        raise ValueError(f"Arguments Value Error - not an unsigned integer: Minimum Count Of Votes and Number Of Pages must be an unsigned integers")

except IOError as e:
    print(e)
    sys.exit()
except TypeError as e:
    print(e)
    sys.exit()
except ValueError as e:
    print(e)
    sys.exit()


# Processing
links, subtexts = get_hacker_news_pages(number_of_pages)
news_list = create_custom_hacker_news(links, subtexts, minimum_score)
pprint.pprint(news_list)