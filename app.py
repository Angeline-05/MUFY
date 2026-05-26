
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
# DYNAMIC THEMES
# ----------------------------

if theme == "Sage":
    bg = "linear-gradient(to bottom right, #f4f7f5, #dde7e1)"
    primary = "#5c7c6f"
    text = "#2f4f4f"
    box = "rgba(255,255,255,0.8)"
    border = "#c7d4cc"

elif theme == "Ocean":
    bg = "linear-gradient(to bottom right, #eef7fb, #d6eaf5)"
    primary = "#4a6fa5"
    text = "#24405c"
    box = "rgba(255,255,255,0.85)"
    border = "#bdd6e6"

elif theme == "Lavender":
    bg = "linear-gradient(to bottom right, #f6f2ff, #e6ddff)"
    primary = "#7b6ba8"
    text = "#4b3f72"
    box = "rgba(255,255,255,0.85)"
    border = "#d5c8f2"

elif theme == "Dark":
    bg = "linear-gradient(to bottom right, #1e1e1e, #2b2b2b)"
    primary = "#8fa3bf"
    text = "#f5f5f5"
    box = "rgba(50,50,50,0.9)"
    border = "#555555"

# Apply CSS
st.markdown(
    f"""
    <style>

    .stApp {{
        background: {bg};
    }}

    h1, h2, h3 {{
        color: {text};
        text-align: center;
    }}

    .quote-box {{
        background-color: {box};
        padding: 20px;
        border-radius: 20px;
        border: 1px solid {border};
        font-size: 22px;
        text-align: center;
        color: {text};
        margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        backdrop-filter: blur(8px);
    }}

    .stTextArea textarea {{
        background-color: {box};
        border-radius: 14px;
        border: 1px solid {border};
        color: {text};
    }}

    .stTextInput input {{
        background-color: {box};
        border-radius: 14px;
        border: 1px solid {border};
        color: {text};
    }}

    .stButton>button {{
        background-color: {primary};
        color: white;
        border-radius: 14px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: 0.3s;
    }}

    .stButton>button:hover {{
        opacity: 0.85;
        transform: scale(1.03);
    }}

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

