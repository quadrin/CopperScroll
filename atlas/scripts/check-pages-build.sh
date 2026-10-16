#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
pages_destination="${1:-$(mktemp -d /tmp/copperscroll-pages.XXXXXX)}"
mkdir -p "$pages_destination"
pages_destination="$(cd "$pages_destination" && pwd)"
if [[ -n "$(ls -A "$pages_destination")" ]]; then
  echo 'Use an empty destination for the Pages build.' >&2
  exit 1
fi
# The same immutable image used by actions/jekyll-build-pages v1.0.13.
docker run --rm --network none --user "$(id -u):$(id -g)" --entrypoint /bin/sh \
  -v "$repo_root:/source:ro" -v "$pages_destination:/site" \
  -e JEKYLL_ENV=production -e PAGES_REPO_NWO=quadrin/CopperScroll \
  ghcr.io/actions/jekyll-build-pages@sha256:6791ebfd912185ed59bfb5fb102664fa872496b79f87ff8b9cfba292a7345041 \
  -c 'github-pages build --source /source --destination /site'
node "$repo_root/atlas/scripts/check-pages-payload.mjs" --site-dir "$pages_destination"
echo "Pages output: $pages_destination"
