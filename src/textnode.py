from enum import Enum

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
    