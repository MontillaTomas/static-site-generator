from enum import Enum

from htmlnode import HTMLNode, LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if isinstance(value, TextNode):
            return (
                self.text == value.text
                and self.text_type == value.text_type
                and self.url == value.url
            )
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(text_node.text, "b")
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(text_node.text, "i")
    if text_node.text_type == TextType.CODE:
        return LeafNode(text_node.text, "code")
    if text_node.text_type == TextType.LINK:
        return LeafNode(
            text_node.text,
            "a",
            {"href": text_node.url},
        )
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            text_node.text,
            "img",
            {"src": text_node.url, "alt": text_node.text},
        )
    raise ValueError("Invalid text type")
