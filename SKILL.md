---
name: omarchy-theme-skill
description: >
  End-to-end pipeline for creating Omarchy theme repositories from artwork
  (public-domain paintings) or game/film IP assets. Covers asset sourcing
  (Wikimedia Commons GAP scans, official CDNs), per-image vision QC, K-means
  palette extraction, repo structure red-lines, git workflow, preview
  discipline, and install verification. Use when asked to create, rework, or
  expand an Omarchy theme, or when a user says "make me an X theme" /
  "theme repo" / "more wallpapers".
argument-hint: "[artist | ip-name]"
license: MIT
---

# Omarchy Theme Pipeline

Proven flow for shipping Omarchy theme repos — public repos installable via
`omarchy theme install <url>`. Forged across nine shipped themes (vangogh,
monet, ukiyo, levitan, black-myth-wukong, ghost-of-tsushima, cyberpunk-2077,
no-rest-for-the-wicked, starcraft) and a four-round rework that this document
exists to prevent.

Two routes, decided FIRST:

- **Artist route** (public-domain paintings → Wikimedia Commons museum scans):
  see [references/artist-pipeline.md](references/artist-pipeline.md)
- **IP route** (game/film official assets):
  see [references/ip-pipeline.md](references/ip-pipeline.md)

Both share Steps 2–6 below. Read the route reference before touching assets;
read the whole SKILL.md before touching a repo.

## Step 0 — Pin the route and the VERSION before anything else

"Make me an X theme" has two opposite readings (official assets vs original
style homage). Assuming wrong = full rework (it happened four rounds straight).
Ask once: official assets, or original-style? If official: pin the GAME/WORK
VERSION too — sequel-era images mixed into an official-source pool get the
whole batch rejected ("I want SC1 Remastered art" rejects SC2-era shots even
though same IP).

## Step 1 — Asset sourcing (route-specific)

Artist route: Wikimedia Commons museum scans ONLY (Google Art Project suffix
= clean bare-painting scan; "<Museum> IMG_nnnn" = installation photo WITH
frame — avoid or budget crop loops). Commons API rate-limits hard: sleep 2–3s
between calls, full browser UA, batch `prop=imageinfo`, wait ~30s after a 429.

IP route: official site HTML → CDN asset URLs (Blizzard ContentStack pattern)
→ try larger size tiers in the URL (`_1600` → `_2600`). wallhaven only as
fallback, `sorting=favorites&atleast=2560x1440`, and EVERY hit needs vision QC
(crossovers/other games/pure logos swim in even at the top of favorites).

NEVER fill asset gaps with AI-generated images for an official-assets theme —
users recognize them instantly and reject the batch.

## Step 2 — Per-image vision QC (mandatory, twice)

Download to a /tmp pool → `magick montage` numbered contact sheet → vision
pass classifying EVERY image (authentic / crossover / wrong-version / logo /
quality+lighting). Then re-montage the final selection and QC again before
commit — crossovers swim in from any source, authoritative pools included.

Acceptance standard is the user's original spec (IP + version), not "looks
like the IP". Same title ≠ same painting: verify SUBJECT after download.

## Step 3 — Palette + repo skeleton

Palette: `python3 scripts/palette_kmeans.py <hero.jpg>` (k=12 K-means) →
colors.toml. Accent comes FROM the artwork, never invented. Comment each color
with its source painting.

Repo files (red-line): `colors.toml`, `icons.theme`, `chromium.theme`,
`preview.png` (1800px montage), `unlock.png` (800×180), `backgrounds/`,
`README.md` (per-image credit), `LICENSE` (MIT code + asset-specific
distribution note), `.gitignore`, `.gitattributes`.

**Red line:** a git-installed theme must NOT contain `*.lua`, `alacritty.toml`,
`foot.ini`, `ghostty.conf`, `kitty.conf`, `vscode.json` — Omarchy silently
drops them (they execute code). 4.0.4+ derives the whole app set from
colors.toml automatically, so don't hand-author those anyway.

Process scripts (fetch/gen/sync/pool) and working notes stay OUT of the repo —
`git ls-files` audit before declaring done.

## Step 4 — Git workflow: two directories, never mix

- **Build repo** (`~/<name>-theme/`, has .git) is the ONLY place you commit.
- **Installed copy** (`~/.config/omarchy/themes/<name>/`) has NO .git — git
  commands there show ghost state. Sync with `rsync -a --delete` (cp leaves
  deleted-file residue), then `ls backgrounds/ | wc -l` against expectation.
- `git reset --hard` does NOT remove untracked files — swap wallpaper sets
  with rsync --delete or manual rm.
- New-wallpaper rounds: files go to THREE places (build repo backgrounds/,
  themes/<name>/backgrounds/, AND the live snapshot
  `~/.local/state/omarchy/current/theme/backgrounds/`) + `omarchy theme bg
  cache` + full `bg next` circle readback.

## Step 5 — preview discipline + verification chain

Every backgrounds change re-montages preview.png in the SAME commit:

```sh
magick montage backgrounds/*.jpg -tile 4x3 -geometry 450x253+4+4 \
  -background '#05070e' /tmp/p.png && magick /tmp/p.png -resize 1800x preview.png
```

Full verification chain (missing one step = "it still shows the old theme"):
① files in `themes/<name>/backgrounds/` → ② `omarchy theme set <name>`
rebuilds the snapshot → ③ `readlink ~/.local/state/omarchy/current/background`
and target EXISTS (dangling symlink silently shows the old image) → ④
`omarchy theme bg current` / `bg next` full-circle readback (every image
identified). Agent-session `grim` verification: `export
XDG_RUNTIME_DIR=/run/user/1000` + `timeout 8 grim -c /tmp/x.png`; screen-level
look is the user's call. Locked session blocks shell restarts — tell the user
to unlock instead of retrying.

## Final selection is the user's

Number the candidates, let the user pick by number (official-source images
still get batch-rejected on taste; positional words like "the last four" map
to filenames badly — always re-list numbered). After deletions, `ls | wc -l`
to confirm the count really dropped (`rm -f` on a typo'd name "succeeds"
silently).

## References

- [references/artist-pipeline.md](references/artist-pipeline.md) — paintings
  route: GAP vs installation scans, Commons specs, palette table, PD-Art
  licensing, series expansion
- [references/ip-pipeline.md](references/ip-pipeline.md) — IP route: CDN
  digging, wallhaven fallback, fan-distribution licensing, aesthetic
  conclusions
- [scripts/palette_kmeans.py](scripts/palette_kmeans.py) — K-means palette
  extraction

## Benchmarks

Nine repos shipped. Per-theme cost: artist route ~10–50 min via agent
delegation, single-artist direct build faster; expansion round ("more
wallpapers") ~15 min including verification chain.
