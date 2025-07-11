import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
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
    def test_url(self):
        node = TextNode("This is a text URL", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text URL", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()