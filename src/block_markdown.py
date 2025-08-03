from textnode import TextType, TextNode

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    whitespaceless_blocks = [block.strip() for block in raw_blocks]
    cleaned_blocks = list(filter(None,whitespaceless_blocks))
    return cleaned_blocks