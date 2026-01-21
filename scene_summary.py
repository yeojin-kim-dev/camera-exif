"""
scene_summary.py

장면(scene)별로 분류된 촬영 데이터(result.xlsx)를 기반으로
ISO와 셔터속도의 분포를 요약하여
경향 분석용 통계 테이블을 생성하는 스크립트.

※ 샘플 수가 적기 때문에 본 결과는
정답값 도출이 아닌 경향 확인용 분석을 목적으로 함.
"""

import pandas as pd

# 원본 데이터 로드 (사진별 EXIF 추출 결과)
df = pd.read_excel("result.xlsx")

# ISO, 셔터속도를 숫자형으로 변환
# (엑셀/EXIF 처리 과정에서 문자열로 들어오는 경우 대비)
df["ISO"] = pd.to_numeric(df["ISO"], errors="coerce")
df["Shutter_sec"] = pd.to_numeric(df["Shutter_sec"], errors="coerce")

# 장면(scene)별 요약 통계 생성
summary = (
    df.groupby("scene")
      .agg(
          n=("ISO", "count"),
          ISO_min=("ISO", "min"),
          ISO_mean=("ISO", "mean"),
          ISO_max=("ISO", "max"),
          Shutter_min=("Shutter_sec", "min"),
          Shutter_mean=("Shutter_sec", "mean"),
          Shutter_max=("Shutter_sec", "max"),
      )
      .reset_index()
)

# 보기 편하도록 소수점 자리 정리
summary["ISO_mean"] = summary["ISO_mean"].round(1)
summary["Shutter_min"] = summary["Shutter_min"].round(4)
summary["Shutter_mean"] = summary["Shutter_mean"].round(4)
summary["Shutter_max"] = summary["Shutter_max"].round(4)

# 장면별 요약 결과를 별도 파일로 저장
# (원본 데이터(result.xlsx)는 수정하지 않음)
summary.to_excel("result_summary.xlsx", index=False)

print("result_summary.xlsx 생성 완료")
print(summary)
