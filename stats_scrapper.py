from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

def generate_facebook_iframes(url, width=35, height=65):
    url = urllib.parse.quote_plus(url)
    like_iframe = f"""<iframe src="https://en-gb.facebook.com/plugins/like.php?href={url}&width={width}&layout=box_count&action=like&size=small&share=false&height={height}&appId" width="{width}" height="{height}" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>""".strip()
    share_iframe = f"""<iframe src="https://en-gb.facebook.com/plugins/share_button.php?href={url}&layout=box_count&size=small&width={width}&height={height}&appId" width="{width}" height="{height}" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>""".strip()

    return {
        "like_iframe": like_iframe,
        "share_iframe": share_iframe
    }

def generate_iframe_soup(iframe):
    soup = BeautifulSoup(iframe, 'html.parser')
    tag = soup.find_all('iframe')[0]
    request = urllib.request.Request(tag['src'])
    response = urllib.request.urlopen(request)
    iframe_soup = BeautifulSoup(response, "html.parser")
    return iframe_soup

def extract_facebook_likes(iframe):
    iframe_soup = generate_iframe_soup(iframe)
    likes_count = iframe_soup.select_one('table td .inlineBlock span').text
    return likes_count

def extract_facebook_shares(iframe):
    iframe_soup = generate_iframe_soup(iframe)
    shares_count = iframe_soup.select_one('span').text
    return shares_count

def extract_facebook_comments_count(iframe):
    return shares_count


url = 'https://www.youtube.com/watch?app=desktop&v=wAuzCjipF00' # example URl

iframes = generate_facebook_iframes(url)
like_iframe = iframes["like_iframe"]
share_iframe = iframes["share_iframe"]
likes_count = extract_facebook_likes(like_iframe)
shares_count = extract_facebook_shares(share_iframe)
print(f"{url} - Likes: {likes_count} Shares: {shares_count}")
