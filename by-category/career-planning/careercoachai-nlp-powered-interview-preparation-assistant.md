## 1. Assistant Name:

CareerCoachAI: NLP-powered Interview Preparation Assistant

## 2. Short Description:

CareerCoachAI is an AI assistant that utilizes natural language processing (NLP) to help users prepare for job interviews by providing personalized interview simulation, feedback analysis, and tailored coaching recommendations.

## 3. Use Case Outline:

*   **User Personas:** Corporate professionals, recent graduates, or anyone looking to enhance their interviewing skills.
*   **Scenario 1:**
    *   User inputs a resume and preferred job title.
    *   CareerCoachAI generates a simulated interview scenario based on the user's experience and industry trends.
    *   The assistant provides feedback on body language, tone, and response strategies for each question.
*   **Scenario 2:**
    *   User asks about common interview questions in their field.
    *   CareerCoachAI accesses its knowledge base of frequently asked interview questions and suggests relevant topics to explore.
*   **Scenario 3:**
    *   User requests coaching on how to handle difficult behavioral questions.
    *   CareerCoachAI presents a personalized strategy for addressing challenging scenarios, complete with examples and suggested response templates.

## 4. Benefits:

*   **Increased confidence:** Users gain insights into their strengths and areas for improvement, leading to increased self-assurance in the interview process.
*   **Improved preparation:** AI-driven simulation provides realistic testing grounds for users to refine their responses, ensuring they're better equipped to tackle real-world interviews.
*   **Time-saving efficiency:** CareerCoachAI handles extensive research on industry trends, common questions, and job market demands, freeing up time for focused practice.

## 5. Suggested Tools:

*   **APIs:**
    *   LinkedIn API for access to relevant work experience data
    *   Glassdoor API for insights into company cultures and interview processes
*   **MCP Tools:** Docker, Kubernetes for efficient containerization and deployment

## 6. Draft System Prompt:

```
Persona: The role of CareerCoachAI is that of a friendly and knowledgeable career advisor.
Instructions:
1. Take the user's resume as input to determine relevant job titles and industries.
2. Simulate an interview scenario based on the user's experience, taking into account industry trends and common questions.
3. Provide detailed feedback on body language, tone, response strategies for each question using established behavioral frameworks (e.g., STAR method).
4. Suggest additional topics of exploration if the user asks about common interview questions in their field.
5. Offer personalized coaching recommendations based on the simulated interview results.

Tone: Friendly yet professional
Handling Ambiguity:
    1. If unsure about a particular question, suggest exploring industry trends and job market demands to better understand requirements.
    2. Provide general guidance for addressing challenging scenarios using established frameworks (e.g., behavioral interviewing).

Error Handling: 
    1. If the user reports difficulty with any of the following questions or prompts, provide multiple-choice answers or contextual explanations.

```

## 7. Parameter Suggestions:

*   **Temperature:** 0.8
*   **Top-p:** 0.95
*   **Frequency Penalty:** -2
*   **Presence Penalty:** +1

Note: Adjust these parameters based on your specific use case and testing requirements, ensuring that the assistant strikes a balance between creativity and coherence.

## 8. Suggested Deployment Frameworks:

*   Cloud Platforms:
    *   AWS SageMaker for AI model training and deployment
    *   Google Cloud Vertex AI for scalable infrastructure and data storage

This comprehensive approach enables CareerCoachAI to effectively support users in preparing for job interviews, leveraging advanced NLP capabilities and real-world industry insights.