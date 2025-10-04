import requests
import datetime
import os
import urllib.parse
import json
from urllib import request, error            
def translate_to_zh(text: str, timeout_seconds: int = 10) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""
    try:
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "zh-CN",
            "dt": "t",
            "q": text,
        }
        query = urllib.parse.urlencode(params)
        url = f"{base_url}?{query}"
        with request.urlopen(url, timeout=timeout_seconds) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            data = resp.read().decode(charset, errors="replace")
            parsed = json.loads(data)
            # Structure: [ [ [ translatedText, originalText, ... ], ... ], ... ]
            segments = parsed[0] if isinstance(parsed, list) and parsed else []
            translated_parts = []
            for seg in segments:
                if isinstance(seg, list) and len(seg) > 0 and isinstance(seg[0], str):
                    translated_parts.append(seg[0])
            zh = "".join(translated_parts).strip()
            return zh
    except Exception as e:
        print(f"Failed to translate meaning: {e}")
    return ""

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
zh_meaning = "Definition not found."
part_of_speech = "unknown"
try:
    meaning_response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if meaning_response.status_code == 200:
        meaning_data = meaning_response.json()
        meaning = meaning_data[0]['meanings'][0]['definitions'][0]['definition']
        part_of_speech = meaning_data[0]['meanings'][0]['partOfSpeech']
        zh_meaning = translate_to_zh(meaning)
    elif meaning_response.status_code == 404:
        zh_meaning = translate_to_zh(word)
except Exception as e:
    print(f"Failed to get meaning: {e}")
    


def map_part_of_speech_to_zh(pos: str) -> str:#返回课可能是空字符串
    mapping = {
        'noun': '名词',
        'verb': '动词',
        'adjective': '形容词',
        'adverb': '副词',
        'pronoun': '代词',
        'preposition': '介词',
        'conjunction': '连词',
        'interjection': '感叹词',
        'article': '冠词',
        'determiner': '限定词',
        'numeral': '数词',
        'proper noun': '专有名词',
        'auxiliary verb': '助动词',
        'phrasal verb': '短语动词',
        'abbreviation': '缩写',
        'prefix': '前缀',
        'suffix': '后缀',
        'unknown': '未知词性',
    }
    key = (pos or '').strip().lower()
    return mapping.get(key, '')

# Write to README.md
today = datetime.datetime.now().strftime("%Y-%m-%d")


# Keep README compatibility with the first item
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"## 📅 Word of the Day - {today}\n\n")
    f.write(f"### **{word}**\n")
    f.write(f"- **Meaning**: {meaning}\n")
    f.write(f"- **zh-Meaning**: {map_part_of_speech_to_zh(part_of_speech)} ;{zh_meaning}\n")
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