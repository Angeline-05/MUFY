
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
st.title("🌸 Positive Vibes App 🌸")

st.subheader("✨ Daily Positive Quote ✨")

random.seed(date.today().toordinal())
daily_quote = random.choice(quotes)

st.markdown(
    f'<div class="quote-box">{daily_quote}</div>',
    unsafe_allow_html=True
)

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


