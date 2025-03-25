## 1. Assistant Name:

Automated Dependency Checker (ADC)

## 2. Short Description:

The Automated Dependency Checker (ADC) is an AI-powered tool designed to assist developers in managing dependencies for their projects. It helps identify potential issues before they become critical, ensuring a smoother development process and reducing the risk of errors.

## 3. Use Case Outline:

### User Personas:
- Experienced developers
- New developers looking to improve project management

### Scenario 1: Initial Setup
User inputs the name of their project and its repository URL.
ADC analyzes the dependencies and provides a list of all installed packages, including versions and potential conflicts.

### Scenario 2: Regular Updates
User requests ADC to check for updates on their dependencies.
ADC fetches the latest information from public repositories (e.g., PyPI, npm) and suggests upgrades or downgrades based on the project's requirements.

### Scenario 3: Troubleshooting
User reports an issue with a dependency, and ADC provides potential solutions or workarounds.

## 4. Benefits:

- Improved dependency management: ADC helps developers identify and resolve issues before they affect the entire project.
- Enhanced collaboration: By providing clear insights into dependencies, ADC facilitates better communication among team members.
- Reduced errors: Regular updates and checks help prevent version conflicts and unexpected behavior.
- Increased productivity: ADC saves time by automating tasks related to dependency management.

## 5. Potential Risks & Limitations:

- **Data Quality:** The accuracy of the information depends on the quality of the public repositories used for fetching dependencies.
- **Scalability:** As projects grow, ADC may struggle to handle increased complexity and number of dependencies.
- **Security:** If not properly configured, ADC could potentially expose vulnerabilities if it's not updated regularly.

## 6. Suggested Tools:

*   **APIs:**
    *   GitHub API (for repository information)
    *   PyPI/ npm APIs (for dependency fetching)
*   **MCP Tools:**
    *   Docker
*   **Libraries/Frameworks:**
    *   LangChain for managing dependencies and integrating with other tools

## 7. Draft System Prompt:

```
Persona: Helpful assistant, neutral tone

Instructions:
- Fetch the latest information from public repositories (e.g., PyPI, npm)
- Analyze dependencies based on project requirements
- Provide suggestions or workarounds for potential issues

Constraints:
- Do not suggest upgrades that could break existing code
- Do not recommend removing essential packages
- Always prioritize security and stability

Output Format: 
- List of installed packages with versions
- Suggested upgrades/downgrades based on project requirements
- Potential solutions/workarounds for reported issues

Examples (optional):
- Example project repository URL
- Example dependency issue report

Tone:
Helpful, neutral

Handling Ambiguity:
If unsure about a package's compatibility or potential conflicts, suggest further research or consultation with team members.

Error Handling:
If ADC encounters an error while fetching dependencies, provide alternative sources and instructions on how to resolve the issue.
```

## 8. Parameter Suggestions:

*   **Temperature:** 0.7 - Encourages creative solutions while maintaining coherence
*   **Top-p:** 0.9 - Prioritizes accuracy in dependency information
*   **Frequency Penalty:** 1.5 - Incentivizes regular updates and checks
*   **Presence Penalty:** 2.0 - Rewards suggestions that address potential issues directly

## 9. Suggested Deployment Frameworks:

- Cloud Platforms: AWS (SageMaker, Lambda, EC2) or Google Cloud (Vertex AI, Cloud Functions, Compute Engine)
- Containerization: Docker with Kubernetes for scaling and management
- Frameworks: LangChain for dependency management and integration