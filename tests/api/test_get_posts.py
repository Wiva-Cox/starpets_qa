import pytest
from api.api_posts.models.post import PostModel

pytestmark = pytest.mark.api


def test_get_post_by_id_success(api_client):

    test_post_id = 1

    response = api_client.get_post_by_id(post_id=test_post_id)

    assert response.status_code == 200, f"Ожидается статус код 200, получили {response.status_code}"
    post = PostModel(**response.json())
    assert post.id == test_post_id, f"В ответе пост id={post.id}, а был запрошен id={test_post_id}"


def test_get_post_not_exists(api_client):

    test_post_id = 9999

    response = api_client.get_post_by_id(post_id=test_post_id)

    assert response.status_code == 404, f"Ожидается статус код 404, получили {response.status_code}"
