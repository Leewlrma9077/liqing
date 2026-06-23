"""Convert source JPG photos to WebP thumbnails (600px) and full-size (1920px)."""
import os
from PIL import Image

SRC = r"C:/Users/lixia/OneDrive/网页制作/爷爷李庆资料"
DST = r"C:/Users/lixia/OneDrive/网页制作/爷爷李庆资料/website/images"

PHOTOS = [
    "右一为李庆.JPG", "画面中间为李庆.JPG", "画面右侧.JPG", "右一.JPG",
    "画面右1.JPG", "IMG_3985.JPG", "IMG_3986.JPG",
    "image0000001A.jpg", "image0000002A.jpg",
    "001.jpg", "002.jpg", "003.jpg", "8x40-1.jpg",
]

os.makedirs(DST, exist_ok=True)

converted = 0
errors = []

for fname in PHOTOS:
    src = os.path.join(SRC, fname)
    if not os.path.isfile(src):
        errors.append(f"MISSING: {fname}")
        continue

    stem = os.path.splitext(fname)[0]
    try:
        img = Image.open(src)
        # Preserve EXIF orientation
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
        if img is None:
            img = Image.open(src)

        # Convert to RGB if necessary (e.g. RGBA -> RGB for WebP)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Thumbnail 600px wide
        thumb = img.copy()
        thumb.thumbnail((600, 600))
        tp = os.path.join(DST, f"thumb_{stem}.webp")
        thumb.save(tp, "WEBP", quality=85)
        print(f"  thumb {fname} -> {tp}  ({thumb.size[0]}x{thumb.size[1]})")

        # Full-size 1920px wide
        full = img.copy()
        full.thumbnail((1920, 1920))
        fp = os.path.join(DST, f"full_{stem}.webp")
        full.save(fp, "WEBP", quality=85)
        print(f"  full  {fname} -> {fp}  ({full.size[0]}x{full.size[1]})")

        converted += 1
    except Exception as e:
        errors.append(f"ERROR on {fname}: {e}")

print(f"\nDone. Converted: {converted}/{len(PHOTOS)}")
if errors:
    print("Issues:")
    for e in errors:
        print(f"  {e}")
