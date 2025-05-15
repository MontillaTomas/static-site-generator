import unittest

from generate_page import extract_title


class TestWebPage(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a title\n\nSome content here.\n\n## Subtitle"
        expected_title = "This is a title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_no_title(self):
        markdown = "Some content here.\n\n## Subtitle"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
