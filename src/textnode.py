from enum import Enum

from src.htmlnode import LeafNode, HTMLNode


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