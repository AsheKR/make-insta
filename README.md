# Instagram

## Requirements

### python version

`3.6.6`

### packages

`pip install -r requirements.txt`

### secrets

`"SECRET_KEY" : "<Django-Settings-SECRET_KEY>"`

## 모델

- POST
    - Author(USER)
    - Comments(COMMENT)
    - photo
    
- COMMENT
    - Author(USER)
    - Post(POST)
    - HashTag(HASHTAG)
    - content
    
- HashTag
    - tag_name
    
- User
    - img_profile
    - site
    - introduce

- PostLike(Intermediate Model)
    - Author(USER)
    - Post(POST)
    - created_at
    
## 화면

- 프로필
    - 내 게시물 목록
    - 내 팔로워 목록
    - 내 팔로잉 목록
    
- 로그인
- 포스트 피드
- 포스트 작성

## 기능

- 회원가입
- 로그인
- 포스트 작성/삭제
- 팔로우/언팔로우
- 포스트 좋아요 / 취소
- 포스트에 댓글 작성/수정/삭제
    - 댓글 작성 시 해시태그 추가
- 해시태그 검색
- 프로필 수정