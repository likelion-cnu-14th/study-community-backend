from sqlalchemy.orm import Session

from ..models import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> list[Post]:
        return self.db.query(Post).order_by(Post.created_at.desc()).all()

    def find_by_id(self, post_id: str) -> Post | None:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def save(self, post: Post) -> Post:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()
