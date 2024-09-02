import json

import requests
import wikipedia

version = 'ru'

WIKI_REQUEST = f'https://{version}.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
wikipedia.set_lang(version)


def get_wiki_data():
    page_correct = False
    random_article = wikipedia.random()
    while not page_correct:
        try:
            random_page = wikipedia.page(random_article)
            page_correct = True
        except wikipedia.DisambiguationError as e:
            random_article = wikipedia.random()

    title = random_page.title
    url = random_page.url
    img_link = ""
    summary = random_page.summary
    if len(random_page.images):
        response = requests.get(WIKI_REQUEST + title)
        json_data = json.loads(response.text)
        try:
            img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        except KeyError:
            img_link = ""

    return title, url, img_link, summary


if __name__ == '__main__':
    title, url, img_link, summary = get_wiki_data()