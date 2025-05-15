import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_unmatched(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_split_nodes_delimiter_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 0)

    def test_split_nodes_with_two_delimiters(self):
        node = TextNode(
            "This is text with a `code block` and another `code block`", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "code block")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_split_nodes_with_multiple_nodes(self):
        node1 = TextNode("This is text with a `code block`", TextType.TEXT)
        node2 = TextNode(" and another `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "code block")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_with_exclamation(self):
        matches = extract_markdown_links(
            "This is text with a ![link](https://www.boot.dev)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev) and another [link](https://www.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://www.boot.dev"),
                ("link", "https://www.boot.dev"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_with_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, nodes)

    def test_text_to_textnodes_with_empty_string(self):
        text = ""
        expected_nodes = []
        nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, nodes)


if __name__ == "__main__":
    unittest.main()
