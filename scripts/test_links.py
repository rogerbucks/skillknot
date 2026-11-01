import unittest

from links import classify, links_in


class LinksIn(unittest.TestCase):
    def test_markdown_link_and_bare_url(self):
        text = "See [a](https://example.com/a) and https://example.org/b."
        self.assertEqual(
            links_in(text), ["https://example.com/a", "https://example.org/b"]
        )

    def test_code_and_angle_brackets_end_a_link(self):
        text = "`https://example.com/x` <https://example.com/y>"
        self.assertEqual(
            links_in(text), ["https://example.com/x", "https://example.com/y"]
        )


class Classify(unittest.TestCase):
    def test_answered(self):
        self.assertEqual(classify(status=200), "ok")

    def test_holding_page_is_not_proof(self):
        self.assertEqual(classify(status=202), "unverified")

    def test_refusals_say_nothing(self):
        for status in (403, 429, 500, 503):
            self.assertEqual(classify(status=status), "unverified")
        self.assertEqual(classify(error="timed out"), "unverified")

    def test_gone(self):
        self.assertEqual(classify(status=404), "broken")
        self.assertEqual(classify(status=410), "broken")
        self.assertEqual(classify(error="no such host"), "broken")


if __name__ == "__main__":
    unittest.main()
