from selenium.webdriver.common.by import By
from data.test_trainer_data import TEST_TRAINER_ID


class TrainerPageLocators:
    trainer_card_id = (By.XPATH, f"//div[@class='header_card_trainer_id_num' and text()='{TEST_TRAINER_ID}']")
    trainer_id = (By.XPATH, f"//div[@class='copy_number_id' and text()='{TEST_TRAINER_ID}']")
    beginning_achievement = (By.ID, "beginning")
