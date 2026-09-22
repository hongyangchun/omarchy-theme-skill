# omarchy-theme-skill

> An [Agent skill](https://agent-skills.dev) that ships the complete, battle-tested
> pipeline for creating **Omarchy theme repositories** — from artwork or game/film
> IP assets to a public repo installable with one command.

Forged while shipping **nine public Omarchy themes** (vangogh, monet, ukiyo,
levitan, black-myth-wukong, ghost-of-tsushima, cyberpunk-2077,
no-rest-for-the-wicked, starcraft) — including a four-round rework whose
lessons are baked into the rules.

## Install

Copy the repo into your agent's skills directory (Hermes, Claude Code, opencode —
anything that reads SKILL.md):

```sh
git clone https://github.com/<you>/omarchy-theme-skill.git ~/.your-agent/skills/omarchy-theme-skill
```

Then just ask your agent: *"make me a Van Gogh theme"* or *"an official
StarCraft Remastered theme"*.

## What's inside

| File | Purpose |
|---|---|
| `SKILL.md` | The pipeline: route decision → asset sourcing → vision QC → palette → repo → verification chain |
| `references/artist-pipeline.md` | Public-domain paintings route: Commons GAP scans, PD-Art licensing, series expansion |
| `references/ip-pipeline.md` | IP route: official CDN digging, wallhaven fallback, fan-distribution licensing |
| `scripts/palette_kmeans.py` | K-means palette extraction from the hero painting |

## Highlights of what it encodes

- **Route pinning first**: "official assets" vs "original homage" — assuming
  wrong costs a full rework (measured: four rounds)
- **Version pinning within an IP**: SC1 Remastered ≠ SC2-era shots
- **GAP scan vs installation photo**: a Google Art Project scan is the bare
  painting; a "<Museum> IMG_nnnn" file is a wall photo with the frame — crop
  logic that treats them the same throws away canvas or leaves frame residue
- **Same title ≠ same painting**: verify the subject, not the filename
- **Crossover QC twice**: anime/other-game/pure-logo images swim in from
  authoritative sources too — montage + vision pass on candidates AND finals
- **Two-directory git discipline**: build repo vs installed copy, rsync
  --delete only, `git ls-files` audit before shipping
- **The full verification chain**: backgrounds → snapshot rebuild → symlink
  target exists → `bg next` full-circle readback

## Themes shipped with this pipeline

vangogh · monet · ukiyo · levitan · black-myth-wukong · ghost-of-tsushima ·
cyberpunk-2077 · no-rest-for-the-wicked · starcraft

*(add your screenshots here)*

## License

MIT for the skill. Artwork licensing guidance per route is inside the
references (PD-Art for paintings; unofficial fan-distribution for IP).
