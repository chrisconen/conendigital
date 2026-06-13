#!/bin/bash
# Cloudflare Pages deploy script — Conen Digital
# Köv. lépések:
# 1. Build blog
# 2. Másold a root HTML fájlokat a cloudflare output könyvtárba

set -e

echo "=== 1. Blog build ==="
cd conen-blog
npm install
npm run build -- --outDir=../dist/blog
cd ..

echo "=== 2. Root fájlok másolása ==="
# Statikus HTML, CSS, JS, képek, stb. a gyökérbe
for f in *.html *.js *.ico *.txt *.xml *.json *.webp *.png *.jpg *.svg *.mp3 *.mp4 *.wfp; do
  if [ -f "$f" ]; then
    cp "$f" dist/
  fi
done

# Mappák
for d in js images heightmaps .well-known; do
  if [ -d "$d" ]; then
    cp -r "$d" dist/
  fi
done

# Cloudflare Pages Functions (szivárgás-audit backend: /api/audit)
if [ -d "functions" ]; then
  cp -r functions dist/
  rm -f dist/functions/.dev.vars            # lokális titkok soha ne kerüljenek deployra
  rm -f dist/functions/api/AUDIT_CONTRACT.md # dokumentáció, nem kell a kimenetbe
fi

echo "=== 3. Kész ==="
ls -la dist/
