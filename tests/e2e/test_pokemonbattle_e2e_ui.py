import allure
import pytest
from data.payment_data import VALID_CARD
from pages.premium_page import PremiumPage
from pages.payment_page import PaymentPage
from pages.payment_3ds_page import Payment3DSPage
from pages.payment_success_page import PaymentSuccessPage


@allure.feature("Навигация по страницам")
class TestNavigation:
    @allure.title("Переход на страницу тренера с главной")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_main_to_trainer(self, main_page):
        main_page.go_to_trainer_page()

    @allure.title("Переход на страницу премиума со страницы тренера")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_trainer_to_premium(self, trainer_page):
        trainer_page.go_to_premium_page()
        premium_page = PremiumPage(trainer_page.driver)
        premium_page.should_be_loaded()


@allure.feature("Ачивки")
class TestAchievements:
    @allure.title("Проверка активности ачивки 'Начало большого пути'")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_beginning_achievement_active(self, trainer_page):
        trainer_page.check_beginning_achievement_active()


@allure.feature("Премиум")
class TestPremium:
    @allure.title("Успешная покупка премиума")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.usefixtures("ensure_no_premium")
    def test_buy_premium(self, premium_page):
        premium_page.set_days(VALID_CARD["days"])
        premium_page.click_buy_premium()

        payment_page = PaymentPage(premium_page.driver)
        payment_page.should_be_loaded()
        payment_page.fill_card_data(VALID_CARD)
        payment_page.click_pay()

        page_3ds = Payment3DSPage(payment_page.driver)
        page_3ds.should_be_loaded()
        page_3ds.enter_secure_code(VALID_CARD["secure_code"])
        page_3ds.confirm_3ds()

        success_page = PaymentSuccessPage(page_3ds.driver)
        success_page.should_be_loaded()
        success_page.back_to_shop()

        final_premium = PremiumPage(success_page.driver)
        final_premium.assert_premium_activated_message()
        final_premium.click_ok_and_return_to_main()

    @allure.title("Отмена премиума")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.usefixtures("ensure_premium")
    def test_cancel_premium(self, premium_page):
        premium_page.assert_premium_active()
        premium_page.click_cancel_premium()
        premium_page.confirm_cancel()
        premium_page.assert_cancelled_message()
