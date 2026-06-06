import requests
from api.api_posts.models.post import PostModel


class PostsClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def create_post(self, payload: dict, headers: dict | None = None, **kwargs) -> requests.Response:

        response = self.session.post(
            f"{self.base_url}/posts",
            json=payload,
            headers=headers,
            **kwargs
        )
        if response.status_code >= 500:
            raise Exception(f"Server Error {response.status_code}: {response.text}")

        elif response.status_code == 201:
            PostModel(**response.json())

        return response


    def get_post_by_id(self, post_id, headers: dict | None = None, **kwargs) -> requests.Response:
        response =  self.session.get(
            f"{self.base_url}/posts/{post_id}",
            headers=headers,
            **kwargs
        )
        if response.status_code >= 500:
            raise Exception(f"Server Error {response.status_code}: {response.text}")

        elif response.status_code == 200:
            PostModel(**response.json())

        return response

