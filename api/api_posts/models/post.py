from pydantic import BaseModel, ConfigDict


class PostModel(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    title: str
    body: str
    userId: int
