#!/usr/bin/env python3
"""Semver bumper — bump version, optionally create git tag."""
import sys, re, subprocess
def current_version():
    try:
        tags = subprocess.check_output(["git","tag","--sort=-v:refname"], text=True).strip().split("\n")
        for t in tags:
            m = re.match(r"v?(\d+\.\d+\.\d+)", t)
            if m: return m.group(1)
    except: pass
    return "0.0.0"
def bump(ver, part):
    major, minor, patch = map(int, ver.split("."))
    if part == "major": return f"{major+1}.0.0"
    if part == "minor": return f"{major}.{minor+1}.0"
    return f"{major}.{minor}.{patch+1}"
def cli():
    part = sys.argv[1] if len(sys.argv)>1 else "patch"
    cur = current_version(); new = bump(cur, part)
    print(f"  {cur} → {new}")
    if "--tag" in sys.argv:
        subprocess.run(["git","tag",f"v{new}"]); print(f"  Tagged v{new}")
if __name__=="__main__": cli()
