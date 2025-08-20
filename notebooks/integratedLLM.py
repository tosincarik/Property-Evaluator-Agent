# %%
!pip install openai python-dotenv pypdf gradio

# %%
from dotenv import load_dotenv
from IPython.display import Markdown
from openai import OpenAI
from pypdf import PdfReader
import os
import gradio as gr

# %%
load_dotenv(override=True)

# %%
openaiapi = os.getenv("OPENAI_API_KEY")
groqapi = os.getenv("groq_api_key")

# %%
if openaiapi:
    print(f"Openai key is found and starts with: {openaiapi[:8]}")
else:
    print("Open ai api not found")

if groqapi:
    print(f"groqapi key is found and starts with: {groqapi[:8]}")
else:
    print("groqapi ai api not found")

# %%
# System prompt tailored for property recommendations
system_prompt_property = """
You are a real estate advisor AI. 
You are given a dataset of properties including location, price, bedrooms, bathrooms, parking spaces, toilets, title, and description. 
When a user provides their preferences (budget, location, property type, number of bedrooms), you must return the top 3 properties that best match their needs. 
Provide a short reasoning for each recommendation. 
Always consider price affordability and feature match.
"""


# %%
processed_path = "../data/processed/cleaned_property_data.csv"

# %%

import pandas as pd

# Ensure df_cleaned is a DataFrame
processed_path = "../data/processed/cleaned_property_data.csv"
df_cleaned = pd.read_csv(processed_path)


# %%
df_cleaned

# %%
openai = OpenAI()

# %%


def chat_property(user_prompt, history=[]):
    messages = [{"role": "system", "content": system_prompt_property}] + history + [{"role": "user", "content": user_prompt}]
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    return reply


# %%
# Example user input
user_prompt = get_recommendation_input(
    budget=200000000, 
    location="Lagos", 
    property_type="Apartment", 
    bedrooms=3
)

# Generate GPT-4 recommendation
reply = chat_property(user_prompt)
print(reply)


# %%
processed_path = "../data/processed/cleaned_property_data.csv"

# %%
import gradio as gr
from openai import OpenAI

processed_path = "C:/Users/Admin/projects/Property-Evaluator-Agent/data/processed/cleaned_property_data.csv"
df_cleaned = pd.read_csv(processed_path)
# Your existing functions
client = OpenAI()

def get_recommendation_input(budget=None, location=None, property_type=None, bedrooms=None):
    """
    Prepare user query and filtered dataset subset for LLM
    """
    df_filtered = df_cleaned  # assume df_cleaned is globally available

    # Filters
    if budget is not None:
        df_filtered = df_filtered[df_filtered['Price'] <= budget]
    if location:
        df_filtered = df_filtered[df_filtered['Location'].str.contains(location, case=False, na=False)]
    if property_type:
        df_filtered = df_filtered[df_filtered['Title'].str.contains(property_type, case=False, na=False)]
    if bedrooms is not None:
        df_filtered = df_filtered[df_filtered['Bedrooms'] == bedrooms]

    # Select top 5
    df_top = df_filtered.sort_values(by='Score', ascending=False).head(5)

    # Build user prompt
    prompt = f"Recommend top properties based on these preferences:\nBudget: {budget}\n"
    prompt += f"Location: {location}\nProperty Type: {property_type}\nBedrooms: {bedrooms}\n\n"
    prompt += "Available properties:\n"
    for idx, row in df_top.iterrows():
        prompt += f"- {row['Title']} | Price: ₦{row['Price']:,.0f} | Location: {row['Location']} | Bedrooms: {row['Bedrooms']} | Bathrooms: {row['Bathrooms']} | Parking: {row['Parking Spaces']} | Toilets: {row['Toilets']} | Score: {row['Score']}\n"
    return prompt


def chat_property(user_message, history):
    """
    Chat wrapper that keeps history and calls GPT
    """
    # Convert Gradio history format [(user, bot), ...] to OpenAI messages
    messages = [{"role": "system", "content": system_prompt_property}]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    reply = response.choices[0].message.content
    return reply


# Function to link filters + chat
def recommend_with_filters(budget, location, property_type, bedrooms, history=[]):
    user_prompt = get_recommendation_input(budget, location, property_type, bedrooms)
    reply = chat_property(user_prompt, history)
    history.append((user_prompt, reply))
    return history, history


# Build Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## 🏡 Property Finder Chatbot")

    with gr.Row():
        budget = gr.Number(label="Budget (₦)", value=200000000)
        location = gr.Textbox(label="Location", placeholder="e.g., Lagos")
        property_type = gr.Textbox(label="Property Type", placeholder="e.g., Apartment")
        bedrooms = gr.Number(label="Bedrooms", value=3)

    chatbot = gr.Chatbot()
    state = gr.State([])

    send_button = gr.Button("Find Properties")

    send_button.click(
        recommend_with_filters,
        inputs=[budget, location, property_type, bedrooms, state],
        outputs=[chatbot, state]
    )

demo.launch()


# %%



