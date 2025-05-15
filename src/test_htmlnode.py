import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("div", "Hello, World!", None, {"class": "greeting"})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html_with_one_prop(self):
        node = HTMLNode("div", "Hello, World!", None, {"class": "greeting"})
        self.assertEqual(node.props_to_html(), ' class="greeting"')

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            "div", "Hello, World!", None, {"class": "greeting", "id": "main"}
        )
        self.assertEqual(node.props_to_html(), ' class="greeting" id="main"')

    def test_props_to_html_with_no_props(self):
        node = HTMLNode("div", "Hello, World!")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("div", "Hello, World!", None, {"class": "greeting"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=div, value=Hello, World!, children=None, props={'class': 'greeting'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode(tag="span", value="Hello, world!")
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode(tag="p", value=None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_with_props(self):
        node = LeafNode(
            tag="p",
            value="Hello, world!",
            props={
                "class": "greeting",
                "id": "main-greeting",
                "data-test": "test-value",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<p class="greeting" id="main-greeting" data-test="test-value">Hello, world!</p>',
        )

    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(None, [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_props(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )


if __name__ == "__main__":
    unittest.main()
