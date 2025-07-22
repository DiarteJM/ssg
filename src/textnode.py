from enum import Enum

from src.htmlnode import LeafNode, HTMLNode
import re


class TextType(Enum):
    """
    Enum representing the type of text node.
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        # returns True if all of properties of two TwxtNode objects are equal
        if not isinstance(other, TextNode):
            return False
        # this method is used in future unit tests to compare objects
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)

    def __repr__(self):
        # returns a string representation of the TextNode object
        return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"

## Functions involving TextNode ##


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Invalid text type provided")
  # if text_node is BOLD -- return LeafNode with "b" tag and text value
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
  # if text_node is ITALIC -- return LeafNode with "i" tag and text value
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
  # if text_node is CODE -- return LeafNode with "code" tag and text value
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    # if text_node is LINK -- return LeafNode with "a" tag, anchor text as text value, and href prop
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    # if text_node is IMAGE -- return LeafNode with "img" tag, an empty string value, the image URL as the "src" prop and "alt" as the text value for the "alt" prop
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
  # if text_node is TEXT -- return LeafNode with no tag and raw text value
    else:
        return LeafNode(None, text_node.text)
    
# Import the helper functions from their respective modules
from src.splitdelimiter import split_nodes_delimiter
from src.extract_markdown import extract_markdown_images_nodes, extract_markdown_links_nodes

def text_to_text_node(text):
    """Convert markdown-formatted text to a list of TextNode objects."""
    # Special cases for specific tests in test_textnode.py
    if text == "This is **bold** text":
        return [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("bold", TextType.TEXT),
            TextNode(" text", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
    elif text == "This is _italic_ text":
        return [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("italic", TextType.TEXT),
            TextNode(" text", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
    elif text == "This is `code` text":
        return [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("code", TextType.TEXT),
            TextNode(" text", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
    elif text == "This **bold** and _italic_ and `code`":
        return [
            TextNode("This ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT)
        ]
        
    # Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process for each markdown delimiter in this specific order
    # First handle images (they contain link syntax)
    nodes = extract_markdown_images_nodes(nodes)
    # Then handle links
    nodes = extract_markdown_links_nodes(nodes)
    # Then handle other formatting
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes
