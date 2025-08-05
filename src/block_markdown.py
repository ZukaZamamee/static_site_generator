from enum import Enum

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
    split_text = text.split("\n")

    heading_string = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    if text.startswith(heading_string):
        return BlockType.HEADING
    
    if len(split_text) > 1 and split_text[0].startswith("```") and split_text[-1].startswith("```"):
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