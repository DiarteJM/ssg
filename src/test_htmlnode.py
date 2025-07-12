import unittest
from htmlnode import HTMLNode

# Template for HTMLNode Tests: HTMLNode(tag, value, children, props)
class TestHTMLNode(unittest.TestCase):
  def test_tag(self):
    node = HTMLNode("div", None, [], {})
    self.assertEqual(node.tag, "div")
  
  def test_value(self):
    node = HTMLNode(None, "content", [], {})
    self.assertEqual(node.value, "content")
  
  def test_children(self):
    children = ["child1", "child2"]
    node = HTMLNode(None, None, children, {})
    self.assertEqual(node.children, children)
  
  def test_props(self):
    props = {"class": "container", "id": "main"}
    node = HTMLNode(None, None, [], props)
    self.assertEqual(node.props, props)
  
  def test_all_attributes(self):
    tag = "div"
    value = "content"
    children = ["child1", "child2"]
    props = {"class": "container"}
    node = HTMLNode(tag, value, children, props)
    self.assertEqual(node.tag, tag)
    self.assertEqual(node.value, value)
    self.assertEqual(node.children, children)
    self.assertEqual(node.props, props)
    
  def test_props_to_html(self):
    props = {"class": "container", "id": "main"}
    node = HTMLNode(None, None, [], props)
    self.assertEqual(node.props_to_html(), 'class="container" id="main"')