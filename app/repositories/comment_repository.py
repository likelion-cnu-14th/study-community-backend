from sqlalchemy.orm import Session

from ..models import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, comment_id: str) -> Comment | None:
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def save(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
        self.db.commit()
