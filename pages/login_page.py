import re

import allure
from playwright.sync_api import Page, expect
from config import BASE_URL


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_test_id("username")
        self.password = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-buttonWRONG")
        self.error_msg = page.get_by_test_id("error")

    @allure.step("Navigate to login page")
    def goto(self):
        self.page.goto(BASE_URL)

    @allure.step("login with username '{username}'")
    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    @allure.step("Validate presence of error message '{error_text}'")
    def validate_presence_of_error_message(self, error_text: str):
        expect(self.error_msg).to_have_text(re.compile(error_text))

