import allure
from playwright.sync_api import Page, expect
from config import BASE_URL


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.products_name = page.get_by_test_id("inventory-item-name")
        self.products_price = page.get_by_test_id("inventory-item-price")
        self.add_to_cart_button = page.get_by_test_id("add-to-cart-sauce-labs-backpack")

    @allure.step("Validate landing on inventory page")
    def validate_landing_on_inventory_page(self):
        expect(self.page).to_have_url(BASE_URL + "inventory.html")

    @allure.step("Validate product details are visible")
    def validate_product_details_are_visible(self):
        expect(self.products_name).to_have_count(6)
        for name in self.products_name.all():
            expect(name).to_be_visible()

        expect(self.products_price).to_have_count(6)
        for price in self.products_price.all():
            expect(price).to_be_visible()

        expect(self.add_to_cart_button).to_be_enabled()
