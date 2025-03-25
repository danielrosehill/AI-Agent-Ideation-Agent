## 1. Assistant Name:

TaskAllocator Pro

## 2. Short Description:

TaskAllocator Pro is an AI-powered task management assistant specifically designed for IT teams to optimize resource allocation, reduce project delays, and improve overall team productivity.

## 3. Use Case Outline:

### User Personas:
- **IT Manager**: Responsible for managing a large-scale IT infrastructure.
- **Junior Engineer**: A junior engineer working on smaller projects under the supervision of an IT manager.

### Scenario 1: IT Manager Task Allocation

*   The IT manager wants to allocate tasks to their team members. They input task details, including complexity, urgency, and dependencies.
*   TaskAllocator Pro analyzes the task requirements and provides a suggested allocation plan based on each team member's workload, skill set, and availability.

### Scenario 2: Junior Engineer Request for Help

*   The junior engineer requests assistance with a complex task. They input their current progress and the required time to complete it.
*   TaskAllocator Pro suggests relevant experts from the IT team who can provide guidance or take over the task.

### Scenario 3: Project Schedule Review

*   The IT manager reviews project schedules, identifying potential delays or bottlenecks.
*   TaskAllocator Pro analyzes task dependencies and recommends optimal orderings to minimize delays and ensure timely completion of projects.

## 4. Benefits:

- **Increased Efficiency**: Automates task allocation, reducing manual planning time by up to 80%.
- **Improved Team Productivity**: Optimizes resource utilization, allowing team members to focus on high-priority tasks.
- **Enhanced Collaboration**: Streamlines communication among team members and stakeholders through a centralized platform.

## 5. Potential Risks & Limitations:

*   **Data Bias**: The assistant's output may reflect biases present in the training data related to task complexity or resource allocation.
*   **Lack of Human Judgment**: AI might struggle with nuanced, context-dependent decisions that require human expertise.

## 6. Context and RAG (Retrieval-Augmented Generation):

- **Context Window:** 2048 tokens - The larger context window allows for better understanding of dependencies between tasks and team member roles.
-   No RAG required - TaskAllocator Pro relies on its internal knowledge graph and task analysis capabilities to provide accurate recommendations.

## 7. Real-time Data and Search:

*   No real-time data required
*   API endpoint-based search functionality is sufficient for retrieving task details, expert profiles, or project schedules.

## 8. Suggested Deployment Frameworks:

- **Cloud Platforms:** AWS (SageMaker, Lambda, EC2)
-   Containerization: Docker
-   Frameworks: LangChain

## 9. Draft System Prompt:

```
Persona:
* Friendly and objective guide for the IT team.
Instructions:
1. Input task details (complexity, urgency, dependencies).
2. Suggest allocation plan based on team member's workload and skill set.
Constraints:
Do not suggest overloading or underutilizing resources.
Output Format: 
Bullet points summarizing task allocations.
Examples (optional):
Provide examples of successful project completions with optimized resource allocation.
Tone:
Informative and helpful.
Handling Ambiguity:
Recommend additional context if necessary, such as team member's availability or skill set updates.

```

## 10. Parameter Suggestions:

- **Temperature:** 1.0 - Encourages objective decision-making.
-   **Top-p:** 0.8
-   **Frequency Penalty:**
    *   Suggested value: 1.2
-   **Presence Penalty:**
    *   Suggested value: 0.5
-   **Max Tokens:** 128 - Sets a reasonable limit for task descriptions.
-   **Stop Sequences:** 
    *   Include strings indicating resource unavailability or critical task dependencies.

By providing clear parameters and utilizing a well-designed RAG system, TaskAllocator Pro can effectively manage tasks and allocate resources to optimize team productivity and project timelines.