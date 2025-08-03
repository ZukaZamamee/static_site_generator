import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node) 
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError(f"Invailid Markdown: Missing closing {delimiter}")
        for index, item in enumerate(split_node):
            if item == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(item, TextType.TEXT))
            else:
                new_nodes.append(TextNode(item, text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)

        if len(extracted_images) == 0:
            new_nodes.append(node) 
            continue

        current_text = node.text
        first_image = extracted_images[0]
        image_alt, image_link = first_image

        split_node = current_text.split(f"![{image_alt}]({image_link})", 1)
        
        if split_node[0] != "":
            new_nodes.append(TextNode(split_node[0], TextType.TEXT))

        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

        if split_node[1] != "":
            remaining_node = TextNode(split_node[1], TextType.TEXT)
            remaining_nodes = split_nodes_image([remaining_node])
            new_nodes.extend(remaining_nodes)
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)

        if len(extracted_links) == 0:
            new_nodes.append(node) 
            continue

        current_text = node.text
        first_link = extracted_links[0]
        link_text, link_url = first_link

        split_node = current_text.split(f"[{link_text}]({link_url})", 1)
        
        if split_node[0] != "":
            new_nodes.append(TextNode(split_node[0], TextType.TEXT))

        new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

        if split_node[1] != "":
            remaining_node = TextNode(split_node[1], TextType.TEXT)
            remaining_nodes = split_nodes_link([remaining_node])
            new_nodes.extend(remaining_nodes)
            
    return new_nodes