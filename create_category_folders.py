#!/usr/bin/env python3
import os
import re

def convert_to_kebab_case(text):
    """Convert a string to kebab case (lowercase with hyphens between words)."""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and other non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remove leading and trailing hyphens
    text = text.strip('-')
    return text

def create_category_folders():
    """Create folders for each category in categories.txt using kebab case."""
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to categories.txt
    categories_file = os.path.join(script_dir, 'categories.txt')
    
    # Path to by-category directory
    by_category_dir = os.path.join(script_dir, 'by-category')
    
    # Create by-category directory if it doesn't exist
    if not os.path.exists(by_category_dir):
        os.makedirs(by_category_dir)
        print(f"Created directory: by-category")
    
    # Check if categories.txt exists
    if not os.path.exists(categories_file):
        print(f"Error: {categories_file} not found.")
        return
    
    # Read categories from file
    with open(categories_file, 'r') as file:
        categories = [line.strip() for line in file if line.strip()]
    
    # Create folders and add .gitkeep files
    created_count = 0
    gitkeep_count = 0
    
    for category in categories:
        folder_name = convert_to_kebab_case(category)
        folder_path = os.path.join(by_category_dir, folder_name)
        
        # Create folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: by-category/{folder_name}")
            created_count += 1
        
        # Add .gitkeep file to the folder
        gitkeep_path = os.path.join(folder_path, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                pass  # Create an empty file
            gitkeep_count += 1
    
    print(f"\nProcess completed. Created {created_count} new folders and added {gitkeep_count} .gitkeep files.")

if __name__ == "__main__":
    create_category_folders()
