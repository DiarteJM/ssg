import os
import sys

from src.extract_title import extract_title
from src.markdown_to_html import markdown_to_html_node

basepath = sys.argv[1] if len(sys.argv) > 1 else '/'

def generate_page(from_path, template_path, dest_path):
  # Print a message like "Generating page from `from_path` to `dest_path` using `template_path`".
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
  # Read the markdown file at "from_path" and store the contents in a variable.
  with open(from_path, 'r', encoding='utf-8') as file:
    markdown_content = file.read()
  # Read the template file at "template_path" and store the contents in a variable.
  with open(template_path, 'r', encoding='utf-8') as file:
    template_content = file.read()
  # Use the "markdown_to_html_node" function and ".to_html()" method to convert the markdown file to an HTML string.
  html_content = markdown_to_html_node(markdown_content).to_html()
  # Use the "extract_title" function to grab the title of the page.
  title = extract_title(markdown_content)
  # Replace the `{{ Title }}` and `{{ Content }}` placeholders in the template with the HTML and title generated.
  full_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
  # Replace any instances of href="/ with href="{basepath}" in the full content.
  full_content = full_content.replace('href="/', f'href="{basepath}"')
  # Replace any instances of src="/ with src="{basepath}" in the full content.
  full_content = full_content.replace('src="/', f'src="{basepath}"')
  # Write the new full HTML page to a file at `dest_path`. Be sure to create any necessary directories if they don't exist.
  os.makedirs(os.path.dirname(dest_path), exist_ok=True)
  with open(dest_path, 'w', encoding='utf-8') as file:
    file.write(full_content)
  # Print a message like "Page generated successfully at `dest_path`".
  print(f"Page generated successfully at {dest_path}")
  return full_content  # Return the full content for testing purposes

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  """
  Recursively crawl the directory at 'dir_path_content' and generate HTML pages for each markdown file found.
  The template file is at 'template_path' and the generated pages should be written to 'dest_dir_path'.
  Generated pages will be written to the destination directory in the same directory structure.
  
  Args:
      dir_path_content (str): Directory containing markdown files
      template_path (str): Path to the HTML template file
      dest_dir_path (str): Destination directory for generated HTML files
  """
  # If the input is a single file rather than a directory
  if os.path.isfile(dir_path_content) and dir_path_content.endswith('.md'):
    # This is a single markdown file, generate its HTML page
    generate_page(dir_path_content, template_path, dest_dir_path)
    return
  
  # Otherwise, this is a directory so crawl it recursively
  for root, dirs, files in os.walk(dir_path_content):
    for file in files:
      if file.endswith('.md'):
        markdown_file_path = os.path.join(root, file)
        relative_path = os.path.relpath(markdown_file_path, dir_path_content)
        dest_file_path = os.path.join(dest_dir_path, relative_path.replace('.md', '.html'))
        
        # Print processing information
        print(f"Processing markdown file: {markdown_file_path} → {dest_file_path}")
        
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        print(f"Creating directory: {os.path.dirname(dest_file_path)}")
        
        # Generate the HTML page using the generate_page function
        generate_page(markdown_file_path, template_path, dest_file_path)
        print(f"Generated page: {dest_file_path}")