"""
exif_to_excel.py

목적:
- 장면(scene)별로 분류된 사진 폴더를 순회하며
- 사진의 EXIF 메타데이터에서 ISO와 셔터속도를 자동 추출
- 수치 분석이 가능하도록 엑셀 파일로 데이터셋 생성

이 스크립트는
전문가 설정값(Expert Reference)을 만들기 위한
원천(raw) 데이터셋 생성 단계에 해당한다.
"""

import exifread
import os
import pandas as pd

# 장면별 폴더가 들어 있는 최상위 디렉토리
# 예: photos/food, photos/night, photos/landscape ...
PHOTO_DIR = "photos"

# 추출한 데이터를 누적할 리스트
rows = []

def frac_to_float(frac):
    """
    EXIF의 ExposureTime은 보통 분수 형태로 저장됨 (예: 1/30).
    이를 초 단위(float)로 변환하여
    이후 평균, 범위 등의 수치 분석이 가능하도록 한다.
    """
    try:
        # exifread Fraction 객체 처리
        return float(frac.num) / float(frac.den)
    except:
        try:
            # 문자열 형태("1/30")로 들어오는 경우 처리
            num, den = str(frac).split("/")
            return float(num) / float(den)
        except:
            return None

# 장면별 폴더 순회
for scene in os.listdir(PHOTO_DIR):
    scene_path = os.path.join(PHOTO_DIR, scene)

    # 파일이 아니라 디렉토리(장면 폴더)만 처리
    if not os.path.isdir(scene_path):
        continue

    # 장면 폴더 안의 이미지 파일 순회
    for file in os.listdir(scene_path):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(scene_path, file)

        # EXIF 메타데이터 로드
        with open(path, "rb") as f:
            tags = exifread.process_file(f, details=False)

        # ISO 감도 추출
        iso = tags.get("EXIF ISOSpeedRatings")

        # 셔터속도(노출 시간) 추출
        shutter_tag = tags.get("EXIF ExposureTime")

        # 셔터속도를 초 단위(float)로 변환
        shutter_sec = frac_to_float(shutter_tag)

        # 한 장의 사진 정보를 dict로 저장
        rows.append({
            "scene": scene,                         # 장면 라벨
            "file": file,                           # 파일명
            "ISO": int(str(iso)) if iso else None,  # ISO 값
            "Shutter_sec": shutter_sec              # 초 단위 셔터속도
        })

# 누적된 데이터를 DataFrame으로 변환
df = pd.DataFrame(rows)

# 엑셀 파일로 저장 (데이터셋 결과물)
df.to_excel("result.xlsx", index=False)

print("result.xlsx 생성 완료")
