#!/usr/bin/env python3
"""
Database Setup for AI Agent Ideation Generator

This script creates the SQLite database schema for storing AI agent ideas.
"""

import os
import sqlite3
import re
from datetime import datetime
from typing import List, Dict, Any

# Constants
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(REPO_PATH, "ideas.db")
CATEGORIES_DIR = os.path.join(REPO_PATH, "by-category")
INDEX_FILE = os.path.join(REPO_PATH, "index.md")

def create_database():
    """Create the SQLite database and tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        folder_name TEXT UNIQUE NOT NULL
    )
    ''')
    
    # Create ideas table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category_id INTEGER NOT NULL,
        file_path TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print("Database created successfully.")

def import_existing_ideas():
    """Import existing ideas from markdown files into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all categories
    categories = []
    if os.path.exists(CATEGORIES_DIR):
        for folder_name in os.listdir(CATEGORIES_DIR):
            category_path = os.path.join(CATEGORIES_DIR, folder_name)
            if os.path.isdir(category_path):
                category_name = folder_name.replace('-', ' ').title()
                categories.append((category_name, folder_name))
    
    # Insert categories into database
    for category_name, folder_name in categories:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (name, folder_name) VALUES (?, ?)",
            (category_name, folder_name)
        )
    
    conn.commit()
    
    # Parse index file to get ideas
    ideas = []
    try:
        with open(INDEX_FILE, 'r') as f:
            lines = f.readlines()
        
        # Skip header lines (first 5 lines)
        table_lines = lines[5:]
        
        for line in table_lines:
            # Parse markdown table row
            if line.startswith('|') and '|' in line[1:]:
                parts = line.strip().split('|')
                if len(parts) >= 5:  # Should have 5 parts including empty first and last
                    date_str = parts[1].strip()
                    name = parts[2].strip()
                    category = parts[3].strip()
                    
                    # Extract link and path
                    link_match = re.search(r'\[(.*?)\]\((.*?)\)', parts[4].strip())
                    if link_match:
                        path = link_match.group(2)
                        
                        # Parse date
                        try:
                            created_at = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            created_at = datetime.now()
                        
                        ideas.append({
                            'name': name,
                            'category': category,
                            'path': path,
                            'created_at': created_at
                        })
    
    except Exception as e:
        print(f"Error parsing index file: {str(e)}")
    
    # Import ideas into database
    for idea in ideas:
        # Get category ID
        cursor.execute(
            "SELECT id FROM categories WHERE name = ?",
            (idea['category'],)
        )
        category_id = cursor.fetchone()
        
        if category_id:
            category_id = category_id[0]
            
            # Get file content
            file_path = os.path.join(REPO_PATH, idea['path'])
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Extract description
                desc_match = re.search(r'## 2\. Short Description:\s*\n\s*(.+?)\s*\n## ', content, re.DOTALL)
                description = desc_match.group(1).strip() if desc_match else ""
                
                # Insert idea into database
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO ideas 
                    (name, description, category_id, file_path, created_at, content) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (idea['name'], description, category_id, idea['path'], 
                     idea['created_at'], content)
                )
    
    conn.commit()
    
    # Count imported ideas
    cursor.execute("SELECT COUNT(*) FROM ideas")
    idea_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"Imported {idea_count} ideas across {category_count} categories.")

if __name__ == "__main__":
    create_database()
    import_existing_ideas()
