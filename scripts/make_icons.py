from pathlib import Path
import subprocess, sys
try:
    from PIL import Image, ImageDraw
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image, ImageDraw

base = Path("app/src/main/res")
for folder, size in [
    ("mipmap-mdpi", 48),
    ("mipmap-hdpi", 72),
    ("mipmap-xhdpi", 96),
    ("mipmap-xxhdpi", 144),
    ("mipmap-xxxhdpi", 192),
]:
    d = base / folder
    d.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (size, size), (5, 8, 22, 255))
    dr = ImageDraw.Draw(img)
    m = max(2, size // 10)
    dr.rounded_rectangle(
        [m, m, size - m, size - m],
        radius=size // 5,
        fill=(15, 23, 42, 255),
        outline=(34, 211, 238, 255),
        width=max(1, size // 24),
    )
    img.save(d / "ic_launcher.png")
print("icons ok")
