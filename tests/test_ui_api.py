import re
from playwright.sync_api import Page, expect


def test_ui_login_then_api_call(page: Page):

    page.goto("https://practicesoftwaretesting.com/auth/login")
    # ... perform real login through UI ...
    page.get_by_test_id("email").fill("customer@practicesoftwaretesting.com")  # confirm actual placeholder/locator
    page.get_by_test_id("password").fill("welcome01")  # confirm actual credentials from the site
    page.get_by_test_id("login-submit").click()  # confirm actual button text

    # Step 2: wait for login to complete — confirm on a page that only shows post-login
    expect(page).to_have_url(re.compile("account"))

    # Token lives in localStorage, not cookies — extract it manually
    token = page.evaluate("() => window.localStorage.getItem('auth-token')")  # adjust key name to actual one used

    # Now attach it manually, since page.request won't pick it up automatically
    response = page.request.get(
        "https://api.practicesoftwaretesting.com/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.ok