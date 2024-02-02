import requests
from bs4 import BeautifulSoup
from lxml import html

# from ims.models import Link


def scrape_with_xpath(url, xpath):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    tree = html.fromstring(response.text)

    elements = tree.xpath(xpath)
    return [element.text.strip() for element in elements if element.text]

