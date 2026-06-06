import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_buy_and_withdraw_item(page, catalog_page):
    """
    E2E: пользователь находит товар в каталоге, оплачивает его через модальное окно
    и получает кнопку «Вывести» после подтверждения сервера по WebSocket.
    """
    # Перехватываем WS-соединение до навигации —
    # соединение открывается при загрузке страницы, важно не пропустить handshake
    with page.expect_websocket() as ws_info:
        catalog_page.navigate()
        catalog_page.wait_for_catalog_load()

    ws = ws_info.value

    # Убеждаемся, что кнопка «Купить» видна на карточке товара
    catalog_page.wait_for_buy_button_visible()

    # Нажимаем «Купить» — на той же странице открывается модальное окно оплаты
    catalog_page.click_buy_button()

    # ПЛАТЁЖ: здесь пользователь проходит оплату в модальном окне.
    # WS-соединение остаётся активным — страница не перезагружается.

    # Ждём от сервера WS-фрейм с подтверждением оплаты — без sleep(), до 60 секунд.
    # Playwright сам poll'ит очередь событий, пока predicate не вернёт True.
    ws.wait_for_event(
        "framereceived",
        predicate=lambda frame: "payment_confirmed" in frame.body,
        timeout=60_000,
    )

    # Сервер подтвердил оплату — фронт отображает кнопку «Вывести» на карточке товара
    expect(catalog_page.withdraw_button).to_be_visible(timeout=10_000)

    # Убеждаемся, что кнопка активна, и нажимаем её
    expect(catalog_page.withdraw_button).to_be_enabled()
    catalog_page.withdraw_button.click()

    # После нажатия появляется модалка с подтверждением — проверяем текст
    expect(catalog_page.success_modal).to_be_visible(timeout=5_000)
    expect(catalog_page.success_modal).to_contain_text("Успешный вывод товара")