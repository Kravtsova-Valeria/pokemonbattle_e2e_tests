import io
import os
import sys
import time
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv
from PIL import Image, ImageChops
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.payment_data import VALID_CARD
from data.urls import BASE_URL_ME, LAVKA_BASE_URL

from pages.payment_page import PaymentPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.trainer_page import TrainerPage
from pages.premium_page import PremiumPage


# UI
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = Chrome(options=chrome_options)
    # driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def load_envs():
    load_dotenv()


@pytest.fixture
def authorized_user(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login()
    return driver


@pytest.fixture
def main_page(authorized_user):
    return MainPage(authorized_user)


@pytest.fixture
def trainer_page(main_page):
    main_page.go_to_trainer_page()
    trainer_page = TrainerPage(main_page.driver)
    trainer_page.should_be_loaded()
    return trainer_page


@pytest.fixture
def premium_page(trainer_page):
    trainer_page.go_to_premium_page()
    premium_page = PremiumPage(trainer_page.driver)
    premium_page.should_be_loaded()
    return premium_page


# API
@pytest.fixture
def trainer_token():
    token = os.getenv("POKEMON_AUTH_TOKEN")
    if not token:
        raise ValueError("POKEMON_AUTH_TOKEN не найден")
    return token


@pytest.fixture
def api_headers(trainer_token):
    return {
        "trainer_token": trainer_token,
        "Content-Type": "application/json"
    }


@pytest.fixture
def ensure_no_premium(api_headers):
    """
    Перед тестом убеждаемся, что премиум отключен.
    После теста (teardown) также отключаем премиум.
    """
    me_response = requests.get(BASE_URL_ME, headers=api_headers)
    assert me_response.status_code == 200, "Ошибка получения статуса премиума"
    is_premium = me_response.json()["data"][0]["is_premium"]
    if is_premium:
        cancel_response = requests.post(
            f"{LAVKA_BASE_URL}/cancel_premium",
            headers=api_headers
        )
        assert cancel_response.status_code == 200, "Не удалось отключить премиум перед тестом"

    yield

    requests.post(f"{LAVKA_BASE_URL}/cancel_premium", headers=api_headers)


@pytest.fixture
def ensure_premium(api_headers):
    """
    Перед тестом убеждаемся, что премиум включен.
    После теста отключаем премиум, чтобы вернуть окружение в исходное состояние.
    """
    me_response = requests.get(BASE_URL_ME, headers=api_headers)
    assert me_response.status_code == 200
    is_premium = me_response.json()["data"][0]["is_premium"]
    if not is_premium:
        payload = {"order_type": "premium", "details": VALID_CARD}
        buy_response = requests.post(
            f"{LAVKA_BASE_URL}/payments",
            json=payload,
            headers=api_headers
        )
        assert buy_response.status_code == 200, f"Не удалось включить премиум: {buy_response.text}"

    yield

    requests.post(f"{LAVKA_BASE_URL}/cancel_premium", headers=api_headers)


# Screenshot
@pytest.fixture(scope="session")
def screenshot_driver():
    chrome_options = Options()
    # оптимальная практика, т.к. шрифты во всех тестах загружаются крайне нестабильно
    chrome_options.add_argument("--disable-remote-fonts")
    driver = Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def screenshot_authorized_user(screenshot_driver):
    login_page = LoginPage(screenshot_driver)
    login_page.open_page()
    login_page.login()

    main_page = MainPage(screenshot_driver)
    main_page.go_to_trainer_page()
    trainer_page = TrainerPage(main_page.driver)
    trainer_page.should_be_loaded()
    time.sleep(20)
    screenshot_driver.get("https://pokemonbattle.ru/")
    return screenshot_driver


@pytest.fixture
def screenshot_main_page(screenshot_authorized_user):
    return MainPage(screenshot_authorized_user)


@pytest.fixture
def screenshot_trainer_page(screenshot_main_page):
    screenshot_main_page.go_to_trainer_page()
    trainer_page = TrainerPage(screenshot_main_page.driver)
    trainer_page.should_be_loaded()
    return trainer_page


@pytest.fixture
def screenshot_premium_page(screenshot_authorized_user):
    main = MainPage(screenshot_authorized_user)
    main.go_to_trainer_page()
    trainer = TrainerPage(main.driver)
    trainer.should_be_loaded()
    trainer.go_to_premium_page()
    premium = PremiumPage(trainer.driver)
    premium.should_be_loaded()
    return premium


@pytest.fixture
def screenshot_payment_page(screenshot_authorized_user):
    driver = screenshot_authorized_user
    driver.get("https://pokemonbattle.ru/")
    main = MainPage(driver)
    main.go_to_trainer_page()
    trainer = TrainerPage(main.driver)
    trainer.should_be_loaded()
    trainer.go_to_premium_page()
    premium = PremiumPage(trainer.driver)
    premium.should_be_loaded()
    premium.set_days(3)
    premium.click_buy_premium()
    payment_page = PaymentPage(premium.driver)
    # Ждём, пока появится поле ввода номера карты – признак загрузки страницы
    payment_page.find(PaymentPage.CARD_NUMBER_INPUT)
    return payment_page


@pytest.fixture(scope="session")
def browser_name():
    return "chrome"


def hide_element(driver, locator):
    # Скрывает элемент(ы) по локатору или WebElement, делая их прозрачными
    if hasattr(locator, "get_attribute"):
        elems = [locator]
    elif isinstance(locator, tuple):
        elems = driver.find_elements(*locator)
    else:
        raise Exception("Некорректный элемент/локатор!")
    for el in elems:
        driver.execute_script(
            "arguments[0].style.transition='none';"
            "arguments[0].style.opacity='0';", el
        )


@pytest.fixture
def screenshot_test(request, browser_name):
    def run(
        driver,
        name: str,
        element=None,
        threshold: float = 0.05,
        baseline_dir: str = Path(request.node.fspath).parent.resolve() / "__snapshots__" / browser_name / sys.platform,
        diff_dir: str = "__screenshot_diffs__",
        mask: list = None
    ):
        # 1. Маскировка динамических элементов
        if mask:
            for loc in mask:
                try:
                    hide_element(driver, loc)
                except Exception:
                    pass
            time.sleep(0.5)

        # 2. Ожидание полной загрузки страницы
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        # 3. Ожидание видимости элемента (если передан)
        if element is not None:
            if isinstance(element, tuple):
                element = driver.find_element(*element)
            WebDriverWait(driver, 5).until(EC.visibility_of(element))

        # 4. Пауза для загрузки шрифтов и завершения анимаций
        time.sleep(5)

        # 5. Снятие скриншота
        if element is None:
            png = driver.get_screenshot_as_png()
        else:
            png = element.screenshot_as_png

        # 6. Сохраняем текущий снимок как изображение Pillow
        actual_image = Image.open(io.BytesIO(png)).convert("RGB")

        # 7. Работа с эталоном
        baseline_path = os.path.join(baseline_dir, name)
        if not os.path.exists(baseline_path):
            # Первый запуск – создаём эталон
            os.makedirs(os.path.dirname(baseline_path), exist_ok=True)
            with open(baseline_path, 'wb') as f:
                f.write(png)
            return

        # Эталон существует – сравниваем
        baseline_image = Image.open(baseline_path).convert("RGB")

        # Если размеры не совпадают – сразу ошибка
        if actual_image.size != baseline_image.size:
            os.makedirs(diff_dir, exist_ok=True)
            actual_path = os.path.join(diff_dir, f"{name[:-4] if name.endswith('.png') else name}_actual.png")
            base_copy = os.path.join(diff_dir, f"{name[:-4] if name.endswith('.png') else name}_baseline.png")
            actual_image.save(actual_path)
            baseline_image.save(base_copy)
            pytest.fail(f"Размеры снимка и эталона не совпадают: {actual_image.size} vs {baseline_image.size}")

        # Вычисляем долю отличающихся пикселей
        diff = ImageChops.difference(actual_image, baseline_image)
        diff_pixels = sum(1 for p in diff.getdata() if p != (0, 0, 0))
        total_pixels = diff.size[0] * diff.size[1]
        diff_ratio = diff_pixels / total_pixels

        if diff_ratio <= threshold:
            return  # тест пройден

        # Расхождение больше порога – создаём диффы
        os.makedirs(diff_dir, exist_ok=True)
        if name.lower().endswith(".png"):
            name_no_ext = name[:-4]
        else:
            name_no_ext = name

        actual_path = os.path.join(diff_dir, f"{name_no_ext}_actual.png")
        base_copy   = os.path.join(diff_dir, f"{name_no_ext}_baseline.png")
        diff_path   = os.path.join(diff_dir, f"{name_no_ext}_diff.png")

        actual_image.save(actual_path)
        baseline_image.save(base_copy)

        # Подсветим различия красным
        mask_img = diff.convert("L").point(lambda v: 255 if v > 10 else 0, mode="1")
        red = Image.new("RGB", actual_image.size, (255, 0, 0))
        highlight = actual_image.copy()
        highlight.paste(red, mask=mask_img)
        highlight.save(diff_path)

        pytest.fail(
            f"Snapshot mismatch for '{name}'. Diff ratio: {diff_ratio:.4f} (threshold={threshold}). "
            f"See {actual_path}, {base_copy}, {diff_path}"
        )
    return run
