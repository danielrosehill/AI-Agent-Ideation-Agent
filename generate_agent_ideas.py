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
from typing import List, Dict, Optional, Tuple, Any
import difflib
import json
import gc
import signal
import threading

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
INDEX_FILE = os.path.join(REPO_PATH, "index.md")
DEFAULT_MODEL = "llama3.2"  # Default to llama3.2
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MAX_RETRIES = 3  # Maximum number of retries for failed generations
RETRY_DELAY = 2  # Delay between retries in seconds
REQUEST_TIMEOUT = 60  # Timeout for Ollama API requests in seconds
INDEX_LOCK = threading.Lock()  # Lock for thread-safe index updates

def load_categories() -> List[str]:
    """Load categories from the categories file."""
    try:
        with open(CATEGORIES_FILE, 'r') as f:
            categories = [line.strip() for line in f.readlines() if line.strip()]
        return categories
    except Exception as e:
        print_error(f"Error loading categories: {str(e)}")
        return []

def load_template() -> str:
    """Load the template for AI agent ideas."""
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
        return template
    except Exception as e:
        print_error(f"Error loading template: {str(e)}")
        return "## Error: Template could not be loaded\n\nPlease check the template file."

def get_category_folder_name(category: str) -> str:
    """Convert category name to folder name format."""
    # Convert spaces to hyphens and make lowercase
    return category.lower().replace(' ', '-')

def get_existing_ideas(category_folder: str) -> List[str]:
    """Get a list of existing ideas in the category folder."""
    ideas = []
    if os.path.exists(category_folder):
        try:
            for filename in os.listdir(category_folder):
                if filename.endswith('.md') and filename != 'prompt.md':
                    file_path = os.path.join(category_folder, filename)
                    try:
                        with open(file_path, 'r') as f:
                            ideas.append(f.read())
                    except Exception as e:
                        print_error(f"Error reading file {file_path}: {str(e)}")
        except Exception as e:
            print_error(f"Error listing directory {category_folder}: {str(e)}")
    return ideas

def is_similar_idea(new_idea: str, existing_ideas: List[str], threshold: float = 0.8) -> bool:
    """Check if the new idea is similar to any existing ideas."""
    for idea in existing_ideas:
        try:
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
        except Exception as e:
            # If there's an error in comparison, log it but continue
            print_error(f"Error comparing ideas: {str(e)}")
            continue
    
    return False

def create_idea_prompt(category: str, template: str, creativity_level: str = None) -> str:
    """Create a prompt for generating AI agent ideas using Jinja2 templating.
    
    Args:
        category: The category for which to generate an idea
        template: The template to use for the idea
        creativity_level: The creativity level to use (None for random selection)
    """
    try:
        # If no creativity level is specified, randomly select one
        if creativity_level is None:
            creativity_levels = ["basic", "moderate", "creative", "highly_creative"]
            creativity_level = random.choice(creativity_levels)
        
        # Create Jinja2 template environment
        env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Define creativity-specific instructions
        creativity_instructions = {
            "basic": "Create a straightforward, practical, and conventional assistant idea. Focus on solving a common problem in a reliable way without being particularly novel or imaginative.",
            "moderate": "Create a somewhat creative assistant idea that improves upon existing solutions with some innovative elements.",
            "creative": "Create an original and imaginative assistant idea that approaches the problem in a novel way.",
            "highly_creative": "Create an extremely innovative, even quirky or unconventional assistant idea that reimagines how this category could be approached. Don't be afraid to be ambitious, surprising, or even slightly humorous."
        }
        
        # Define the prompt template
        prompt_template = env.from_string("""
You are an AI Agent Ideation Assistant. Your task is to generate a {{ creativity_level }} idea for an AI assistant within the category: {{ category }}.

CREATIVITY LEVEL: {{ creativity_level }}
{{ creativity_instructions }}

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
        return prompt_template.render(
            category=category, 
            template=template, 
            creativity_level=creativity_level.replace('_', ' '),
            creativity_instructions=creativity_instructions[creativity_level]
        )
    except Exception as e:
        print_error(f"Error creating prompt: {str(e)}")
        return f"Error creating prompt: {str(e)}"

def generate_idea_with_ollama(category: str, model: str, template: str, creativity_level: str = None) -> Tuple[str, str]:
    """Generate an AI agent idea using Ollama API with retry logic.
    
    Args:
        category: The category for which to generate an idea
        model: The model to use for generation
        template: The template to use for the idea
        creativity_level: The creativity level to use (None for random selection)
    """
    # If no creativity level is specified, randomly select one
    if creativity_level is None:
        creativity_levels = ["basic", "moderate", "creative", "highly_creative"]
        creativity_level = random.choice(creativity_levels)
    
    # Set temperature based on creativity level
    temperature_settings = {
        "basic": 0.5,       # Lower temperature for more predictable, conventional ideas
        "moderate": 0.7,    # Moderate temperature for some creativity
        "creative": 0.85,   # Higher temperature for more creative ideas
        "highly_creative": 1.0  # Maximum temperature for highly creative, potentially quirky ideas
    }
    
    # Set frequency and presence penalties based on creativity level
    frequency_penalty_settings = {
        "basic": 0.1,
        "moderate": 0.2,
        "creative": 0.3,
        "highly_creative": 0.4
    }
    
    presence_penalty_settings = {
        "basic": 0.1,
        "moderate": 0.2,
        "creative": 0.3,
        "highly_creative": 0.4
    }
    
    # Get temperature for the selected creativity level
    temperature = temperature_settings[creativity_level]
    frequency_penalty = frequency_penalty_settings[creativity_level]
    presence_penalty = presence_penalty_settings[creativity_level]
    
    prompt = create_idea_prompt(category, template, creativity_level)
    
    # Try multiple times in case of failure
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_p": 0.92,
                        "frequency_penalty": frequency_penalty,
                        "presence_penalty": presence_penalty
                    }
                },
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                if attempt < MAX_RETRIES - 1:
                    print_error(f"Ollama API error (attempt {attempt+1}/{MAX_RETRIES}): {response.status_code} - {response.text}")
                    time.sleep(RETRY_DELAY)
                    continue
                else:
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
            
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                print_error(f"Timeout error (attempt {attempt+1}/{MAX_RETRIES}): Request to Ollama timed out after {REQUEST_TIMEOUT} seconds")
                time.sleep(RETRY_DELAY)
            else:
                raise Exception(f"Timeout error: Request to Ollama timed out after {REQUEST_TIMEOUT} seconds")
        except requests.exceptions.ConnectionError:
            if attempt < MAX_RETRIES - 1:
                print_error(f"Connection error (attempt {attempt+1}/{MAX_RETRIES}): Could not connect to Ollama")
                time.sleep(RETRY_DELAY)
            else:
                raise Exception("Connection error: Could not connect to Ollama")
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print_error(f"Error (attempt {attempt+1}/{MAX_RETRIES}): {str(e)}")
                time.sleep(RETRY_DELAY)
            else:
                print_error(f"Error generating idea with Ollama: {e}")
                # Fallback to a simple template with error message
                return f"## 1. Assistant Name:\n\n{category} Assistant (Error)\n\n## 2. Short Description:\n\nError generating idea: {str(e)}\n", f"{category.lower()}-assistant-error"
    
    # If we get here, all attempts failed
    return f"## 1. Assistant Name:\n\n{category} Assistant (Error)\n\n## 2. Short Description:\n\nError generating idea after {MAX_RETRIES} attempts\n", f"{category.lower()}-assistant-error"

def update_index(assistant_name: str, category: str, file_path: str) -> bool:
    """Update the index.md file with a new idea entry."""
    try:
        # Use a lock to prevent multiple threads from updating the index simultaneously
        with INDEX_LOCK:
            # Create the index file if it doesn't exist
            if not os.path.exists(INDEX_FILE):
                with open(INDEX_FILE, 'w') as f:
                    f.write("# AI Agent Ideas Index\n\n")
                    f.write("This page provides a chronological index of all generated AI agent ideas, with the newest ideas listed first.\n\n")
                    f.write("| Date Generated | Assistant Name | Category | Link |\n")
                    f.write("|----------------|----------------|----------|------|\n")
            
            # Get the current date and time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create a relative path for the link
            relative_path = os.path.relpath(file_path, REPO_PATH)
            
            # Create the new row for the table
            new_row = f"| {current_datetime} | {assistant_name} | {category} | [{assistant_name}]({relative_path}) |\n"
            
            # Read the existing content
            with open(INDEX_FILE, 'r') as f:
                content = f.readlines()
            
            # Find the position to insert the new row (after the table header)
            insert_position = 0
            for i, line in enumerate(content):
                if line.startswith("|----"):
                    insert_position = i + 1
                    break
            
            # Insert the new row
            if insert_position > 0:
                content.insert(insert_position, new_row)
                
                # Write the updated content back to the file
                with open(INDEX_FILE, 'w') as f:
                    f.writelines(content)
                
                return True
            else:
                print_error("Could not find table header in index.md")
                return False
                
    except Exception as e:
        print_error(f"Error updating index: {str(e)}")
        return False

def save_idea(idea: str, category: str, filename: str) -> str:
    """Save the generated idea to the appropriate category folder and update the index."""
    try:
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
        
        # Extract the assistant name for the index
        name_match = re.search(r'## 1\. Assistant Name:\s*\n\s*(.+?)\s*\n', idea)
        if name_match:
            assistant_name = name_match.group(1).strip()
        else:
            assistant_name = filename.replace('-', ' ').title()
        
        # Update the index with the new idea
        update_index(assistant_name, category, file_path)
        
        return file_path
    except Exception as e:
        print_error(f"Error saving idea: {str(e)}")
        # Return a path even though saving failed, so the caller knows where it would have been saved
        return os.path.join(CATEGORIES_DIR, get_category_folder_name(category), f"{filename}-error.md")

def get_available_models() -> List[Dict[str, Any]]:
    """Get a list of available models from Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code != 200:
            print_error(f"Error getting models: {response.status_code} - {response.text}")
            return []
        
        return response.json().get("models", [])
    except Exception as e:
        print_error(f"Error getting models: {str(e)}")
        return []

def print_colored(text: str, color_code: str):
    """Print colored text to the console."""
    print(f"{color_code}{text}\033[0m")

def print_header(text: str):
    """Print a header with formatting."""
    print("\n" + "=" * 80)
    print_colored(text, "\033[1;36m")  # Bold Cyan
    print("=" * 80)

def print_success(text: str):
    """Print a success message."""
    print_colored(text, "\033[1;32m")  # Bold Green

def print_error(text: str):
    """Print an error message."""
    print_colored(text, "\033[1;31m")  # Bold Red

def print_info(text: str):
    """Print an info message."""
    print_colored(text, "\033[1;34m")  # Bold Blue

def interactive_mode():
    """Run the script in interactive mode."""
    print_header("AI Agent Ideation Generator - Interactive Mode")
    
    # Get available models
    models = get_available_models()
    if not models:
        print_error("No models found. Make sure Ollama is running and has models pulled.")
        return
    
    # Display available models
    print_info("Available models:")
    for i, model in enumerate(models, 1):
        model_name = model.get("name")
        model_size = model.get("details", {}).get("parameter_size", "Unknown size")
        print(f"{i}. {model_name} ({model_size})")
    
    # Select model
    while True:
        try:
            model_idx = int(input("\nSelect a model (number): ")) - 1
            if 0 <= model_idx < len(models):
                selected_model = models[model_idx]["name"]
                break
            else:
                print_error("Invalid selection. Please try again.")
        except ValueError:
            print_error("Please enter a number.")
    
    print_success(f"Selected model: {selected_model}")
    
    # Get number of ideas to generate
    while True:
        try:
            num_ideas = int(input("\nHow many ideas would you like to generate? "))
            if num_ideas > 0:
                break
            else:
                print_error("Please enter a positive number.")
        except ValueError:
            print_error("Please enter a number.")
    
    # Get similarity threshold
    while True:
        try:
            similarity_threshold = float(input("\nEnter similarity threshold (0.0-1.0, default 0.8): ") or "0.8")
            if 0.0 <= similarity_threshold <= 1.0:
                break
            else:
                print_error("Please enter a value between 0.0 and 1.0.")
        except ValueError:
            print_error("Please enter a valid number.")
    
    print_header("Starting Generation")
    print_info(f"Generating {num_ideas} ideas with model {selected_model}")
    print_info(f"Similarity threshold: {similarity_threshold}")
    
    # Load categories and template
    categories = load_categories()
    if not categories:
        print_error("No categories found. Please check the categories file.")
        return
    
    template = load_template()
    
    # Setup for graceful termination
    stop_event = threading.Event()
    
    def signal_handler(sig, frame):
        print_info("\nStopping generation gracefully. Please wait...")
        stop_event.set()
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate ideas
    successful_generations = 0
    attempts = 0
    
    try:
        while successful_generations < num_ideas and not stop_event.is_set():
            attempts += 1
            
            # Periodically clean up memory
            if attempts % 50 == 0:
                gc.collect()
            
            # Randomly select a category
            category = random.choice(categories)
            
            print_info(f"\nGenerating idea {successful_generations+1}/{num_ideas} for category: {category}")
            
            try:
                # Generate the idea
                idea, filename = generate_idea_with_ollama(category, selected_model, template)
                
                # Check if the idea is similar to existing ideas
                category_folder = os.path.join(CATEGORIES_DIR, get_category_folder_name(category))
                existing_ideas = get_existing_ideas(category_folder)
                
                if is_similar_idea(idea, existing_ideas, similarity_threshold):
                    print_info(f"Skipped: Similar idea already exists for {category}")
                    continue
                
                # Save the idea
                file_path = save_idea(idea, category, filename)
                
                # Extract the assistant name for display
                name_match = re.search(r'## 1\. Assistant Name:\s*\n\s*(.+?)\s*\n', idea)
                if name_match:
                    assistant_name = name_match.group(1).strip()
                    print_success(f"Generated: {assistant_name} (Category: {category})")
                else:
                    print_success(f"Generated idea for category: {category}")
                
                print_info(f"Saved to: {file_path}")
                
                successful_generations += 1
                
            except Exception as e:
                print_error(f"Error: {str(e)}")
                # Wait a bit before trying again
                time.sleep(1)
            
            # Small delay between generations to prevent overloading Ollama
            time.sleep(0.1)
        
        if stop_event.is_set():
            print_header("Generation stopped by user")
        else:
            print_header("Generation Complete")
        
        print_success(f"Successfully generated {successful_generations} ideas after {attempts} attempts.")
        
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
    finally:
        # Final memory cleanup
        gc.collect()

def main():
    """Main function to generate AI agent ideas."""
    parser = argparse.ArgumentParser(description="Generate AI agent ideas")
    parser.add_argument("num_ideas", type=int, nargs="?", default=10, help="Number of ideas to generate")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help=f"Ollama model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--similarity-threshold", type=float, default=0.8, help="Threshold for similarity checking (0.0-1.0, default: 0.8)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    # Non-interactive mode
    print_header("AI Agent Ideation Generator")
    
    # Validate arguments
    if args.num_ideas <= 0:
        print_error("Number of ideas must be positive")
        return
    
    if not (0.0 <= args.similarity_threshold <= 1.0):
        print_error("Similarity threshold must be between 0.0 and 1.0")
        return
    
    # Check if Ollama is available
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print_error("Error: Ollama is not available. Make sure it's running.")
            return
    except Exception as e:
        print_error(f"Error connecting to Ollama: {str(e)}")
        return
    
    # Check if the model exists
    models = get_available_models()
    model_names = [model.get("name") for model in models]
    
    if args.model not in model_names:
        print_error(f"Model '{args.model}' not found in Ollama.")
        print_info("Available models:")
        for model_name in model_names:
            print(f"- {model_name}")
        return
    
    print_info(f"Using model: {args.model}")
    print_info(f"Generating {args.num_ideas} ideas")
    print_info(f"Similarity threshold: {args.similarity_threshold}")
    
    # Load categories and template
    categories = load_categories()
    if not categories:
        print_error("No categories found. Please check the categories file.")
        return
    
    template = load_template()
    
    # Setup for graceful termination
    stop_event = threading.Event()
    
    def signal_handler(sig, frame):
        print_info("\nStopping generation gracefully. Please wait...")
        stop_event.set()
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate ideas
    successful_generations = 0
    attempts = 0
    
    try:
        while successful_generations < args.num_ideas and not stop_event.is_set():
            attempts += 1
            
            # Periodically clean up memory
            if attempts % 50 == 0:
                gc.collect()
            
            # Randomly select a category
            category = random.choice(categories)
            
            # Show progress
            progress = f"[{successful_generations}/{args.num_ideas}]"
            print(f"{progress} Generating idea for category: {category}...", end="\r")
            
            try:
                # Generate the idea
                idea, filename = generate_idea_with_ollama(category, args.model, template)
                
                # Check if the idea is similar to existing ideas
                category_folder = os.path.join(CATEGORIES_DIR, get_category_folder_name(category))
                existing_ideas = get_existing_ideas(category_folder)
                
                if is_similar_idea(idea, existing_ideas, args.similarity_threshold):
                    print(f"{progress} Skipped: Similar idea already exists for {category}".ljust(80))
                    continue
                
                # Save the idea
                file_path = save_idea(idea, category, filename)
                
                # Extract the assistant name for display
                name_match = re.search(r'## 1\. Assistant Name:\s*\n\s*(.+?)\s*\n', idea)
                if name_match:
                    assistant_name = name_match.group(1).strip()
                    print(f"{progress} Generated: {assistant_name} (Category: {category})".ljust(80))
                else:
                    print(f"{progress} Generated idea for category: {category}".ljust(80))
                
                successful_generations += 1
                
            except Exception as e:
                print(f"{progress} Error: {str(e)}".ljust(80))
                # Wait a bit before trying again
                time.sleep(1)
            
            # Small delay between generations to prevent overloading Ollama
            time.sleep(0.1)
        
        print("\n" + "=" * 80)
        if stop_event.is_set():
            print_info("Generation stopped by user")
        else:
            print_info("Generation Complete")
        
        print_success(f"Successfully generated {successful_generations} ideas after {attempts} attempts.")
        
    except Exception as e:
        print_error(f"\nUnexpected error: {str(e)}")
    finally:
        # Final memory cleanup
        gc.collect()

if __name__ == "__main__":
    main()
