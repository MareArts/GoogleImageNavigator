# -*- coding: utf-8 -*-
import webbrowser as b
from bs4 import BeautifulSoup
import requests as req
import re
import json
from _collections import OrderedDict
from urllib.parse import quote
import random

# Fake a user-agent.
user_agent_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

base_url = 'https://www.google.com/search?{}&tbm=isch&tbs={}'

matcher = re.compile(r'tbs=(.*)tbo', re.UNICODE)


def get_rimg(imgurl, imgdii):
    base_url = "https://images.google.com/async/imgrc?async=q:,cidx:1,_id:irc_imgrc1,_pms:il&imgurl={}&imgdii={}"
    res = req.get(url=base_url.format(quote(imgurl), quote(imgdii)),
                  headers=user_agent_header)
    html = res.text
    capture = matcher.search(html)
    output = capture.group()[4:-13] if capture is not None else None
    print(output)
    return output

def get_initial_images(ggl_img_url):
    resp = req.get(ggl_img_url, headers=user_agent_header)
    soup = BeautifulSoup(resp.text, 'lxml')
    img_divs = soup.findAll("div", {"class": "rg_meta"})
    div_dicts = OrderedDict()  # we return in order
    for div in img_divs:
        try:
            d = json.loads(div.text)
            div_dicts[d['id']] = d
        except:
            pass
    print(div_dicts)
    return div_dicts

query = "q=" + input()
related_image = ""

incognito = True

browser = b.get()
browser.args = "%s --incognito" if incognito else "%s"

browser.open(base_url.format(query, related_image))

#TODO allow user to step back to their previous url?

while True:
    action = input()
    if action == "q":  # change query
        query = "q=" + input()
    elif action == "n":  # no query param, empty space
        query = ""
    else:
        pass
    img_dict = get_initial_images(base_url.format(query, related_image))
    related_image = None
    while related_image is None:
        k, dv = list(img_dict.items())[random.randint(0, 10 if len(img_dict) > 10 else len(img_dict))]
        related_image = get_rimg(dv['ou'], k)  # ou = original url
    browser.open(base_url.format(query, related_image))


# TODO show comparison of first search-word and new?