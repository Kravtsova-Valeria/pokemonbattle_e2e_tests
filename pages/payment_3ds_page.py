import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class Payment3DSPage(BasePage):
    SECURE_CODE_INPUT = (By.XPATH, "//input[@placeholder='00000']")
    CONFIRM_BUTTON = (By.XPATH, "//div[@class='style_1_base_button_payment_body']/button[@type='submit' and contains(@class, 'style_1_base_button_payment')]")

    def should_be_loaded(self):
        self.element_visible(self.SECURE_CODE_INPUT)

    @allure.step("Вводим защитный код: {code}")
    def enter_secure_code(self, code: str):
        self.type(self.SECURE_CODE_INPUT, code)
        self.find(self.SECURE_CODE_INPUT).send_keys("\t")

    @allure.step("Подтверждаем 3DS")
    def confirm_3ds(self):
        self.scroll_to(self.CONFIRM_BUTTON)
        self.click(self.CONFIRM_BUTTON)
        self.wait.until(EC.url_contains("/payment_success"))
