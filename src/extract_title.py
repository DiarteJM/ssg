

def extract_title(markdown):
  # should pull the h1 header from the markdown file/text (the line that starts with a single #) and return it.
  # If no h1 header is found, raise an Exception.
  # Example: extract_title("# Hello") should return "Hello" - strip the # and any leading/trailing whitespace.
  
  lines = markdown.split("\n")
  for line in lines:
    if line.startswith("# "):
      return line[2:].strip() # Should return title without the # character and any whitespace
  # If we get here, no title was found
  raise Exception("No header found")

