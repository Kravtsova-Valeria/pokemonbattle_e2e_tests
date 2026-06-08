import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from data.urls import BASE_URL, TRAINER_PAGE
from data.test_trainer_data import TEST_TRAINER_ID


class MainPage(BasePage):
    URL = BASE_URL
    TRAINER_CARD_ID = (By.XPATH, f"//div[@class='header_card_trainer_id_num' and text()='{TEST_TRAINER_ID}']")

    @allure.step("Переходим на страницу тренера")
    def go_to_trainer_page(self):
        self.click(self.TRAINER_CARD_ID)
        self.wait_for_url(TRAINER_PAGE)
