import os
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from data.urls import BASE_URL
from data.test_trainer_data import TEST_TRAINER_ID


class LoginPage(BasePage):
    URL = BASE_URL
    LOGIN_INPUT = (By.ID, "k_email")
    PASSWORD_INPUT = (By.ID, "k_password")
    LOGIN_BUTTON = (By.CLASS_NAME, "k_form_send_auth")
    TRAINER_CARD_ID = (By.XPATH, f"//div[@class='header_card_trainer_id_num' and text()='{TEST_TRAINER_ID}']")

    def open_page(self):
        self.open(self.URL)

    @allure.step("Авторизуем пользователя")
    def login(self, email: str = None, password: str = None):
        email = email or os.getenv("LOGIN")
        password = password or os.getenv("PASSWORD")
        self.type(self.LOGIN_INPUT, email)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.element_visible(self.TRAINER_CARD_ID)
