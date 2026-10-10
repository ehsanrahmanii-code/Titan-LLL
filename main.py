#!/usr/bin/env python3
"""Titan LLL - Android entry point (WebView bootstrap)"""
from __future__ import annotations
import os, sys, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def main():
    time.sleep(1.2)
    try:
        import titan_compat  # noqa: F401
    except Exception as e:
        print("compat:", e)
    try:
        import TITAN_PRO_V75_PWA as titan
    except ImportError as e:
        print("ERROR: TITAN_PRO_V75_PWA.py missing:", e)
        sys.exit(1)
    try:
        titan.app.config["APP_NAME"] = "Titan LLL"
    except Exception:
        pass
    print("Starting Titan LLL on 0.0.0.0:5000 ...")
    titan.app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, threaded=True)

if __name__ == "__main__":
    main()
