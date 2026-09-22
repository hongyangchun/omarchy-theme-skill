# Artist/Painting Omarchy Theme Pipeline

Proven end-to-end flow for creating Omarchy theme repos out of public-domain
art. Validated by shipping multiple public repos (vangogh, monet, ukiyo, each 8+ wallpapers, built via agent delegation in ~10-50 min per theme).

## Repo Structure (17 files, red-line compliant)

- `colors.toml` — full palette; comment each color with its source painting
  ("Starry Night midnight", not bare hex)
- `icons.theme`, `chromium.theme` — kept by the installer
- `preview.png` (1800×1012 banner) + `unlock.png` (800×180 plymouth banner)
  — draw procedurally with PIL (serif CJK title panel + 3 painted scenes),
  then vision-check the render once
- `backgrounds/` — 4-8 paintings, HORIZONTAL only, ≥3000px wide, JPG q90,
  ≤10MB each (downsample to 3840px wide if over), numbered
  `NN-english-name.jpg`
- `README.md` — install command (`omarchy theme install
  https://github.com/<you>/omarchy-<name>-theme`), palette table,
  per-image credit (title / year / museum / Commons link)
- `LICENSE` (MIT), `.gitignore`, `.gitattributes` (wallpapers = binary)

**Red line:** a theme installed from git must NOT contain `*.lua`,
`alacritty.toml`, `foot.ini`, `ghostty.conf`, `kitty.conf`, `vscode.json`
— Omarchy silently drops these (warning on stderr) because they execute
code or name programs. Everything else (btop.theme, gtk.css, shell.toml…)
is kept.

## Palette Extraction

K-means (k=12) over the downloaded paintings → dark-mode base + one
saturated accent that names the artist's signature contrast:

| Theme | Base | Accent | Notes |
|---|---|---|---|
| vangogh | #0d1226 starry midnight | #e6b23c wheatfield gold | selection #20305c |
| monet | #141b26 harbor mist | #d4a13e haystack gold | blue #4e88b4 regatta sky |
| ukiyo | #101a28 prussian blue | #d9b45e Edo gold | washi cream fg #ede4c8 |

Hyprland `col.active_border` = accent→blue 45° gradient (roman-republic
convention).

## Wallpaper Sourcing Rules

- Wikimedia Commons ONLY, museum scans (Google Art Project, Met Open
  Access, Rijksmuseum, Getty, AIC, museum-official). Reject replica-site
  uploads (artsdot etc.) even when they're the only hit.
- Landscape orientation only. Ukiyo-e is portrait-native: Hokusai's
  landscape ōban series (Fugaku Sanjūrokkei variants — Great Wave 8242px
  on Commons, Red Fuji, Gotenyama MET DP141091) + Hiroshige landscapes fill
  an 8-slot deck.
- Verify each download with PIL (one Great Wave copy arrived 61-byte
  truncated) AND a vision pass that it's the right painting.
- Credit per image in README (title / year / museum / Commons link);
  note public-domain status.
- Monet note: early works (Impression Sunrise 1600px) have small scans —
  don't force ≥3000px when the museum scan tops out lower.
- 4.0.4+ theme engine note: a colors.toml-only theme is enough — the
  installer auto-derives the full app set (kitty/foot/ghostty/alacritty/
  vscode/btop/helix/neovim/obsidian/shell.toml/hyprland.lua…) into the
  active snapshot, so don't hand-author those files (the repo red line
  above bans several of them anyway). Verify activation via the snapshot
  `~/.local/state/omarchy/current/theme/` (fresh mtimes + colors.toml
  header) and `omarchy theme bg current` / `bg next` — NOT via
  `~/.config/omarchy/current/` (that path doesn't exist in 4.x).

## Delegation & Verification Pattern

1. `delegate_task` to opencode with: reference repo path
   (`~/omarchy-vangogh-theme`), red-line list, wallpaper spec, palette
   approach, target repo name, git proxy (`export
   https_proxy=http://127.0.0.1:10808`), push target (user's GitHub,
   `gh` already authenticated as your account), and local install-test of
   the pushed repo as final validation.
2. Independently verify the child's self-report: GitHub API for
   existence/visibility/pushed-at; count files; red-line grep. Gotchas:
   summary JSONs can claim pushed:true for a repo whose exact name needs a
   variant check (ukiy**o**, not ukiyoe — a guessed variant 404s); a single
   GitHub API call returning None is transient — retry once before
   concluding "not pushed".
3. Local install: theme slug = directory name; re-run
   `omarchy theme set <name>` after wallpaper updates so `bg next` sees
   the full deck. Big repos (~60MB) can exceed proxy clone timeouts —
   install from a local copy in that case.
4. Let the user pick wallpapers by eye (numbered lists); palette edits are minutes-level.

## Museum-scan frame traps (Levitan session lessons)

Not every large Commons file is a clean painting. Two frame traps:
- **Gallery installation photos**: Commons files titled "... in the <Museum>
  Gallery IMG_nnnn.jpg" are photos of the painting ON THE WALL — frame,
  mat, and wall color included. Crop coordinates guessed from a downscaled
  vision view took two rounds and still left frame edges. Prefer files that
  are museum SCANS (Google Art Project suffix, Met Open Access, etc.); if
  only an installation photo exists, budget for a crop-verify-crop loop or
  pick another canvas.
- **Same title, different painting**: search results can return a DIFFERENT
  canvas by the same artist with a similar name (variant title with a
  location suffix). After downloading, vision-verify SUBJECT against the
  requested painting ("is this actually the famous one?"), not just
  "is this a clean image" — a wrong-painting theme ships looking correct.
- **GAP scans need no cropping**: a Google Art Project scan is already the
  bare painting — cropping it by guessed percentages THROWS AWAY most of
  the canvas. Vision-check what the full image IS before assuming frame
  residue; ask vision for frame boundaries in percent only when a frame is
  actually visible.
- Verify the final deck with one montage + one vision pass (every image:
  pure painting, no frame, correct subject) before packaging.

## Series Status

vangogh / monet / ukiyo shipped (each 8 wallpapers). levitan shipped
2026-09 (11 paintings after a "more wallpapers" pass: Golden Autumn
Slobodka GAP 7158px, March, Evening Bells, Above Eternal Quiet, Birch
Grove, Evening Golden Plyos, The Lake 1899–1900, After the Rain. Plyos,
Evening on the Volga, Autumn Day. Sokolniki, The Oak; "Twilight Gallery"
palette — bg #1a1b1e canvas-dark, fg #d6cfc0 parchment, accent #c9a227
evening-bells gold, one ANSI color per painting; icons Yaru-sage-dark).
levitan was built directly by the main agent (no delegation) — for a
single-artist deck, direct build with vision checks is faster than
spawning opencode. Levitan deck floor: scans ≥1180px wide accepted
(monet's ≥3000px rule relaxed — Russian museum scans top out lower);
rejected for size: Fresh Wind Volga / Vladimirka / Istra (≤1000px).
Expansion-round workflow ("多来几张"): Commons search by subject keywords
(en + ru titles both hit) → batch imageinfo resolution check → download
≥1180px candidates → one 3×2 montage + one vision pass (frame/subject)
→ cp to build repo + themes/<name>/ + state snapshot (three places, see
wallpaper-update pitfall below) → `omarchy theme bg cache` → `bg next`
full-circle readback verifying every new image enters the cycle.
Note: when the theme being expanded is the ACTIVE theme, cp must reach
THREE targets — build repo, `~/.config/omarchy/themes/<name>/backgrounds/`,
and the live snapshot `~/.local/state/omarchy/current/theme/backgrounds/` —
then `omarchy theme bg cache`; the two-path rule below predates 4.x's
state-snapshot layout and under-copies.
Recommended cadence: → 梵高已扩到 8 幅（追加杏花/罗纳河星夜/阿尔勒卧室/夜间咖啡馆），
monet/ukiyo 各 8 幅。Candidate future
series: Klimt, 浮世绘花鸟卷, album-cover themes. Same pipeline applies.

## Local-build shortcut (levitan path, single-artist decks)

For a one-artist request ("用 X 的名画做主题") the fastest validated loop is
direct build, no delegation: Commons search (en+ru title variants) →
batched `prop=imageinfo` resolution gate → download to /tmp pool → montage
+ one vision pass (frame/subject) → palette from the deck's dominant mood
(vision describes, agent picks hex, name each color's source painting in
colors.toml comments) → repo files (colors.toml/icons.theme/README/
LICENSE PD-Art/palette.svg) → PIL preview (hero painting + palette strip)
+ darkened unlock.png → `cp -r` into `~/.config/omarchy/themes/<slug>/` →
`omarchy theme set <slug>` → verify via `~/.local/state/omarchy/current/
theme/colors.toml` header + `omarchy theme bg current/next` readback →
`gh repo create <name> --public --source=. --push`. grim screenshot
verification: works with `export XDG_RUNTIME_DIR=/run/user/1000` + `timeout 8
grim -c /tmp/x.png` (see SKILL.md/hyprland-056.md note) — readback commands +
grim + user eyeball all available.

## Video-explainer adjacency (evaluation started 2026-09-09)

anything2explainer + native-subtitle-quote-image are under LIVE evaluation
(deleg_cdd36c42) as a complementary pair — candidates, license boundaries
(a2e = PolyForm NC) and status in `references/video-pipeline-evaluation.md`.
anything2explainer's own lessons.md warns: tmux fork has a machine-wide cap
(13 sessions open → build-group 8 failed "Device not configured"); parallel
build groups are heavy — sample-render 10-15s only for evaluation.
Marked FIRST candidate if user starts a video pipeline (公众号图文矩阵延伸);
NC license blocks commercialization. Related rejected alternative:
OpenMontage (broader agentic video prod, less focused).

## Wallpaper-update pitfall (hit 2026-09-09)

After pushing new wallpapers to a theme repo, the ACTIVE theme's bg-cycle
still shows the old set: `omarchy theme bg next` reads ONLY the snapshot
`~/.local/state/omarchy/current/theme/backgrounds/` plus the user layer
`~/.config/omarchy/backgrounds/<name>/` — never `themes/<name>/backgrounds/`.
Fix (pick one):
- Quick: cp new jpgs into BOTH `themes/<name>/backgrounds/` AND
  `~/.config/omarchy/backgrounds/<name>/` (mkdir -p the latter). `find -L`
  merges both with same-name dedup.
- Clean: re-run `omarchy theme set <name>` to rebuild the snapshot.
- `git pull` inside themes/<name> can hang via proxy — plain cp is faster.
Also: theme slug comes from the install DIRECTORY name (a /tmp/monet-test
path installs a theme literally named "monet-test"); verify exact repo slug
via GitHub API before install (ukiy**o**, not ukiyoe).
Commons API rate-limits hard (429 within a few search rounds) — sleep 2–3s
between requests, use a full browser UA string, wait ~30s after a 429, and
prefer single batched `prop=imageinfo` calls (multiple titles joined with
`|`) over repeated `list=search` rounds.
