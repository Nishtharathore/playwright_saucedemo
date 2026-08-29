import allure
from playwright.sync_api import Page, expect


class MyAccountPage:
    def __init__(self, page: Page):
        self.page = page
        self.home_button = page.get_by_test_id("nav-home")

    @allure.step("Click on home button")
    def click_on_home_button(self):
        self.home_button.click()


