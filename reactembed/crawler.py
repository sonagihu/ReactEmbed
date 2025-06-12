import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import Set

BASE_URL = "https://ko.react.dev/reference/react"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
BASE_DOMAIN = urlparse(BASE_URL).netloc

os.makedirs(DATA_DIR, exist_ok=True)

def get_soup(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def is_valid_url(url: str) -> bool:
    """URL이 크롤링 대상인지 확인"""
    parsed = urlparse(url)
    return (
        parsed.netloc == BASE_DOMAIN and
        parsed.path.startswith("/reference/react/") and
        not parsed.fragment  # 같은 페이지의 다른 섹션은 제외
    )

def get_doc_links(url: str, visited: Set[str]) -> Set[str]:
    """재귀적으로 문서 링크를 수집"""
    if url in visited:
        return set()
    
    visited.add(url)
    soup = get_soup(url)
    links = set()
    
    # 모든 링크 수집
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(url, href)
        
        if is_valid_url(full_url) and full_url not in visited:
            links.add(full_url)
            # 재귀적으로 하위 문서 링크 수집
            sub_links = get_doc_links(full_url, visited)
            links.update(sub_links)
    
    return links

def sanitize_filename(filename):
    # 특수문자 제거 및 공백을 언더스코어로 변경
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_')
    # 연속된 언더스코어를 하나로 변경
    filename = re.sub(r'_+', '_', filename)
    # 파일명이 비어있거나 .으로 시작하는 경우 처리
    if not filename or filename.startswith('.'):
        filename = 'untitled'
    return filename

def process_code_blocks(soup):
    """code 태그를 마크다운 코드 블록으로 변환"""
    for code in soup.find_all('code'):
        # dir="ltr" 속성을 가진 code 태그는 건너뛰기
        if code.get('dir') == 'ltr':
            continue
            
        # 코드 블록의 언어를 결정 (class 속성에서 추출)
        lang = ''
        if code.get('class'):
            for cls in code.get('class'):
                if cls.startswith('language-'):
                    lang = cls.replace('language-', '')
                    break
        
        # 코드 내용을 마크다운 형식으로 변환
        code_content = code.get_text()
        code_md = f"\n```{lang}\n{code_content}\n```\n"
        
        # code 태그를 마크다운 형식으로 교체
        code.replace_with(BeautifulSoup(code_md, 'html.parser'))

def save_markdown(url):
    soup = get_soup(url)
    
    # code 태그 처리
    process_code_blocks(soup)
    
    # 문서 제목 추출
    title = soup.find('h1')
    title_text = title.text.strip() if title else "untitled"
    
    # URL에서 마지막 부분을 파일명으로 사용
    url_path = url.split('/')[-1]
    if not url_path:
        url_path = "index"
    
    # 파일명 생성
    filename = sanitize_filename(f"{url_path}_{title_text}") + ".md"
    filepath = os.path.join(DATA_DIR, filename)
    
    # 본문 내용 추출 (main 태그 기준)
    main = soup.find('main')
    content = main.get_text("\n", strip=True) if main else ""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title_text}\n\n")
        f.write(f"URL: {url}\n\n")
        f.write(content)
    print(f"Saved: {filepath}")

def main():
    visited = set()
    links = get_doc_links(BASE_URL, visited)
    print(f"Found {len(links)} docs.")
    for url in links:
        save_markdown(url)

if __name__ == "__main__":
    main() 