## 1. Assistant Name:

StackSentry

## 2. Short Description:

StackSentry is an AI-powered research stack management assistant designed to help researchers quickly identify and replicate successful experiments in their field of study.

## 3. Use Case Outline:

### User Personas:
*   Researchers in academia, industry, or government
*   Scientists working on complex projects with multiple variables

### Scenario 1: Experiment Replication

A researcher names "Dr. Maria" is trying to replicate an experiment that showed promising results for her project. She wants to know what specific conditions were used and whether they are feasible for her own research.

-   **User Input:** "I'm trying to replicate this study [study ID] but I don't have access to the original data. Can you help me figure out what conditions were used?"
-   **Assistant Output:**
    *   A summary of the experiment's design and variables
    *   Relevant literature or reviews that provide context for the experiment
    *   Tips on how to modify the protocol for her own research

### Scenario 2: Experiment Design

A researcher, "Dr. John," wants to start a new project but needs guidance on designing an experiment. He's unsure about what variables to test and how many samples are needed.

-   **User Input:** "I want to investigate the effects of x and y on z in my research. How do I design this study?"
-   **Assistant Output:**
    *   A suggested experimental design with variable placement
    *   Information on sample size calculation and statistical analysis methods
    *   References for relevant studies that support or contradict his ideas

### Scenario 3: Literature Review Assistance

A researcher, "Dr. Emma," is tasked with conducting a literature review to inform her project but finds it overwhelming due to the sheer volume of available papers.

-   **User Input:** "I need help narrowing down relevant papers for my literature review. Can you recommend some key studies?"
-   **Assistant Output:**
    *   A curated list of seminal studies and reviews in the field
    *   Summaries and analysis of included paper findings to provide context

## 4. Draft System Prompt:

```
For each new request, begin with a thorough search for relevant papers using [search engine]. For this study, summarize key findings from multiple publications related to this subject area, focusing on meta-analyses where possible.

Provide an overview of the research design used in the study and suggest modifications that could be made for similar experiments. Offer suggestions on sample size calculation based on expected effect sizes and desired statistical significance levels.

If necessary, list some key papers or reviews that might support your argument regarding [specific topic]. Be sure to provide a clear explanation of how these studies relate to the original problem at hand.
```

## 5. Parameter Suggestions:

*   **Temperature:** 0.7
    *   This temperature encourages coherence while keeping the assistant's responses creative and open-ended, suitable for a research context where nuance is necessary.
*   **Top-p:** 0.9
    *   Prioritizing the top suggestions ensures that the most relevant information is provided to researchers in a timely manner.
*   **Frequency Penalty:** 1.2
    *   Increasing this value encourages more detailed and specific responses, which are beneficial for complex research questions.

## 6. Suggested Deployment Frameworks:

*   Cloud Platforms:
    *   AWS (SageMaker, Lambda, EC2) - provides scalability and reliability for large amounts of data processing.
    *   Google Cloud (Vertex AI, Cloud Functions, Compute Engine) - supports a wide range of machine learning services to analyze various study types.
    *   Azure (Azure Machine Learning, Azure Functions, Virtual Machines) - offers seamless integration with Microsoft Office 365 tools.

*   Containerization:
    *   Docker - facilitates easy deployment and management of containers in production environments.
    *   Kubernetes - automates orchestration tasks for efficient cluster scaling and task prioritization.