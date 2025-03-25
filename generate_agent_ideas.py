#!/usr/bin/env python3
"""
AI Agent Ideation Generator

This script generates ideas for AI agents based on randomly selected categories.
It uses Ollama with Jinja2 templating to generate the ideas and saves them to the appropriate category folders.
"""

import os
import sys
import random
import re
import time
import argparse
from datetime import datetime
import hashlib
from typing import List, Dict, Optional, Tuple
import difflib
import json

# Check if required packages are installed, if not install them
try:
    import requests
    import jinja2
except ImportError:
    import subprocess
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "jinja2"])
    import requests
    import jinja2

# Constants
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
CATEGORIES_FILE = os.path.join(REPO_PATH, "categories.txt")
TEMPLATE_FILE = os.path.join(REPO_PATH, "templates", "template.md")
CATEGORIES_DIR = os.path.join(REPO_PATH, "by-category")
DEFAULT_MODEL = "llama3.2"  # Default to llama3.2
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def load_categories() -> List[str]:
    """Load categories from the categories file."""
    with open(CATEGORIES_FILE, 'r') as f:
        categories = [line.strip() for line in f.readlines() if line.strip()]
    return categories

def load_template() -> str:
    """Load the template for AI agent ideas."""
    with open(TEMPLATE_FILE, 'r') as f:
        template = f.read()
    return template

def get_category_folder_name(category: str) -> str:
    """Convert category name to folder name format."""
    # Convert spaces to hyphens and make lowercase
    return category.lower().replace(' ', '-')

def get_existing_ideas(category_folder: str) -> List[str]:
    """Get a list of existing ideas in the category folder."""
    ideas = []
    if os.path.exists(category_folder):
        for filename in os.listdir(category_folder):
            if filename.endswith('.md') and filename != 'prompt.md':
                file_path = os.path.join(category_folder, filename)
                with open(file_path, 'r') as f:
                    ideas.append(f.read())
    return ideas

def is_similar_idea(new_idea: str, existing_ideas: List[str], threshold: float = 0.8) -> bool:
    """Check if the new idea is similar to any existing ideas."""
    for idea in existing_ideas:
        # Extract the assistant name and description for comparison
        new_name_match = re.search(r'## 1\. Assistant Name:\s*\n\s*(.+?)\s*\n', new_idea)
        existing_name_match = re.search(r'## 1\. Assistant Name:\s*\n\s*(.+?)\s*\n', idea)
        
        new_desc_match = re.search(r'## 2\. Short Description:\s*\n\s*(.+?)\s*\n', new_idea)
        existing_desc_match = re.search(r'## 2\. Short Description:\s*\n\s*(.+?)\s*\n', idea)
        
        if new_name_match and existing_name_match:
            new_name = new_name_match.group(1)
            existing_name = existing_name_match.group(1)
            
            # Check name similarity
            name_similarity = difflib.SequenceMatcher(None, new_name, existing_name).ratio()
            if name_similarity > threshold:
                return True
        
        if new_desc_match and existing_desc_match:
            new_desc = new_desc_match.group(1)
            existing_desc = existing_desc_match.group(1)
            
            # Check description similarity
            desc_similarity = difflib.SequenceMatcher(None, new_desc, existing_desc).ratio()
            if desc_similarity > threshold:
                return True
    
    return False

def create_idea_prompt(category: str, template: str) -> str:
    """Create a prompt for generating AI agent ideas using Jinja2 templating."""
    # Create Jinja2 template environment
    env = jinja2.Environment(
        loader=jinja2.BaseLoader(),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Define the prompt template
    prompt_template = env.from_string("""
You are an AI Agent Ideation Assistant. Your task is to generate a creative, original, and highly specific idea for an AI assistant within the category: {{ category }}.

IMPORTANT: Do NOT create a generic assistant that covers the entire category. Instead, focus on a very specific niche, use case, or problem within that category.

For example:
- Instead of a general "Cooking Assistant", create something like "SousVide Master" - an assistant specifically for sous vide cooking techniques
- Instead of a general "Productivity Assistant", create something like "Meeting Summarizer Pro" - an assistant that specifically creates actionable summaries from meeting transcripts
- Instead of a general "Travel Assistant", create something like "Solo Female Traveler Safety Guide" - an assistant focused on safety tips for women traveling alone

Your idea should be:
1. Highly specific and focused on a particular niche within the category
2. Original and creative - not an obvious or common assistant concept
3. Practical and solve a real problem for users
4. Have a catchy, memorable name that clearly indicates its specific purpose

Here's the template to fill out:

{{ template }}

Generate a complete, detailed, and creative AI assistant idea for a specific niche within the {{ category }} category. Be specific, original, and provide concrete examples.
""")
    
    # Render the template with the provided variables
    return prompt_template.render(category=category, template=template)

def generate_idea_with_ollama(category: str, model: str, template: str) -> Tuple[str, str]:
    """Generate an AI agent idea using Ollama API."""
    prompt = create_idea_prompt(category, template)
    
    # Generate the idea using Ollama API
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.85,  # Increased for more creativity
                    "top_p": 0.92,        # Slightly increased
                    "frequency_penalty": 0.3,  # Increased to reduce repetition
                    "presence_penalty": 0.3    # Increased to encourage novelty
                }
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
        
        generated_text = response.json()["response"].strip()
        
        # Extract assistant name for the filename
        name_match = re.search(r'## 1\. Assistant Name:\s*\n\s*(.+?)\s*\n', generated_text)
        if name_match:
            assistant_name = name_match.group(1).strip()
        else:
            # If name not found, generate a random name based on category
            assistant_name = f"{category}-Specialized-Assistant"
        
        # Create a filename-friendly version of the assistant name
        filename = assistant_name.lower().replace(' ', '-').replace('/', '-').replace('\\', '-')
        filename = re.sub(r'[^\w\-]', '', filename)
        
        return generated_text, filename
    
    except Exception as e:
        print(f"Error generating idea with Ollama: {e}")
        # Fallback to a simple template with error message
        return f"## 1. Assistant Name:\n\n{category} Assistant (Error)\n\n## 2. Short Description:\n\nError generating idea: {str(e)}\n", f"{category.lower()}-assistant-error"

def save_idea(idea: str, category: str, filename: str) -> str:
    """Save the generated idea to the appropriate category folder."""
    folder_name = get_category_folder_name(category)
    category_folder = os.path.join(CATEGORIES_DIR, folder_name)
    
    # Create the category folder if it doesn't exist
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
    
    # Use just the filename without timestamp
    file_path = os.path.join(category_folder, f"{filename}.md")
    
    # If file already exists, add a number suffix
    counter = 1
    original_file_path = file_path
    while os.path.exists(file_path):
        file_path = original_file_path.replace('.md', f'-{counter}.md')
        counter += 1
    
    with open(file_path, 'w') as f:
        f.write(idea)
    
    return file_path

def get_available_models() -> List[Dict]:
    """Get a list of available models from Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            return []
        
        return response.json().get("models", [])
    except Exception as e:
        print(f"Error fetching available models: {e}")
        return []

def print_colored(text: str, color_code: str) -> None:
    """Print colored text to the console."""
    print(f"{color_code}{text}\033[0m")

def print_header(text: str) -> None:
    """Print a header with formatting."""
    print("\n" + "=" * 60)
    print_colored(f"  {text}", "\033[1;36m")  # Bold Cyan
    print("=" * 60)

def print_success(text: str) -> None:
    """Print a success message."""
    print_colored(text, "\033[1;32m")  # Bold Green

def print_error(text: str) -> None:
    """Print an error message."""
    print_colored(text, "\033[1;31m")  # Bold Red

def print_info(text: str) -> None:
    """Print an info message."""
    print_colored(text, "\033[1;34m")  # Bold Blue

def interactive_mode() -> None:
    """Run the script in interactive mode."""
    print_header("AI Agent Ideation Generator")
    
    # Check if Ollama is available
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            print_error("Error: Ollama is not available. Make sure it's running.")
            sys.exit(1)
    except Exception as e:
        print_error(f"Error connecting to Ollama: {e}")
        print_info("Make sure Ollama is running on http://localhost:11434")
        sys.exit(1)
    
    # Get available models
    models = get_available_models()
    if not models:
        print_error("No models found in Ollama. Please pull at least one model.")
        sys.exit(1)
    
    # Display available models
    print_header("Available Models")
    for i, model in enumerate(models, 1):
        model_name = model.get("name")
        model_size = model.get("details", {}).get("parameter_size", "Unknown size")
        print(f"{i}. {model_name} ({model_size})")
    
    # Let user select a model
    while True:
        try:
            choice = input("\nSelect a model (number): ")
            model_index = int(choice) - 1
            if 0 <= model_index < len(models):
                selected_model = models[model_index]["name"]
                print_success(f"Selected model: {selected_model}")
                break
            else:
                print_error("Invalid selection. Please try again.")
        except ValueError:
            print_error("Please enter a valid number.")
    
    # Ask for number of suggestions
    while True:
        try:
            num_suggestions = input("\nHow many AI agent ideas would you like to generate? ")
            num_suggestions = int(num_suggestions)
            if num_suggestions > 0:
                break
            else:
                print_error("Please enter a positive number.")
        except ValueError:
            print_error("Please enter a valid number.")
    
    # Ask for similarity threshold
    while True:
        try:
            threshold_input = input("\nEnter similarity threshold (0.0-1.0, default: 0.8): ")
            if not threshold_input:
                similarity_threshold = 0.8
                break
            
            similarity_threshold = float(threshold_input)
            if 0.0 <= similarity_threshold <= 1.0:
                break
            else:
                print_error("Threshold must be between 0.0 and 1.0.")
        except ValueError:
            print_error("Please enter a valid number.")
    
    # Load categories and template
    categories = load_categories()
    if not categories:
        print_error("No categories found in the categories file")
        sys.exit(1)
    
    template = load_template()
    
    # Generate ideas
    print_header(f"Generating {num_suggestions} AI agent ideas using {selected_model}")
    
    successful_generations = 0
    attempts = 0
    max_attempts = num_suggestions * 2  # Allow for some failures
    
    while successful_generations < num_suggestions and attempts < max_attempts:
        attempts += 1
        
        # Randomly select a category
        category = random.choice(categories)
        print(f"\nGenerating idea {successful_generations + 1}/{num_suggestions} for category: {category}")
        
        try:
            # Generate the idea
            idea, filename = generate_idea_with_ollama(category, selected_model, template)
            
            # Check if the idea is similar to existing ideas
            category_folder = os.path.join(CATEGORIES_DIR, get_category_folder_name(category))
            existing_ideas = get_existing_ideas(category_folder)
            
            if is_similar_idea(idea, existing_ideas, similarity_threshold):
                print_info(f"Similar idea already exists for {category}. Skipping...")
                continue
            
            # Save the idea
            file_path = save_idea(idea, category, filename)
            print_success(f"Idea saved to: {file_path}")
            
            successful_generations += 1
            
        except Exception as e:
            print_error(f"Error generating idea: {e}")
            # Wait a bit before trying again
            time.sleep(1)
    
    if successful_generations < num_suggestions:
        print_error(f"\nWarning: Only generated {successful_generations} ideas after {attempts} attempts.")
    else:
        print_success(f"\nSuccessfully generated {successful_generations} AI agent ideas!")

def main():
    """Main function to generate AI agent ideas."""
    parser = argparse.ArgumentParser(description="Generate AI agent ideas")
    parser.add_argument("num_suggestions", type=int, nargs="?", 
                        help="Number of suggestions to generate (optional in interactive mode)")
    parser.add_argument("--similarity-threshold", type=float, default=0.8, 
                        help="Threshold for similarity check (0.0-1.0, default: 0.8)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                        help=f"Ollama model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # If interactive mode is requested or no num_suggestions is provided
    if args.interactive or args.num_suggestions is None:
        interactive_mode()
        return
    
    # Non-interactive mode
    if args.num_suggestions <= 0:
        print("Number of suggestions must be greater than 0")
        sys.exit(1)
    
    # Check if Ollama is available and the model is loaded
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            print(f"Error: Ollama is not available.")
            print("Make sure Ollama is running.")
            sys.exit(1)
        
        # Check if the model is in the list of available models
        models = response.json().get("models", [])
        model_found = False
        for m in models:
            if m.get("name") == args.model:
                model_found = True
                break
        
        if not model_found:
            # If model not found, try to pull it
            print(f"Model {args.model} not found. Attempting to pull...")
            pull_response = requests.post(
                "http://localhost:11434/api/pull",
                json={"name": args.model}
            )
            
            if pull_response.status_code != 200:
                print(f"Error pulling model {args.model}.")
                print("Available models:")
                for model in models:
                    print(f"- {model.get('name')}")
                sys.exit(1)
    
    except Exception as e:
        print(f"Error checking Ollama availability: {e}")
        print("Make sure Ollama is running.")
        sys.exit(1)
    
    # Load categories
    categories = load_categories()
    if not categories:
        print("No categories found in the categories file")
        sys.exit(1)
    
    # Load template
    template = load_template()
    
    print(f"Generating {args.num_suggestions} AI agent ideas using {args.model}...")
    
    successful_generations = 0
    attempts = 0
    max_attempts = args.num_suggestions * 2  # Allow for some failures
    
    while successful_generations < args.num_suggestions and attempts < max_attempts:
        attempts += 1
        
        # Randomly select a category
        category = random.choice(categories)
        print(f"\nGenerating idea {successful_generations + 1}/{args.num_suggestions} for category: {category}")
        
        try:
            # Generate the idea
            idea, filename = generate_idea_with_ollama(category, args.model, template)
            
            # Check if the idea is similar to existing ideas
            category_folder = os.path.join(CATEGORIES_DIR, get_category_folder_name(category))
            existing_ideas = get_existing_ideas(category_folder)
            
            if is_similar_idea(idea, existing_ideas, args.similarity_threshold):
                print(f"Similar idea already exists for {category}. Skipping...")
                continue
            
            # Save the idea
            file_path = save_idea(idea, category, filename)
            print(f"Idea saved to: {file_path}")
            
            successful_generations += 1
            
        except Exception as e:
            print(f"Error generating idea: {e}")
            # Wait a bit before trying again
            time.sleep(1)
    
    if successful_generations < args.num_suggestions:
        print(f"\nWarning: Only generated {successful_generations} ideas after {attempts} attempts.")
    else:
        print(f"\nSuccessfully generated {successful_generations} AI agent ideas!")

if __name__ == "__main__":
    main()
