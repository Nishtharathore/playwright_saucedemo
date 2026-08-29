import re
from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_name = page.get_by_test_id("product-name")
        self.empty_state_message = page.get_by_test_id("no-results")
        self.skeleton_loader = page.locator(".skeleton")
        self.products_price = page.get_by_test_id("product-price")

    def goto(self):
        self.page.goto("https://practicesoftwaretesting.com/")

    def validate_empty_state_visible(self):
        expect(self.empty_state_message).to_have_text(re.compile("There are no products found"))

    def validate_skeleton_is_visible(self):
        expect(self.skeleton_loader).to_be_visible()