from pathlib import Path
p = Path("app/src/main/python/TITAN_PRO_V75_PWA.py")
t = p.read_text(encoding="utf-8")
old = (
    "    if android_storage_present:\n"
    "        raise RuntimeError(\n"
    '            "LLL storage is present but not writable. TITAN will not fall back "\n'
    '            "to the script directory or another location. Grant storage permission "\n'
    '            "and make Internal Storage/LLL writable."\n'
    "        )"
)
new = (
    "    if android_storage_present:\n"
    "        # Fall through to TITAN_HOME so app can start.\n"
    "        pass"
)
if old in t:
    p.write_text(t.replace(old, new, 1), encoding="utf-8")
    print("patched storage lock")
else:
    print("storage block not found or already patched")
