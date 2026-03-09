---
description: Translate a new Korean weekly lab folder to English automatically
---

# 한국어 → 영어 자동 번역 워크플로우 (KR → EN Translation Workflow)

이 워크플로우는 `ko/weekN/` 폴더에 새로운 한국어 실습 콘텐츠가 추가되었을 때, 자동으로 `en/weekN/` 영어 버전을 생성합니다.

## 사용법 (Usage)
채팅에서 아래와 같이 입력:
```
/translate-new-week
```
또는 자유롭게:
```
"ko/week3 폴더의 내용을 영어로 번역해서 en/week3에 만들어줘"
```

---

## 워크플로우 단계 (Steps)

### 1. 대상 주차 확인
- `ko/` 폴더 내에서 가장 최근 추가된 weekN 폴더를 식별
- 해당 폴더가 `en/` 에 아직 존재하지 않는지 확인

### 2. 영어 폴더 생성
- `en/weekN/` 디렉터리 생성

// turbo
### 3. 마크다운 문서 번역
- `ko/weekN/` 내 모든 `.md` 파일을 영어로 번역
- 파일명도 영문으로 변경 (예: `03주차_실습_XXX.md` → `week03_lab_XXX.md`)
- 학술 용어는 정확한 영문 표준 표현 사용
- 내부 링크 경로 업데이트

### 4. Python 스크립트 번역
- `ko/weekN/` 내 모든 `.py` 파일의 한국어 주석을 영어로 번역
- 코드 로직은 변경하지 않음 (주석, 문자열만 번역)
- 파일명은 동일하게 유지

// turbo
### 5. 이미지 및 데이터 파일 복사
- `ko/weekN/` 내 모든 이미지 파일 (`.png`, `.jpg`, `.bmp` 등)을 `en/weekN/`로 복사
- 기타 데이터 파일 (`.csv`, `.json` 등)도 복사
```bash
cp ko/weekN/*.png en/weekN/
cp ko/weekN/*.jpg en/weekN/ 2>/dev/null
cp ko/weekN/*.csv en/weekN/ 2>/dev/null
```

### 6. README 업데이트
아래 3개의 README 파일에 새 주차 항목을 추가:

#### 6-1. 최상위 `README.md`
- 한국어 테이블과 영어 테이블 모두에 새 주차 행 추가

#### 6-2. `ko/README.md`
- `📂 주차별 실습 내용 요약` 섹션에 새 주차 항목 추가
- 해당 주차 상세 튜토리얼 링크 포함

#### 6-3. `en/README.md`
- `📂 Weekly Lab Summary` 섹션에 새 주차 항목 추가
- 해당 주차 상세 영문 튜토리얼 링크 포함

### 7. 검증
- `en/weekN/` 폴더 내 파일 목록 확인
- 번역된 `.md` 파일의 내부 링크가 올바른지 확인
- Python 스크립트의 이미지 경로가 올바른지 확인

---

## 주의사항
- 번역 시 학술 용어의 정확성을 최우선으로 합니다
- 코드 로직은 절대 변경하지 않습니다 (주석과 print 문자열만 번역)
- 이미지 파일은 언어 무관이므로 그대로 복사합니다
- `CHATME.md` 같은 대화 기록 파일은 번역하지 않습니다
