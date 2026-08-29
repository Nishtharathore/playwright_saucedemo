# Playwright Test Automation Framework (Python)

A Python + Playwright UI automation framework with a Page Object Model, network
interception/stubbing tests, parallel execution, trace-based debugging, and CI/CD
with Allure reporting. Built alongside my [Selenium UI Automation Framework](https://github.com/Nishtharathore/sauce_demo_test),
which made it possible to compare the two tools' architectures directly rather than
relying on documentation alone.

## Tech Stack

Playwright (Python) · pytest + pytest-playwright · pytest-xdist · Allure · GitHub Actions

## What's Covered

- **POM, no BasePage** — Playwright's auto-waiting (actionability checks) removes
  the need for Selenium-style `wait_and_click()`/`wait_and_fill()` wrappers.
- **Login flows** (SauceDemo) — valid, invalid, locked-out (parametrized).
- **Network stubbing** (`page.route()`) — SauceDemo has no real backend, so image
  loads are stubbed to `404` to confirm the page still renders correctly.
- **API stubbing suite** (Toolshop, real backend) — see finding below.
- **Auth mechanism check** — `APIRequestContext`'s automatic session-sharing
  only applies to cookie-based auth, not `localStorage` JWTs; token has to be
  extracted manually either way.
- **Parallel execution** (`pytest -n auto`), no shared-state issues.
- **Trace Viewer**, `--tracing retain-on-failure` — full timeline/DOM/network replay
  for failed tests only.
- **CI/CD** — GitHub Actions: install → run with tracing → upload trace artifact on
  failure (via `steps.<id>.outcome`, since `continue-on-error` masks `if: failure()`)
  → generate + publish Allure report to GitHub Pages.

## Finding: Toolshop has no client-side error handling for failed API responses

| Stubbed response | Result |
|---|---|
| Empty result (`data: []`) | ✅ Correct "no products found" |
| `500` error | 🐛 Stuck on skeleton loader, no error shown |
| Wrong data type / missing field / unparseable body / wrong shape | 🐛 Same |
| Delayed but valid response | ✅ Recovers correctly |

Every *failure* mode (transport, parse, shape) collapses into the same symptom —
indefinite skeleton loader, no user feedback — while legitimately empty or delayed
(but valid) responses are handled fine. Hard to catch without interception, since it
requires the real API to be in a broken state.

## Running Locally

```bash
pip install -r requirements.txt
playwright install --with-deps chromium

pytest tests/test_login.py -n auto                            # parallel
pytest tests/test_login.py --tracing retain-on-failure        # failed cases can be traced using trace viewer using command : playwright show-trace <path_of_zip_file>
pytest tests/test_login.py --alluredir=allure-results         # generating allure reports as well
allure serve allure-results)                                  # for viewing allure report
```