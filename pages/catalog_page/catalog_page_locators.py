"""
Стратегия выбора локаторов:
1. Приоритет — data-testid атрибуты: не зависят от дизайна и текста
2. Fallback — семантические role-локаторы (get_by_role)
3. Последний вариант — CSS классы с wildcard (хрупкие, но лучше XPath)

На реальном проекте StarPets мы бы согласовали с разработчиками
добавление data-testid на все интерактивные элементы карточки товара.
"""

class CatalogPageLocators():
    SEARCH_INPUT = "searchbox"
    PRODUCT_CARD = '[data-testid="product-card"]'
    PRODUCT_CARD_FALLBACK = '.product-card, [class*="card"], [class*="item"]'
    BUY_RU_BTN = "Купить"
    BUY_EN_BTN = "Buy"
    WITHDRAW_BTN = '[data-testid="withdraw-button"]'
    SUCCESS_MODAL = '[data-testid="success-modal"]'