from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from helpers import login, logout
from config import ADMIN_USERNAME, ADMIN_PASSWORD
import time

class TestPredictionFlow:

    def test_prediction_flow_for_admin(self, driver):
        print("📍 Login sebagai admin")
        login(driver, ADMIN_USERNAME, ADMIN_PASSWORD)

        # Step 1: Tunggu sidebar muncul
        print("📍 Menunggu sidebar...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stSidebar']"))
        )

        # Step 2: Klik menu "Prediksi"
        print("📍 Klik radio menu 'Prediksi'...")
        prediction_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Prediksi')]"))
        )
        prediction_menu.click()

        # Step 3: Tunggu halaman Prediksi termuat (berdasarkan tombol atau header)
        try:
            print("📍 Menunggu tombol 'Tuning dan Prediksi' muncul...")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Tuning dan Prediksi')]"))
            )
        except TimeoutException:
            print("⛔ Gagal memuat halaman prediksi. Cek login atau role.")
            assert False

        time.sleep(1)  # beri waktu tambahan agar input benar-benar tersedia

        # Step 4: Isi form harga dan diskon
        print("📍 Mengisi input harga dan diskon...")
        print("📍 Mencari semua input...")
        inputs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='number' or @type='text']"))
        )
        assert len(inputs) >= 2, "Tidak ditemukan dua input field!"

        harga_input = inputs[0]
        diskon_input = inputs[1]

        harga_input.clear()
        harga_input.send_keys("75000")

        diskon_input.clear()
        diskon_input.send_keys("5")

        print("📍 Klik tombol 'Tuning dan Prediksi'...")
        predict_button = driver.find_element(By.XPATH, "//button[contains(., 'Tuning dan Prediksi')]")
        predict_button.click()

        # Step 6: Tunggu hasil prediksi muncul
        print("📍 Menunggu hasil prediksi muncul...")
        prediction_result = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(., 'Prediksi kelas')]"))
        )

        accuracy_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(., 'Akurasi model')]"))
        )

        # Step 7: Ambil nilai prediksi dari <strong>Murah/Mahal</strong>
        predicted_label = prediction_result.find_element(By.TAG_NAME, "strong").text

        # Step 8: Verifikasi tampilannya
        print(f"✅ Prediksi ditemukan: {predicted_label}")
        print(f"📊 Detail: {prediction_result.text}")
        print(f"📈 Akurasi: {accuracy_result.text}")

        assert "Prediksi kelas" in prediction_result.text
        assert "Akurasi model" in accuracy_result.text
        assert predicted_label in ["Murah", "Mahal"], "Hasil prediksi tidak valid"

        # Step 9: Logout
        print("📍 Logout admin")
        logout(driver)
