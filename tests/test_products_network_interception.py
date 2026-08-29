import time
import pytest
from playwright.sync_api import Page, expect
from pages import tool_shop_page_objects

PRODUCTS_API_PATTERN = "**/products*"


class TestProductsNetworkMocking:
    """
    KNOWN ISSUE: Toolshop shows no error state on API failures — the skeleton
    loader remains visible indefinitely instead of surfacing an error to the user.
    This test documents current (undesirable) behavior. If Toolshop ever adds
    proper error handling, Below tests should be updated to assert the error message.
    """
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.products_page = tool_shop_page_objects.ProductsPage(page)


    def test_empty_products_state(self):
        self.page.route(
            PRODUCTS_API_PATTERN,
            lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body='{"current_page":1,"data":[],"from":null,"last_page":1,"per_page":9,"to":null,"total":0}'
            )
        )
        self.products_page.goto()
        self.products_page.validate_empty_state_visible()

    def test_products_api_error(self):
        self.page.route(
            PRODUCTS_API_PATTERN,
            lambda route: route.fulfill(status=500)
        )
        self.products_page.goto()
        self.products_page.validate_skeleton_is_visible()

    def test_products_malformed_data_type(self):
        # data is a string instead of an array
        malformed_body = '{"current_page":1,"data":"unexpected string","from":null,"last_page":1,"per_page":9,"to":null,"total":0}'
        self.page.route(
            PRODUCTS_API_PATTERN,
            lambda route: route.fulfill(status=200, content_type="application/json", body=malformed_body)
        )
        self.products_page.goto()
        self.products_page.validate_skeleton_is_visible()

    def test_products_missing_required_field(self):
        # price field removed from product object
        malformed_body = '{"current_page":1,"data":[{"id":"01M16BZ8CEP9BEVQP7D71Z614J","name":"Combination Pliers","description":"...","is_location_offer":false,"is_rental":false,"co2_rating":"D","in_stock":true,"is_eco_friendly":false,"product_image":{},"category":{},"brand":{}}],"from":1,"last_page":1,"per_page":9,"to":1,"total":1}'
        self.page.route(
            PRODUCTS_API_PATTERN,
            lambda route: route.fulfill(status=200, content_type="application/json", body=malformed_body)
        )
        self.products_page.goto()
        self.products_page.validate_skeleton_is_visible()

    def test_products_wrong_shape_response(self):
        self.page.route(
            PRODUCTS_API_PATTERN,
            lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body="[]"
            )
        )
        self.products_page.goto()
        self.products_page.validate_skeleton_is_visible()

    def test_products_slow_response(self):
        def slow_handler(route):
            time.sleep(3)
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"current_page":1,"data":[{"id":"01M16BZ8CEP9BEVQP7D71Z614J","name":"Combination Pliers","description":"...","price":14.15,"is_location_offer":false,"is_rental":false,"co2_rating":"D","in_stock":true,"is_eco_friendly":false,"product_image":{"id":"01M16BZ8BQC9D2K80303KBC6KQ","by_name":"Helinton Fantin","by_url":"https://unsplash.com/@fantin","source_name":"Unsplash","source_url":"https://unsplash.com/photos/W8BNwvOvW4M","file_name":"pliers01.avif","title":"Combination pliers"},"category":{"id":"01M16BZ8B1HE798KFAC6C1CPS2","name":"Pliers","slug":"pliers"},"brand":{"id":"01M16BZ8007HVSCF2NS75DX6Q1","name":"ForgeFlex Tools"}}],"from":1,"last_page":1,"per_page":9,"to":1,"total":1}'
            )

        self.page.route(PRODUCTS_API_PATTERN, slow_handler)
        self.products_page.goto()
        # after the delay resolves, products should actually render
        expect(self.products_page.product_name.first).to_be_visible(timeout=5000)