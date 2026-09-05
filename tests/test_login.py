import pytest
from playwright.sync_api import Page
from pages import sauce_demo_page_objects

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.login_page = sauce_demo_page_objects.LoginPage(page)
        self.inventory_page = sauce_demo_page_objects.InventoryPage(page)

    def test_valid_login(self):
        self.login_page.goto()
        self.login_page.login("standard_user", "secret_sauce")
        self.inventory_page.validate_landing_on_inventory_page()


    # @pytest.mark.parametrize("username,password,expected_error", [
    #     ("standard_user", "wrong_password", "Username and password do not match"),
    #     ("locked_out_user", "secret_sauce", "locked out"),
    # ])
    # def test_invalid_login(self,username, password, expected_error):
    #     self.login_page.goto()
    #     self.login_page.login(username, password)
    #     self.login_page.validate_presence_of_error_message(expected_error)
    #
    # def test_inventory_image_fails_gracefully(self):
    #     self.login_page.goto()
    #     self.login_page.login("standard_user", "secret_sauce")
    #
    #     self.page.route("**/assets/**.jpg", lambda route: route.fulfill(status=404))
    #     self.page.reload()
    #
    #     self.inventory_page.validate_landing_on_inventory_page()
    #     self.inventory_page.validate_product_details_are_visible()
    #
