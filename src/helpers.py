import os
import shutil
import logging

from src.generate_page import generate_page


def _recursive_copy(src_path, dest_path):
    """
    Recursively copy files and directories from src_path to dest_path.
    
    Args:
        src_path (str): Source path
        dest_path (str): Destination path
    """
    
    try:
        # List all items in the current source directory
        items = os.listdir(src_path)
        
        for item in items:
            src_item_path = os.path.join(src_path, item)
            dest_item_path = os.path.join(dest_path, item)
            
            if os.path.isfile(src_item_path):
                # Copy file with metadata preservation
                shutil.copy2(src_item_path, dest_item_path)
                logging.info(f"📄 Copied file: {src_item_path} → {dest_item_path}")
                
            elif os.path.isdir(src_item_path):
                # Create directory in destination
                os.makedirs(dest_item_path, exist_ok=True)
                logging.info(f"📁 Created directory: {dest_item_path}")
                
                # Recursively copy directory contents
                _recursive_copy(src_item_path, dest_item_path)
                
            else:
                # Handle special files (symlinks, etc.)
                logging.warning(f"⚠️  Skipping special file: {src_item_path}")
                
    except PermissionError as e:
        logging.error(f"❌ Permission denied accessing {src_path}: {e}")
    except FileNotFoundError as e:
        logging.error(f"❌ File not found: {e}")
    except Exception as e:
        logging.error(f"❌ Error processing {src_path}: {e}")


def copy_static_to_public_single(src_dir="static", dest_dir="public", content_dir="content", template_file="template.html", _is_root_call=True):
    """
    Alternative implementation as a single recursive function that also generates pages.
    
    Args:
        src_dir (str): Source directory path
        dest_dir (str): Destination directory path
        content_dir (str): Content directory containing markdown files (default: "content")
        template_file (str): Path to HTML template file (default: "template.html")
        _is_root_call (bool): Internal flag for root call detection
    """
    
    if _is_root_call:
        # Set up logging only on the initial call
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Validate source directory
        if not os.path.exists(src_dir) or not os.path.isdir(src_dir):
            logging.error(f"Invalid source directory: {src_dir}")
            return False
        
        # Clear and recreate destination directory
        if os.path.exists(dest_dir):
            logging.info(f"Clearing destination directory: {dest_dir}")
            shutil.rmtree(dest_dir)
        
        os.makedirs(dest_dir, exist_ok=True)
        logging.info(f"Created destination directory: {dest_dir}")
    
    try:
        items = os.listdir(src_dir)
        
        for item in items:
            src_item = os.path.join(src_dir, item)
            dest_item = os.path.join(dest_dir, item)
            
            if os.path.isfile(src_item):
                shutil.copy2(src_item, dest_item)
                logging.info(f"📄 Copied: {src_item} → {dest_item}")
                
            elif os.path.isdir(src_item):
                os.makedirs(dest_item, exist_ok=True)
                logging.info(f"📁 Created: {dest_item}")
                
                # Recursive call
                copy_static_to_public_single(src_item, dest_item, content_dir, template_file, _is_root_call=False)
        
        if _is_root_call:
            logging.info("✓ Static files copied successfully")
            
            # Generate HTML page from markdown content
            markdown_file = os.path.join(content_dir, "index.md")
            output_file = os.path.join(dest_dir, "index.html")
            
            if os.path.exists(markdown_file) and os.path.exists(template_file):
                logging.info(f"Generating page from '{markdown_file}' using '{template_file}'")
                generate_page(markdown_file, template_file, output_file)
                logging.info(f"✓ Page generated at '{output_file}'")
            else:
                if not os.path.exists(markdown_file):
                    logging.warning(f"⚠️  Markdown file not found: {markdown_file}")
                if not os.path.exists(template_file):
                    logging.warning(f"⚠️  Template file not found: {template_file}")
                logging.info("Skipping page generation due to missing files")
            
            logging.info("✓ Build operation completed successfully")
            return True
            
    except Exception as e:
        logging.error(f"❌ Error: {e}")
        return False if _is_root_call else None