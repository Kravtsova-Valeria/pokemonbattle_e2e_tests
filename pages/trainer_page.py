import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from data.urls import TRAINER_PAGE, PREMIUM_PAGE
from data.test_trainer_data import TEST_TRAINER_ID


class TrainerPage(BasePage):
    URL = TRAINER_PAGE
    TRAINER_ID = (By.XPATH, f"//div[@class='copy_number_id' and text()='{TEST_TRAINER_ID}']")
    PREMIUM_BUTTON = (By.XPATH, "//div[@data-qa='premium']")
    BEGINNING_ACHIEVEMENT = (By.ID, "beginning")
    # Screenshot
    TRAINER_CARD = (By.XPATH, "//div[@class='single_page_body_content_inner_top']")
    ACHIEVEMENT_ICONS = (By.XPATH, "//div[@class='achievements']")
    # Общий локатор для динамических текстовых значений (уровень, покеболы)
    DYNAMIC_TEXT = (By.XPATH, "//span[contains(@class, 'single_page_body_content_inner_top_list_attr_one_text')]")
    # Общий локатор для слайдеров (уровень, покеболы)
    DYNAMIC_SLIDER = (By.XPATH, "//ul[contains(@class, 'single_page_body_content_inner_top_list_attr_one_slide')]")

    def should_be_loaded(self):
        self.element_visible(self.TRAINER_ID)
        self.element_visible(self.TRAINER_CARD)  # для test_screenshot_trainer_card
        assert self.get_current_url() == self.URL

    @allure.step("Проверяем, что ачивка 'Начало большого пути' активна")
    def check_beginning_achievement_active(self):
        achievement = self.element_visible(self.BEGINNING_ACHIEVEMENT)
        class_attr = achievement.get_attribute("class")
        assert "active" in class_attr, f"Ачивка не активна: class={class_attr}"

    @allure.step("Переходим на страницу покупки премиума")
    def go_to_premium_page(self):
        button = self.find(self.PREMIUM_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.click(self.PREMIUM_BUTTON)
        self.wait_for_url(PREMIUM_PAGE)
