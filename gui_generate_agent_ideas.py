#!/usr/bin/env python3
"""
AI Agent Ideation Generator GUI

This script provides a graphical user interface for generating ideas for AI agents
based on randomly selected categories. It uses Ollama with Jinja2 templating to generate
the ideas and saves them to the appropriate category folders.
"""

import os
import sys
import random
import re
import time
import gc
from datetime import datetime
import hashlib
import difflib
import json
from typing import List, Dict, Optional, Tuple, Any

# Check if required packages are installed, if not install them
try:
    import requests
    import jinja2
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QComboBox, QSpinBox, QTextEdit, QProgressBar,
        QRadioButton, QButtonGroup, QLineEdit, QGroupBox, QMessageBox,
        QSlider, QSplitter, QFrame, QCheckBox
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QIcon
except ImportError:
    import subprocess
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "jinja2", "PyQt6"])
    import requests
    import jinja2
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QComboBox, QSpinBox, QTextEdit, QProgressBar,
        QRadioButton, QButtonGroup, QLineEdit, QGroupBox, QMessageBox,
        QSlider, QSplitter, QFrame, QCheckBox
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QIcon

# Import functions from the CLI version
from generate_agent_ideas import (
    load_categories, load_template, get_category_folder_name,
    get_existing_ideas, is_similar_idea, create_idea_prompt,
    generate_idea_with_ollama, save_idea, get_available_models
)

# Constants
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
CATEGORIES_FILE = os.path.join(REPO_PATH, "categories.txt")
TEMPLATE_FILE = os.path.join(REPO_PATH, "templates", "template.md")
CATEGORIES_DIR = os.path.join(REPO_PATH, "by-category")
DEFAULT_MODEL = "llama3.2"  # Default to llama3.2
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MAX_RETRIES = 3  # Maximum number of retries for failed generations
RETRY_DELAY = 2  # Delay between retries in seconds

# Worker thread for generating ideas
class IdeaGeneratorThread(QThread):
    # Signals
    progress_update = pyqtSignal(int, int)  # current, total
    idea_generated = pyqtSignal(str, str, str)  # idea, category, filename
    idea_skipped = pyqtSignal(str)  # reason
    error_occurred = pyqtSignal(str)  # error message
    generation_complete = pyqtSignal(int, int)  # successful, total attempts
    
    def __init__(self, model: str, num_ideas: int, similarity_threshold: float, parent=None):
        super().__init__(parent)
        self.model = model
        self.num_ideas = num_ideas
        self.similarity_threshold = similarity_threshold
        self.running = True
        self.unlimited = False
        self.memory_cleanup_interval = 50  # Clean up memory every 50 generations
        
    def set_unlimited(self, unlimited: bool):
        self.unlimited = unlimited
        
    def stop(self):
        self.running = False
        
    def run(self):
        # Load categories and template
        categories = load_categories()
        if not categories:
            self.error_occurred.emit("No categories found in the categories file")
            return
        
        template = load_template()
        
        successful_generations = 0
        attempts = 0
        
        while (self.unlimited or successful_generations < self.num_ideas) and self.running:
            attempts += 1
            
            # Periodically clean up memory
            if attempts % self.memory_cleanup_interval == 0:
                gc.collect()
            
            # Randomly select a category
            category = random.choice(categories)
            self.progress_update.emit(successful_generations, self.num_ideas if not self.unlimited else -1)
            
            # Try to generate with retries
            retry_count = 0
            generation_successful = False
            
            while retry_count < MAX_RETRIES and not generation_successful and self.running:
                try:
                    # Generate the idea
                    idea, filename = generate_idea_with_ollama(category, self.model, template)
                    
                    # Check if the idea is similar to existing ideas
                    category_folder = os.path.join(CATEGORIES_DIR, get_category_folder_name(category))
                    existing_ideas = get_existing_ideas(category_folder)
                    
                    if is_similar_idea(idea, existing_ideas, self.similarity_threshold):
                        self.idea_skipped.emit(f"Similar idea already exists for {category}")
                        generation_successful = True  # Consider it successful to avoid retries for similarity
                        break
                    
                    # Save the idea
                    file_path = save_idea(idea, category, filename)
                    self.idea_generated.emit(idea, category, file_path)
                    
                    successful_generations += 1
                    generation_successful = True
                    
                except Exception as e:
                    retry_count += 1
                    error_msg = f"Error generating idea (attempt {retry_count}/{MAX_RETRIES}): {str(e)}"
                    self.error_occurred.emit(error_msg)
                    
                    if retry_count < MAX_RETRIES and self.running:
                        self.error_occurred.emit(f"Retrying in {RETRY_DELAY} seconds...")
                        time.sleep(RETRY_DELAY)
                    else:
                        self.error_occurred.emit("Max retries reached, skipping this generation")
            
            # Small delay between generations to prevent overloading Ollama
            if self.running and generation_successful:
                time.sleep(0.1)
        
        self.generation_complete.emit(successful_generations, attempts)

# Main window
class AIAgentIdeationGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Agent Ideation Generator")
        self.setMinimumSize(800, 600)
        
        # Initialize UI
        self.init_ui()
        
        # Check Ollama availability and load models
        self.check_ollama()
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Title
        title_label = QLabel("AI Agent Ideation Generator")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create a splitter for the main content
        splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(splitter)
        
        # Top section: Configuration
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        
        # Model selection
        model_group = QGroupBox("Model Selection")
        model_layout = QVBoxLayout(model_group)
        
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(300)
        self.refresh_button = QPushButton("Refresh Models")
        self.refresh_button.clicked.connect(self.load_models)
        
        model_hbox = QHBoxLayout()
        model_hbox.addWidget(QLabel("Select Model:"))
        model_hbox.addWidget(self.model_combo)
        model_hbox.addWidget(self.refresh_button)
        model_hbox.addStretch(1)
        
        model_layout.addLayout(model_hbox)
        config_layout.addWidget(model_group)
        
        # Number of ideas
        ideas_group = QGroupBox("Number of Ideas")
        ideas_layout = QVBoxLayout(ideas_group)
        
        # Radio buttons for preset values
        self.ideas_type_group = QButtonGroup(self)
        
        presets_layout = QHBoxLayout()
        
        for preset in [50, 100, 500, 1000]:
            radio = QRadioButton(str(preset))
            self.ideas_type_group.addButton(radio)
            presets_layout.addWidget(radio)
        
        # Custom number option
        self.custom_radio = QRadioButton("Custom:")
        self.ideas_type_group.addButton(self.custom_radio)
        self.custom_spinbox = QSpinBox()
        self.custom_spinbox.setRange(1, 10000)
        self.custom_spinbox.setValue(10)
        self.custom_spinbox.setEnabled(False)
        
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(self.custom_radio)
        custom_layout.addWidget(self.custom_spinbox)
        
        # Unlimited option
        self.unlimited_radio = QRadioButton("Until stopped")
        self.ideas_type_group.addButton(self.unlimited_radio)
        
        # Connect radio buttons
        self.ideas_type_group.buttonClicked.connect(self.on_ideas_type_changed)
        
        # Default selection
        self.ideas_type_group.buttons()[0].setChecked(True)
        
        ideas_layout.addLayout(presets_layout)
        ideas_layout.addLayout(custom_layout)
        ideas_layout.addWidget(self.unlimited_radio)
        
        config_layout.addWidget(ideas_group)
        
        # Similarity threshold
        similarity_group = QGroupBox("Similarity Threshold")
        similarity_layout = QVBoxLayout(similarity_group)
        
        self.similarity_slider = QSlider(Qt.Orientation.Horizontal)
        self.similarity_slider.setRange(0, 100)
        self.similarity_slider.setValue(80)  # Default 0.8
        self.similarity_label = QLabel("0.80")
        
        self.similarity_slider.valueChanged.connect(self.update_similarity_label)
        
        similarity_layout.addWidget(QLabel("Set similarity threshold for duplicate detection:"))
        
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("0.0"))
        slider_layout.addWidget(self.similarity_slider)
        slider_layout.addWidget(QLabel("1.0"))
        slider_layout.addWidget(self.similarity_label)
        
        similarity_layout.addLayout(slider_layout)
        config_layout.addWidget(similarity_group)
        
        # Advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QVBoxLayout(advanced_group)
        
        self.auto_scroll_checkbox = QCheckBox("Auto-scroll log")
        self.auto_scroll_checkbox.setChecked(True)
        advanced_layout.addWidget(self.auto_scroll_checkbox)
        
        self.clear_log_button = QPushButton("Clear Log")
        self.clear_log_button.clicked.connect(self.clear_log)
        advanced_layout.addWidget(self.clear_log_button)
        
        config_layout.addWidget(advanced_group)
        
        # Generate button
        self.generate_button = QPushButton("Generate Ideas")
        self.generate_button.setMinimumHeight(40)
        self.generate_button.clicked.connect(self.start_generation)
        
        self.stop_button = QPushButton("Stop Generation")
        self.stop_button.setMinimumHeight(40)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_generation)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.generate_button)
        buttons_layout.addWidget(self.stop_button)
        
        config_layout.addLayout(buttons_layout)
        
        # Add configuration widget to splitter
        splitter.addWidget(config_widget)
        
        # Bottom section: Progress and output
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        
        # Progress bar
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_label = QLabel("Ready")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        
        output_layout.addWidget(progress_group)
        
        # Output log
        log_group = QGroupBox("Output Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        log_layout.addWidget(self.log_text)
        
        output_layout.addWidget(log_group)
        
        # Add output widget to splitter
        splitter.addWidget(output_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([300, 300])
        
        # Set the main widget
        self.setCentralWidget(main_widget)
        
        # Initialize generator thread
        self.generator_thread = None
        
        # Setup periodic memory cleanup
        self.cleanup_timer = QTimer(self)
        self.cleanup_timer.timeout.connect(self.perform_memory_cleanup)
        self.cleanup_timer.start(60000)  # Run every minute
    
    def perform_memory_cleanup(self):
        """Perform periodic memory cleanup."""
        gc.collect()
    
    def clear_log(self):
        """Clear the log text area."""
        self.log_text.clear()
        self.log_message("Log cleared")
    
    def check_ollama(self):
        """Check if Ollama is available and load models."""
        self.log_message("Checking Ollama availability...")
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code != 200:
                self.show_error("Error: Ollama is not available. Make sure it's running.")
                return
            
            self.log_message("Ollama is available.")
            self.load_models()
            
        except requests.exceptions.ConnectionError:
            self.show_error("Error: Could not connect to Ollama. Make sure it's running on http://localhost:11434")
        except requests.exceptions.Timeout:
            self.show_error("Error: Connection to Ollama timed out. The server might be overloaded.")
        except Exception as e:
            self.show_error(f"Error connecting to Ollama: {str(e)}\nMake sure Ollama is running on http://localhost:11434")
    
    def load_models(self):
        """Load available models from Ollama."""
        self.log_message("Loading available models...")
        self.model_combo.clear()
        
        try:
            models = get_available_models()
            if not models:
                self.show_error("No models found in Ollama. Please pull at least one model.")
                return
            
            for model in models:
                model_name = model.get("name")
                model_size = model.get("details", {}).get("parameter_size", "Unknown size")
                self.model_combo.addItem(f"{model_name} ({model_size})", model_name)
            
            self.log_message(f"Loaded {len(models)} models.")
        except Exception as e:
            self.show_error(f"Error loading models: {str(e)}")
    
    def on_ideas_type_changed(self, button):
        """Handle change in ideas type selection."""
        self.custom_spinbox.setEnabled(button == self.custom_radio)
    
    def update_similarity_label(self):
        """Update the similarity threshold label."""
        value = self.similarity_slider.value() / 100.0
        self.similarity_label.setText(f"{value:.2f}")
    
    def get_num_ideas(self) -> int:
        """Get the number of ideas to generate based on UI selection."""
        selected_button = self.ideas_type_group.checkedButton()
        
        if selected_button == self.custom_radio:
            return self.custom_spinbox.value()
        elif selected_button == self.unlimited_radio:
            return -1  # Unlimited
        else:
            return int(selected_button.text())
    
    def start_generation(self):
        """Start generating ideas."""
        # Get selected model
        if self.model_combo.count() == 0:
            self.show_error("No models available. Please check Ollama.")
            return
        
        model_data = self.model_combo.currentData()
        
        # Get number of ideas
        num_ideas = self.get_num_ideas()
        unlimited = (num_ideas == -1)
        if unlimited:
            num_ideas = 1000000  # Just a large number for the thread
        
        # Get similarity threshold
        similarity_threshold = self.similarity_slider.value() / 100.0
        
        # Update UI
        self.generate_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        
        if unlimited:
            self.progress_bar.setFormat("Unlimited - %v ideas generated")
        else:
            self.progress_bar.setMaximum(num_ideas)
            self.progress_bar.setFormat("%v/%m ideas generated (%p%)")
        
        self.log_message(f"Starting generation with model: {model_data}")
        self.log_message(f"Number of ideas: {'Unlimited' if unlimited else num_ideas}")
        self.log_message(f"Similarity threshold: {similarity_threshold}")
        
        # Create and start generator thread
        self.generator_thread = IdeaGeneratorThread(model_data, num_ideas, similarity_threshold)
        self.generator_thread.set_unlimited(unlimited)
        
        # Connect signals
        self.generator_thread.progress_update.connect(self.update_progress)
        self.generator_thread.idea_generated.connect(self.on_idea_generated)
        self.generator_thread.idea_skipped.connect(self.on_idea_skipped)
        self.generator_thread.error_occurred.connect(self.on_error)
        self.generator_thread.generation_complete.connect(self.on_generation_complete)
        
        # Start generation
        self.generator_thread.start()
    
    def stop_generation(self):
        """Stop the idea generation process."""
        if self.generator_thread and self.generator_thread.isRunning():
            self.log_message("Stopping generation...")
            self.stop_button.setEnabled(False)  # Prevent multiple clicks
            self.stop_button.setText("Stopping...")
            self.generator_thread.stop()
            
            # Don't wait here as it would freeze the UI
            # Instead, we'll update the UI when the thread signals completion
    
    def update_progress(self, current: int, total: int):
        """Update the progress bar."""
        if total == -1:  # Unlimited mode
            self.progress_bar.setMaximum(0)  # Indeterminate mode
            self.progress_bar.setValue(0)
            self.progress_label.setText(f"Generated {current} ideas so far...")
        else:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
            self.progress_label.setText(f"Generated {current} of {total} ideas...")
    
    def on_idea_generated(self, idea: str, category: str, file_path: str):
        """Handle a successfully generated idea."""
        self.log_message(f"Generated idea for category: {category}")
        self.log_message(f"Saved to: {file_path}")
        
        # Extract the assistant name for display
        name_match = re.search(r'## 1\. Assistant Name:\s*\n\s*(.+?)\s*\n', idea)
        if name_match:
            assistant_name = name_match.group(1).strip()
            self.log_message(f"Assistant: {assistant_name}")
    
    def on_idea_skipped(self, reason: str):
        """Handle a skipped idea."""
        self.log_message(f"Skipped: {reason}")
    
    def on_error(self, error_message: str):
        """Handle an error during generation."""
        self.log_message(f"ERROR: {error_message}", error=True)
    
    def on_generation_complete(self, successful: int, attempts: int):
        """Handle completion of the generation process."""
        self.generate_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.stop_button.setText("Stop Generation")
        
        if self.generator_thread and self.generator_thread.unlimited:
            self.log_message(f"Generation stopped. Generated {successful} ideas in {attempts} attempts.")
        else:
            if successful < attempts:
                self.log_message(f"Generation complete. Generated {successful} ideas after {attempts} attempts.")
            else:
                self.log_message(f"Generation complete. Successfully generated {successful} ideas!")
        
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)
        self.progress_label.setText(f"Completed: {successful} ideas generated")
        
        # Perform memory cleanup after generation
        gc.collect()
    
    def log_message(self, message: str, error: bool = False):
        """Add a message to the log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format based on error status
        if error:
            formatted_message = f"<span style='color:red;'>[{timestamp}] {message}</span>"
        else:
            formatted_message = f"[{timestamp}] {message}"
        
        # Add to log
        self.log_text.append(formatted_message)
        
        # Scroll to bottom if auto-scroll is enabled
        if self.auto_scroll_checkbox.isChecked():
            scrollbar = self.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def show_error(self, message: str):
        """Show an error message dialog."""
        self.log_message(message, error=True)
        QMessageBox.critical(self, "Error", message)
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.generator_thread and self.generator_thread.isRunning():
            # Ask for confirmation if generation is running
            reply = QMessageBox.question(
                self, 'Confirm Exit',
                'Generation is still running. Are you sure you want to exit?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.generator_thread.stop()
                self.generator_thread.wait(1000)  # Wait up to 1 second
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
        
        # Clean up resources
        self.cleanup_timer.stop()
        gc.collect()

def main():
    app = QApplication(sys.argv)
    window = AIAgentIdeationGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
