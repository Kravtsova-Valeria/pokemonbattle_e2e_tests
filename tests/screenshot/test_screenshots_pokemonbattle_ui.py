import allure
import pytest
from pages.trainer_page import TrainerPage
from pages.premium_page import PremiumPage


@allure.feature("Скриншотные тесты")
class TestScreenshots:
    @allure.title("Проверка вёрстки карточки тренера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_screenshot_trainer_card(self, screenshot_trainer_page, screenshot_test):
        """
        Делает снимок карточки характеристик тренера,
        скрывая часто меняющиеся элементы (покеболы, уровень, ачивки).
        """
        screenshot_trainer_page.should_be_loaded()

        dynamic_elements = [
            TrainerPage.DYNAMIC_TEXT,
            TrainerPage.DYNAMIC_SLIDER,
            TrainerPage.ACHIEVEMENT_ICONS,
        ]

        screenshot_test(
            screenshot_trainer_page.driver,
            name="trainer_card.png",
            element=TrainerPage.TRAINER_CARD,
            mask=dynamic_elements,
            threshold=0.2
        )


@allure.feature("Скриншотные тесты")
class TestScreenshotsPremium:
    @allure.title("Проверка блока ввода дней и стоимости 'Премиума'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("days", [1, 31, 181, 366])
    def test_screenshot_premium_days_block(self, screenshot_premium_page, screenshot_test, days):
        """
        Вводит указанное количество дней, дожидается появления стоимости за день
        и делает скриншот блока покупки премиума.
        """
        screenshot_premium_page.prepare_premium_block_screenshot(days)

        screenshot_test(
            screenshot_premium_page.driver,
            name=f"premium_block_{days}_days.png",
            element=PremiumPage.PREMIUM_BLOCK,
            threshold=0.2
        )


@allure.feature("Скриншотные тесты формы оплаты")
class TestScreenshotsPayment:
    @allure.title("Пустая форма оплаты")
    @allure.severity(allure.severity_level.NORMAL)
    def test_payment_empty_form(self, screenshot_payment_page, screenshot_test):
        screenshot_test(
            screenshot_payment_page.driver,
            name="payment_empty_form.png",
            threshold=0.2
        )

    @allure.title("Заполненная форма (валидные данные)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_payment_filled_valid(self, screenshot_payment_page, screenshot_test):
        screenshot_payment_page.fill_valid_card_and_blur()
        screenshot_test(
            screenshot_payment_page.driver,
            name="payment_filled_valid.png",
            threshold=0.2
        )

    @allure.title("Неверный номер карты")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("invalid_card", ["0000 0000 0000 0000"])
    def test_payment_invalid_card_number(self, screenshot_payment_page, screenshot_test, invalid_card):
        screenshot_payment_page.fill_invalid_card_number_and_blur(invalid_card)
        screenshot_test(
            screenshot_payment_page.driver,
            name="payment_invalid_card.png",
            threshold=0.2
        )

    @allure.title("Неверный срок карты")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("invalid_expiry", ["11/11"])
    def test_payment_invalid_expiry(self, screenshot_payment_page, screenshot_test, invalid_expiry):
        screenshot_payment_page.fill_invalid_expiry_and_blur(invalid_expiry)
        screenshot_test(
            screenshot_payment_page.driver,
            name="payment_invalid_expiry.png",
            threshold=0.2
        )
