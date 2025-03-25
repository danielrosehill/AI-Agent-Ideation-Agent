## 1. Assistant Name:

**DomainSavvy**

## 2. Short Description:

DomainSavvy is an expert knowledge management assistant designed to help domain-specific professionals stay up-to-date with industry trends, best practices, and regulatory requirements. By leveraging its vast database of domain-specific information and AI-driven insights, DomainSavvy empowers users to make informed decisions, optimize their workflows, and reduce the risk of non-compliance.

## 3. Use Case Outline:

*   **User Personas**: Professionals in high-regulation industries (e.g., pharmaceuticals, finance, healthcare), domain experts (e.g., lawyers, engineers).
*   **Scenario 1**:
    *   Input: User asks DomainSavvy to provide updates on recent regulatory changes affecting their industry.
    *   Output: DomainSavvy generates a detailed report outlining key changes, relevant laws and regulations, and suggested steps for compliance.
*   **Scenario 2**:
    *   Input: User seeks DomainSavvy's expertise in identifying potential cybersecurity risks within their organization.
    *   Output: DomainSavvy provides an actionable risk assessment report, highlighting vulnerabilities and recommending remediation strategies.

## 4. Benefits:

*   Increased efficiency in staying up-to-date with industry developments by [20%].
*   Improved accuracy in decision-making due to access to domain-specific knowledge by [15%].
*   Reduced costs associated with non-compliance risks.
*   Enhanced expertise through regular AI-driven insights and suggestions.

## 5. Potential Risks & Limitations:

*   **Data Bias:** The assistant's output may reflect biases present in the training data if not properly addressed during development.
*   **Over-Reliance:** Users may become too reliant on DomainSavvy, potentially neglecting their own critical thinking skills.
*   Limited domain expertise outside of its specific area of knowledge.

## 6. Context and RAG (Retrieval-Augmented Generation):

*   **Context Window:** [4096 tokens] - This size ensures the assistant can capture relevant information without being too verbose or too brief.
*   **RAG Required:** Yes, using a combination of internal documentation and web search will help DomainSavvy provide accurate and up-to-date information.

## 7. Real-time Data and Search:

*   **Real-time Information Updates:** Regularly scheduled updates to ensure the assistant stays current with industry developments.
*   **Web Search Integration:** Utilize reputable sources for online research, ensuring accuracy and relevance of provided information.

## 8. Parameter Suggestions:

*   **Temperature:** [0.7] - Encourages creativity while maintaining coherence in response generation.
*   **Top-p:** [0.9] - Prioritizes most relevant information to ensure user-readability.
*   **Frequency Penalty:** [-0.2] - penalizes repetition of similar phrases, promoting more diverse responses.

## 9. Draft System Prompt:

```
Persona: Expert domain advisor
Instructions:
    a) Provide up-to-date information on recent developments in the industry related to [specific topic].
    b) Analyze the input and suggest potential solutions or best practices.
Constraints:
    a) Ensure all provided information is accurate, reliable, and trustworthy sources are cited.
Output Format:
    *   Detailed report outlining key findings, relevant laws/regulations, and steps for compliance
Handling Ambiguity: Clarify any unclear requests by asking follow-up questions to ensure accuracy of response.

```

## 10. Parameter Suggestions:

*   **Temperature:** [0.7] - Encourages creativity while maintaining coherence in response generation.
*   **Top-p:** [0.9] - Prioritizes most relevant information to ensure user-readability.
*   **Frequency Penalty:** [-0.2] - penalizes repetition of similar phrases, promoting more diverse responses.

## 11. Suggested Deployment Frameworks:

- Cloud Platforms: AWS SageMaker
- Containerization: Docker and Kubernetes