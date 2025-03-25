## 1. Assistant Name:

[Assistant Name Here]

## 2. Short Description:

[A concise description (1-3 sentences) of the assistant's primary function and purpose.  What problem does it solve?  Who is the target user?]

## 3. Use Case Outline:

[Describe the primary use case(s) for this assistant.  Provide specific examples of how users would interact with it.]

*   **User Personas**: Who are the users? 
*   **Scenario 1:** [Describe a specific user scenario, including the user's input and the expected assistant output.]
*   **Scenario 2:** [Describe another scenario, highlighting a different aspect of the assistant's functionality.]
*   **Scenario 3:** [And so on...]

## 4. Benefits:

[List the key benefits of using this assistant.  Be specific and quantifiable whenever possible. Examples:]

*   Increased efficiency in [task] by [percentage or time saved].
*   Improved accuracy in [task] by [percentage or metric].
*   Reduced costs associated with [task] by [amount or percentage].
*   Enhanced user experience by [specific improvement].
*   Automated [task], freeing up human resources for [other tasks].
*   Provides [unique capability] that was previously unavailable.

## 5. Potential Risks & Limitations:

[Honestly assess the potential downsides, limitations, and risks. Examples:]

*   **Data Bias:** The assistant's output may reflect biases present in the training data.
*   **Hallucinations:** The assistant may generate incorrect or nonsensical information.
*   **Lack of Common Sense:** The assistant may struggle with tasks requiring real-world understanding.
*   **Security Concerns:**  If handling sensitive data, describe data security measures.
*   **Over-Reliance:** Users may become overly dependent on the assistant.
*   **Limited Domain Expertise:** The assistant may not perform well outside its specific area of training.
*   **Explainability:**  The reasoning behind the assistant's responses may be opaque.
*   **Cost:** The cost of running and maintaining the assistant (compute, API calls, etc.).
*   **Latency:** Potential delays in response time.
*   **Ethical Concerns**: Outline any potential ethical issues.

## 6. Context and RAG (Retrieval-Augmented Generation):

*   **Context Window:** [Specify the required context window size (e.g., 4096 tokens, 8k tokens).  Justify the choice.]
*   **RAG Required:** [Yes/No] - [If yes, explain why RAG is beneficial. Specify the type of data RAG should use (e.g., internal documentation, knowledge base, web search).  Describe the RAG implementation approach.]

## 7. Real-time Data and Search:

*   **Real-time Data Required:** [Yes/No] - [If yes, specify the data sources and frequency of updates needed.]
*   **Search Required:** [Yes/No] - [If yes, specify the type of search (e.g., web search, internal database search) and the search engine/API to be used.]

## 8. Multimodal Capabilities:

*   **Vision Required:** [Yes/No] - [If yes, describe what the assistant needs to see/analyze (e.g., images, documents, charts) and why. Suggest specific vision APIs or models that would be suitable.]
*   **Multimodal Input/Output Required:** [Yes/No] - [If yes, specify which modalities (audio, video, images, etc.) and how they would be used. Suggest specific APIs or frameworks for handling these modalities.]
*   **Specialized Processing Needs:** [If applicable, describe any specialized processing requirements for handling multimodal data, such as OCR, image recognition, audio transcription, etc.]

## 9. Suggested Tools:

[List any APIs, libraries, frameworks, or platforms that would be beneficial or necessary for the assistant's operation.  Include specific versions if relevant.]

*   **APIs:**
    *   [API Name] ([Link to API Documentation]) - [Purpose of using this API]
    *   [Another API Name] ([Link]) - [Purpose]
*   **MCP Tools:**
     * [Tool Name] - [Purpose]
*   **Libraries/Frameworks:**
    *   [Library Name] (e.g., LangChain, Transformers) - [Purpose]
    *   [Framework Name] (e.g., TensorFlow, PyTorch) - [Purpose]

## 10. Draft System Prompt:

```
[Write the system prompt here.  This should be a complete and detailed instruction set for the AI model.  Be precise and unambiguous.  Include:]

*   **Persona:**  The role or personality of the assistant.
*   **Instructions:**  Clear, step-by-step instructions on how to respond to user input.
*   **Constraints:**  What the assistant *should not* do.
*   **Output Format:**  How the response should be structured (e.g., bullet points, JSON, code blocks).
*   **Examples (optional):**  Few-shot examples can be included to guide the assistant's behavior.
*   **Tone:**  The desired tone of the assistant (e.g., formal, informal, helpful, humorous).
*   **Handling Ambiguity:** Instructions on how to handle ambiguous or unclear requests.
*   **Error Handling**: What to do when something unexpected is given to the prompt.
```

## 11. Parameter Suggestions:

*   **Temperature:** [Suggested value (e.g., 0.7)] - [Justification: e.g., "A temperature of 0.7 encourages creativity while maintaining coherence."]
*   **Top-p:** [Suggested value (e.g., 0.9)] - [Justification]
*   **Frequency Penalty:** [Suggested value] - [Justification]
*   **Presence Penalty:** [Suggested value] - [Justification]
*   **Max Tokens:** [Suggested value] - [Justification:  Set a reasonable limit to control response length and cost.]
*   **Stop Sequences:** [List any strings that should cause the assistant to stop generating text.]
*   **Other Parameters**: Any specific instructions for the model.

## 12. Suggested Deployment Frameworks:

[List potential deployment options. Examples:]

*   **Cloud Platforms:**
    *   AWS (SageMaker, Lambda, EC2)
    *   Google Cloud (Vertex AI, Cloud Functions, Compute Engine)
    *   Azure (Azure Machine Learning, Azure Functions, Virtual Machines)
*   **Containerization:**
    *   Docker, Kubernetes
*   **Frameworks:**
    *   LangChain, LlamaIndex
*   **Other**: API endpoint, Chatbot Framework