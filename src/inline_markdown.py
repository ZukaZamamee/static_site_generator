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