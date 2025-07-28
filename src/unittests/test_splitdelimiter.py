import unittest
from src.textnode import TextNode, TextType
from src.splitdelimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link


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
        nodes = split_nodes_delimiter(
            [text_node, bold_node], "*", TextType.ITALIC)
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

class TestSplitNodesImage(unittest.TestCase):
    def test_basic_image_split(self):
        node = TextNode(
            "This is an ![alt text](image.jpg) in text", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "alt text")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "image.jpg")
        self.assertEqual(nodes[2].text, " in text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_multiple_images(self):
        node = TextNode(
            "![first](img1.jpg) middle ![second](img2.jpg)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "first")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(nodes[0].url, "img1.jpg")
        self.assertEqual(nodes[1].text, " middle ")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)
        self.assertEqual(nodes[2].text, "second")
        self.assertEqual(nodes[2].text_type, TextType.IMAGE)
        self.assertEqual(nodes[2].url, "img2.jpg")

    def test_image_at_start(self):
        node = TextNode(
            "![start](start.jpg) after image", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "start")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(nodes[0].url, "start.jpg")
        self.assertEqual(nodes[1].text, " after image")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

    def test_image_at_end(self):
        node = TextNode("before image ![end](end.jpg)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "before image ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "end")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "end.jpg")

    def test_no_images(self):
        node = TextNode("No images here", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "No images here")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_empty_nodes_list(self):
        nodes = split_nodes_image([])
        self.assertEqual(nodes, [])

    def test_ignore_non_text_type(self):
        node = TextNode("![image](url.jpg)", TextType.BOLD)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "![image](url.jpg)")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_mixed_node_types(self):
        text_node = TextNode(
            "Hello ![world](world.jpg)", TextType.TEXT)
        bold_node = TextNode("Stay bold", TextType.BOLD)
        nodes = split_nodes_image([text_node, bold_node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "world.jpg")
        self.assertEqual(nodes[2].text, "Stay bold")
        self.assertEqual(nodes[2].text_type, TextType.BOLD)

    def test_complex_image_url(self):
        node = TextNode(
            "![complex](https://example.com/image.jpg?size=large&format=png)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "complex")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(
            nodes[0].url, "https://example.com/image.jpg?size=large&format=png")

    def test_consecutive_images(self):
        node = TextNode(
            "![first](img1.jpg)![second](img2.jpg)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "first")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(nodes[0].url, "img1.jpg")
        self.assertEqual(nodes[1].text, "second")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "img2.jpg")

    def test_empty_alt_text(self):
        node = TextNode("![](empty.jpg) no alt text", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(nodes[0].url, "empty.jpg")
        self.assertEqual(nodes[1].text, " no alt text")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

class TestSplitNodesLink(unittest.TestCase):
    def test_basic_link_split(self):
        node = TextNode(
            "This is a [link text](https://example.com) in text", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link text")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
        self.assertEqual(nodes[2].text, " in text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_multiple_links(self):
        node = TextNode(
            "[first](https://first.com) middle [second](https://second.com)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "first")
        self.assertEqual(nodes[0].text_type, TextType.LINK)
        self.assertEqual(nodes[0].url, "https://first.com")
        self.assertEqual(nodes[1].text, " middle ")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)
        self.assertEqual(nodes[2].text, "second")
        self.assertEqual(nodes[2].text_type, TextType.LINK)
        self.assertEqual(nodes[2].url, "https://second.com")

    def test_link_at_start(self):
        node = TextNode(
            "[start](https://start.com) after link", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "start")
        self.assertEqual(nodes[0].text_type, TextType.LINK)
        self.assertEqual(nodes[0].url, "https://start.com")
        self.assertEqual(nodes[1].text, " after link")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

    def test_link_at_end(self):
        node = TextNode(
            "before link [end](https://end.com)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "before link ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "end")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://end.com")

    def test_no_links(self):
        node = TextNode("No links here", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "No links here")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_empty_nodes_list(self):
        nodes = split_nodes_link([])
        self.assertEqual(nodes, [])

    def test_ignore_non_text_type(self):
        node = TextNode(
            "[link](https://url.com)", TextType.BOLD)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(
            nodes[0].text, "[link](https://url.com)")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_mixed_node_types(self):
        text_node = TextNode(
            "Hello [world](https://world.com)", TextType.TEXT)
        bold_node = TextNode("Stay bold", TextType.BOLD)
        nodes = split_nodes_link([text_node, bold_node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://world.com")
        self.assertEqual(nodes[2].text, "Stay bold")
        self.assertEqual(nodes[2].text_type, TextType.BOLD)

    def test_complex_link_url(self):
        node = TextNode(
            "[complex](https://example.com/path?query=value&param=test#fragment)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "complex")
        self.assertEqual(nodes[0].text_type, TextType.LINK)
        self.assertEqual(
            nodes[0].url, "https://example.com/path?query=value&param=test#fragment")

    def test_consecutive_links(self):
        node = TextNode(
            "[first](https://first.com)[second](https://second.com)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "first")
        self.assertEqual(nodes[0].text_type, TextType.LINK)
        self.assertEqual(nodes[0].url, "https://first.com")
        self.assertEqual(nodes[1].text, "second")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://second.com")

    def test_empty_link_text(self):
        node = TextNode(
            "[](https://empty.com) no link text", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.LINK)
        self.assertEqual(nodes[0].url, "https://empty.com")
        self.assertEqual(nodes[1].text, " no link text")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)

    def test_relative_urls(self):
        node = TextNode(
            "[relative](/path/to/page)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "relative")
        self.assertEqual(nodes[0].text_type, TextType.LINK)
        self.assertEqual(nodes[0].url, "/path/to/page")

    def test_anchor_links(self):
        node = TextNode("[anchor](#section)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "anchor")
        self.assertEqual(nodes[0].text_type, TextType.LINK)
        self.assertEqual(nodes[0].url, "#section")


if __name__ == "__main__":
    unittest.main()
