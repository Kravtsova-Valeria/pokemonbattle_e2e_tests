import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class PaymentPage(BasePage):
    CARD_NUMBER_INPUT = (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
    CARD_EXPIRY_INPUT = (By.XPATH, "//input[@placeholder='00/00']")
    CARD_CVV_INPUT = (By.XPATH, "//input[@placeholder='000']")
    CARD_HOLDER_INPUT = (By.XPATH, "//input[@placeholder='GERMAN DOLNIKOV']")
    PAY_BUTTON = (By.XPATH, "//div[@class='style_1_base_button_payment_body']/button[@type='submit' and contains(@class, 'style_1_base_button_payment')]")

    # Screenshot
    FORM_BLOCK = (By.XPATH, "//div[@class='payment_page_content']")
    RECEIPT_BUTTON = (By.XPATH, "//div[@class='payment_receipt_open_button']")
    ERROR_MESSAGE = (By.XPATH, "//span[@class='style_1_base_input_error']")
    ERROR_EXPIRY_MESSAGE = (By.XPATH, "//span[@class='style_1_base_input_error' and contains(text(),'Неверный срок')]")

    # Screenshot

    def blur_active_element(self):
        self.driver.execute_script("document.activeElement.blur();")
        import time
        time.sleep(0.5)

    def fill_valid_card_and_blur(self):
        from data.payment_data import VALID_CARD
        self.fill_card_data(VALID_CARD)
        self.blur_active_element()

    def fill_invalid_card_number_and_blur(self, card_number: str):
        card_field = self.find(self.CARD_NUMBER_INPUT)
        card_field.clear()
        card_field.send_keys(card_number)
        self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        self.blur_active_element()

    def fill_invalid_expiry_and_blur(self, expiry: str):
        from data.payment_data import VALID_CARD
        card_field = self.find(self.CARD_NUMBER_INPUT)
        card_field.clear()
        card_field.send_keys(VALID_CARD["card_number"])
        expiry_field = self.find(self.CARD_EXPIRY_INPUT)
        expiry_field.clear()
        expiry_field.send_keys(expiry)
        self.blur_active_element()
        # Ждём сообщение "Неверный срок"
        self.wait.until(EC.visibility_of_element_located(self.ERROR_EXPIRY_MESSAGE))
        # Ещё раз убираем курсор
        self.blur_active_element()

    def should_be_loaded(self):
        self.element_visible(self.CARD_NUMBER_INPUT)

    @allure.step("Заполняем данные карты")
    def fill_card_data(self, card_data: dict):
        card_number = self.find(self.CARD_NUMBER_INPUT)
        self.driver.execute_script("arguments[0].value = arguments[1];", card_number, card_data["card_number"])
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", card_number)

        self.type(self.CARD_EXPIRY_INPUT, card_data["card_actual"])
        self.type(self.CARD_CVV_INPUT, card_data["card_cvv"])
        self.type(self.CARD_HOLDER_INPUT, card_data["card_name"])
        self.find(self.CARD_HOLDER_INPUT).send_keys("\t")

    @allure.step("Нажимаем кнопку оплаты")
    def click_pay(self):
        pay_btn = self.find(self.PAY_BUTTON)
        self.wait.until(lambda d: pay_btn.get_attribute("disabled") is None)
        self.scroll_to(self.PAY_BUTTON)
        self.click(self.PAY_BUTTON)
        self.wait.until(EC.url_contains("/payment_3ds"))
