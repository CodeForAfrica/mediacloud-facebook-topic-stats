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
