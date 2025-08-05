import textwrap
from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    whitespaceless_blocks = [block.strip() for block in raw_blocks]
    cleaned_blocks = list(filter(None,whitespaceless_blocks))
    return cleaned_blocks

def block_to_block_type(text):
    split_text = [line.strip() for line in text.split("\n")]

    heading_string = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    if text.startswith(heading_string):
        return BlockType.HEADING
    
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE

    if text.startswith(">"):
        for line in split_text:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if text.startswith("- "):
        for line in split_text:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if text.startswith("1. "):
        i = 1
        for line in split_text:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html(block)
        case _:
            raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = [line.strip() for line in block.split("\n")]
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    if block.startswith("# "):
        level = 1
    elif block.startswith("## "):
        level = 2
    elif block.startswith("### "):
        level = 3
    elif block.startswith("#### "):
        level = 4
    elif block.startswith("##### "):
        level = 5
    elif block.startswith("###### "):
        level = 6
    else:
        raise ValueError("Invalid Heading Level")
    
    text = block[level + 1 :].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)
    
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    lines = block.split("\n")
    content_lines = lines[1:-1]
    code_block = "\n".join(content_lines)  + "\n"
    code_block = textwrap.dedent(code_block)
    raw_text_node = TextNode(code_block,TextType.TEXT, None)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html(block):
    lines = block.split("\n")
    new_line = []
    for line in lines:
        line = line.strip()
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_line.append(line[1:].strip())
    paragraph = " ".join(new_line)
    children = text_to_children(paragraph)
    return ParentNode("blockquote", children)

def unordered_list_to_html(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        line = line.strip()
        if not line.startswith("- "):
            raise ValueError("invalid unordered list block")
        text = line[2:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children)) 
    return ParentNode("ul", html_items)

def ordered_list_to_html(block):
    lines = block.split("\n")
    html_items = []
    i = 1
    for line in lines:
        line = line.strip()
        if not line.startswith(f"{i}. "):
            raise ValueError("invalid ordered list block")
        text = line[len(f"{i}. "):].strip()
        i += 1
        children = text_to_children(text)
        html_items.append(ParentNode("li", children)) 
    return ParentNode("ol", html_items)
