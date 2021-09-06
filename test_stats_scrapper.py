from unittest import TestCase
from stats_scrapper import StatsExtractor

class TestStatsExtractor(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.stats_extractor = StatsExtractor()

    def test_stats_get_fetched(self):
        # test that stats actually get fetched
        url_to_get_stats_for = "https://developers.facebook.com/docs/plugins/comments#configurator"
        stats = self.stats_extractor.get_stats(url_to_get_stats_for)
        assert type(stats) == dict
        assert "count" in stats
        assert "accuracy" in stats
        assert stats["count"] > 0
    
    def test_get_stats_on_invalid_url(self):
        invalid_url = "http://totally.bogus.url.123456.com"
        stats = self.stats_extractor.get_stats(invalid_url)
        assert type(stats) == dict
        assert int(stats["count"]) == 0
    
    def test_get_stats_on_a_non_url(self):
        non_url = "notaurl"
        stats = self.stats_extractor.get_stats(non_url)
        assert type(stats) == dict
        assert "Can't generate stats url for the given URL" in stats["error"]["message"]
