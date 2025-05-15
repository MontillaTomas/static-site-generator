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


def create_html_node(block: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.PARAGRAPH:
        normalized_text = re.sub(r"\s+", " ", block).strip()
        children = text_to_children(normalized_text)
        return ParentNode(tag="p", children=children)
    elif block_type == BlockType.HEADING:
        level = block.count("#")
        heading_content = block[level:].strip()
        children = text_to_children(heading_content)
        return ParentNode(tag=f"h{level}", children=children)
    elif block_type == BlockType.CODE:
        code_content = re.findall(r"```([\s\S]*?)```", block)
        if code_content:
            code = code_content[0]
            lines = [line.strip() for line in code.split("\n")]
            processed_code = "\n".join(lines[1:])
            code_node = LeafNode(tag="code", value=processed_code)
            return ParentNode(tag="pre", children=[code_node])
        return ParentNode(tag="pre", children=[LeafNode(tag="code", value="")])
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        lines = [line.strip() for line in lines]
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = "\n".join(new_lines)
        children = text_to_children(content)
        return ParentNode(tag="blockquote", children=children)
    elif block_type == BlockType.UNORDERED_LIST:
        items = block.split("\n")
        items = [item.strip() for item in items]
        items = [re.sub(r"^-\s+", "", item) for item in items]
        list_items = [
            ParentNode(tag="li", children=text_to_children(item)) for item in items
        ]
        return ParentNode(tag="ul", children=list_items)
    elif block_type == BlockType.ORDERED_LIST:
        items = block.split("\n")
        items = [item.strip() for item in items]
        items = [re.sub(r"^\d+\.\s+", "", item) for item in items]
        list_items = [
            ParentNode(tag="li", children=text_to_children(item)) for item in items
        ]
        return ParentNode(tag="ol", children=list_items)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        nodes.append(create_html_node(block, type))
    return ParentNode(tag="div", children=nodes)
