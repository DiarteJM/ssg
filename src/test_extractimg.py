import unittest
from src.extract_images import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    # Basic extraction tests
    def test_basic_image(self):
        text = "![alt text](image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "image.png"))
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_basic_link(self):
        text = "[link text](https://example.com)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link text", "https://example.com"))

    def test_multiple_images(self):
        text = "![first](img1.png) some text ![second](img2.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("first", "img1.png"))
        self.assertEqual(images[1], ("second", "img2.png"))
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_multiple_links(self):
        text = "[link1](url1.com) text [link2](url2.com)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("link1", "url1.com"))
        self.assertEqual(links[1], ("link2", "url2.com"))

    def test_mixed_content(self):
        text = "![img](pic.png) text [link](url.com)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("img", "pic.png"))
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link", "url.com"))

    # Edge cases
    def test_empty_text(self):
        text = ""
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_no_images_or_links(self):
        text = "Plain text without any markdown"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_empty_alt_text(self):
        text = "![](image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("", "image.png"))

    def test_empty_url(self):
        text = "![alt]()"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt", ""))

    # Special cases
    def test_nested_brackets(self):
        text = "![alt [with brackets]](image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)  # Should not match due to nested brackets

    def test_nested_parentheses(self):
        text = "![alt](path(to)image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)  # Should not match due to nested parentheses

    def test_escaping_brackets(self):
        text = "!\\[not an image\\](not-image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)

    def test_url_with_spaces(self):
        text = "![alt text](path/to my/image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "path/to my/image.png"))

    def test_multiline_text(self):
        text = """
        ![first](img1.png)
        Some text here
        ![second](img2.png)
        """
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("first", "img1.png"))
        self.assertEqual(images[1], ("second", "img2.png"))

    # Invalid syntax tests
    def test_malformed_image_syntax(self):
        text = "![incomplete"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)

    def test_malformed_link_syntax(self):
        text = "[incomplete"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_invalid_image_marker(self):
        text = "!invalid![alt](image.png)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt", "image.png"))


if __name__ == "__main__":
    unittest.main()

