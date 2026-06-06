import pytest
from playwright.sync_api import sync_playwright

from config.settings import settings


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def api_client():
    from api.api_posts.posts_client import PostsClient
    return PostsClient(base_url=settings.base_api_url)


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser_type = getattr(p, settings.browser)
        browser = browser_type.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo,
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance, request):
    context = browser_instance.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
    )
    page = context.new_page()
    yield page
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        page.screenshot(path=f"reports/screenshots/{request.node.name}.png")
    context.close()


@pytest.fixture
def catalog_page(page):
    from pages.catalog_page.catalog_page import CatalogPage
    return CatalogPage(page)
