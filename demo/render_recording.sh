#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
SHOWCASE="file://${ROOT// /%20}/demo/showcase/index.html"
FRAMES="$ROOT/demo/output/frames"
VIDEO="$ROOT/demo/output/boardroom-analyst-demo.mp4"

mkdir -p "$FRAMES"

for step in 1 2 3 4 5 6; do
  profile="/private/tmp/chrome-boardroom-frame-$step-$$"
  frame="$FRAMES/frame_00${step}.png"
  rm -f "$frame"
  "$CHROME" \
    --headless=new \
    --disable-gpu \
    --disable-crash-reporter \
    --disable-background-networking \
    --disable-component-update \
    --disable-sync \
    --no-first-run \
    --no-default-browser-check \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget=1000 \
    --user-data-dir="$profile" \
    --screenshot="$frame" \
    --window-size=1280,720 \
    "$SHOWCASE?step=$step" >/dev/null 2>&1 &
  chrome_pid=$!
  for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
    if [ -s "$frame" ]; then
      break
    fi
    sleep 0.5
  done
  kill "$chrome_pid" >/dev/null 2>&1 || true
  pkill -f "$profile" >/dev/null 2>&1 || true
  wait "$chrome_pid" >/dev/null 2>&1 || true
  if [ ! -s "$frame" ]; then
    echo "Failed to render $frame" >&2
    exit 1
  fi
done

ffmpeg -y \
  -framerate 0.5 \
  -i "$FRAMES/frame_%03d.png" \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1:color=white,fps=30" \
  -pix_fmt yuv420p \
  "$VIDEO"

echo "$VIDEO"
