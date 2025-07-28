import unittest
from src.textnode import TextNode, TextType, text_node_to_html_node
from src.htmlnode import HTMLNode, LeafNode


class TestTextNodeToHTMLNode(unittest.TestCase):
    # Basic conversion tests

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_to_html(self):
        node = TextNode("This is some bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is some bold text")

    def test_italic_to_html(self):
        node = TextNode("This is some italicized text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is some italicized text")

    def test_code_to_html(self):
        node = TextNode("This is a code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code block")

    def test_url_link_to_html(self):
        node = TextNode("This is a text URL", TextType.LINK,
                        "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text URL")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image_url_to_html(self):
        node = TextNode("This is an image", TextType.IMAGE,
                        "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
                         "src": "https://example.com/image.png", "alt": "This is an image"})

    # Edge cases tests
    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

    def test_link_without_url(self):
        node = TextNode("This is a link", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": None})

    def test_image_without_url(self):
        node = TextNode("This is an image", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": None, "alt": "This is an image"})

    def test_empty_url_link(self):
        node = TextNode("Empty URL", TextType.LINK, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Empty URL")
        self.assertEqual(html_node.props, {"href": ""})

    def test_empty_url_image(self):
        node = TextNode("Empty URL Image", TextType.IMAGE, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "", "alt": "Empty URL Image"})

    def test_invalid_text_type_to_html(self):
        # Pass a non-TextType enum value to trigger the ValueError
        node = TextNode("This is a text node", "invalid_type")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Invalid text type provided")


if __name__ == "__main__":
    unittest.main()
