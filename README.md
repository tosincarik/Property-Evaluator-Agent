🏡 Property Advisor AI Chatbot

A real estate AI tool designed to assist property investors and buyers in Lagos by evaluating and recommending the best properties based on their preferences. The chatbot utilizes OpenAI's GPT-4 to provide ranked property suggestions along with reasoning, making property decision-making efficient and data-driven.

Project Overview

The Property Advisor AI Chatbot helps real estate investors and homebuyers quickly identify suitable properties in Lagos using AI. By processing user input (budget, location, property type, and number of bedrooms), the chatbot matches this information with available property data and ranks the most suitable properties based on price, location, and amenities.

Problem Statement

Manual property research can be time-consuming, inconsistent, and error-prone. Buyers often face challenges such as fluctuating prices, multiple listings, and varying property quality, making the decision-making process complicated.

Solution

This AI-driven property advisor integrates OpenAI’s GPT-4 to analyze a dataset of properties and deliver top recommendations. Users provide their preferences, and the AI ranks the most suitable properties, offering detailed reasoning for each recommendation. The system aims to help users make quicker, more informed decisions.

Features

Property Recommendation: Input preferences (budget, location, property type, bedrooms) and get the top 3 properties ranked by GPT-4 based on your input.

Natural Language Chat: Engage in a dynamic conversation with the AI to refine property preferences.

User-Friendly Interface: Simple, intuitive design built with Gradio for easy interaction.

Real-Time Results: Immediate suggestions based on real-time property data (static dataset used for demo purposes).

Dataset

Source: Due to Hugging Face’s 10MB size limitation, the dataset is hosted on Google Sheets for demo purposes. The dataset is synthetic but representative of typical property listings in Lagos.

Dataset Link: Property Dataset - Google Sheets

Columns Include:

Title

Price

Location

Bedrooms

Bathrooms

Size

Property Type

Score (based on a custom scoring algorithm)

Workflow
Data Processing

Initial Data Processing:

First, an IPython notebook (.ipynb) was used to clean, process, and structure the dataset for the chatbot's requirements. The notebook included steps such as handling missing values, filtering data, and transforming the dataset to make it ready for AI analysis.

The processed dataset was then saved and used for further analysis in subsequent steps.

Transition to Python Script:

After completing the data preprocessing, the IPython notebook was converted into a Python script (app.py) for deployment in Hugging Face, which does not support Jupyter notebooks natively.

The Python script now runs the data processing, interacts with GPT-4, and serves the chatbot application.

How It Works

User Input: Users enter their preferences, such as budget, location, property type, and number of bedrooms.

LLM Analysis: OpenAI's GPT-4 evaluates the dataset and generates property recommendations.

Evaluation Logic: The properties are filtered and ranked based on relevance to user preferences.

Output: The AI generates a list of the top 3 recommended properties, with explanations for each.

Installation & Requirements

To run this project locally, follow the steps below:

Prerequisites

Python 3.9+

Dependencies:

openai (for GPT-4 integration)

pandas (for data manipulation)

gradio (for building the UI)

python-dotenv (for managing environment variables)
