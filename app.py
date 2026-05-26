
import streamlit as st
import random
import json
import os
from datetime import date, datetime

# ----------------------------
# PAGE SETTINGS
# ----------------------------
st.set_page_config(
    page_title="Positive Vibes App",
    page_icon="🌸",
    layout="centered"
)

# ----------------------------
# CUSTOM CSS (Cute Theme)
# ----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fff0f6;
    }

    h1, h2, h3 {
        color: #ff4d8d;
        text-align: center;
    }

    .quote-box {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #ffcce0;
        font-size: 22px;
        text-align: center;
        color: #ff4d8d;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    .stTextArea textarea {
        background-color: #fff7fa;
        border-radius: 12px;
        border: 2px solid #ffcce0;
    }

    .stButton>button {
        background-color: #ff80ab;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }

    .stButton>button:hover {
        background-color: #ff4d8d;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# QUOTES
# ----------------------------
quotes = [
    "You are doing better than you think 🌷",
    "Small steps are still progress ✨",
    "Your feelings matter 💖",
    "You deserve happiness 🌸",
    "Believe in yourself a little more today ☁️",
    "Rest is productive too 🌼",
    "You are enough just as you are 💕",
    "A new day means new opportunities 🌈",
    "Keep going, you're growing 🌱",
    "You can do hard things ⭐"
]

# ----------------------------
# DAILY QUOTE
# ----------------------------
# ----------------------------
# DAILY QUOTE
# ----------------------------
st.title("🌸 Bloom Space 🌸")

st.subheader("✨ Daily Positive Quote ✨")

# Save quote in session state
if "current_quote" not in st.session_state:
    st.session_state.current_quote = random.choice(quotes)

# Display quote
st.markdown(
    f'<div class="quote-box">{st.session_state.current_quote}</div>',
    unsafe_allow_html=True
)

# Button to change quote
if st.button("🌷 New Positive Quote"):
    st.session_state.current_quote = random.choice(quotes)
    st.rerun()

# ----------------------------
# JOURNAL SECTION
# ----------------------------
st.subheader("📝 Daily Journal")

journal_text = st.text_area(
    "Write about your day:",
    height=200,
    placeholder="Today I felt..."
)

# ----------------------------
# SAVE JOURNAL
# ----------------------------
JOURNAL_FILE = "journal_entries.json"

if os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "r") as file:
        journal_data = json.load(file)
else:
    journal_data = {}

if st.button("💾 Save Journal"):
    today = str(date.today())

    journal_data[today] = {
        "entry": journal_text,
        "time": datetime.now().strftime("%H:%M")
    }

    with open(JOURNAL_FILE, "w") as file:
        json.dump(journal_data, file, indent=4)

    st.success("Journal saved successfully 💖")

# ----------------------------
# STREAK SYSTEM
# ----------------------------
st.subheader("🔥 Your Streak")

streak = 0

dates = sorted(journal_data.keys(), reverse=True)

if dates:
    previous_date = None

    for d in dates:
        current_date = datetime.strptime(d, "%Y-%m-%d").date()

        if previous_date is None:
            if current_date == date.today():
                streak += 1
                previous_date = current_date
        else:
            difference = (previous_date - current_date).days

            if difference == 1:
                streak += 1
                previous_date = current_date
            else:
                break

st.markdown(
    f"""
    <div class="quote-box">
        🔥 Current Streak: <b>{streak} days</b>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# PREVIOUS JOURNALS
# ----------------------------
st.subheader("📖 Previous Journal Entries")

if journal_data:
    for entry_date in sorted(journal_data.keys(), reverse=True):
        with st.expander(f"📅 {entry_date}"):
            st.write(journal_data[entry_date]["entry"])
            st.caption(f"Saved at {journal_data[entry_date]['time']}")
else:
    st.write("No journal entries yet 🌸")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.markdown(
    "<center>Made with 💖 using Streamlit</center>",
    unsafe_allow_html=True
)

# ----------------------------
# AI POSITIVITY CHATBOT
# ----------------------------
st.subheader("🤖 Positivity Chat Buddy")

# Save chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_message = st.chat_input("Type your thoughts here...")

# Bot response function
def positivity_bot(message):
    message = message.lower()

    if "sad" in message:
        return "I'm here for you 💖 Sad days do not last forever."

    elif "stress" in message or "stressed" in message:
        return "Take things one step at a time 🌸 You do not need to carry everything at once."

    elif "tired" in message:
        return "You deserve rest too ☁️ Please be gentle with yourself."

    elif "anxious" in message:
        return "Pause for a moment 🌿 Breathe slowly. You are safe."

    elif "lonely" in message:
        return "Even when it feels lonely, you are still worthy of love and care ✨"

    elif "happy" in message:
        return "YAYYY 🌷 Hold onto that happiness!"

    else:
        return "You are doing better than you think 💕"

# When user sends message
if user_message:

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    # Generate bot response
    bot_reply = positivity_bot(user_message)

    # Save bot response
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

# Display chat messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

