import exifread
import os

PHOTO_DIR = "photos"

for root, _, files in os.walk(PHOTO_DIR):
    for file in files:
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(root, file)

        print("======", file, "======")

        with open(path, "rb") as f:
            tags = exifread.process_file(f, details=False)

        iso = tags.get("EXIF ISOSpeedRatings")
        shutter = tags.get("EXIF ExposureTime")

        print("ISO:", iso)
        print("Shutter(ExposureTime):", shutter)
