import requests
from groq import Groq

import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# API KEYS (add your real keys)
# ----------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

url = "https://api.monday.com/v2"

query = """
{
  boards (ids: [5026872371,5026872367]) {
    name
    items_page(limit:50) {
      items {
        name
        column_values {
          text
          column {
            title
          }
        }
      }
    }
  }
}
"""

headers = {
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json"
}

# ----------------------------
# FETCH LIVE DATA
# ----------------------------
def fetch_monday_data():
    try:
        response = requests.post(url, json={"query": query}, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ----------------------------
# FORMAT DATA
# ----------------------------
def format_board_data(data):

    output = ""

    for board in data["data"]["boards"]:
        output += f"\nBoard: {board['name']}\n"

        for item in board["items_page"]["items"]:
            output += f"\nItem: {item['name']}\n"

            for col in item["column_values"]:
                title = col["column"]["title"]
                value = col["text"] if col["text"] else "Unknown"
                output += f"{title}: {value}\n"

    return output

# ----------------------------
# LIMIT DATA SIZE
# ----------------------------
def limit_data_size(text):
    return text[:3500]

# ----------------------------
# ASK AI
# ----------------------------
def ask_ai(question, structured_data):

    prompt = f"""
You are a Business Intelligence assistant.

Here is monday.com data:

{structured_data}

Answer clearly like explaining to a founder.

Question: {question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content