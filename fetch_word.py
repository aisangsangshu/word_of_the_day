import requests
import datetime

# Step 1: Get a random word from Random Word API
word_response = requests.get("https://random-word-api.herokuapp.com/word")
word = word_response.json()[0]

# Step 2: Get the definition from Free Dictionary API
definition_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
def_response = requests.get(definition_url)

# Step 3: Parse the definition
if def_response.status_code == 200:
    data = def_response.json()
    try:
        meaning = data[0]['meanings'][0]['definitions'][0]['definition']
    except (KeyError, IndexError):
        meaning = "Definition structure not found."
else:
    meaning = "Definition not found."

# Step 4: Save to markdown
date = datetime.datetime.now().strftime("%Y-%m-%d")
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# Word of the Day ({date})\n\n")
    f.write(f"**{word.capitalize()}**\n\n")
    f.write(f"**Meaning:** {meaning}\n")
