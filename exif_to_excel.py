import exifread
import os
import pandas as pd

PHOTO_DIR = "photos"
rows = []

def frac_to_float(frac):
    try:
        return float(frac.num) / float(frac.den)
    except:
        try:
            num, den = str(frac).split("/")
            return float(num) / float(den)
        except:
            return None

for scene in os.listdir(PHOTO_DIR):
    scene_path = os.path.join(PHOTO_DIR, scene)
    if not os.path.isdir(scene_path):
        continue

    for file in os.listdir(scene_path):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(scene_path, file)

        with open(path, "rb") as f:
            tags = exifread.process_file(f, details=False)

        iso = tags.get("EXIF ISOSpeedRatings")
        shutter_tag = tags.get("EXIF ExposureTime")

        shutter_sec = frac_to_float(shutter_tag)

        rows.append({
            "scene": scene,
            "file": file,
            "ISO": int(str(iso)) if iso else None,
            "Shutter_sec": shutter_sec
        })

df = pd.DataFrame(rows)
df.to_excel("result.xlsx", index=False)

print("result.xlsx 생성 완료")
