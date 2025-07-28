import unittest
from src.textnode import TextNode, TextType

from src.extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    extract_markdown_images_nodes,
    extract_markdown_links_nodes,
    markdown_to_blocks
)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is an ![image](https://example.com/image.jpg) and another ![second image](https://example.com/image2.jpg)"
        expected = [("image", "https://example.com/image.jpg"),
                    ("second image", "https://example.com/image2.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is a [link](https://example.com) and another [second link](https://example.com/page)"
        expected = [("link", "https://example.com"),
                    ("second link", "https://example.com/page")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_not_images(self):
        text = "This is a [link](https://example.com) and an ![image](https://example.com/image.jpg)"
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_nodes(self):
        nodes = [TextNode(
            "This is an ![image](https://example.com/image.jpg) test", TextType.TEXT)]
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" test", TextType.TEXT)
        ]
        result = extract_markdown_images_nodes(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

    def test_extract_markdown_links_nodes(self):
        nodes = [
            TextNode("This is a [link](https://example.com) test", TextType.TEXT)]
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" test", TextType.TEXT)
        ]
        result = extract_markdown_links_nodes(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_empty_input(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_whitespace(self):
        markdown = "  \n\n  \n  "
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    # New tests for edge cases:
    def test_extract_markdown_images_empty_input(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_empty_input(self):
        text = ""
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_no_matches(self):
        text = "This is just plain text with no images"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_no_matches(self):
        text = "This is just plain text with no links"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_nodes_multiple_images(self):
        nodes = [
            TextNode("Start ![img1](url1) middle ![img2](url2) end", TextType.TEXT)]
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end", TextType.TEXT)
        ]
        result = extract_markdown_images_nodes(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

    def test_extract_markdown_links_nodes_multiple_links(self):
        nodes = [
            TextNode("Start [link1](url1) middle [link2](url2) end", TextType.TEXT)]
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" end", TextType.TEXT)
        ]
        result = extract_markdown_links_nodes(nodes)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

    def test_extract_markdown_images_nodes_non_text_node(self):
        nodes = [TextNode("image", TextType.IMAGE, "url")]
        result = extract_markdown_images_nodes(nodes)
        # Should return the node unchanged
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "image")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "url")

    def test_extract_markdown_links_nodes_non_text_node(self):
        nodes = [TextNode("link", TextType.LINK, "url")]
        result = extract_markdown_links_nodes(nodes)
        # Should return the node unchanged
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "link")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "url")

    def test_markdown_to_blocks_single_paragraph(self):
        markdown = "Just a single paragraph with no line breaks."
        expected = ["Just a single paragraph with no line breaks."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_trailing_whitespace(self):
        markdown = "Paragraph with trailing spaces.  \n  \n"
        expected = ["Paragraph with trailing spaces."]
        self.assertEqual(markdown_to_blocks(markdown), expected)


if __name__ == "__main__":
    unittest.main()
