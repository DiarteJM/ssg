import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # Basic equality tests
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_with_non_textnode(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, "This is a text node")

    # TextType tests
    def test_bold(self):
        node = TextNode("This is some bold text", TextType.BOLD)
        node2 = TextNode("This is some bold text", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_italic(self):
        node = TextNode("This is some italicized text", TextType.ITALIC)
        node2 = TextNode("This is some italicized text", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_code(self):
        node = TextNode("This is a code block", TextType.CODE)
        node2 = TextNode("This is a code block", TextType.CODE)
        self.assertEqual(node, node2)

    def test_link(self):
        node = TextNode("This is a text URL", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text URL", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)
    
    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        node2 = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(node, node2)

    # Edge cases
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_url_with_non_url_type(self):
        # URL should be ignored for non-LINK/IMAGE types
        node = TextNode("Text", TextType.TEXT, "https://example.com")
        node2 = TextNode("Text", TextType.TEXT, None)
        self.assertNotEqual(node, node2)  # They should be different because __eq__ compares urls

    def test_none_url_with_link_type(self):
        node = TextNode("Link text", TextType.LINK)
        self.assertIsNone(node.url)

    def test_none_url_with_image_type(self):
        node = TextNode("Alt text", TextType.IMAGE)
        self.assertIsNone(node.url)

    # String representation
    def test_repr(self):
        node = TextNode("Test text", TextType.BOLD, "https://example.com")
        expected = 'TextNode(text=Test text, text_type=bold, url=https://example.com)'
        self.assertEqual(repr(node), expected)
            
            
if __name__ == "__main__":
    unittest.main()