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

# make request for url
def get_url(url):
    try:
        with closing(get(url, stream=True)) as resp:
            # make sure response is good before continuing
            if good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error with request')
        return None

# Check that response status is 200
# and contains html
def good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

# Get all the restaurant menu links
# from the main page list
def get_menu_links(outp):
    # Get raw html with request
    raw_html = get_url(RESTAURANT_LIST_URL)
    html = BeautifulSoup(raw_html, 'html.parser')
    links = []

    print("Getting restaurant menu links from " + RESTAURANT_LIST_URL)

    # Menu links have a restaurant name and -prices in the link
    # They are organized in a list
    menu_left = html.find("ul")
    li_tags = menu_left.find_all("li")
    
    # For each list item, get the link
    for li in li_tags:        
        a = li.find("a")        
        href = a.get("href")
        if "-prices" in href:
            links.append(href)

    # populate a dictionary
    link_dict = { "links": links }
    
    # dump dictionary to json
    if outp:
        with open('menu_links.json', 'w') as json_file:
            json.dump(link_dict, json_file)

    return link_dict

# Parse menus from menu_links into dictionary
# that includes names, prices, quantities
def get_menus(menu_links):
    menu_dict = dict()

    # For each restaurant link, parse the menu table
    for link in menu_links["links"]:
        print("Getting menu from " + link)
        raw_html = get_url(link)
        html = BeautifulSoup(raw_html, 'html.parser')

        # A list of menu items
        items_list = []
        tbody = html.find("tbody")
        tr_tags = tbody.find_all("tr")

        # get the restaurant name from the URL
        restaurant = link[35:-8]

        # menu items have a category like:
        # "Beverages, snacks, breakfast"
        category = None

        # For each table row
        for tr in tr_tags:
            td_tags = tr.find_all("td")

            # Some table rows are headers
            # for categories
            if len(td_tags) == 1:
                h2 = td_tags[0].find("h2")

                if h2 != None:
                    category = h2.text

            # otherwise it should have an item
            # with 3 columns: item, size, price
            elif len(td_tags) == 3:
                item_dict = dict()
                attr_dict = dict()
                attr_dict["category"] = category
                attr_dict["size"] = td_tags[1].text
                attr_dict["price"] = td_tags[2].text[1:]
                item_dict[td_tags[0].text] = attr_dict
                items_list.append(item_dict)

        # add the list of items to this restaurant in the dict
        menu_dict[restaurant] = items_list

    # output to JSON
    with open('menus.json', 'w') as json_file:
        json.dump(menu_dict, json_file)

    return menu_dict

def main():
    get_menus(get_menu_links(False))

if __name__ == '__main__':
    main()
    
