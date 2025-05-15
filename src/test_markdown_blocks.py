import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_block_to_heading(self):
        md = "# This is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_to_block_to_six_heading(self):
        md = "###### This is a six heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_code(self):
        md = "```python\nprint('Hello, World!')\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_quote(self):
        md = "> This is a quote"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_unordered_list(self):
        md = "- Item 1\n- Item 2"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_ordered_list(self):
        md = "1. Item 1\n2. Item 2"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_paragraph(self):
        md = "This is a paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_empty(self):
        md = ""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_invalid_heading(self):
        md = "##This is not a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html, expected_html)

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(
            html,
            expected_html,
        )

    def test_heading_h1(self):
        md = """
    # This is a heading
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h1>This is a heading</h1></div>"
        self.assertEqual(html, expected_html)

    def test_heading_h6(self):
        md = """
    ###### This is a six heading
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h6>This is a six heading</h6></div>"
        self.assertEqual(html, expected_html)

    def test_quote(self):
        md = """
    > This is a quote
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><blockquote>This is a quote</blockquote></div>"
        self.assertEqual(html, expected_html)

    def test_double_quote(self):
        md = """
    > This is a quote
    > This is a second quote
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><blockquote>This is a quote\nThis is a second quote</blockquote></div>"
        self.assertEqual(html, expected_html)

    def test_unordered_list(self):
        md = """
    - Item 1
    - Item 2
    - Item 3
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )
        self.assertEqual(html, expected_html)

    def test_ordered_list(self):
        md = """
    1. Item 1
    2. Item 2
    3. Item 3
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>"
        )
        self.assertEqual(html, expected_html)


if __name__ == "__main__":
    unittest.main()
