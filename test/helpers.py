# helpers.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import STREAMLIT_URL

def login(driver, username, password):
    driver.get(STREAMLIT_URL)

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Username']"))
    )
    password_input = driver.find_element(By.XPATH, "//input[@aria-label='Password']")

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']"))
    )
    login_button.click()

    time.sleep(2) 

def logout(driver):
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Keluar')]"))
    )
    logout_button.click()
    time.sleep(2)

