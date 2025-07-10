import os
import re
import requests
from time import sleep
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# === Load API Key from .env ===
load_dotenv()
GOOGLE_API_KEY = os.getenv("TRANSLATION_API_KEY")
IMG_SAVE_DIR = "images"

# === Configure Chrome ===
options = Options()
options.add_argument("--lang=es")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

def go_to_opinion_section():
    driver.get("https://elpais.com/")
    sleep(3)
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Aceptar")]').click()
        sleep(1)
    except:
        pass

    try:
        opinion_link = driver.find_element(By.XPATH, '//a[contains(@href, "/opinion/")]')
        driver.execute_script("arguments[0].scrollIntoView();", opinion_link)
        sleep(1)
        driver.execute_script("arguments[0].click();", opinion_link)
        sleep(3)
    except Exception as e:
        print(f"Error navigating to Opinion section: {e}")
        driver.quit()
        exit(1)

def download_image(title):
    # Try multiple image sources
    try:
        # 1. Try standard <picture><img>
        img_elem = driver.find_element(By.CSS_SELECTOR, 'picture img')
        img_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
        if not img_url or not img_url.startswith("http"):
            raise Exception("Invalid picture src")
    except:
        try:
            # 2. Try og:image meta tag
            img_url = driver.find_element(By.XPATH, '//meta[@property="og:image"]').get_attribute("content")
        except:
            try:
                # 3. Try any <img> on the page
                img_elem = driver.find_element(By.TAG_NAME, "img")
                img_url = img_elem.get_attribute("src")
            except:
                img_url = None

    if img_url and img_url.startswith("http"):
        try:
            os.makedirs(IMG_SAVE_DIR, exist_ok=True)
            safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title[:30])
            img_path = os.path.join(IMG_SAVE_DIR, f"{safe_title}.jpg")
            img_data = requests.get(img_url, timeout=10).content
            with open(img_path, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded image: {img_path}")
            return img_url
        except Exception as e:
            print(f"Failed to download image: {e}")
    else:
        print("No image URL found.")
    return None

def scrape_articles():
    article_links = []
    for elem in driver.find_elements(By.CSS_SELECTOR, 'article a')[:5]:
        href = elem.get_attribute("href")
        if href and href.startswith("https://elpais.com") and href not in article_links:
            article_links.append(href)

    data = []
    for href in article_links:
        try:
            driver.get(href)
            sleep(2)

            title = driver.find_element(By.TAG_NAME, "h1").text
            paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p')
            content = "\n".join([p.text for p in paragraphs if len(p.text.strip()) > 20])

            img_url = download_image(title)

            data.append({
                "title": title,
                "content": content,
                "image_url": img_url
            })
        except Exception as e:
            print(f"Skipping article due to error: {e}")
    return data

def translate_titles(titles):
    translations = []
    for title in titles:
        try:
            url = "https://translation.googleapis.com/language/translate/v2"
            params = {
                'q': title,
                'target': 'en',
                'key': GOOGLE_API_KEY
            }
            response = requests.post(url, data=params)
            result = response.json()
            translated_text = result['data']['translations'][0]['translatedText']
            translations.append(translated_text)
        except Exception as e:
            print(f"Translation failed: {e}")
            translations.append("[Translation failed]")
    return translations

def analyze_translations(translated_titles):
    text = " ".join(translated_titles).lower()
    words = re.findall(r'\w+', text)
    word_counts = Counter(words)
    print("\n--- Repeated Words (appearing >1 times) ---")
    for word, count in word_counts.items():
        if count > 1:
            print(f"{word}: {count}")

def main():
    go_to_opinion_section()
    articles = scrape_articles()

    print("\n--- Original Articles (Spanish) ---")
    for i, art in enumerate(articles, 1):
        print(f"\nArticle {i}: {art['title']}")
        print(f"Content: {art['content'][:400]}...")

    titles = [a["title"] for a in articles]
    translated_titles = translate_titles(titles)

    print("\n--- Translated Titles (English) ---")
    for i, title in enumerate(translated_titles, 1):
        print(f"{i}. {title}")

    analyze_translations(translated_titles)
    driver.quit()

if __name__ == "__main__":
    main()

