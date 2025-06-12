import os
import requests
import easyocr
import numpy
from PIL import Image
from io import BytesIO
import logging
import argparse

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageParser:
    def __init__(self, languages=['ko', 'en']):
        """
        이미지 파서 초기화
        :param languages: 인식할 언어 리스트 (기본값: 한국어, 영어)
        """
        self.reader = easyocr.Reader(languages)
        logger.info(f"EasyOCR initialized with languages: {languages}")

    def download_image(self, image_path):
        """
        URL 또는 로컬 파일 경로에서 이미지 로드
        :param image_path: 이미지 URL 또는 로컬 파일 경로
        :return: PIL Image 객체
        """
        try:
            if image_path.startswith(('http://', 'https://')):
                # URL인 경우
                response = requests.get(image_path)
                response.raise_for_status()
                return Image.open(BytesIO(response.content))
            else:
                # 로컬 파일인 경우
                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {image_path}")
                return Image.open(image_path)
        except Exception as e:
            logger.error(f"이미지 로드 중 오류 발생 ({image_path}): {str(e)}")
            raise

    def extract_text(self, image_url):
        """
        이미지에서 텍스트 추출
        :param image_url: 이미지 URL
        :return: 추출된 텍스트 리스트
        """
        try:
            # 이미지 다운로드
            image = self.download_image(image_url)
            
            # 텍스트 추출
            results = self.reader.readtext(numpy.array(image))
            
            # 결과 정리
            extracted_texts = []
            for (bbox, text, prob) in results:
                if prob > 0.5:  # 신뢰도가 50% 이상인 텍스트만 추출
                    extracted_texts.append({
                        'text': text,
                        'confidence': prob,
                        'position': bbox
                    })
            
            logger.info(f"Successfully extracted {len(extracted_texts)} texts from image")
            return extracted_texts
            
        except Exception as e:
            logger.error(f"Error extracting text from {image_url}: {str(e)}")
            raise

def main():
    # 커맨드 라인 인자 파싱
    parser = argparse.ArgumentParser(description='이미지에서 텍스트를 추출합니다.')
    parser.add_argument('image_url', type=str, help='텍스트를 추출할 이미지의 URL')
    args = parser.parse_args()

    # 이미지 파서 초기화
    image_parser = ImageParser()
    
    try:
        # 이미지에서 텍스트 추출
        results = image_parser.extract_text(args.image_url)
        
        # 결과 출력
        print("\n추출된 텍스트:")
        for idx, result in enumerate(results, 1):
            print(f"\n{idx}. 텍스트: {result['text']}")
            print(f"   신뢰도: {result['confidence']:.2f}")
            print(f"   위치: {result['position']}")
            
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    main() 