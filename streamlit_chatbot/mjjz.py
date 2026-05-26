
import streamlit as st
import random
import json
import os
from datetime import date, datetime, timedelta

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="MindBloom",
    page_icon="🌿",
    layout="centered"
)

# ----------------------------
# LOGIN SYSTEM (SIMPLE)
# ----------------------------
USERS_FILE = "users.json"

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🌿 MindBloom")

if st.session_state.user is None:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    def login():
        if username in users and users[username] == password:
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Invalid login")

    def signup():
        if username == "" or password == "":
            st.warning("Fill in all fields")
        else:
            users[username] = password
            with open(USERS_FILE, "w") as f:
                json.dump(users, f)
            st.success("Account created! Now log in.")

    with col1:
        if st.button("Login"):
            login()

    with col2:
        if st.button("Sign Up"):
            signup()

    st.stop()

st.success(f"Welcome {st.session_state.user} 🌿")

# ----------------------------
# DATA FILE PER USER
# ----------------------------
BASE_DIR = os.path.dirname(__file__)
JOURNAL_FILE = os.path.join(BASE_DIR, f"journal_{st.session_state.user}.json")

if os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "r") as f:
        journal_data = json.load(f)
else:
    journal_data = {}

# ----------------------------
# QUOTES
# ----------------------------
quotes = [
    "You are doing better than you think 🌿",
    "Small steps still count ✨",
    "Rest is productive too ☁️",
    "You are enough as you are 🌱",
    "Breathe. You are safe. 🌙",
    "Growth takes time 🌼",
    "One day at a time 🌤️",
    "You are not behind 🌿",
    "Keep going gently ✨",
    "Your feelings are valid 🤍"
]

# ----------------------------
# THEME SWITCHER
# ----------------------------
theme = st.selectbox("🎨 Choose Theme", ["Sage", "Ocean", "Dark", "Minimal", "Pink"])

if theme == "Sage":
    bg = "linear-gradient(to bottom right, #f4f7f5, #dde7e1)"
    primary = "#5c7c6f"
    text = "#2f4f4f"
    box = "rgba(255,255,255,0.8)"
    border = "#c7d4cc"

elif theme == "Ocean":
    bg = "linear-gradient(to bottom right, #e8f4f8, #d6eaf5)"
    primary = "#3b6ea5"
    text = "#1f3b57"
    box = "rgba(255,255,255,0.85)"
    border = "#bcd7e6"

elif theme == "Dark":
    bg = "linear-gradient(to bottom right, #1c1c1c, #2a2a2a)"
    primary = "#8aa4c4"
    text = "#f2f2f2"
    box = "rgba(40,40,40,0.9)"
    border = "#444"

elif theme == "Pink":
    bg = "linear-gradient(to bottom right, #fff0f6, #ffd6e7)"
    primary = "#ff4d8d"
    text = "#4a2b3a"
    box = "rgba(255,255,255,0.85)"
    border = "#ffc1d6"

else:
    bg = "#f7f7f7"
    primary = "#555"
    text = "#222"
    box = "white"
    border = "#ddd"

st.markdown(f"""
<style>
.stApp {{ background: {bg}; }}
h1, h2, h3 {{ color: {text}; text-align: center; }}
.quote-box {{
    background: {box};
    padding: 20px;
    border-radius: 16px;
    border: 1px solid {border};
    color: {text};
    text-align: center;
    margin-bottom: 15px;
}}
.stButton>button {{
    background: {primary};
    color: white;
    border-radius: 10px;
    padding: 10px 15px;
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# QUOTE
# ----------------------------
if "quote" not in st.session_state:
    st.session_state.quote = random.choice(quotes)

st.subheader("✨ Daily Quote")
st.markdown(f"<div class='quote-box'>{st.session_state.quote}</div>", unsafe_allow_html=True)

if st.button("🌿 New Quote"):
    st.session_state.quote = random.choice(quotes)
    st.rerun()

# ----------------------------
# JOURNAL + MOOD
# ----------------------------
st.subheader("📝 Journal & Mood")

mood = st.selectbox("Mood", ["😊 Happy", "😌 Calm", "😐 Neutral", "😔 Sad", "😟 Anxious", "😴 Tired"])
text = st.text_area("Write your thoughts...")

def save_entry():
    if text.strip() == "":
        st.warning("Write something first 🌿")
        return

    today = str(date.today())

    journal_data[today] = {
        "mood": mood,
        "entry": text,
        "time": datetime.now().strftime("%H:%M")
    }

    with open(JOURNAL_FILE, "w") as f:
        json.dump(journal_data, f, indent=4)

    st.success("Saved ✨")

if st.button("💾 Save Entry"):
    save_entry()

# ----------------------------
# STREAK
# ----------------------------
st.subheader("🔥 Streak")

streak = 0
for i, d in enumerate(sorted(journal_data.keys(), reverse=True)):
    if i == 0:
        streak = 1
    else:
        prev = datetime.strptime(sorted(journal_data.keys(), reverse=True)[i-1], "%Y-%m-%d").date()
        curr = datetime.strptime(d, "%Y-%m-%d").date()
        if (prev - curr).days == 1:
            streak += 1
        else:
            break

st.markdown(f"<div class='quote-box'>🔥 {streak} day streak</div>", unsafe_allow_html=True)

# ----------------------------
# WEEKLY SUMMARY
# ----------------------------
st.subheader("📊 Weekly Summary")

week_ago = date.today() - timedelta(days=7)

entries = [
    journal_data[d]
    for d in journal_data
    if datetime.strptime(d, "%Y-%m-%d").date() >= week_ago
]

st.write(f"Entries this week: {len(entries)}")

if entries:
    mood_count = {}
    for e in entries:
        m = e["mood"]
        mood_count[m] = mood_count.get(m, 0) + 1

    st.write("Mood breakdown:")
    st.write(mood_count)

# ----------------------------
# HISTORY
# ----------------------------
st.subheader("📖 History")

for d in sorted(journal_data.keys(), reverse=True):
    with st.expander(d):
        st.write("Mood:", journal_data[d]["mood"])
        st.write(journal_data[d]["entry"])
        st.caption(journal_data[d]["time"])


