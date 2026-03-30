from datetime import datetime, timezone

from fastapi import HTTPException

from ..models import Post
from ..schemas import PostCreate
from ..repositories import PostRepository


class PostService:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def get_all_posts(self) -> list[Post]:
        return self.post_repo.find_all()

    def get_post(self, post_id: str) -> Post:
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        return post

    def create_post(self, data: PostCreate) -> Post:
        post = Post(
            id=str(int(datetime.now(timezone.utc).timestamp() * 1000)),
            title=data.title,
            content=data.content,
            author=data.author,
        )
        return self.post_repo.save(post)

    def delete_post(self, post_id: str) -> None:
        post = self.get_post(post_id)
        self.post_repo.delete(post)

    def like_post(self, post_id: str) -> Post:
        post = self.get_post(post_id)
        post.likes += 1
        return self.post_repo.save(post)
