A Multi-LLM AI tool that helps real estate investors and buyers in Lagos make informed property decisions by evaluating data and ranking recommendations from multiple LLMs.

Project Overview

Investors and buyers often struggle to identify optimal properties due to fluctuating prices, multiple listings, and varying neighborhood quality. This advisor leverages multiple large language models (LLMs) to provide ranked property recommendations with reasoning, enabling fast, data-driven decisions.

Business Case

Problem: Manual property research is time-consuming, inconsistent, and error-prone.

Solution: Integrate multiple LLMs to evaluate property datasets and deliver top recommendations efficiently.

Dataset

Source: Static CSV dataset for demo purposes.

Columns include: Title, Price, Location, Bedrooms, Bathrooms, Size, Property Type.

Note: Dataset is synthetic but representative to demonstrate workflow.

Architecture & Workflow

User Input: Budget, location, property type, preferences.

LLM Analysis: Two LLMs (e.g., GPT-4 + Grok/Claude) independently evaluate the dataset.

Evaluation Logic: Mechanism compares outputs and selects the best recommendations.

Output: Top 3 properties with brief explanations for each choice.

(Optional: include a simple workflow diagram here)

Installation & Requirements

Python 3.9+

Install dependencies:
