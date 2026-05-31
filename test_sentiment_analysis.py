import unittest
from SentimentAnalysis import sentiment_analyzer

class TestSentimentAnalyzer(unittest.TestCase):

    def test_positive(self):
        result = sentiment_analyzer(
            "I am very happy today"
        )

        self.assertEqual(
            result["label"],
            "SENT_POSITIVE"
        )

unittest.main()