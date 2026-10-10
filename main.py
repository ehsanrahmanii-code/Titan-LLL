#!/usr/bin/env python3
"""Titan LLL - Android entry point (WebView bootstrap)."""
from __future__ import annotations

import os
import sys
import time
import traceback
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def _patch_titan_storage_lock() -> None:
    """Prevent hard-crash when shared storage is visible but not writable yet."""
    path = Path(BASE_DIR) / "TITAN_PRO_V75_PWA.py"
    if not path.is_file():
        return
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return
    if "Fall through to TITAN_HOME" in text:
        return
    old = (
        '    if android_storage_present:\n'
        '        raise RuntimeError(\n'
        '            "LLL storage is present but not writable. TITAN will not fall back "\n'
        '            "to the script directory or another location. Grant storage permission "\n'
        '            "and make Internal Storage/LLL writable."\n'
        '        )'
    )
    new = (
        '    if android_storage_present:\n'
        '        # Fall through to TITAN_HOME / app-private LLL so the app can start.\n'
        '        pass'
    )
    if old in text:
        try:
            path.write_text(text.replace(old, new, 1), encoding="utf-8")
            print("patched TITAN storage lock")
        except Exception as e:
            print("patch write failed:", e)


def _prepare_home() -> None:
    candidates = []
    for key in ("ANDROID_ARGUMENT", "ANDROID_PRIVATE", "HOME", "TMPDIR"):
        v = (os.environ.get(key) or "").strip()
        if v:
            candidates.append(Path(v) / "LLL")
    candidates.extend(
        [
            Path("/data/data/org.titanlll.titanlll/files/LLL"),
            Path("/data/user/0/org.titanlll.titanlll/files/LLL"),
            Path.home() / "LLL",
            Path(BASE_DIR) / "LLL",
            Path("/storage/emulated/0/LLL"),
            Path("/sdcard/LLL"),
        ]
    )
    for c in candidates:
        try:
            c.mkdir(parents=True, exist_ok=True)
            probe = c / ".w"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            os.environ["TITAN_HOME"] = str(c)
            print("TITAN_HOME=", c)
            return
        except Exception:
            continue


def main() -> None:
    try:
        _prepare_home()
        _patch_titan_storage_lock()
        time.sleep(0.5)
        try:
            import titan_compat  # noqa: F401
        except Exception as e:
            print("compat warn:", e)

        import TITAN_PRO_V75_PWA as titan

        print("Starting Titan LLL Flask on 0.0.0.0:5000")
        titan.app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True,
        )
    except Exception:
        traceback.print_exc()
        time.sleep(20)
        raise


if __name__ == "__main__":
    main()
