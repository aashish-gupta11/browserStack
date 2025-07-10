# BrowserStack Selenium Automation Assignment

## 📄 What is this Assignment?

**Technical Assignment: Run Selenium Test on BrowserStack**

This project demonstrates:

- Web scraping
- API integration
- Text processing
- Cross-browser automation using BrowserStack

**Steps Implemented:**

1. **Visit the website:**  
   [El País](https://elpais.com/) – a Spanish news outlet.
2. **Verify language:**  
   Ensure the website displays content in Spanish.
3. **Scrape Articles:**  
   - Navigate to the **Opinion** section.
   - Fetch the first **five** articles.
   - Print each article’s title and content in Spanish.
   - Download and save the cover image (if available).
4. **Translate Headers:**
   - Use a translation API to translate titles into English.
   - Print translated headers.
5. **Analyze Headers:**
   - Identify words repeated more than twice in all translated titles.
   - Print each repeated word with its occurrence count.
6. **Cross-Browser Testing:**
   - Execute the solution locally.
   - Run tests on BrowserStack in **5 parallel threads** across desktop and mobile browsers.

---

## ▶️ How to Run This Project

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
2. **Create Environment Variables:**

    Create a .env file in the project root:

    BROWSERSTACK_USERNAME=your_browserstack_username
    BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
    TRANSLATION_API_KEY=your_translation_api_key

3. **Run Locally:**

    -python main.py
    
    This will:- 
        -Scrape articles.
        -Translate titles.
        -Print results.

4. **Run on BrowserStack:**

    -python browserstack_parallel.py
    
    This will:
        -Launch parallel sessions across 5 browsers/devices.
        -Open the website and validate accessibility.

