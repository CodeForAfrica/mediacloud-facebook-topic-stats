from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
    "Accept-Language": "en-US,en;q=0.5",
}

class StatsExtractor:
    def _generate_facebook_stats_url(self, url: str, width:int=35, height:int=65) -> str:
        url = urllib.parse.quote_plus(url)

        # Since facebook returns the aggregate of likes count, shares count and comments count in likes plugin, shares plugin and comments plugin,
        # we can use any of the plugin to get the total stats of a shared url
        stats_url = f"""https://en-gb.facebook.com/plugins/like.php?href={url}&width={width}&layout=box_count&action=like&size=small&share=false&height={height}&appId"""
        return stats_url

    def _generate_iframe_soup(self, likes_url:str, referer_url:str) -> BeautifulSoup:
        headers["Referer"] = referer_url
        request = urllib.request.Request(likes_url, headers=headers)
        response = urllib.request.urlopen(request)
        iframe_soup = BeautifulSoup(response, "html.parser")
        return iframe_soup

    def _extract_facebook_stats(self, stats_url:str, referer_url:str) -> dict:
        iframe_soup = self._generate_iframe_soup(stats_url, referer_url)
        stats_count = iframe_soup.select_one('table td .inlineBlock span').text
        if stats_count.endswith("K"): # e.g 1.2K => one thousand two hundred. We require another 100 in order to get to 1.3K so we can say the accuracy is 100 
            accuracy = 100
            stats_count = int(stats_count[:-1]) * 1000
            
        elif stats_count.endswith("M"): # e.g 1.2M => one million two hundred thousand. We require another 100,000 in order to get to 1.3M so we can say the accuracy is 100,000
            accuracy = 100000
            stats_count = int(stats_count[:-1]) * 1000000
        elif stats_count.endswith("B"): # e.g 1.2B => one billion two hundred million. We require another 1,000,000 in order to get to 1.3B so we can say the accuracy is 1,000,000
            accuracy = 1000000
            stats_count = int(stats_count[:-1]) * 1000000000
        else:
            accuracy = 1

        return {"count": stats_count, "accuracy": accuracy}

    def get_stats(self, url_to_get_stats_for: str) -> dict:
        stats_url = self._generate_facebook_stats_url(url_to_get_stats_for)
        stats = self._extract_facebook_stats(stats_url, url_to_get_stats_for)
        return stats
