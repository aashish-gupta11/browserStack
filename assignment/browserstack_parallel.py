from dotenv import load_dotenv
import os
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import selenium

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")


BROWSER_CONFIGS = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "Chrome Test"
        }
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "Safari Test"
        }
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Firefox Test"
        }
    },
    {
        "browserName": "iPhone",
        "bstack:options": {
            "deviceName": "iPhone 14",
            "osVersion": "16",
            "realMobile": "true",
            "sessionName": "iPhone Test"
        }
    },
    {
        "browserName": "Android",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S23",
            "osVersion": "13",
            "realMobile": "true",
            "sessionName": "Android Test"
        }
    },
]


def run_test(capability):
    try:
        session_name = capability["bstack:options"].get("sessionName", "Unnamed")
        print(f"Launching {session_name}...")

        # Create Options dynamically
        options = webdriver.ChromeOptions()
        for key, value in capability.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(
            command_executor=f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
            options=options
        )

        driver.get("https://elpais.com/")
        title = driver.title
        print(f"{session_name}: {title}")

        driver.quit()

    except Exception:
        import traceback
        print(f"\nError in {session_name}:\n")
        traceback.print_exc()


if __name__ == "__main__":
    print("Selenium version:", selenium.__version__)
    print("Selenium file:", selenium.__file__)
    print("Starting BrowserStack tests...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_test, BROWSER_CONFIGS)

    print("All BrowserStack tests complete.")
