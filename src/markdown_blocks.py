import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown: str) -> BlockType:
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    elif re.match(r"```[\s\S]*?```", markdown):
        return BlockType.CODE
    elif re.match(r"^> ", markdown):
        return BlockType.QUOTE
    elif re.match(r"^-\s", markdown):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\.\s", markdown):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def paragraph_to_html_node(paragraph: str) -> HTMLNode:
    normalized_text = re.sub(r"\s+", " ", paragraph).strip()
    children = text_to_children(normalized_text)
    if not children:
        return LeafNode(tag="p", value="")
    return ParentNode(tag="p", children=children)


def heading_to_html_node(heading: str) -> HTMLNode:
    level = heading.count("#")
    heading_content = heading[level:].strip()
    children = text_to_children(heading_content)
    if not children:
        return LeafNode(tag=f"h{level}", value="")
    return ParentNode(tag=f"h{level}", children=children)


def code_to_html_node(code: str) -> HTMLNode:
    code_content = re.findall(r"```([\s\S]*?)```", code)
    if code_content:
        code = code_content[0]
        lines = [line.strip() for line in code.split("\n")]
        processed_code = "\n".join(lines[1:])
        code_node = LeafNode(tag="code", value=processed_code)
        return ParentNode(tag="pre", children=[code_node])
    return ParentNode(tag="pre", children=[LeafNode(tag="code", value="")])


def quote_to_html_node(quote: str) -> HTMLNode:
    lines = quote.split("\n")
    lines = [line.strip() for line in lines]
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    if not children:
        return LeafNode(tag="blockquote", value="")
    return ParentNode(tag="blockquote", children=children)


def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    items = [item.strip() for item in items]
    items = [re.sub(r"^-\s", "", item) for item in items]
    list_items = [
        ParentNode(tag="li", children=text_to_children(item)) for item in items
    ]
    list_items = []
    for item in items:
        children = text_to_children(item)
        if not children:
            list_items.append(LeafNode(tag="li", value=""))
        else:
            list_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=list_items)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    items = [item.strip() for item in items]
    items = [re.sub(r"^\d+\.\s+", "", item) for item in items]
    list_items = [
        ParentNode(tag="li", children=text_to_children(item)) for item in items
    ]
    return ParentNode(tag="ol", children=list_items)


def create_html_node(block: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        nodes.append(create_html_node(block, type))
    return ParentNode(tag="div", children=nodes)
