## 1. Assistant Name:

ChoreWizard: Household Scheduling Mastermind

## 2. Short Description:

ChoreWizard is an AI-powered household scheduling assistant that helps users optimize their daily routines by automating chore assignments, generating personalized schedules, and providing real-time task updates. Its primary function solves the problem of inefficient time management for households with multiple occupants.

## 3. Use Case Outline:

### User Personas:
- Busy working professionals
- Stay-at-home parents
- Retirees living alone or with elderly family members

**Scenario 1:** A household with two adults and one child schedules chores, such as laundry, cleaning, and grocery shopping. ChoreWizard provides an optimized schedule for each person based on their availability and preferences.

**Scenario 2:** A single retiree needs to manage daily tasks like meal preparation, medication reminders, and appointment scheduling while living alone. ChoreWizard assists with generating personalized routines that address specific care needs.

**Scenario 3:** Two young adults sharing a house create a schedule for cleaning, cooking, and personal hygiene tasks using ChoreWizard's advanced collaboration features.

### Benefits:

- Improved household organization by up to 30% through optimized schedules
- Increased productivity of up to 25% thanks to efficient task delegation
- Enhanced family dynamics due to shared responsibilities, reducing stress among all household members

## 4. Potential Risks & Limitations:

- Over-reliance on automation may lead to decreased accountability and personal responsibility.
- Data privacy could be a concern for some users if they are not comfortable with the amount of data ChoreWizard collects.

## 5. Context and RAG (Retrieval-Augmented Generation):

- **Context Window:** The assistant requires access to up-to-date household schedules, calendars, and task lists within the provided context window.
- **RAG Required:** Yes - ChoreWizard uses internal knowledge graphs and external APIs for real-time data retrieval.

## 6. Real-time Data and Search:

- **Real-time Data Required:** Yes
- **Search Required:** No

## 7. Suggested Tools:

*   **APIs:**
    *   Google Calendar API (for calendar data)
    *   Task management APIs like Trello or Todoist for task tracking
    *   Weather APIs for climate-based scheduling suggestions
*   **MCP Tools:** Docker and Kubernetes for containerization and deployment.
*   **Frameworks:** LangChain, LlamaIndex.

## 8. Draft System Prompt:

```
Persona: ChoreWizard AI assistant

Instructions:
- Generate a personalized schedule based on user input (household members' availability, preferences).
- Assign chores to household members with consideration for overlap and efficiency.
- Provide real-time updates for scheduled tasks and reminders.
Constraints:
- All suggestions must be aligned with the provided calendar data.
Output Format: 
- Output should include detailed schedules by person or day of the week in a clear format (e.g., bullet points).
Examples (optional): Example input includes "Household members are available on Monday." ChoreWizard responds accordingly for scheduling and task assignments.

Tone:
- Neutral, helpful

Handling Ambiguity: 
- If there is any ambiguity with user input or conflicting preferences, the system prompts for clarification to ensure an accurate schedule.
Error Handling: 
- If data retrieval fails due to API issues or network connectivity problems, ChoreWizard displays a notification asking users to try again later.

```

## 9. Parameter Suggestions:

*   **Temperature:** Optimally set around 0.7 for creativity while maintaining coherence.
*   **Top-p:** Adjusted values based on user feedback and performance metrics (target around 0.85).
*   **Frequency Penalty:** Suggested value is low, allowing the model to explore longer sequences as necessary.
*   **Presence Penalty:** Adjusted penalties ensure relevant task suggestions without over-reliance.
*   **Max Tokens:** Set a reasonable limit (e.g., 50 tokens) for response length and cost control.
- List of stop sequences includes phrases like "I can't help you with that" or similar user-unfriendly input signals.

## 10. Suggested Deployment Frameworks:

- Cloud Platforms: AWS SageMaker, Google Cloud Vertex AI, Azure Machine Learning
- Containerization: Docker and Kubernetes for scalability and flexibility.
- Frameworks: LangChain, LlamaIndex for efficient task delegation and real-time data processing.

This comprehensive approach ensures ChoreWizard not only optimizes household schedules but also provides a user-centric interface that integrates seamlessly with existing tools and services.