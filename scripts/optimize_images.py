#!/usr/bin/env python3
"""批量優化圖片 - 轉換為 WebP 並調整尺寸"""
import subprocess
from pathlib import Path

INPUT_DIR = Path(".")
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

SPECS = {
    "class.png": {"width": 1200, "quality": 80},     # Hero 背景
    "solo.jpg": {"width": 400, "quality": 80},       # 師傅照片
    "class_hall.jpg": {"width": 800, "quality": 80},  # 上課環境
    "class_8year.JPG": {"width": 800, "quality": 80}, # 器械班實況
    "solo2.jpg": {"width": 400, "quality": 80},      # 師傅示範器械
}

def optimize_image(src_name, spec):
    src = INPUT_DIR / src_name
    if not src.exists():
        print(f"⚠️  Missing: {src_name}")
        return False
    
    stem = src.stem
    out = OUTPUT_DIR / f"{stem}.webp"
    
    cmd = [
        "magick", str(src),
        "-resize", f"{spec['width']}x>",
        "-quality", str(spec['quality']),
        "-define", "webp:lossless=false",
        str(out)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size_kb = out.stat().st_size / 1024
        print(f"✅ {src_name} → {out.name} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"❌ {src_name}: {result.stderr}")
        return False

def main():
    print("Starting image optimization...\n")
    for src_name, spec in SPECS.items():
        optimize_image(src_name, spec)
    print("\nDone!")

if __name__ == "__main__":
    main()