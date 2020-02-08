# NLP Drive Thru
# This is a webscrpaing script
# to get the list of URLs
# for restaurant menus.

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json

RESTAURANT_LIST_URL = "https://www.fastfoodmenuprices.com/all-restaurants/"

def get_url(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error with request')
        return None


def good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def main():
    raw_html = get_url(RESTAURANT_LIST_URL)
    html = BeautifulSoup(raw_html, 'html.parser')
    links = []

    print("Getting restaurant menu links from " + RESTAURANT_LIST_URL)

    menu_left = html.find("ul")
    li_tags = menu_left.find_all("li")
    
    for li in li_tags:        
        a = li.find("a")        
        href = a.get("href")
        if "-prices" in href:
            links.append(href)

    link_dict = { "links": links }
    
    with open('menu_links.json', 'w') as json_file:
        json.dump(link_dict, json_file)

if __name__ == '__main__':
    main()
    
