from typing import Tuple
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout

    def open(self, url: str):
        with allure.step(f"Открываем страницу: {url}"):
            self.driver.get(url)

    def find(self, locator: Tuple[str, str]):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_many(self, locator: Tuple[str, str]):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: Tuple[str, str]):
        with allure.step(f"Кликаем по элементу: {locator}"):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.scroll_to(locator)
            element.click()
            return element

    def type(self, locator: Tuple[str, str], text: str, clear_first: bool = True):
        with allure.step(f"Вводим текст '{text}' в элемент {locator}"):
            element = self.find(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            return element

    def scroll_to(self, locator: Tuple[str, str]):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def wait_for_url(self, url: str):
        self.wait.until(EC.url_to_be(url))

    def get_current_url(self) -> str:
        return self.driver.current_url

    def element_visible(self, locator: Tuple[str, str]):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        try:
            self.find(locator)
            return True
        except Exception:
            return False
