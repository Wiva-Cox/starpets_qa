from playwright.sync_api import Page, expect
from pages.catalog_page.catalog_page_locators import CatalogPageLocators

from config.settings import settings


class CatalogPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_role(CatalogPageLocators.SEARCH_INPUT)
        self.product_cards = page.locator(CatalogPageLocators.PRODUCT_CARD)
        self.product_cards_fallback = page.locator(CatalogPageLocators.PRODUCT_CARD_FALLBACK)
        self.buy_button = page.get_by_role("button", name=CatalogPageLocators.BUY_RU_BTN)
        self.buy_button_en = page.get_by_role("button", name=CatalogPageLocators.BUY_EN_BTN)
        self.withdraw_button = page.locator(CatalogPageLocators.WITHDRAW_BTN)
        self.success_modal = page.locator(CatalogPageLocators.SUCCESS_MODAL)


    def navigate(self) -> None:
        self.page.goto(settings.base_ui_url + "/adopt-me")

    def wait_for_catalog_load(self) -> None:
        locator = self.product_cards
        try:
            expect(locator).not_to_have_count(0, timeout=10000)
        except Exception:
            locator = self.product_cards_fallback
            expect(locator).not_to_have_count(0, timeout=10000)
        self._active_cards = locator

    def get_card_count(self) -> int:
        locator = getattr(self, "_active_cards", self.product_cards)
        return locator.count()

    def open_first_card(self) -> None:
        locator = getattr(self, "_active_cards", self.product_cards)
        locator.first.click()

    def wait_for_buy_button_visible(self) -> None:
        try:
            expect(self.buy_button_en).to_be_visible(timeout=10000)
        except Exception:
            expect(self.buy_button).to_be_visible(timeout=10000)

    def click_buy_button(self) -> None:
        try:
            self.buy_button_en.first.click()
        except Exception:
            self.buy_button.first.click()
