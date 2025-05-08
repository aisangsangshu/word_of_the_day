import requests
import datetime

# Get random word
word = "default"
try:
    word_response = requests.get("https://random-word-api.vercel.app/api?words=1")
    word_response.raise_for_status()  # Will throw error if status code is not 2xx

    words = word_response.json()
    if words:
        word = words[0]
except Exception as e:
    print(f"Failed to get word: {e}")

# Get meaning
meaning = "Definition not found."
try:
    meaning_response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if meaning_response.status_code == 200:
        meaning_data = meaning_response.json()
        meaning = meaning_data[0]['meanings'][0]['definitions'][0]['definition']
except Exception as e:
    print(f"Failed to get meaning: {e}")

# Write to markdown
today = datetime.datetime.now().strftime("%Y-%m-%d")
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"## 📅 Word of the Day - {today}\n\n")
    f.write(f"### **{word}**\n")
    f.write(f"- **Meaning**: {meaning}\n")
    f.write(f"\n---\n")
