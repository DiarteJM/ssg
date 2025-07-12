
class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children if children is not None else []
    self.props = props if props is not None else {}
    
  def to_html(self):
    # should raise a NotImplementedError if not implemented in subclass - child classes should override this method
    raise NotImplementedError
  
  def props_to_html(self):
    # should return a string that represents the HTML attributes of the node
    return ' '.join(f'{key}="{value}"' for key, value in self.props.items() if value is not None)
  
  def __repr__(self):
    # return a string representation of the HTMLNode object
    return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
  
class LeafNode(HTMLNode):
  def __init__(self, tag, value=None, props=None):
    super().__init__(tag=tag, value=value, props=props)
    if value is None:
      raise ValueError("LeafNode must have a value")
    
  def to_html(self):
    if self.value is None:
      raise ValueError("LeafNode must have a value to convert to HTML")
    if self.tag is None:
      return self.value
    
    props_str = self.props_to_html()
    props_space = " " if props_str else ""
    
    return f"<{self.tag}{props_space}{props_str}>{self.value}</{self.tag}>"
  
class ParentNode(HTMLNode):
  def __init__(self, tag, value=None, children=None, props=None):
    # Parent node ignores the value parameter as it only uses children
    super().__init__(tag=tag, children=children, props=props)
    
    if children is None or len(children) == 0:
      raise ValueError("ParentNode must have children")
    
  def to_html(self):
    # if object does not have a tag, raise ValueError
    if self.tag is None:
      raise ValueError("ParentNode must have a tag")
    # if children is a missing value, raise ValueError with different message
    if self.children is None:
      raise ValueError("ParentNode must have children")
    # else return string representing HTML tag of node AND its children
    # - should be recursive method (each recursion being called is a nested child node)
    children_html = ''.join(child.to_html() for child in self.children)
    props_str = self.props_to_html()
    props_space = " " if props_str else ""
    return f"<{self.tag}{props_space}{props_str}>{children_html}</{self.tag}>"