# React Documentation Crawler

React 공식 문서를 크롤링하여 마크다운 파일로 저장하는 Python 프로젝트입니다.

## 기능

- ko.react.dev/reference/react 문서 크롤링
- 재귀적 문서 탐색
- 마크다운 형식으로 저장

## 설치 방법

```bash
# Poetry 설치 (아직 설치하지 않은 경우)
curl -sSL https://install.python-poetry.org | python3 -

# 의존성 설치
poetry install
```

## 사용 방법

```bash
poetry run python reactembed/crawler.py
```

## 프로젝트 구조

```
reactembed/
├── data/               # 크롤링된 마크다운 파일 저장
├── reactembed/         # 소스 코드
│   ├── __init__.py
│   └── crawler.py
├── pyproject.toml      # 프로젝트 설정
└── README.md
```

## 라이선스

MIT 