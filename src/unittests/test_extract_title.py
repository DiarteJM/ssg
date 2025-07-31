import unittest
import sys
import os

# Add the parent directory to sys.path to import extract_title
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        """Test extracting a basic title from markdown."""
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_title_with_extra_whitespace(self):
        """Test extracting a title with extra whitespace."""
        markdown = "#    Lots   of    spaces    "
        self.assertEqual(extract_title(markdown), "Lots   of    spaces")
    
    def test_title_in_multiline_markdown(self):
        """Test extracting a title from multi-line markdown."""
        markdown = """Some text before
# The Main Title
Some text after"""
        self.assertEqual(extract_title(markdown), "The Main Title")
    
    def test_title_at_end_of_markdown(self):
        """Test extracting a title from the end of multi-line markdown."""
        markdown = """Some text before
Another line
# The Main Title"""
        self.assertEqual(extract_title(markdown), "The Main Title")
    
    def test_title_with_special_characters(self):
        """Test extracting a title with special characters."""
        markdown = "# Title with *italics*, **bold**, and `code`"
        self.assertEqual(extract_title(markdown), "Title with *italics*, **bold**, and `code`")
    
    def test_no_title(self):
        """Test that an exception is raised when no title is found."""
        markdown = "This markdown has no title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No header found", str(context.exception))
    
    def test_empty_string(self):
        """Test that an exception is raised for an empty string."""
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No header found", str(context.exception))
    
    def test_hash_without_space(self):
        """Test that a line with just a hash without a space isn't considered a title."""
        markdown = "#NoSpace"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No header found", str(context.exception))
    
    def test_multiple_titles_returns_first(self):
        """Test that if multiple titles exist, only the first one is returned."""
        markdown = """# First Title
Some content
# Second Title"""
        self.assertEqual(extract_title(markdown), "First Title")
    
    def test_title_with_hash_inside(self):
        """Test extracting a title that contains a hash symbol."""
        markdown = "# Title with # inside"
        self.assertEqual(extract_title(markdown), "Title with # inside")


if __name__ == "__main__":
    unittest.main()
