# AI Assistant Ideation Agent

![alt text](banner.jpg)

 # AI Assistant Ideation Tool

This repository contains a CLI and GUI application designed to facilitate the ideation of AI assistants. It leverages the Ollama API to provide model selection capabilities within both interfaces.

## Functionality

The core function of this tool is to assist users in generating ideas for AI assistants

*   **Predefined Folder Structure:** The agent employs a predefined list of folders that are populated using a Python script. This structure is intended to provide a framework for organizing and categorizing ideas. Users should customize these folders to align with their specific needs and the types of agents they wish to develop.
*   **Customizable Parameters**: Allows users to determine the number of iterations run by the agent as well as the duplication threshold.
*   **Templating**: The system prompt is produced by a template which also specifies a listing of parameters.

## Usage

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Customize the folder structure:** Modify the Python script responsible for populating the folder structure to reflect your desired organization.
3.  **Run the CLI or GUI application:** Follow the instructions within the repository to launch either the command-line or graphical interface.
4.  **Select an OLAMA model:** Choose the desired language model from the available options.
5.  **Configure ideation parameters:** Set the number of iterations and duplication threshold to control the ideation process.
6.  **Run the ideation process:** Initiate the agent to generate ideas based on the selected model, folder structure, and parameters.

## Considerations

*   **Avoiding Duplication and Through Memory:** This is a basic model for the implementation and could be greatly improved upon.
*   **Customization is Key:** The predefined folder structure is a starting point. Tailor it to your specific project and the types of AI assistants you are interested in developing.
*   **Template Customization:** The user should customize the template to produce the most relevant system prompt.

## Future Enhancements

*   **Database Integration:** Replace the current file-based implementation with a SQLite or other database for improved data management.
*   **Cloud LLM Support:** Adapt the tool to utilize cloud-based large language models.

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/AI-Agent-Ideation-Agent.git
   cd AI-Agent-Ideation-Agent
   ```

2. Make sure Ollama is installed and running:
   ```
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Make the script executable:
   ```
   chmod +x generate_agent_ideas.py
   ```

## Usage

 

### Parameters (CLI)

- `--model`: Specify which Ollama model to use (default: llama3.2)
- `--similarity-threshold`: Set the threshold for similarity checking (default: 0.8)
- `--interactive` or `-i`: Run in interactive mode
 

## Batch Generation Examples

For generating ideas in large batches:

```
# Generate 100 ideas
python generate_agent_ideas.py 100 --model llama3.2

# Generate 200 ideas with mistral model
python generate_agent_ideas.py 200 --model mistral

# Generate 500 ideas with zephyr model
python generate_agent_ideas.py 500 --model zephyr:7b

# Generate 1000 ideas with gemma3 model
python generate_agent_ideas.py 1000 --model gemma3
```

 

## Repository Structure

- `by-category/`: Contains subfolders for each category with generated ideas
- `templates/`: Contains the template for AI agent ideas
- `categories.txt`: List of categories for AI agent ideas
- `generate_agent_ideas.py`: Main script for generating ideas

 
 