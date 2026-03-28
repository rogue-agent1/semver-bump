#!/usr/bin/env python3
"""Semantic version bumper and comparator."""
import sys, re

def parse(v):
    v = v.lstrip('v')
    m = re.match(r'(\d+)\.(\d+)\.(\d+)(?:-(.+))?', v)
    if not m: raise ValueError(f"Invalid semver: {v}")
    return int(m[1]), int(m[2]), int(m[3]), m[4]

def bump(v, part):
    ma, mi, pa, pre = parse(v)
    if part == 'major': return f"{ma+1}.0.0"
    if part == 'minor': return f"{ma}.{mi+1}.0"
    if part == 'patch': return f"{ma}.{mi}.{pa+1}"
    raise ValueError(f"Unknown part: {part}")

def compare(a, b):
    pa, pb = parse(a)[:3], parse(b)[:3]
    if pa > pb: return 1
    if pa < pb: return -1
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 3: print("Usage: semver_bump.py <bump|compare> <version> [part|version2]"); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'bump':
        part = sys.argv[3] if len(sys.argv) > 3 else 'patch'
        print(bump(sys.argv[2], part))
    elif cmd == 'compare':
        r = compare(sys.argv[2], sys.argv[3])
        sym = '=' if r == 0 else ('>' if r > 0 else '<')
        print(f"{sys.argv[2]} {sym} {sys.argv[3]}")
