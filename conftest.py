import glob
import os
import time
import allure
import pytest
from playwright.sync_api import Playwright

@pytest.fixture(scope="session", autouse=True)
def set_test_id_attribute(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    # attach the report to the test item so fixtures can check it later
    setattr(item, f"rep_{rep.when}", rep)


GITHUB_USERNAME = "Nishtharathore"
REPO_NAME = "playwright_saucedemo"
PAGES_BASE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"


@pytest.fixture(autouse=True)
def attach_trace_to_allure(request):
    start_time = time.time()
    yield

    test_failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False

    if test_failed:
        # find any trace.zip created during/after this test, rather than guessing the folder name
        candidates = glob.glob("test-results/**/trace.zip", recursive=True)
        recent_traces = [f for f in candidates if os.path.getmtime(f) >= start_time]

        if recent_traces:
            local_path = max(recent_traces, key=os.path.getmtime)  # the newest match

            # give it a clean, predictable public filename
            safe_name = request.node.name.replace("[", "-").replace("]", "")
            public_filename = f"trace-{safe_name}.zip"

            allure.attach.file(local_path, name="Trace file (download)", attachment_type=allure.attachment_type.ZIP)

            trace_public_url = f"{PAGES_BASE_URL}/traces/{public_filename}"
            viewer_link = f"https://trace.playwright.dev/?trace={trace_public_url}"
            allure.attach(
                f'<a href="{viewer_link}" target="_blank">Open Trace Viewer</a>',
                name="Trace Viewer (live)",
                attachment_type=allure.attachment_type.HTML
            )

            # stash the rename mapping so the CI copy step can use predictable names
            os.makedirs("test-results-renamed", exist_ok=True)
            import shutil
            shutil.copy(local_path, f"test-results-renamed/{public_filename}")
