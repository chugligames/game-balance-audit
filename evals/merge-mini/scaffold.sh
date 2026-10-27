#!/usr/bin/env bash
# Copies the example game into the eval's empty workspace (run with --scaffold).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -R "$HERE/../../examples/merge-mini/." .
