from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode, LeafNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    inputs:
    - old_nodes: list of TextNode objects
    - delimiter: a string that will be used to split the text in the nodes
    - text_type: type of TextNode to create for the split parts
    
    - If old node is not a TextNode.TEXT, just add to the new list as is (we only split TextNode.TEXT objects - no other objects)
    - if a matching closing delimiter is not found, just raise Exception with a helpful error message (invalid Markdown syntax)
    - Use the split() method to split the text in the node by the delimiter
    - Use the extend() method to add the new nodes to the new list
    
    output:
    - returns a new list of nodes where any "text" type nodes in the input list are (potentially) split into multiple nodes based on syntax. 
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue

        # Check for unmatched delimiters
        count = node.text.count(delimiter)
        if count % 2 != 0:
            raise Exception(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in text '{node.text}'")

        # Check for consecutive delimiters
        if delimiter + delimiter in node.text:
            raise Exception(f"Invalid Markdown syntax: consecutive delimiters '{delimiter}{delimiter}' in text '{node.text}'")

        # Split the text and process parts
        parts = node.text.split(delimiter)
        in_special = False  # Tracks whether we're inside a special section (bold, italic, etc.)

        for i, text in enumerate(parts):
            # Skip empty middle sections
            if i > 0 and i < len(parts) - 1 and not text:
                in_special = not in_special
                continue

            if text or i == 0 or i == len(parts) - 1:
                node_type = text_type if in_special else TextType.TEXT
                if text:  # Only create nodes for non-empty text
                    new_nodes.append(TextNode(text, node_type))
            in_special = not in_special

    return new_nodes
