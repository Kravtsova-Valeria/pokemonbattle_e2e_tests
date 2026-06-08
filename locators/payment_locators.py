from selenium.webdriver.common.by import By


class PaymentLocators:
    # Страница /premium
    days_input = (By.XPATH, "//input[@name='day']")
    buy_premium_button = (By.ID, "buy-premium")

    # Страница /payment/0
    card_number_input = (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
    card_expiry_input = (By.XPATH, "//input[@placeholder='00/00']")
    card_cvv_input = (By.XPATH, "//input[@placeholder='000']")
    card_holder_input = (By.XPATH, "//input[@placeholder='GERMAN DOLNIKOV']")
    pay_button = (By.XPATH, "//div[@class='style_1_base_button_payment_body']/button[@type='submit' and contains(@class, 'style_1_base_button_payment')]")

    # Страница /payment_3ds
    secure_code_input = (By.XPATH, "//input[@placeholder='00000']")
    confirm_3ds_button = (By.XPATH, "//div[@class='style_1_base_button_payment_body']/button[@type='submit' and contains(@class, 'style_1_base_button_payment')]")

    # Страница /payment_success
    success_title = (By.XPATH, "//h3[@class='payment_status_top_title style_1_caption_20_500' and text()='Покупка прошла успешно']")
    back_to_shop_link = (By.XPATH, "//p[@class='style_1_base_link_blue link_back' and text()='Вернуться в магазин']")

    # Страница /premium
    premium_activated_text = (By.XPATH, "//div[@class='k_title_premium' and text()='Премиум успешно подключен!']")
    ok_button = (By.ID, "ok-battles-premium")
