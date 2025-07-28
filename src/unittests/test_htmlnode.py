import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    # Constructor tests
    def test_default_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_tag(self):
        node = HTMLNode("div")
        self.assertEqual(node.tag, "div")
  
    def test_value(self):
        node = HTMLNode(value="content")
        self.assertEqual(node.value, "content")
  
    def test_children(self):
        children = ["child1", "child2"]
        node = HTMLNode(children=children)
        self.assertEqual(node.children, children)
  
    def test_props(self):
        props = {"class": "container", "id": "main"}
        node = HTMLNode(props=props)
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

    # Method tests
    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html(self):
        props = {"class": "container", "id": "main"}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), 'class="container" id="main"')

    def test_props_to_html_with_none_values(self):
        props = {"class": "container", "id": None, "style": "color: red"}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), 'class="container" style="color: red"')

    def test_repr(self):
        node = HTMLNode("div", "content", ["child"], {"class": "container"})
        expected = 'HTMLNode(tag=div, value=content, children=[\'child\'], props={\'class\': \'container\'})'
        self.assertEqual(repr(node), expected)
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_node_basic(self):
        leaf = LeafNode("span", "Leaf content", {"class": "leaf"})
        self.assertEqual(leaf.tag, "span")
        self.assertEqual(leaf.value, "Leaf content")
        self.assertEqual(leaf.children, [])
        self.assertEqual(leaf.props, {"class": "leaf"})

    def test_leaf_node_no_value(self):
        with self.assertRaises(ValueError) as context:
            LeafNode("span")
        self.assertEqual(str(context.exception), "LeafNode must have a value")

    def test_leaf_node_empty_string_value(self):
        leaf = LeafNode("span", "")
        self.assertEqual(leaf.value, "")

    def test_leaf_node_to_html_basic(self):
        leaf = LeafNode("span", "content", {"class": "leaf"})
        self.assertEqual(leaf.to_html(), '<span class="leaf">content</span>')

    def test_leaf_node_to_html_no_props(self):
        leaf = LeafNode("span", "content")
        self.assertEqual(leaf.to_html(), '<span>content</span>')

    def test_leaf_node_to_html_none_props(self):
        leaf = LeafNode("span", "content", {"class": None, "id": "main"})
        self.assertEqual(leaf.to_html(), '<span id="main">content</span>')

    def test_leaf_node_to_html_no_tag(self):
        leaf = LeafNode(None, "content")
        self.assertEqual(leaf.to_html(), 'content')

class TestParentNode(unittest.TestCase):
    def test_parent_node_basic(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", children=[child])
        self.assertEqual(parent.to_html(), "<div><span>child</span></div>")

    def test_parent_node_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", children=None)
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_parent_node_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", children=[])

    def test_parent_node_no_tag(self):
        child = LeafNode("span", "child")
        parent = ParentNode(None, children=[child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_parent_node_with_props(self):
        child = LeafNode("span", "content")
        parent = ParentNode("div", children=[child], props={"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><span>content</span></div>'
        )

    def test_parent_node_props_with_none(self):
        child = LeafNode("span", "content")
        parent = ParentNode("div", children=[child], props={"class": None, "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div id="main"><span>content</span></div>'
        )

    def test_parent_node_mixed_children(self):
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        parent1 = ParentNode("p", children=[leaf1])
        parent2 = ParentNode("div", children=[parent1, leaf2])
        self.assertEqual(
            parent2.to_html(),
            "<div><p><b>bold</b></p><i>italic</i></div>"
        )

    def test_parent_node_ignore_value(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", value="ignored", children=[child])
        self.assertEqual(parent.to_html(), "<div><span>child</span></div>")

    def test_deeply_nested_structure(self):
        leaf1 = LeafNode("span", "text1")
        leaf2 = LeafNode("span", "text2")
        parent1 = ParentNode("div", children=[leaf1])
        parent2 = ParentNode("div", children=[leaf2])
        grandparent = ParentNode("section", children=[parent1, parent2])
        self.assertEqual(
            grandparent.to_html(),
            "<section><div><span>text1</span></div><div><span>text2</span></div></section>"
        )