import os
import uuid
import pandas as pd
import gradio as gr
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate keys
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key not found in environment variables")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in environment variables")

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# System prompt for property recommendations
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

# Logging functions
def log_interaction(session_id, user_message, bot_reply):
    try:
        supabase.table("interactions").insert({
            "session_id": session_id,
            "user_message": user_message,
            "bot_reply": bot_reply
        }).execute()
    except Exception as e:
        print(f"[Log Interaction Error]: {e}")

def log_filters(session_id, budget, location, property_type, bedrooms):
    try:
        supabase.table("filters").insert({
            "session_id": session_id,
            "budget": budget,
            "location": location,
            "property_type": property_type,
            "bedrooms": bedrooms
        }).execute()
    except Exception as e:
        print(f"[Log Filters Error]: {e}")

def log_recommendations(session_id, df_top, limit=3):
    try:
        recs = df_top.sort_values(by="Score", ascending=False).head(limit)
        payload = []
        for _, r in recs.iterrows():
            payload.append({
                "session_id": session_id,
                "property_title": str(r.get("Title", "")),
                "price": float(r.get("Price", 0) or 0),
                "location": str(r.get("Location", "")),
                "score": float(r.get("Score", 0) or 0),
            })
        if payload:
            supabase.table("recommendations").insert(payload).execute()
    except Exception as e:
        print(f"[Log Recommendations Error]: {e}")

# Core functions
def get_recommendation_input(budget=None, location=None, property_type=None, bedrooms=None):
    """Filter dataset and prepare prompt for LLM"""
    df_filtered = df_cleaned.copy()

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

    return prompt, df_top

def chat_property(user_message, history):
    """Send conversation to OpenAI API with chat history"""
    messages = [{"role": "system", "content": system_prompt_property}]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[Chat API Error]: {e}")
        return "Sorry, I couldn't process your request at the moment."

def recommend_with_filters(budget, location, property_type, bedrooms, history=None, session_id=None):
    """Handles filtering, chat, and logging"""
    if history is None:
        history = []

    if session_id is None:
        session_id = str(uuid.uuid4())

    user_prompt, df_top = get_recommendation_input(budget, location, property_type, bedrooms)
    reply = chat_property(user_prompt, history)
    history.append((user_prompt, reply))

    # Log to Supabase
    log_filters(session_id, budget, location, property_type, bedrooms)
    log_recommendations(session_id, df_top)
    log_interaction(session_id, user_prompt, reply)

    return history, history, session_id

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 🏡 Property Finder Chatbot")

    with gr.Row():
        budget = gr.Number(label="Budget (₦)", value=200000000)
        location = gr.Textbox(label="Location", placeholder="e.g., Lagos")
        property_type = gr.Textbox(label="Property Type", placeholder="e.g., Apartment")
        bedrooms = gr.Number(label="Bedrooms", value=3)

    chatbot = gr.Chatbot()
    state = gr.State([])
    session_state = gr.State(None)

    send_button = gr.Button("Find Properties")

    send_button.click(
        recommend_with_filters,
        inputs=[budget, location, property_type, bedrooms, state, session_state],
        outputs=[chatbot, state, session_state]
    )

demo.launch()
