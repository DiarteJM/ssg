
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
  def __init__(self, tag, value=None, children=None, props=None):
    super().__init__(tag, value, children, props)
    if value is None:
      raise ValueError("LeafNode must have a value")
    
  def to_html(self):
    if self.value is None:
      raise ValueError("LeafNode must have a value to convert to HTML")
    if self.tag is None:
      return self.value
    
    props_str = ""
    
    if self.props:
      props_str =  " ".join(f'{key}="{value}"' for key, value in self.props.items() if value is not None)
      
    return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
  
  