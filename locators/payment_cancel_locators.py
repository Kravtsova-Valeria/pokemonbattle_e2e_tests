from selenium.webdriver.common.by import By


class PaymentCancelLocators:
    premium_active_text = (By.XPATH, "//div[@class='k_title_premium' and text()='Премиум подключен!']")
    cancel_premium_button = (By.ID, "cancel-premium")
    confirm_cancel_button = (By.ID, "cancel-go-premium")
    cancelled_message = (By.XPATH, "//div[@class='k_pre_title_premium k_big_font_premium' and text()='Вы отменили подписку :(']")
