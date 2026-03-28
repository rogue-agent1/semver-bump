#!/usr/bin/env python3
"""semver_bump - Bump semantic versions (major.minor.patch)."""
import sys, re

def parse(v):
    v = v.lstrip('v')
    m = re.match(r'(\d+)\.(\d+)\.(\d+)(?:-(.+))?', v)
    if not m: return None
    return [int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4) or '']

def bump(ver, part='patch', pre=None):
    v = parse(ver)
    if not v: print(f"Invalid: {ver}"); sys.exit(1)
    if part == 'major': v[0]+=1; v[1]=0; v[2]=0
    elif part == 'minor': v[1]+=1; v[2]=0
    elif part == 'patch': v[2]+=1
    result = f"{v[0]}.{v[1]}.{v[2]}"
    if pre: result += f"-{pre}"
    return result

def compare(a, b):
    va, vb = parse(a), parse(b)
    for i in range(3):
        if va[i] != vb[i]: return 1 if va[i] > vb[i] else -1
    return 0

def main():
    args = sys.argv[1:]
    if not args or '-h' in args:
        print("Usage:\n  semver_bump.py 1.2.3 patch|minor|major [--pre alpha]\n  semver_bump.py compare 1.2.3 1.3.0"); return
    if args[0] == 'compare':
        r = compare(args[1], args[2])
        sym = '=' if r==0 else ('>' if r>0 else '<')
        print(f"{args[1]} {sym} {args[2]}")
    else:
        ver = args[0]
        part = args[1] if len(args)>1 else 'patch'
        pre = args[args.index('--pre')+1] if '--pre' in args else None
        print(bump(ver, part, pre))

if __name__ == '__main__': main()
