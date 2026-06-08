from selenium.webdriver.common.by import By


class PremiumPageLocators:
    pokemon_premium_button = (By.XPATH, "//div[@data-qa='premium']")
    premium_find = (By.XPATH, "//span[@data-qa='info-line-premium']")
