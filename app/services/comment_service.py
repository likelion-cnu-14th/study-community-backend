from datetime import datetime, timezone

from fastapi import HTTPException

from ..models import Comment
from ..schemas import CommentCreate
from ..repositories import PostRepository, CommentRepository


class CommentService:
    def __init__(self, post_repo: PostRepository, comment_repo: CommentRepository):
        self.post_repo = post_repo
        self.comment_repo = comment_repo

    def create_comment(self, post_id: str, data: CommentCreate) -> Comment:
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        comment = Comment(
            id=str(int(datetime.now(timezone.utc).timestamp() * 1000)),
            content=data.content,
            author=data.author,
            post_id=post_id,
        )
        return self.comment_repo.save(comment)

    def delete_comment(self, comment_id: str) -> None:
        comment = self.comment_repo.find_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
        self.comment_repo.delete(comment)
