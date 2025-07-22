from extract_markdown import extract_markdown_images, extract_markdown_links
from src.textnode import TextNode, TextType


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
            raise Exception(
                f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in text '{node.text}'")

        # Check for consecutive delimiters
        if delimiter + delimiter in node.text:
            raise Exception(
                f"Invalid Markdown syntax: consecutive delimiters '{delimiter}{delimiter}' in text '{node.text}'")

        # Split the text and process parts
        parts = node.text.split(delimiter)
        # Tracks whether we're inside a special section (bold, italic, etc.)
        in_special = False

        for i, text in enumerate(parts):
            # Skip empty middle sections
            if i > 0 and i < len(parts) - 1 and not text:
                in_special = not in_special
                continue

            if text or i == 0 or i == len(parts) - 1:
                node_type = text_type if in_special else TextType.TEXT
            if text:
                new_nodes.append(TextNode(text, node_type))
            in_special = not in_special
    return new_nodes


def split_nodes_image(old_nodes):
    # should behave just like the split_nodes_delimiter function, but for images
    # should not need a delimiter or text_type as input; always will operate on images
    new_nodes = []
    # make use of extraction functions previously written and defined
    # if there are no images, just return list with original TextNode object in it
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text_type == TextType.TEXT:
            # extract images from the text using previously defined extraction functions
            images = extract_markdown_images(node.text)
            if not images:
                # don't append any TextNodes that have empty text to the final list
                # handle the "no images found" case - if extraction returns empty list, just append the original node
                new_nodes.append(node)
                continue
            # handle the "has images found" case - if there are images, need to make a recursive call to grab each image
            alt_text = images[0][0]
            image_url = images[0][1]
            # create a new TextNode for the first image
            # use the first image as a delimiter to split the text
            delimiter = f"![{alt_text}]({image_url})"
            # split the text and process parts
            sections = node.text.split(delimiter, maxsplit=1)
            # if sections[0] is not empty, add it as a TEXT node
            # Add the current image as the IMAGE node (you already have what is needed from images[0])
            # if sections[1] is not empty, you need to process it for more images if the length of images > 1
            before_image = sections[0]
            after_image = sections[1] if len(sections) > 1 else ""
            if before_image:
                new_nodes.append(TextNode(before_image, TextType.TEXT))
            if images:
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            if after_image:
                # Create a new TextNode with the remaining text
                remainder_text_node = TextNode(after_image, TextType.TEXT)
                # Recursively call split_nodes_image on the remaining text
                remainder_text_node = split_nodes_image([remainder_text_node])
                # all all the resulting nodes to new_nodes
                new_nodes.extend(remainder_text_node)
    return new_nodes

    # split_nodes_image should be very similar to split_nodes_delimiter
    # use the split() method with large strings as delimiter
    # has optional second 'maxsplits' parameter - can set to 1 if you only want to split the string once at most
    # for each image extracted from text, split the text before and after image markdown


def split_nodes_link(old_nodes):
    # should behave just like the split_nodes_delimiter function, but for links
    # should not need a delimiter or text_type as input; always will operate on links
    new_nodes = []
    # make use of extraction functions previously written and defined
    # if there are no links, just return list with original TextNode object in it
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text_type == TextType.TEXT:
            # extract links from the text using previously defined extraction functions
            links = extract_markdown_links(node.text)
            if not links:
                # don't append any TextNodes that have empty text to the final list
                # handle the "no links found" case - if extraction returns empty list, just append the original node
                new_nodes.append(node)
                continue
            # handle the "has links found" case - if there are links, need to make a recursive call to grab each link
            link_text = links[0][0]
            link_url = links[0][1]
            # create a new TextNode for the first link
            # use the first link as a delimiter to split the text
            delimiter = f"[{link_text}]({link_url})"
            # split the text and process parts
            sections = node.text.split(delimiter, maxsplit=1)
            # if sections[0] is not empty, add it as a TEXT node
            # Add the current link as the LINK node (you already have what is needed from links[0])
            # if sections[1] is not empty, you need to process it for more links if the length of links > 1
            before_link = sections[0]
            after_link = sections[1] if len(sections) > 1 else ""
            if before_link:
                new_nodes.append(TextNode(before_link, TextType.TEXT))
            if links:
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            if after_link:
                # Create a new TextNode with the remaining text
                remainder_text_node = TextNode(after_link, TextType.TEXT)
                # Recursively call split_nodes_link on the remaining text
                remainder_text_node = split_nodes_link([remainder_text_node])
                # all all the resulting nodes to new_nodes
                new_nodes.extend(remainder_text_node)
    return new_nodes
    # split_nodes_link should be very similar to split_nodes_delimiter
    # use the split() method with large strings as delimiter
    # has optional second 'maxsplits' parameter - can set to 1 if you only want to split the string once at most
    # for each link extracted from text, split the text before and after link markdown
