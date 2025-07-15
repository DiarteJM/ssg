import unittest
from src.textnode import TextNode, TextType
from src.splitdelimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    # Basic split tests
    def test_basic_split(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_multiple_splits(self):
        node = TextNode("*One* normal *Two*", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "One")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text, " normal ")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)
        self.assertEqual(nodes[2].text, "Two")
        self.assertEqual(nodes[2].text_type, TextType.BOLD)

    # Non-text type tests
    def test_ignore_non_text_type(self):
        node = TextNode("*Already bold*", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "*Already bold*")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_mixed_node_types(self):
        text_node = TextNode("Hello *world*", TextType.TEXT)
        bold_node = TextNode("Stay bold", TextType.BOLD)
        nodes = split_nodes_delimiter([text_node, bold_node], "*", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, "Stay bold")
        self.assertEqual(nodes[2].text_type, TextType.BOLD)

    # Edge cases
    def test_empty_nodes_list(self):
        nodes = split_nodes_delimiter([], "*", TextType.BOLD)
        self.assertEqual(nodes, [])

    def test_no_delimiters(self):
        node = TextNode("Plain text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_empty_text_between_delimiters(self):
        node = TextNode("Before *text* After", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Before ")
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " After")

    def test_consecutive_delimiters(self):
        node = TextNode("**Bold**", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertTrue("Invalid Markdown syntax" in str(context.exception))

    # Error cases
    def test_unmatched_delimiter(self):
        node = TextNode("Unmatched *delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertTrue("Invalid Markdown syntax" in str(context.exception))

    def test_multiple_unmatched_delimiters(self):
        node = TextNode("*One* *Two", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertTrue("Invalid Markdown syntax" in str(context.exception))

    # Special cases
    def test_delimiter_at_start(self):
        node = TextNode("*Bold* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Bold")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text, " text")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

    def test_delimiter_at_end(self):
        node = TextNode("text *Bold*", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "text ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "Bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
