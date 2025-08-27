# test_auth.py

import pytest
from helpers import login, logout
from config import ADMIN_USERNAME, ADMIN_PASSWORD, USER_USERNAME, USER_PASSWORD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAuthentication:
    def test_invalid_login(self, driver):
        login(driver, "user_salah", "pass_salah")

        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Username atau password tidak ditemukan')]"))
        )
        assert error_message.is_displayed()

    def test_admin_login_and_navigation(self, driver):
        login(driver, ADMIN_USERNAME, ADMIN_PASSWORD)

        sidebar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stSidebar']"))
        )
        sidebar_text = sidebar.text

        assert "Prediksi" in sidebar_text
        assert "Kelola Barang" in sidebar_text
        assert "List Barang" in sidebar_text
        assert "Riwayat Prediksi" not in sidebar_text  # ini memang tidak ada di sidebar

        logout(driver)

    def test_user_login_and_navigation(self, driver):
        login(driver, USER_USERNAME, USER_PASSWORD)

        sidebar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stSidebar']"))
        )
        sidebar_text = sidebar.text
        assert "Prediksi" not in sidebar_text
        assert "Riwayat Prediksi" not in sidebar_text
        assert "List Barang" in sidebar_text

        logout(driver)
