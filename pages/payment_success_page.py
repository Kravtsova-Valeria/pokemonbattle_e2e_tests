import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from data.urls import PREMIUM_PAGE


class PaymentSuccessPage(BasePage):
    SUCCESS_TITLE = (By.XPATH, "//h3[@class='payment_status_top_title style_1_caption_20_500' and text()='Покупка прошла успешно']")
    BACK_TO_SHOP_LINK = (By.XPATH, "//p[@class='style_1_base_link_blue link_back' and text()='Вернуться в магазин']")

    def should_be_loaded(self):
        assert self.element_visible(self.SUCCESS_TITLE).is_displayed()

    @allure.step("Возвращаемся в магазин")
    def back_to_shop(self):
        self.click(self.BACK_TO_SHOP_LINK)
        self.wait_for_url(PREMIUM_PAGE)
