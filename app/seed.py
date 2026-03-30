from datetime import datetime, timezone

from .database import SessionLocal
from .models import Post, Comment


def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(Post).count() > 0:
            return

        posts_data = [
            {
                "id": "1",
                "title": "커뮤니티에 오신 것을 환영합니다!",
                "content": "안녕하세요! 이곳은 자유롭게 소통하는 커뮤니티입니다. 궁금한 점이나 나누고 싶은 이야기를 자유롭게 작성해주세요.",
                "author": "관리자",
                "created_at": datetime(2026, 3, 20, 9, 0, tzinfo=timezone.utc),
                "likes": 5,
                "comments": [
                    {"id": "c1", "content": "반갑습니다! 잘 부탁드려요 😊", "author": "수빈", "created_at": datetime(2026, 3, 20, 10, 30, tzinfo=timezone.utc)},
                    {"id": "c2", "content": "커뮤니티 오픈 축하해요!", "author": "민준", "created_at": datetime(2026, 3, 20, 11, 15, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": "2",
                "title": "Next.js 공부하는 분 계신가요?",
                "content": "요즘 Next.js App Router를 공부하고 있는데, 같이 스터디하실 분 있으면 댓글 남겨주세요! 매주 토요일 오후에 온라인으로 진행하려고 합니다.",
                "author": "지원",
                "created_at": datetime(2026, 3, 21, 14, 20, tzinfo=timezone.utc),
                "likes": 12,
                "comments": [
                    {"id": "c3", "content": "저도 관심 있어요! 참여하고 싶습니다.", "author": "하은", "created_at": datetime(2026, 3, 21, 15, 0, tzinfo=timezone.utc)},
                    {"id": "c4", "content": "토요일 오후 몇 시에 하나요?", "author": "서준", "created_at": datetime(2026, 3, 21, 16, 45, tzinfo=timezone.utc)},
                    {"id": "c5", "content": "저도 끼워주세요~", "author": "수빈", "created_at": datetime(2026, 3, 22, 9, 10, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": "3",
                "title": "오늘 점심 뭐 먹을까요",
                "content": "학교 앞에 새로 생긴 돈까스 집 가본 사람 있나요? 맛있다고 해서 가보려는데 후기 궁금합니다!",
                "author": "민준",
                "created_at": datetime(2026, 3, 22, 11, 30, tzinfo=timezone.utc),
                "likes": 3,
                "comments": [
                    {"id": "c6", "content": "거기 치즈돈까스 진짜 맛있어요 강추!", "author": "지원", "created_at": datetime(2026, 3, 22, 11, 50, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": "4",
                "title": "React useState 질문이요",
                "content": "useState로 상태를 변경했는데 바로 console.log를 찍으면 이전 값이 나와요. 왜 그런 건가요? 비동기인가요?",
                "author": "하은",
                "created_at": datetime(2026, 3, 23, 16, 0, tzinfo=timezone.utc),
                "likes": 8,
                "comments": [
                    {"id": "c7", "content": "맞아요! setState는 비동기로 동작해서, 다음 렌더링에서 반영돼요. useEffect로 변경된 값을 확인할 수 있어요.", "author": "서준", "created_at": datetime(2026, 3, 23, 16, 30, tzinfo=timezone.utc)},
                    {"id": "c8", "content": "저도 처음에 이거 때문에 엄청 헤맸어요 ㅋㅋ", "author": "민준", "created_at": datetime(2026, 3, 23, 17, 0, tzinfo=timezone.utc)},
                ],
            },
            {
                "id": "5",
                "title": "TypeScript 처음 쓰는데 어렵네요",
                "content": "JavaScript만 쓰다가 TypeScript 처음 써보는데 타입 에러가 너무 많이 뜹니다... 익숙해지면 편해지나요?",
                "author": "서준",
                "created_at": datetime(2026, 3, 24, 10, 0, tzinfo=timezone.utc),
                "likes": 15,
                "comments": [],
            },
        ]

        for post_data in posts_data:
            comments_data = post_data.pop("comments")
            post = Post(**post_data)
            db.add(post)
            db.flush()

            for comment_data in comments_data:
                comment = Comment(**comment_data, post_id=post.id)
                db.add(comment)

        db.commit()
    finally:
        db.close()
