"""
etl/load_expert_data.py

엑셀로 정리된 전문가(레퍼런스) 데이터를 SQLite에 벌크 적재하는 스크립트.

- result.xlsx           -> expert_photos
- result_summary.xlsx   -> expert_scene_stats

주의:
- 엑셀(.xlsx)과 DB(.db)는 로컬 산출물이므로 깃허브에 올리지 않는다(.gitignore).
"""

import sqlite3
from pathlib import Path
import pandas as pd


# ====== 경로 설정 ======
DB_PATH = Path("db/app.db")
RAW_XLSX = Path("result.xlsx")
SUMMARY_XLSX = Path("result_summary.xlsx")


def load_expert_photos(conn: sqlite3.Connection) -> int:
    """
    result.xlsx -> expert_photos 적재
    엑셀 컬럼 기대값: scene, file, ISO, Shutter_sec
    """
    df = pd.read_excel(RAW_XLSX)

    # 엑셀 컬럼명을 DB 컬럼명에 맞게 변환
    df = df.rename(columns={
        "scene": "scene_type",
        "file": "file_name",
        "ISO": "iso",
        "Shutter_sec": "shutter_sec",
    })

    # 숫자형으로 변환(문자열로 들어왔을 때 대비)
    df["iso"] = pd.to_numeric(df["iso"], errors="coerce")
    df["shutter_sec"] = pd.to_numeric(df["shutter_sec"], errors="coerce")

    # 필요한 컬럼만 남김
    df = df[["scene_type", "file_name", "iso", "shutter_sec"]]

    rows = list(df.itertuples(index=False, name=None))

    conn.executemany(
        """
        INSERT INTO expert_photos (scene_type, file_name, iso, shutter_sec)
        VALUES (?, ?, ?, ?)
        """,
        rows
    )

    return len(rows)


def load_expert_scene_stats(conn: sqlite3.Connection) -> int:
    """
    result_summary.xlsx -> expert_scene_stats 적재
    엑셀 컬럼 기대값:
      scene, n, ISO_min, ISO_mean, ISO_max, Shutter_min, Shutter_mean, Shutter_max
    """
    df = pd.read_excel(SUMMARY_XLSX)

    # scene -> scene_type
    df = df.rename(columns={"scene": "scene_type"})

    # 숫자형 변환
    for col in ["n", "ISO_min", "ISO_mean", "ISO_max", "Shutter_min", "Shutter_mean", "Shutter_max"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 엑셀 컬럼명을 DB 컬럼명에 맞게 변환
    df = df.rename(columns={
        "ISO_min": "iso_min",
        "ISO_mean": "iso_mean",
        "ISO_max": "iso_max",
        "Shutter_min": "shutter_min",
        "Shutter_mean": "shutter_mean",
        "Shutter_max": "shutter_max",
    })

    df = df[[
        "scene_type",
        "n",
        "iso_min", "iso_mean", "iso_max",
        "shutter_min", "shutter_mean", "shutter_max"
    ]]

    rows = list(df.itertuples(index=False, name=None))

    conn.executemany(
        """
        INSERT INTO expert_scene_stats
        (scene_type, n, iso_min, iso_mean, iso_max, shutter_min, shutter_mean, shutter_max)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    return len(rows)


def main():
    # 파일 존재 체크
    if not DB_PATH.exists():
        raise FileNotFoundError(f"DB가 없습니다: {DB_PATH} (먼저 python etl/init_db.py 실행)")
    if not RAW_XLSX.exists():
        raise FileNotFoundError(f"엑셀 파일이 없습니다: {RAW_XLSX}")
    if not SUMMARY_XLSX.exists():
        raise FileNotFoundError(f"요약 엑셀 파일이 없습니다: {SUMMARY_XLSX}")

    with sqlite3.connect(DB_PATH) as conn:
        inserted_raw = load_expert_photos(conn)
        inserted_summary = load_expert_scene_stats(conn)
        conn.commit()

    print(f"✅ expert_photos 삽입 완료: {inserted_raw} rows")
    print(f"✅ expert_scene_stats 삽입 완료: {inserted_summary} rows")
    print("✅ ETL 완료")


if __name__ == "__main__":
    main()
