from datetime import datetime, timezone

from fastapi import HTTPException

from ..models import Post
from ..schemas import PostCreate
from ..repositories import PostRepository

_liked_posts: set[str] = set()


class PostService:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def get_all_posts(self) -> list[Post]:
        return self.post_repo.find_all()

    def get_post(self, post_id: str) -> Post:
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail={"error": "게시글을 찾을 수 없습니다."})
        return post

    def create_post(self, data: PostCreate) -> Post:
        if not data.title or not data.content:
            raise HTTPException(status_code=400, detail={"error": "제목과 내용은 필수입니다."})
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

    def toggle_like(self, post_id: str) -> Post:
        post = self.get_post(post_id)
        if post_id in _liked_posts:
            post.likes -= 1
            _liked_posts.discard(post_id)
        else:
            post.likes += 1
            _liked_posts.add(post_id)
        return self.post_repo.save(post)
