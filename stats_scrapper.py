from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://mediacloud.org/"
}

def generate_facebook_stats_url(url, width=35, height=65):
    url = urllib.parse.quote_plus(url)

    # Since facebook returns the aggregate of likes count, shares count and comments count in likes plugin, shares plugin and comments plugin,
    # we can use any of the plugin to get the total stats of a shared url
    stats_url = f"""https://en-gb.facebook.com/plugins/like.php?href={url}&width={width}&layout=box_count&action=like&size=small&share=false&height={height}&appId"""
    return stats_url

def generate_iframe_soup(likes_url):
    request = urllib.request.Request(likes_url, headers=headers)
    response = urllib.request.urlopen(request)
    iframe_soup = BeautifulSoup(response, "html.parser")
    return iframe_soup

def extract_facebook_stats(stats_url):
    iframe_soup = generate_iframe_soup(stats_url)
    stats_count = iframe_soup.select_one('table td .inlineBlock span').text
    if stats_count.endswith("K"): # e.g 1.2K => one thousand two hundred. We require another 100 in order to get to 1.3K so we can say the accuracy is 100 
        accuracy = 100
    elif stats_count.endswith("M"): # e.g 1.2M => one million two hundred thousand. We require another 100,000 in order to get to 1.3M so we can say the accuracy is 100,000
        accuracy = 100000
    elif stats_count.endswith("B"): # e.g 1.2B => one billion two hundred million. We require another 1,000,000 in order to get to 1.3B so we can say the accuracy is 1,000,000
        accuracy = 1000000
    else:
        accuracy = 1

    return {"count": stats_count, "accuracy": accuracy}
