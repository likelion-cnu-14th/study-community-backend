from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import CommentCreate, CommentResponse
from ..repositories import PostRepository, CommentRepository
from ..services import CommentService

router = APIRouter(prefix="/api", tags=["comments"])


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(PostRepository(db), CommentRepository(db))


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    post_id: str,
    data: CommentCreate,
    service: CommentService = Depends(get_comment_service),
):
    comment = service.create_comment(post_id, data)
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        author=comment.author,
        createdAt=comment.created_at,
    )


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(
    comment_id: str,
    service: CommentService = Depends(get_comment_service),
):
    service.delete_comment(comment_id)
