#!/usr/bin/env python3
"""
AI Agent Ideation Generator GUI

This script provides a graphical user interface for the AI Agent Ideation Generator.
It allows users to select a model, set the number of ideas to generate, and view the progress.
"""

import sys
import os
import re
import time
import random
import threading
import gc
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
import traceback

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QComboBox, QPushButton, QSpinBox, QTextEdit, QProgressBar,
        QSlider, QCheckBox, QGroupBox, QRadioButton, QButtonGroup, QSplitter,
        QMessageBox, QFileDialog
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
    from PyQt6.QtGui import QFont, QTextCursor, QIcon
except ImportError:
    print("PyQt6 is not installed. Installing now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QComboBox, QPushButton, QSpinBox, QTextEdit, QProgressBar,
        QSlider, QCheckBox, QGroupBox, QRadioButton, QButtonGroup, QSplitter,
        QMessageBox, QFileDialog
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
    from PyQt6.QtGui import QFont, QTextCursor, QIcon

# Import the core functionality
try:
    from generate_agent_ideas import (
        load_categories, load_template, get_category_folder_name,
        get_existing_ideas, is_similar_idea, generate_idea_with_ollama,
        save_idea, get_available_models, update_index
    )
except ImportError:
    print("Error importing core functionality. Make sure generate_agent_ideas.py is in the same directory.")
    sys.exit(1)

# Constants
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
CATEGORIES_DIR = os.path.join(REPO_PATH, "by-category")
DEFAULT_MODEL = "llama3.2"
MAX_RETRIES = 3  # Maximum number of retries for failed generations
RETRY_DELAY = 2  # Delay between retries in seconds

class IdeaGeneratorThread(QThread):
    """Thread for generating AI agent ideas."""
    
    # Signals for updating the UI
    progress_updated = pyqtSignal(int, int)  # current, total
    idea_generated = pyqtSignal(str, str, str, str)  # assistant name, category, file path, creativity level
    log_message = pyqtSignal(str)  # log message
    error_occurred = pyqtSignal(str)  # error message
    generation_complete = pyqtSignal()  # emitted when generation is complete
    
    def __init__(self, model: str, num_ideas: int, similarity_threshold: float, unlimited: bool = False, use_creativity_distribution: bool = True):
        super().__init__()
        self.model = model
        self.num_ideas = num_ideas
        self.similarity_threshold = similarity_threshold
        self.unlimited = unlimited
        self.use_creativity_distribution = use_creativity_distribution
        self.running = True
        self.categories = load_categories()
        self.template = load_template()
    
    def run(self):
        """Run the idea generation thread."""
        if not self.categories:
            self.error_occurred.emit("No categories found. Please check the categories file.")
            return
        
        successful_generations = 0
        attempts = 0
        
        try:
            while (self.unlimited or successful_generations < self.num_ideas) and self.running:
                attempts += 1
                
                # Periodically clean up memory
                if attempts % 20 == 0:
                    gc.collect()
                
                # Randomly select a category
                category = random.choice(self.categories)
                
                # Randomly select a creativity level if distribution is enabled
                creativity_level = None
                if self.use_creativity_distribution:
                    creativity_levels = ["basic", "moderate", "creative", "highly_creative"]
                    creativity_level = random.choice(creativity_levels)
                
                self.log_message.emit(f"Generating idea for category: {category}" + 
                                     (f" (Creativity: {creativity_level.replace('_', ' ')})" if creativity_level else ""))
                
                # Try to generate with retries
                retry_count = 0
                generation_successful = False
                while retry_count < MAX_RETRIES and not generation_successful and self.running:
                    try:
                        # Generate the idea
                        idea, filename = generate_idea_with_ollama(category, self.model, self.template, creativity_level)
                        
                        # Check if the idea is similar to existing ideas
                        category_folder = os.path.join(CATEGORIES_DIR, get_category_folder_name(category))
                        existing_ideas = get_existing_ideas(category_folder)
                        
                        if is_similar_idea(idea, existing_ideas, self.similarity_threshold):
                            self.log_message.emit(f"Skipped: Similar idea already exists for {category}")
                            break
                        
                        # Save the idea
                        file_path = save_idea(idea, category, filename)
                        
                        # Extract the assistant name for display
                        name_match = re.search(r'## 1\. Assistant Name:\s*\n\s*(.+?)\s*\n', idea)
                        if name_match:
                            assistant_name = name_match.group(1).strip()
                        else:
                            assistant_name = filename.replace('-', ' ').title()
                        
                        # Format creativity level for display
                        display_creativity = creativity_level.replace('_', ' ').title() if creativity_level else "Random"
                        
                        self.log_message.emit(f"Generated: {assistant_name} (Category: {category}, Creativity: {display_creativity})")
                        self.log_message.emit(f"Saved to: {file_path}")
                        
                        # Emit the idea generated signal
                        self.idea_generated.emit(assistant_name, category, file_path, display_creativity if creativity_level else "Random")
                        
                        successful_generations += 1
                        self.progress_updated.emit(successful_generations, self.num_ideas)
                        
                        generation_successful = True
                        
                    except Exception as e:
                        retry_count += 1
                        error_message = f"Error (attempt {retry_count}/{MAX_RETRIES}): {str(e)}"
                        self.log_message.emit(error_message)
                        
                        if retry_count >= MAX_RETRIES:
                            self.error_occurred.emit(f"Failed to generate idea after {MAX_RETRIES} attempts: {str(e)}")
                        else:
                            # Wait before retrying
                            time.sleep(RETRY_DELAY)
                
                # Small delay between generations to prevent overloading Ollama
                time.sleep(0.1)
            
            if self.running:
                self.log_message.emit(f"Generation complete. Generated {successful_generations} ideas after {attempts} attempts.")
                self.generation_complete.emit()
            else:
                self.log_message.emit(f"Generation stopped. Generated {successful_generations} ideas after {attempts} attempts.")
        
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}\n{traceback.format_exc()}"
            self.error_occurred.emit(error_message)
        finally:
            # Final memory cleanup
            gc.collect()
    
    def stop(self):
        """Stop the idea generation thread."""
        self.running = False

class ModelRefreshThread(QThread):
    """Thread for refreshing the list of available models."""
    
    # Signals for updating the UI
    models_refreshed = pyqtSignal(list)  # list of models
    error_occurred = pyqtSignal(str)  # error message
    
    def run(self):
        """Run the model refresh thread."""
        try:
            models = get_available_models()
            self.models_refreshed.emit(models)
        except Exception as e:
            self.error_occurred.emit(f"Error refreshing models: {str(e)}")

class MainWindow(QMainWindow):
    """Main window for the AI Agent Ideation Generator GUI."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("AI Agent Ideation Generator")
        self.setMinimumSize(800, 600)
        
        # Initialize variables
        self.generator_thread = None
        self.model_refresh_thread = None
        self.auto_scroll = True
        
        # Create the main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Create a splitter for the top controls and bottom log
        splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(splitter)
        
        # Create the top controls widget
        top_widget = QWidget()
        top_layout = QVBoxLayout()
        top_widget.setLayout(top_layout)
        splitter.addWidget(top_widget)
        
        # Model selection
        model_group = QGroupBox("Model Selection")
        model_layout = QHBoxLayout()
        model_group.setLayout(model_layout)
        top_layout.addWidget(model_group)
        
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(200)
        model_layout.addWidget(self.model_combo)
        
        self.refresh_button = QPushButton("Refresh Models")
        model_layout.addWidget(self.refresh_button)
        model_layout.addStretch()
        
        # Number of ideas
        ideas_group = QGroupBox("Number of Ideas")
        ideas_layout = QVBoxLayout()
        ideas_group.setLayout(ideas_layout)
        top_layout.addWidget(ideas_group)
        
        # Radio buttons for preset numbers
        presets_layout = QHBoxLayout()
        ideas_layout.addLayout(presets_layout)
        
        self.ideas_button_group = QButtonGroup(self)
        
        for preset in [50, 100, 500, 1000]:
            radio = QRadioButton(str(preset))
            self.ideas_button_group.addButton(radio)
            presets_layout.addWidget(radio)
        
        # Custom number input
        custom_layout = QHBoxLayout()
        ideas_layout.addLayout(custom_layout)
        
        self.custom_radio = QRadioButton("Custom:")
        self.ideas_button_group.addButton(self.custom_radio)
        custom_layout.addWidget(self.custom_radio)
        
        self.ideas_spinbox = QSpinBox()
        self.ideas_spinbox.setMinimum(1)
        self.ideas_spinbox.setMaximum(10000)
        self.ideas_spinbox.setValue(10)
        custom_layout.addWidget(self.ideas_spinbox)
        
        # Until stopped option
        self.unlimited_checkbox = QCheckBox("Generate until stopped")
        ideas_layout.addWidget(self.unlimited_checkbox)
        
        # Set the default selection
        self.ideas_button_group.buttons()[0].setChecked(True)
        
        # Advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QVBoxLayout()
        advanced_group.setLayout(advanced_layout)
        top_layout.addWidget(advanced_group)
        
        # Similarity threshold
        similarity_layout = QHBoxLayout()
        advanced_layout.addLayout(similarity_layout)
        
        similarity_layout.addWidget(QLabel("Similarity Threshold:"))
        
        self.similarity_slider = QSlider(Qt.Orientation.Horizontal)
        self.similarity_slider.setMinimum(0)
        self.similarity_slider.setMaximum(100)
        self.similarity_slider.setValue(80)  # Default to 0.8
        similarity_layout.addWidget(self.similarity_slider)
        
        self.similarity_label = QLabel("0.80")
        similarity_layout.addWidget(self.similarity_label)
        
        # Creativity distribution
        self.creativity_checkbox = QCheckBox("Use creativity distribution")
        self.creativity_checkbox.setChecked(True)
        advanced_layout.addWidget(self.creativity_checkbox)
        
        # Auto-scroll checkbox
        self.auto_scroll_checkbox = QCheckBox("Auto-scroll log")
        self.auto_scroll_checkbox.setChecked(True)
        advanced_layout.addWidget(self.auto_scroll_checkbox)
        
        # Control buttons
        buttons_layout = QHBoxLayout()
        top_layout.addLayout(buttons_layout)
        
        self.start_button = QPushButton("Start Generation")
        self.start_button.setMinimumHeight(40)
        buttons_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Generation")
        self.stop_button.setMinimumHeight(40)
        self.stop_button.setEnabled(False)
        buttons_layout.addWidget(self.stop_button)
        
        self.clear_log_button = QPushButton("Clear Log")
        buttons_layout.addWidget(self.clear_log_button)
        
        # Progress bar
        progress_layout = QHBoxLayout()
        top_layout.addLayout(progress_layout)
        
        progress_layout.addWidget(QLabel("Progress:"))
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("0/0")
        progress_layout.addWidget(self.progress_label)
        
        # Create the log widget
        log_widget = QWidget()
        log_layout = QVBoxLayout()
        log_widget.setLayout(log_layout)
        splitter.addWidget(log_widget)
        
        log_layout.addWidget(QLabel("Log:"))
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier New", 10))
        log_layout.addWidget(self.log_text)
        
        # Set the splitter sizes
        splitter.setSizes([300, 300])
        
        # Connect signals and slots
        self.refresh_button.clicked.connect(self.refresh_models)
        self.start_button.clicked.connect(self.start_generation)
        self.stop_button.clicked.connect(self.stop_generation)
        self.clear_log_button.clicked.connect(self.clear_log)
        self.similarity_slider.valueChanged.connect(self.update_similarity_label)
        self.unlimited_checkbox.stateChanged.connect(self.toggle_unlimited)
        self.auto_scroll_checkbox.stateChanged.connect(self.toggle_auto_scroll)
        self.creativity_checkbox.stateChanged.connect(self.toggle_creativity_distribution)
        
        # Initialize the UI
        self.refresh_models()
        self.log_message("AI Agent Ideation Generator GUI started")
        self.log_message("Please select a model and number of ideas to generate")
    
    def refresh_models(self):
        """Refresh the list of available models."""
        self.log_message("Refreshing models...")
        self.refresh_button.setEnabled(False)
        
        self.model_refresh_thread = ModelRefreshThread()
        self.model_refresh_thread.models_refreshed.connect(self.update_models)
        self.model_refresh_thread.error_occurred.connect(self.log_error)
        self.model_refresh_thread.finished.connect(lambda: self.refresh_button.setEnabled(True))
        self.model_refresh_thread.start()
    
    def update_models(self, models: List[Dict[str, Any]]):
        """Update the model selection combo box."""
        self.model_combo.clear()
        
        if not models:
            self.log_error("No models found. Make sure Ollama is running and has models pulled.")
            return
        
        for model in models:
            model_name = model.get("name")
            model_size = model.get("details", {}).get("parameter_size", "Unknown size")
            self.model_combo.addItem(f"{model_name} ({model_size})", model_name)
        
        # Try to select the default model
        default_index = self.model_combo.findData(DEFAULT_MODEL)
        if default_index >= 0:
            self.model_combo.setCurrentIndex(default_index)
        
        self.log_message(f"Found {len(models)} models")
    
    def update_similarity_label(self, value: int):
        """Update the similarity threshold label."""
        threshold = value / 100.0
        self.similarity_label.setText(f"{threshold:.2f}")
    
    def toggle_unlimited(self, state: int):
        """Toggle the unlimited generation mode."""
        unlimited = state == Qt.CheckState.Checked.value
        
        for button in self.ideas_button_group.buttons():
            button.setEnabled(not unlimited)
        
        self.ideas_spinbox.setEnabled(not unlimited)
    
    def toggle_auto_scroll(self, state: int):
        """Toggle auto-scrolling of the log."""
        self.auto_scroll = state == Qt.CheckState.Checked.value
    
    def toggle_creativity_distribution(self, state: int):
        """Toggle the creativity distribution."""
        self.creativity_checkbox.setChecked(state == Qt.CheckState.Checked.value)
    
    def get_num_ideas(self) -> int:
        """Get the number of ideas to generate."""
        if self.custom_radio.isChecked():
            return self.ideas_spinbox.value()
        
        for button in self.ideas_button_group.buttons():
            if button.isChecked() and button != self.custom_radio:
                return int(button.text())
        
        return 10  # Default
    
    def start_generation(self):
        """Start generating AI agent ideas."""
        if self.generator_thread and self.generator_thread.isRunning():
            return
        
        # Get the selected model
        model_index = self.model_combo.currentIndex()
        if model_index < 0:
            self.log_error("Please select a model first")
            return
        
        model = self.model_combo.currentData()
        
        # Get the number of ideas
        unlimited = self.unlimited_checkbox.isChecked()
        num_ideas = 0 if unlimited else self.get_num_ideas()
        
        # Get the similarity threshold
        similarity_threshold = self.similarity_slider.value() / 100.0
        
        # Get the creativity distribution
        use_creativity_distribution = self.creativity_checkbox.isChecked()
        
        # Update the UI
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        
        if unlimited:
            self.progress_label.setText("∞")
            self.progress_bar.setMaximum(0)  # Indeterminate progress
        else:
            self.progress_label.setText(f"0/{num_ideas}")
            self.progress_bar.setMaximum(num_ideas)
        
        # Log the start
        self.log_message(f"Starting generation with model: {model}")
        self.log_message(f"Number of ideas: {'Unlimited' if unlimited else num_ideas}")
        self.log_message(f"Similarity threshold: {similarity_threshold:.2f}")
        self.log_message(f"Creativity distribution: {'Enabled' if use_creativity_distribution else 'Disabled'}")
        
        # Create and start the generator thread
        self.generator_thread = IdeaGeneratorThread(model, num_ideas, similarity_threshold, unlimited, use_creativity_distribution)
        self.generator_thread.progress_updated.connect(self.update_progress)
        self.generator_thread.idea_generated.connect(self.idea_generated)
        self.generator_thread.log_message.connect(self.log_message)
        self.generator_thread.error_occurred.connect(self.log_error)
        self.generator_thread.generation_complete.connect(self.generation_complete)
        self.generator_thread.start()
    
    def stop_generation(self):
        """Stop generating AI agent ideas."""
        if self.generator_thread and self.generator_thread.isRunning():
            self.log_message("Stopping generation...")
            self.generator_thread.stop()
            
            # Update the UI
            self.stop_button.setEnabled(False)
            
            # Wait for the thread to finish
            QTimer.singleShot(100, self.check_thread_finished)
    
    def check_thread_finished(self):
        """Check if the generator thread has finished."""
        if self.generator_thread and self.generator_thread.isRunning():
            # Still running, check again later
            QTimer.singleShot(100, self.check_thread_finished)
        else:
            # Thread finished, update the UI
            self.start_button.setEnabled(True)
            self.log_message("Generation stopped")
    
    def update_progress(self, current: int, total: int):
        """Update the progress bar and label."""
        if self.unlimited_checkbox.isChecked():
            self.progress_label.setText(f"{current}/∞")
        else:
            self.progress_bar.setValue(current)
            self.progress_label.setText(f"{current}/{total}")
    
    def idea_generated(self, assistant_name: str, category: str, file_path: str, creativity_level: str):
        """Handle a generated idea."""
        # This method can be extended to do more with the generated ideas
        pass
    
    def generation_complete(self):
        """Handle completion of idea generation."""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.log_message("Generation complete")
    
    def log_message(self, message: str):
        """Add a message to the log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        self.log_text.append(log_entry)
        
        if self.auto_scroll:
            # Scroll to the bottom
            cursor = self.log_text.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.log_text.setTextCursor(cursor)
    
    def log_error(self, message: str):
        """Add an error message to the log."""
        self.log_message(f"ERROR: {message}")
    
    def clear_log(self):
        """Clear the log text."""
        self.log_text.clear()
        self.log_message("Log cleared")
    
    def closeEvent(self, event):
        """Handle the window close event."""
        if self.generator_thread and self.generator_thread.isRunning():
            # Ask for confirmation
            reply = QMessageBox.question(
                self, "Confirm Exit",
                "Idea generation is still running. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Stop the thread
                self.generator_thread.stop()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """Main function to run the GUI."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
