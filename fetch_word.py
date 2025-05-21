import requests
import datetime
import os

# Get random word
word = "default"
try:
    word_response = requests.get("https://random-word-api.vercel.app/api?words=1")
    word_response.raise_for_status()

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

# Write to README.md
today = datetime.datetime.now().strftime("%Y-%m-%d")
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"## 📅 Word of the Day - {today}\n\n")
    f.write(f"### **{word}**\n")
    f.write(f"- **Meaning**: {meaning}\n")
    f.write(f"\n---\n")

# Export values to GitHub Actions
output_path = os.environ.get("GITHUB_OUTPUT")
if output_path:
    with open(output_path, "a") as f:
        f.write(f"word={word}\n")
        # Escape any special characters in the meaning that might break sed
        escaped_meaning = meaning.replace("'", "'\\''").replace("&", "\\&").replace("/", "\\/")
        f.write(f"meaning={escaped_meaning}\n")
        f.write(f"date={today}\n")
else:
    print("GITHUB_OUTPUT environment variable not set. Outputs will not be available to GitHub Actions.")
    # Still print the outputs for debugging
    print(f"::set-output name=word::{word}")
    print(f"::set-output name=meaning::{meaning}")
    print(f"::set-output name=date::{today}")