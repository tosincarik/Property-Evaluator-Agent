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


openaiapi = os.getenv("OPENAI_API_KEY")
groqapi = os.getenv("groq_api_key")


if openaiapi:
    print(f"Openai key is found and starts with: {openaiapi[:8]}")
else:
    print("Open ai api not found")

if groqapi:
    print(f"groqapi key is found and starts with: {groqapi[:8]}")
else:
    print("groqapi ai api not found")

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



# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 🏡 Property Finder Chatbot")

    # Input fields for structured filters
    with gr.Row():
        budget = gr.Number(label="Budget (₦)", value=200000000)
        location = gr.Textbox(label="Location", placeholder="e.g., Lagos")
        property_type = gr.Textbox(label="Property Type", placeholder="e.g., Apartment")
        bedrooms = gr.Number(label="Bedrooms", value=3)

    # Chatbot display
    chatbot = gr.Chatbot()
    state = gr.State([])
    session_state = gr.State(None)

    # Single user input box for free text
    user_input = gr.Textbox(
        label="Type your message",
        placeholder="Enter your preferences or ask about properties...",
        lines=1
    )

    # Only one button: Find Properties
    find_btn = gr.Button("Find Properties")

    def handle_find_properties(user_message, budget, location, property_type, bedrooms, history, session_id):
        if session_id is None:
            session_id = str(uuid.uuid4())

        # Use filters if user_message is empty, otherwise prioritize message
        if user_message.strip():
            reply = chat_property(user_message, history)
            log_interaction(session_id, user_message, reply)
        else:
            # Use structured filters
            user_prompt, df_top = get_recommendation_input(budget, location, property_type, bedrooms)
            reply = chat_property(user_prompt, history)
            log_filters(session_id, budget, location, property_type, bedrooms)
            log_recommendations(session_id, df_top)
            log_interaction(session_id, user_prompt, reply)

        history.append((user_message if user_message.strip() else user_prompt, reply))

        return history, history, session_id, ""  # Clear input box

    # Connect button
    find_btn.click(
        handle_find_properties,
        inputs=[user_input, budget, location, property_type, bedrooms, state, session_state],
        outputs=[chatbot, state, session_state, user_input]
    )

demo.launch()


