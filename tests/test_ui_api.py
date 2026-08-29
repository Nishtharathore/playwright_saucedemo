import re
from playwright.sync_api import Page, expect


def test_ui_login_then_api_call(page: Page):

    page.goto("https://practicesoftwaretesting.com/auth/login")
    page.get_by_test_id("email").fill("customer@practicesoftwaretesting.com")
    page.get_by_test_id("password").fill("welcome01")
    page.get_by_test_id("login-submit").click()

    expect(page).to_have_url(re.compile("account"))

    # Token lives in localStorage, not cookies — extract it manually
    token = page.evaluate("() => window.localStorage.getItem('auth-token')")

    response = page.request.get(
        "https://api.practicesoftwaretesting.com/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.ok