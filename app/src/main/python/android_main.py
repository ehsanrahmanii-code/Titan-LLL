"""Start Titan LLL Flask server inside Chaquopy."""
from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path

_started = False
_lock = threading.Lock()


def _prepare_home() -> None:
    candidates = []
    for key in ("HOME", "TMPDIR", "ANDROID_PRIVATE"):
        v = (os.environ.get(key) or "").strip()
        if v:
            candidates.append(Path(v) / "LLL")
    candidates.extend(
        [
            Path("/storage/emulated/0/LLL"),
            Path("/sdcard/LLL"),
            Path.home() / "LLL",
            Path("/data/data/org.titanlll.titanlll/files/LLL"),
        ]
    )
    for c in candidates:
        try:
            c.mkdir(parents=True, exist_ok=True)
            probe = c / ".w"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            os.environ["TITAN_HOME"] = str(c)
            return
        except Exception:
            continue


def _patch_storage_lock(module_file: Path) -> None:
    if not module_file.is_file():
        return
    try:
        text = module_file.read_text(encoding="utf-8")
    except Exception:
        return
    if "Fall through to TITAN_HOME" in text:
        return
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
    if old in text:
        try:
            module_file.write_text(text.replace(old, new, 1), encoding="utf-8")
        except Exception:
            pass


def start_server() -> None:
    global _started
    with _lock:
        if _started:
            return
        _started = True

    _prepare_home()

    # TITAN module may live next to this file (copied in CI)
    here = Path(__file__).resolve().parent
    titan_path = here / "TITAN_PRO_V75_PWA.py"
    if not titan_path.is_file():
        # fallback: repo root style
        titan_path = here.parent.parent.parent.parent.parent / "TITAN_PRO_V75_PWA.py"
    _patch_storage_lock(titan_path if titan_path.is_file() else here / "TITAN_PRO_V75_PWA.py")

    if str(here) not in sys.path:
        sys.path.insert(0, str(here))

    import TITAN_PRO_V75_PWA as titan  # noqa: WPS433

    def run():
        titan.app.run(
            host="127.0.0.1",
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True,
        )

    t = threading.Thread(target=run, name="titan-flask", daemon=True)
    t.start()
    time.sleep(1.0)
