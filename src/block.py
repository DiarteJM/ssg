import contextlib
from enum import Enum

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"
  
def block_to_block_type(block):
  # If block is empty, default to paragraph
  if not block.strip():
    return BlockType.PARAGRAPH

  # Check for heading (1-6 '#' followed by space), allow leading spaces
  stripped = block.lstrip()
  if any(stripped.startswith('#' * i + ' ') for i in range(1, 7)):
    return BlockType.HEADING

  # Check for code block (starts and ends with ```), must be at start of line
  if block.startswith('```') and block.rstrip().endswith('```'):
    return BlockType.CODE

  # Check for quote block (each line starts with '>'), allow leading spaces, allow '>' or '> '
  lines = block.split('\n')
  if all(line.lstrip().startswith('>') and (line.lstrip() == '>' or line.lstrip().startswith('> ')) for line in lines):
    return BlockType.QUOTE

  # Check for unordered list (each line starts with '-', '*', or '+', allow leading spaces)
  unordered_markers = ('- ', '* ', '+ ')
  if all(any(line.lstrip().startswith(marker) for marker in unordered_markers) for line in lines):
    return BlockType.UNORDERED_LIST

  # Check for ordered list (each line starts with number followed by '. ', allow leading spaces, allow any numbers)
  import re
  ordered_list_pattern = re.compile(r"^\s*\d+\. ")
  if all(ordered_list_pattern.match(line) for line in lines):
    return BlockType.ORDERED_LIST
  # Default case: paragraph
  return BlockType.PARAGRAPH
  