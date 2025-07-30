import unittest
from src.block import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
  
  def test_heading_block(self):
    # Test all heading levels (1-6)
    self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
    
  def test_heading_edge_cases(self):
    # Too many hashtags
    self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
    # No space after hashtag
    self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
    # Leading space before hashtag (should still be recognized)
    self.assertEqual(block_to_block_type("  # Heading with leading space"), BlockType.HEADING)
    # Empty heading
    self.assertEqual(block_to_block_type("#"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("# "), BlockType.HEADING)
  
  def test_code_block(self):
    # Standard code block
    self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
    # Code block with language
    self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), BlockType.CODE)
    # Multiline code block
    self.assertEqual(block_to_block_type("```\nline 1\nline 2\nline 3\n```"), BlockType.CODE)
  
  def test_code_block_edge_cases(self):
    # Incomplete code block (missing closing backticks)
    self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)
    # Empty code block
    self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)
    # Code block with only whitespace
    self.assertEqual(block_to_block_type("```\n  \n```"), BlockType.CODE)
    # Backticks not at start of line (should be paragraph)
    self.assertEqual(block_to_block_type(" ```\ncode\n```"), BlockType.PARAGRAPH)
    
  def test_quote_block(self):
    # Standard quote
    self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
    # Multiline quote
    self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
    # Quote with formatting
    self.assertEqual(block_to_block_type("> **Bold** and *italic*"), BlockType.QUOTE)
  
  def test_quote_edge_cases(self):
    # Quote with leading space (should still be recognized)
    self.assertEqual(block_to_block_type("  > Quote with leading space"), BlockType.QUOTE)
    # Empty quote
    self.assertEqual(block_to_block_type(">"), BlockType.QUOTE)
    # Quote with just space after >
    self.assertEqual(block_to_block_type("> "), BlockType.QUOTE)
    # Not a quote (no space after >)
    self.assertEqual(block_to_block_type(">Not a quote"), BlockType.PARAGRAPH)
  
  def test_unordered_list(self):
    # Standard list items with different markers
    self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
    self.assertEqual(block_to_block_type("* Item 1"), BlockType.UNORDERED_LIST)
    self.assertEqual(block_to_block_type("+ Item 1"), BlockType.UNORDERED_LIST)
    # Multiline list
    self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)
    # Mixed markers (should still be unordered list)
    self.assertEqual(block_to_block_type("- Item 1\n* Item 2\n+ Item 3"), BlockType.UNORDERED_LIST)
  
  def test_unordered_list_edge_cases(self):
    # List with leading spaces
    self.assertEqual(block_to_block_type("  - Item with leading space"), BlockType.UNORDERED_LIST)
    # Empty list item
    self.assertEqual(block_to_block_type("-"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("- "), BlockType.UNORDERED_LIST)
    # No space after marker
    self.assertEqual(block_to_block_type("-Not a list"), BlockType.PARAGRAPH)
    
  def test_ordered_list(self):
    # Standard ordered list
    self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
    # Multiline ordered list
    self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)
    # Non-sequential numbers
    self.assertEqual(block_to_block_type("1. Item 1\n5. Item 2\n10. Item 3"), BlockType.ORDERED_LIST)
  
  def test_ordered_list_edge_cases(self):
    # List with leading spaces
    self.assertEqual(block_to_block_type("  1. Item with leading space"), BlockType.ORDERED_LIST)
    # Empty list item
    self.assertEqual(block_to_block_type("1."), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("1. "), BlockType.ORDERED_LIST)
    # No space after period
    self.assertEqual(block_to_block_type("1.Not a list"), BlockType.PARAGRAPH)
    # Letters instead of numbers (should be paragraph)
    self.assertEqual(block_to_block_type("a. Not an ordered list"), BlockType.PARAGRAPH)
    
  def test_paragraph(self):
    # Standard paragraph
    self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
    # Multiline paragraph
    self.assertEqual(block_to_block_type("Line 1\nLine 2\nLine 3"), BlockType.PARAGRAPH)
    # Paragraph with formatting
    self.assertEqual(block_to_block_type("Text with **bold** and *italic*"), BlockType.PARAGRAPH)
    
  def test_paragraph_edge_cases(self):
    # Empty string
    self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
    # Only whitespace
    self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)
    # Newlines only
    self.assertEqual(block_to_block_type("\n\n"), BlockType.PARAGRAPH)
    
  def test_mixed_content(self):
    # Content that might look like multiple types but should be paragraph
    self.assertEqual(block_to_block_type("Not a > quote"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("Not a - list"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("Not a 1. list"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("Not a # heading"), BlockType.PARAGRAPH)
    self.assertEqual(block_to_block_type("Not a ```code``` block"), BlockType.PARAGRAPH)

if __name__ == '__main__':
  unittest.main()