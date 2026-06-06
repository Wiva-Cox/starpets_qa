import uuid
import pytest
from api.api_posts.models.post import PostModel

pytestmark = pytest.mark.api


def test_create_post_success(api_client):
    payload = {"title": "Test Post", "body": "Test body", "userId": 1}

    response = api_client.create_post(payload)

    assert response.status_code == 201, f"Ожидается статус код 201, получили {response.status_code}"
    post = PostModel(**response.json())
    assert post.id > 0, "Id поста меньше 0"
    assert post.title == payload["title"], "title поста не соответствует отправленному"
    assert post.userId == payload["userId"], "userId поста не соответствует отправленному"


def test_create_post_empty_body(api_client):
    """
    ВАЖНО: jsonplaceholder.typicode.com не валидирует входные данные
    и возвращает 201 даже на пустой запрос. Это особенность mock-сервиса.

    Данный тест заведомо упадет из-за того, что приходит статус код 201
    и автоматически запускается валидация по модели с помощью Pydantic

    На реальном API StarPets ожидаемое поведение:
    - Статус 422 Unprocessable Entity
    - Тело ответа содержит список ошибок валидации по каждому полю
    - Пример: {"errors": [{"field": "title", "message": "required"}]}
    """
    payload = {}
    response = api_client.create_post(payload)

    assert response.status_code == 422, f"Ожидается статус код 422, получили {response.status_code}"


def test_create_post_invalid_data(api_client):
    """
    Данный тест заведомо упадет из-за того, что приходит статус код 201
    и автоматически запускается валидация по модели с помощью Pydantic

    На реальном API StarPets ожидаемое поведение:
    - Статус 422 Unprocessable Entity
    - Тело ответа содержит список ошибок валидации по каждому полю
    - Пример: {"errors": [{"field": "title", "message": "required"}]}
    """

    payload = {"title": 12345, "body": "body", "userId": "not_an_int"}

    response = api_client.create_post(payload)

    assert response.status_code == 422, f"Ожидается статус код 422, получили {response.status_code}"


def test_create_post_unauthorized(api_client):
    """
    ВАЖНО: jsonplaceholder не проверяет авторизацию.

    Данный тест заведомо упадет из-за того, что приходит статус код 201
    и автоматически запускается валидация по модели с помощью Pydantic

    На реальном API StarPets:
    - Без токена → 401 Unauthorized
    - С невалидным токеном → 401 Unauthorized
    - С токеном без прав → 403 Forbidden

    Реальный тест выглядел бы так:
    response = api_client.create_post(payload, headers={"Authorization": "Bearer bad_token"})
    assert response.status_code == 401
    assert response.json()["message"] == "Invalid or expired token"
    """
    payload = {"title": "Auth Test", "body": "body", "userId": 1}

    response = api_client.create_post(
        payload,
        headers={"Authorization": "Bearer invalid_token_12345"},
    )

    assert response.status_code == 401, f"Ожидается статус код 401, получили {response.status_code}"
    assert response.json()["message"] == "Invalid or expired token", "Сообщение об ошибке отсутствует или не соответствует ожидаемому"


def test_idempotency_key(api_client):
    """
    Эмуляция идемпотентности с X-Idempotency-Key.

    Как это работает на реальном бэкенде StarPets:

    1. Клиент генерирует уникальный UUID и отправляет его в заголовке
       X-Idempotency-Key при каждом запросе на создание заказа/покупки.

    2. Бэкенд при получении запроса проверяет в Redis/БД:
       - Ключ НЕ существует → выполнить операцию, сохранить результат с ключом (TTL ~24h)
       - Ключ СУЩЕСТВУЕТ → вернуть сохранённый ответ без повторного выполнения

    3. Что это защищает:
       - Двойное списание баланса при сетевых ретраях
       - Дублирование заказа при повторном клике пользователя
       - Race condition при параллельных запросах

    4. Что мы проверяем в реальном тесте StarPets:
       - Все 3 ответа возвращают одинаковый id созданного ресурса
       - В БД создана ровно 1 запись, а не 3
       - Второй и третий ответы идут быстрее (из кеша)

    На jsonplaceholder ключ игнорируется, поэтому мы проверяем только
    что заголовок корректно передаётся и сервис не возвращает ошибку.
    """
    key = str(uuid.uuid4())
    headers={"X-Idempotency-Key": key}
    payload = {"title": "Idempotency Test", "body": "body", "userId": 1}

    responses = [
        api_client.create_post_with_idempotency_key(payload, headers)
        for _ in range(3)
    ]

    assert all(r.status_code == 201 for r in responses)

    ids = [r.json().get("id") for r in responses]
    assert len(set(ids)) == 1, f"ID отличаются в разных запросах: {ids}"

    print(f"\nIdempotency key: {key}")
    print(f"Response IDs (jsonplaceholder returns same id for all): {ids}")
