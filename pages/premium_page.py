import time
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from data.urls import PREMIUM_PAGE


class PremiumPage(BasePage):
    URL = PREMIUM_PAGE
    DAYS_INPUT = (By.XPATH, "//input[@name='day']")  # Screenshot too
    BUY_PREMIUM_BUTTON = (By.ID, "buy-premium")  # Screenshot too
    PREMIUM_FIND = (By.XPATH, "//span[@data-qa='info-line-premium']")
    PREMIUM_ACTIVATED_TEXT = (By.XPATH, "//div[@class='k_title_premium' and text()='Премиум успешно подключен!']")
    OK_BUTTON = (By.ID, "ok-battles-premium")

    PREMIUM_ACTIVE_TEXT = (By.XPATH, "//div[@class='k_title_premium' and text()='Премиум подключен!']")
    CANCEL_PREMIUM_BUTTON = (By.ID, "cancel-premium")
    CONFIRM_CANCEL_BUTTON = (By.ID, "cancel-go-premium")
    CANCELLED_MESSAGE = (By.XPATH, "//div[@class='k_pre_title_premium k_big_font_premium' and text()='Вы отменили подписку :(']")

    # Screenshot
    COST_DAYS = (By.XPATH, "//span[@class='k_skidka_premium']")
    PREMIUM_BLOCK = (By.XPATH, "//div[@class='login__content profile k_page_main_premium']")
    FLEX_CONTAINER = (By.XPATH, "//div[@class='k_flex_premium']")

    # Screenshot
    def wait_discount_visible(self):
        # Ожидаем завершения анимации появления стоимости за день
        self.wait.until(
            lambda d: d.find_element(*self.COST_DAYS).get_attribute("style").strip() == ""
        )

    # Screenshot
    @allure.step("Вводим количество дней: {days} и ожидаем появления скидки")
    def prepare_premium_block_screenshot(self, days: int):
        days_input = self.find(self.DAYS_INPUT)
        days_input.clear()
        days_input.send_keys(str(days))
        self.wait_discount_visible()
        self.driver.execute_script("document.activeElement.blur();")
        time.sleep(2)
        block = self.find(self.PREMIUM_BLOCK)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
            block
        )

##########
    def should_be_loaded(self):
        self.element_visible(self.PREMIUM_FIND)
        assert self.get_current_url() == self.URL

    @allure.step("Выбираем количество дней: {days}")
    def set_days(self, days: int):
        self.type(self.DAYS_INPUT, str(days))

    @allure.step("Нажимаем кнопку 'Купить премиум'")
    def click_buy_premium(self):
        self.click(self.BUY_PREMIUM_BUTTON)
        self.wait.until(EC.url_contains("/payment/"))

    @allure.step("Проверяем, что премиум активен")
    def assert_premium_active(self):
        assert self.element_visible(self.PREMIUM_ACTIVE_TEXT).is_displayed()

    @allure.step("Нажимаем 'Отменить премиум'")
    def click_cancel_premium(self):
        self.click(self.CANCEL_PREMIUM_BUTTON)

    @allure.step("Подтверждаем отмену")
    def confirm_cancel(self):
        self.click(self.CONFIRM_CANCEL_BUTTON)

    @allure.step("Проверяем сообщение об отмене подписки")
    def assert_cancelled_message(self):
        assert self.element_visible(self.CANCELLED_MESSAGE).is_displayed()

    @allure.step("Проверяем сообщение об успешном подключении премиума")
    def assert_premium_activated_message(self):
        assert self.element_visible(self.PREMIUM_ACTIVATED_TEXT).is_displayed()

    @allure.step("Нажимаем 'ОК' и возвращаемся на главную")
    def click_ok_and_return_to_main(self):
        self.click(self.OK_BUTTON)
        main_page_indicator = (By.XPATH, "//div[contains(@class,'header_card_trainer_id')]")
        self.element_visible(main_page_indicator)
