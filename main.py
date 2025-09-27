import os
from dotenv import load_dotenv

from datetime import datetime as dt
import time

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from retrying import retry

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


load_dotenv(".env.local")
logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s %(message)s"
)
logging.info(f"cwd: {os.getcwd()}")

cookie = os.getenv("SESSION_COOKIE")
logging.info(f"cookie: {cookie}")


def setup_driver():
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
    chromium_bin = os.getenv("CHROME_BIN", "/usr/bin/chromium")

    options = webdriver.ChromeOptions()
    options.binary_location = chromium_bin

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-background-timer-throttling")

    options.page_load_strategy = "eager"

    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=options)


# def setup_driver_debug():
#     from webdriver_manager.chrome import ChromeDriverManager
#
#     options = webdriver.ChromeOptions()
#
#     options.add_argument("--headless=new")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--no-sandbox")
#
#     options.page_load_strategy = 'eager'
#
#
#
#     service = Service(ChromeDriverManager().install())
#     browser = webdriver.Chrome(service=service, options=options)
#
#     return browser


@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def login(session_cookie: str):
    browser = None
    try:
        browser = setup_driver()
        # browser = setup_driver_debug()

        browser.set_window_size(1024, 768)

        browser.get("https://music.163.com")

        logging.info("Injecting session cookie")

        # cookie_value = session_cookie.strip()
        # logging.info(f"Session cookie length: {len(cookie_value)}")

        browser.delete_all_cookies()
        browser.add_cookie(
            {
                "name": "MUSIC_U",
                "value": session_cookie,
                # "domain": ".music.163.com",
                # "path": "/"
            }
        )



        browser.refresh()

        time.sleep(2)
        dt_str = dt.now().strftime("%Y-%m-%d_%H:%M:%S")
        browser.save_screenshot(f"login_record/{dt_str}.png")
        

        # chrome hangs:
        # HTTPConnectionPool(host='localhost', port=60710): Read timed out. (read timeout=120)

        # try:
        #
        #     # logging.info("checkpoint 1")
        #
        #     # WebDriverWait(browser, 10).until(
        #     #     EC.frame_to_be_available_and_switch_to_it((By.ID, "g_iframe"))
        #     # )
        #     #
        #     # logging.info("checkpoint 2")
        #     #
        #     # info_xpath = """//*[@id="discover-module"]/div[2]/div[2]/div"""
        #     # myinfo_element = WebDriverWait(browser, 15).until(
        #     #     EC.presence_of_element_located((By.XPATH, info_xpath))
        #     # )
        #
        #     logging.info("checkpoint 1")
        #
        #     iframe_el = WebDriverWait(browser, 15).until(
        #         EC.presence_of_element_located((By.ID, "g_iframe"))
        #     )
        #
        #     logging.info("checkpoint 2")
        #
        #     browser.switch_to.frame(iframe_el)
        #
        #     logging.info("checkpoint 3")
        #
        #     myinfo_element = WebDriverWait(browser, 20).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, "div.n-myinfo"))
        #     )
        #
        #
        #
        #     logging.info("login successful")
        #
        # except Exception as e:
        #     logging.error("failed to find div.n-myinfo")
        #     raise

        logging.info("login successful")

    except Exception as e:
        logging.error(f"login failed: {e}")
        raise
    finally:
        if browser:
            browser.quit()


def main():
    try:
        cookie = os.getenv("SESSION_COOKIE")
        if not cookie:
            raise ValueError("SESSION_COOKIE not found")

        logging.info("======= START LOGIN =======")
        login(cookie)
        logging.info("===== END LOGIN: SUCC =====")

    except Exception as e:
        logging.error(f"failure: {e}")
        logging.info("===== END LOGIN: FAIL =====")


if __name__ == "__main__":
    main()
