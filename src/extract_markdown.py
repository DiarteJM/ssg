import re
from src.textnode import TextNode, TextType

def extract_markdown_images(text):
    """Extract image patterns from plain text."""
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    """Extract link patterns from plain text."""
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_images_nodes(old_nodes):
    """Extract image markdown patterns and convert to image TextNodes."""
    new_nodes = []
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        matches = re.findall(image_pattern, old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        for alt_text, url in matches:
            parts = remaining_text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = parts[1] if len(parts) > 1 else ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                
    return new_nodes

def extract_markdown_links_nodes(old_nodes):
    """Extract link markdown patterns and convert to link TextNodes."""
    new_nodes = []
    link_pattern = r"\[(.*?)\]\((.*?)\)"
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        matches = re.findall(link_pattern, old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        for text, url in matches:
            parts = remaining_text.split(f"[{text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining_text = parts[1] if len(parts) > 1 else ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                
    return new_nodes

def markdown_to_blocks(markdown):
    # takes a raw Markdown string (representing a full document) and returns a list of Block strings.
    md_split = markdown.split("\n\n")
    
    result = []

    for block in md_split:
        blocks_strip = block.strip()
        if blocks_strip:
            # handle indentation on lines
            lines = blocks_strip.split("\n")
            # print(lines)
            # strip each line and join together with new lines
            str_block = "\n".join(line.strip() for line in lines)
            result.append(str_block)
            
    # print(result)
    return result
        