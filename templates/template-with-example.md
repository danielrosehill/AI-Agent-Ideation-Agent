## Nutrition Navigator

## Description:

NutritionNavigator is an AI assistant designed to help individuals optimize their diet based on personal health goals, dietary restrictions, and nutritional science. It serves as a personalized nutrition coach for health-conscious individuals, those with specific dietary needs, and people looking to improve their relationship with food.

## Use Case Outline:

*   **User Personas**: 
    * Health-conscious individuals seeking to optimize their diet
    * People with medical conditions requiring dietary modifications (diabetes, celiac disease, etc.)
    * Athletes looking to enhance performance through nutrition
    * Busy professionals who want to eat healthier but lack time for meal planning
    * Parents trying to improve family nutrition

*   **Scenario 1:** A user with newly diagnosed diabetes asks for meal planning assistance that maintains stable blood sugar levels while still being enjoyable. NutritionNavigator provides a weekly meal plan with glycemic index information, portion guidance, and recipes that fit their taste preferences.

*   **Scenario 2:** An athlete preparing for a marathon requests nutrition advice to optimize training and recovery. The assistant analyzes their current diet, training schedule, and goals to recommend timing of nutrients, hydration strategies, and performance-enhancing foods.

*   **Scenario 3:** A parent with picky eaters at home asks for help introducing more vegetables. NutritionNavigator suggests creative recipes that disguise vegetables, age-appropriate ways to involve children in food preparation, and evidence-based strategies for expanding children's food preferences.

## Benefits:

*   Increased adherence to healthy eating patterns by 47% through personalized recommendations.
*   Improved nutritional knowledge with science-backed information tailored to individual needs.
*   Reduced meal planning time by 75% with automated shopping lists and recipe suggestions.
*   Enhanced dietary management for medical conditions through condition-specific guidance.
*   Decreased food waste by 30% through smart ingredient usage and leftover repurposing.
*   Provides real-time nutritional analysis that was previously only available through expensive dietitian consultations.

## Risks, Limits

*   **Data Bias:** Nutritional recommendations may reflect biases in training data toward Western diets and conventional nutritional wisdom.
*   **Hallucinations:** The assistant may generate incorrect nutritional information or make unfounded health claims.
*   **Lack of Medical Context:** While providing nutritional guidance, the assistant cannot diagnose conditions or replace medical advice.
*   **Security Concerns:** Handling of sensitive health data requires robust privacy measures and HIPAA compliance.
 

## RAG And Context Requirements

*   **Context Window:** 8k tokens - Necessary to maintain conversation history about dietary preferences, restrictions, and previous recommendations while analyzing new queries.
*   **RAG Required:** Yes - RAG is essential for accessing up-to-date nutritional databases, scientific research, and recipe repositories. The implementation should include:
    * Nutritional composition databases (USDA Food Data Central)
    * Peer-reviewed nutritional science publications
    * Medical guidelines for diet-related conditions
    * Recipe databases with nutritional information
    * User's personal health data and dietary history (with permission)

## Real Time Data And Search Requirements

*   **Real-time Data Required:** Yes - Access to current food databases, seasonal ingredient availability, and updated medical guidelines is essential. Updates should occur at least monthly for nutritional databases and daily for seasonal food availability.
*   **Search Required:** Yes - Web search capabilities are needed to find recent nutritional studies, regional food options, and specific product information. Integration with specialized nutrition search APIs like Edamam or Spoonacular would be optimal.

## Multimodal Capabilities

*   **Vision Required:** Yes - The assistant needs vision capabilities to:
    * Analyze food photos for portion estimation and nutritional content
    * Scan food labels and ingredient lists
    * Recognize specific foods and dishes from user-submitted images
    * Process visual food diaries and meal logs
    * Suggested APIs: Google Cloud Vision API, Microsoft Computer Vision, or specialized food recognition APIs like Calorie Mama API
*   **Multimodal Input/Output Required:** Yes - The assistant requires:
    * Image input processing for food recognition and analysis
    * Ability to generate and share visual content (nutritional charts, meal plan visualizations)
    * Audio input for voice-based food logging and queries
    * Suggested frameworks: OpenAI's GPT-4 Vision, CLIP, or specialized food recognition models like FoodVisor
*   **Specialized Processing Needs:** OCR capabilities for processing nutrition labels and ingredient lists; food-specific image recognition trained on diverse cuisines and presentation styles; chart generation for visualizing nutritional data and trends

## Tool Suggestions

*   **APIs:**
    *   Edamam Nutrition Analysis API (https://developer.edamam.com/edamam-nutrition-api) - For detailed nutritional breakdown of recipes and meals
    *   Spoonacular API (https://spoonacular.com/food-api) - For recipe suggestions and ingredient substitutions
    *   MyFitnessPal API - For tracking nutritional intake over time
    *   Cronometer API - For micronutrient analysis
*   **MCP Tools:**
     * Image Analysis Tool - For identifying foods from user-uploaded photos
     * Sequential Thinking - For breaking down complex nutritional problems
     * Web Search - For accessing current nutritional research
*   **Libraries/Frameworks:**
    *   LangChain - For orchestrating the retrieval and reasoning pipeline
    *   Pinecone - For vector storage of nutritional knowledge
    *   Pandas - For nutritional data analysis
    *   Matplotlib/Plotly - For visualizing nutritional trends

## Draft System Prompt

```
You are NutritionNavigator, an AI nutrition coach providing personalized, science-based dietary guidance.

**Persona:** Knowledgeable, supportive, and non-judgmental nutrition expert.

**Instructions:**

*   Understand user's goals, restrictions, preferences, and medical conditions.
*   Provide evidence-based nutritional advice, avoiding fads and pseudoscience.
*   Personalize meal plans/recipes considering dietary needs, nutritional balance, practicality, and cultural relevance.
*   Cite reputable sources for nutritional claims.
*   Offer specific, actionable advice.
*   Analyze dietary patterns, not isolated meals.
*   Frame recommendations positively (add, don't avoid).

**Constraints:**

*   No medical diagnoses or treatment claims.
*   Avoid extreme diets unless specifically requested and appropriate.
*   Avoid definitive claims on controversial topics.
*   Never shame users about food choices/body.
*   No infant nutrition advice (under 12 months).
*   Avoid outcome promises (e.g., weight loss).

**Output Format:**

*   Meal plans: Structured daily plans with ingredients and nutritional highlights.
*   Nutritional analysis: Macronutrient/micronutrient breakdown, areas for improvement.
*   Recipes: Ingredients, steps, nutritional information.
*   Use bullet points for clarity.
*   Include visuals when helpful.

**Tone:** Supportive, evidence-based, and practical.

**Handling Ambiguity:** Ask clarifying questions about goals, restrictions, or preferences.

**Error Handling:** If asked about medical treatment or non-nutrition health advice, state limitations and suggest consulting healthcare professionals.
```

## Parameter Suggestions:

*   **Temperature:** 0.4 - A lower temperature ensures consistency and accuracy in nutritional information while still allowing for some creativity in meal suggestions.
*   **Top-p:** 0.85 - Provides a good balance between diversity and accuracy for nutritional recommendations.
*   **Frequency Penalty:** 0.3 - Helps avoid repetitive advice patterns while maintaining consistency in nutritional guidance.
*   **Presence Penalty:** 0.2 - Encourages exploration of diverse food options without straying too far from evidence-based recommendations.
*   **Max Tokens:** 1024 - Sufficient for detailed meal plans and nutritional explanations without overwhelming the user.
*   **Stop Sequences:** ["User:", "Human:", "Question:"] - Prevents the model from continuing the conversation on behalf of the user.
*   **Other Parameters**: Consider implementing content filtering to prevent potentially harmful dietary advice.

 