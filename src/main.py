import os
import shutil
import logging
import sys
from pathlib import Path

# Add necessary paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from src.generate_page import generate_page, generate_pages_recursive
from src.helpers import _recursive_copy, copy_static_to_public_single

def process_markdown_directory(content_dir, dest_dir, template_file, base_path=None, skip_root_index=False):
    """
    Recursively process markdown files in a directory structure and generate HTML files.
    
    Args:
        content_dir (str): Source directory with markdown files
        dest_dir (str): Destination directory for generated HTML files
        template_file (str): Path to HTML template file
        base_path (str, optional): Base content path for determining relative paths. Defaults to None.
        skip_root_index (bool, optional): Skip processing the root index.md file. Defaults to False.
    """
    if base_path is None:
        base_path = content_dir
    
    for item in os.listdir(content_dir):
        item_path = os.path.join(content_dir, item)
        
        # Skip hidden files/directories
        if item.startswith('.'):
            continue
            
        # Process directories recursively
        if os.path.isdir(item_path):
            # Get relative path from base content directory
            rel_path = os.path.relpath(item_path, base_path)
            
            # Create corresponding directory in destination
            output_dir = os.path.join(dest_dir, rel_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # Process markdown files in this directory
            process_markdown_directory(item_path, dest_dir, template_file, base_path, False)
            
        # Process markdown files
        elif item.endswith('.md'):
            # Skip the root index.md if requested (because it's processed separately)
            if skip_root_index and content_dir == base_path and item == 'index.md':
                continue
                
            # Get relative path from base content directory
            rel_path = os.path.relpath(os.path.dirname(item_path), base_path)
            
            # If this is index.md, output to directory index.html
            if item == 'index.md':
                output_file_path = os.path.join(dest_dir, rel_path, 'index.html')
            else:
                # For other md files, create a directory with the same name and an index.html inside
                basename = os.path.splitext(item)[0]
                output_dir = os.path.join(dest_dir, rel_path, basename)
                os.makedirs(output_dir, exist_ok=True)
                output_file_path = os.path.join(output_dir, 'index.html')
            
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            
            # Generate the HTML file
            logging.info(f"Generating page from '{item_path}' to '{output_file_path}'")
            generate_page(item_path, template_file, output_file_path)
            logging.info(f"✓ Page generated at '{output_file_path}'")

def copy_static_to_public(src_dir="static", dest_dir="public", content_dir="content", template_file="template.html"):
    """
    Build the public directory by:
    1. Clearing the destination directory
    2. Copying all contents from src_dir to dest_dir recursively
    3. Generating an HTML page from markdown content using a template
    
    Args:
        src_dir (str): Source directory path (default: "static")
        dest_dir (str): Destination directory path (default: "public")
        content_dir (str): Content directory containing markdown files (default: "content")
        template_file (str): Path to HTML template file (default: "template.html")
    
    Returns:
        bool: True if operation successful, False otherwise
    """
    
    # Set up logging for better debugging
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    
    try:
        # Check if source directory exists
        if not os.path.exists(src_dir):
            logging.error(f"Source directory '{src_dir}' does not exist")
            return False
        
        if not os.path.isdir(src_dir):
            logging.error(f"Source '{src_dir}' is not a directory")
            return False
        
        # Step 1: Clear destination directory
        if os.path.exists(dest_dir):
            logging.info(f"Removing existing contents of '{dest_dir}'")
            shutil.rmtree(dest_dir)
        
        # Create fresh destination directory
        os.makedirs(dest_dir, exist_ok=True)
        logging.info(f"Created clean destination directory '{dest_dir}'")
        
        # Step 2: Start recursive copy
        logging.info(f"Starting recursive copy from '{src_dir}' to '{dest_dir}'")
        _recursive_copy(src_dir, dest_dir)
        logging.info("✓ Static files copied successfully")
        
        # Step 3: Generate HTML pages from markdown content recursively
        logging.info("Processing markdown files recursively...")
        
        # Process all markdown files in the content directory using the new generate_pages_recursive function
        if os.path.exists(content_dir) and os.path.isdir(content_dir):
            if os.path.exists(template_file):
                logging.info(f"Generating pages from '{content_dir}' using '{template_file}'")
                # Use the recursive function to generate pages for all markdown files
                generate_pages_recursive(content_dir, template_file, dest_dir)
                logging.info(f"✓ Pages generated in '{dest_dir}'")
            else:
                logging.warning(f"⚠️  Template file not found: {template_file}")
        else:
            logging.warning(f"⚠️  Content directory not found: {content_dir}")
        
        logging.info("✓ Build operation completed successfully")
        return True
        
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False

# Usage example and testing
if __name__ == "__main__":
    # Example 1: Use default directories and files
    # This will:
    # - Clear the 'public' directory
    # - Copy 'static' folder contents to 'public'
    # - Generate 'public/index.html' from 'content/index.md' using 'template.html'
    success = copy_static_to_public()
    
    # Example 2: Use custom directories and template
    # success = copy_static_to_public(
    #     src_dir="assets", 
    #     dest_dir="dist", 
    #     content_dir="pages", 
    #     template_file="templates/main.html"
    # )
    
    # Example 3: Use single function approach
    # success = copy_static_to_public_single()
    
    if success:
        print("Build completed successfully!")
    else:
        print("Build failed. Check logs for details.")