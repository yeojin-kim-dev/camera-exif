"""
check_exif.py

목적:
- 사진 파일에 EXIF 메타데이터가 실제로 존재하는지 확인
- ISO, 셔터속도(ExposureTime)를 정상적으로 읽을 수 있는지 검증

이 파일은
'사진 파일 내부 설정값을 코드로 추출할 수 있는가?'에 대한
기술적 가능성(PoC)을 확인하기 위한 테스트 코드이다.
"""

import exifread
import os

# EXIF를 확인할 사진들이 들어 있는 디렉토리
PHOTO_DIR = "photos"

# photos 폴더 하위의 모든 파일을 재귀적으로 순회
for root, _, files in os.walk(PHOTO_DIR):
    for file in files:
        # 이미지 파일만 처리
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(root, file)

        # 현재 처리 중인 파일 이름 출력 (확인용)
        print("======", file, "======")

        # 바이너리 모드로 파일을 열어 EXIF 메타데이터 읽기
        with open(path, "rb") as f:
            # details=False → 핵심 EXIF 태그만 로드
            tags = exifread.process_file(f, details=False)

        # ISO 감도 추출
        iso = tags.get("EXIF ISOSpeedRatings")

        # 셔터속도(노출 시간) 추출
        # 보통 분수 형태 (예: 1/30)
        shutter = tags.get("EXIF ExposureTime")

        # 추출 결과 출력
        print("ISO:", iso)
        print("Shutter(ExposureTime):", shutter)
