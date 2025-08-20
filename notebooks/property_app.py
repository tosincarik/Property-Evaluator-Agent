from dotenv import load_dotenv
from openai import OpenAI
import os
import pandas as pd
import gradio as gr

# Load environment variables
load_dotenv(override=True)
openaiapi = os.getenv("OPENAI_API_KEY")

# System prompt tailored for property recommendations
system_prompt_property = """
You are a real estate advisor AI. 
You are given a dataset of properties including location, price, bedrooms, bathrooms, parking spaces, toilets, title, and description. 
When a user provides their preferences (budget, location, property type, number of bedrooms), you must return the top 3 properties that best match their needs. 
Provide a short reasoning for each recommendation. 
Always consider price affordability and feature match.
"""

# Load property dataset
sheet_url = "https://docs.google.com/spreadsheets/d/15h3j-Q-Xepsok2ru5Au_havdWMdJ983qBGBXzceCuig/export?format=csv&gid=474984245"
df_cleaned = pd.read_csv(sheet_url)

# Initialize OpenAI client
client = OpenAI()

# Function to filter properties and prepare user prompt
def get_recommendation_input(budget=None, location=None, property_type=None, bedrooms=None):
    df_filtered = df_cleaned

    if budget is not None:
        df_filtered = df_filtered[df_filtered['Price'] <= budget]
    if location:
        df_filtered = df_filtered[df_filtered['Location'].str.contains(location, case=False, na=False)]
    if property_type:
        df_filtered = df_filtered[df_filtered['Title'].str.contains(property_type, case=False, na=False)]
    if bedrooms is not None:
        df_filtered = df_filtered[df_filtered['Bedrooms'] == bedrooms]

    df_top = df_filtered.sort_values(by='Score', ascending=False).head(5)

    prompt = f"Recommend top properties based on these preferences:\nBudget: {budget}\n"
    prompt += f"Location: {location}\nProperty Type: {property_type}\nBedrooms: {bedrooms}\n\n"
    prompt += "Available properties:\n"
    for idx, row in df_top.iterrows():
        prompt += f"- {row['Title']} | Price: ₦{row['Price']:,.0f} | Location: {row['Location']} | Bedrooms: {row['Bedrooms']} | Bathrooms: {row['Bathrooms']} | Parking: {row['Parking Spaces']} | Toilets: {row['Toilets']} | Score: {row['Score']}\n"
    return prompt

# Chat wrapper
def chat_property(user_message, history):
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

# Unified function: handles both first filter-based suggestion and free conversation
def respond(message, history, budget=None, location=None, property_type=None, bedrooms=None):
    # If the message is empty (initial click), use the filters
    if message.strip() == "":
        user_prompt = get_recommendation_input(budget, location, property_type, bedrooms)
    else:
        user_prompt = message

    reply = chat_property(user_prompt, history)
    history.append((user_prompt, reply))
    return history, history

# Build Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## 🏡 Property Finder Chatbot")

    chatbot = gr.Chatbot(type="messages")
    state = gr.State([])

    with gr.Row():
        budget = gr.Number(label="Budget (₦)", value=200000000)
        location = gr.Textbox(label="Location", placeholder="e.g., Lagos")
        property_type = gr.Textbox(label="Property Type", placeholder="e.g., Apartment")
        bedrooms = gr.Number(label="Bedrooms", value=3)

    user_input = gr.Textbox(label="Your message", placeholder="Type follow-up questions or preferences here")
    send_button = gr.Button("Send")

    # Connect both button and Enter key to respond()
    send_button.click(respond, inputs=[user_input, state, budget, location, property_type, bedrooms], outputs=[chatbot, state])
    user_input.submit(respond, inputs=[user_input, state, budget, location, property_type, bedrooms], outputs=[chatbot, state])

demo.launch()
