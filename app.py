import streamlit as st
from main import fetch_monday_data, format_board_data, limit_data_size, ask_ai

st.title("📊 Monday.com AI Business Intelligence Agent")

question = st.text_input("Ask a business question:")

if question:

    st.write("🔎 Fetching live data from monday.com...")
    data = fetch_monday_data()

    st.write("🧹 Formatting data...")
    clean_data = format_board_data(data)

    small_data = limit_data_size(clean_data)

    st.write("🤖 Asking AI...")
    answer = ask_ai(question, small_data)

    st.subheader("AI Answer")
    st.write(answer)
if "error" in data:
    st.error("Failed to fetch monday data")