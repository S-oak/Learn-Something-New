"""
learn_something_new.py
-------------------
Get a random or semi-random Wikipedia article summary from the command line.

Usage:
    python learn_something_new.py           # completely random topic
    python learn_something_new.py cat      # random result from a search term
"""

import random
import sys
import wikipedia

def main():
    try:
        page, rand = get_random_topic()   
    except wikipedia.PageError:
        sys.exit("A wikipedia page could not be found. Please try again.")

    print(f"Your random topic is: {rand}.")
    print(page.summary)
    print(f"Learn more at: {page.url}")


def get_random_topic():
    if len(sys.argv) == 2:
        topic = str(sys.argv[1])
        results = wikipedia.search(topic, results=5)
        if not results:
            sys.exit("No results found for that topic.")

        max_attempts = 5
        for _ in range(max_attempts):
            rand = random.choice(results)
            try:
                page = wikipedia.page(title=rand)
                return page, rand
            except wikipedia.DisambiguationError as e:
                # Pick randomly from the disambiguation options and try again
                if e.options:
                    rand = random.choice(e.options)
                    try:
                        page = wikipedia.page(title=rand)
                        return page, rand
                    except wikipedia.DisambiguationError:
                        continue
                    except wikipedia.PageError:
                        continue
                else:
                    continue
            except wikipedia.PageError:
                continue

        sys.exit("Could not find a valid Wikipedia page from the search results.")

    else:
        rand = str(wikipedia.random())
        page = wikipedia.page(title=rand)
    
    return page, rand


if __name__ =="__main__":
    main()