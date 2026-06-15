---
name: animeskill
description: Generate short 1-3 second chroma-key animation videos from a static character image using xAI Grok Imagine. Use when the user asks to animate a local character image into a walk, attack, hit, idle, jump, cast, or similar game-animation clip for later sprite-sheet conversion, especially with 480x480 or 720x720 square output and green or magenta chroma-key backgrounds.
---

# Animeskill

## Purpose

Create short square character animation clips on a flat chroma-key background for later sprite-sheet extraction. Prefer xAI Grok Imagine image-to-video with `grok-imagine-video`.

## Required Inputs

Collect these values before generation:

- Source character image: local PNG/JPG path or a user-attached image.
- Action: `walk`, `attack`, `hit`, `idle`, `jump`, `cast`, `run`, or a concise custom motion.
- Duration: `1`, `2`, or `3` seconds.
- Size: `480x480` or `720x720`.
- Chroma key: `#00FF00` or `#FF00FF`.

If the user omits size or chroma key, ask for only the missing values. Do not offer `1024x1024`.

## Cost Warning

Before any paid API call, show the estimated xAI cost and ask for confirmation. Use current repo defaults unless updated by the user:

- `480x480`: `480p` at `$0.05/sec` plus `$0.002` input image.
- `720x720`: `720p` at `$0.07/sec` plus `$0.002` input image.

Example: `720x720`, `2s` costs about `$0.142`. Remind the user that retries are also billable.

## Generation Workflow

1. Validate inputs: duration in `1..3`, size in `480x480|720x720`, chroma in `#00FF00|#FF00FF`.
2. Normalize non-English user requests into concise English API wording using `references/prompting.md`.
3. Build a concise English prompt using `references/prompting.md`.
4. Estimate cost and request confirmation.
5. Use `scripts/generate_xai_video.py` when possible:

```bash
python skills/animeskill/scripts/generate_xai_video.py \
  --image person.png \
  --action "walk cycle, side view" \
  --duration 2 \
  --size 720x720 \
  --chroma "#00FF00" \
  --output out/walk_720.mp4
```

6. Save the downloaded MP4. Do not perform chroma cleanup, sprite-sheet conversion, or heavy post-processing unless explicitly requested.

## API Key Handling

Use this order for xAI credentials:

1. `XAI_API_KEY` environment variable.
2. Animeskill user config at `~/.animeskill/config.json`, or the path in `ANIMESKILL_CONFIG`.

If no key is available, ask the user for the key and run:

```bash
python <skill-path>/scripts/configure_xai_key.py
```

Never print the key, commit it, or store it inside a project repository.

## Prompt Rules

Keep prompts specific and restrictive:

- The user may write in Russian or another language, but the final xAI prompt and `--action` value should be concise English.
- Preserve the exact character identity, silhouette, outfit, colors, and proportions from the source image.
- Center the full character in frame.
- Treat the output as a technical green-screen asset, not an illustrated scene.
- Require every background pixel from edge to edge to be the same flat chroma color.
- Allow only two visual layers: the animated character and the pure chroma background.
- Keep the background absolutely clean: no contact shadows, ambient shadows, cast shadows, floor, wall, room, scenery, reflections, glow, outlines, ground plane, horizon line, texture, particles, lighting falloff, noise, gradients, vignettes, or color variation.
- Avoid camera movement, zoom, cuts, text, props, and extra characters.
- Ask for readable game-animation motion suitable for sprite-sheet extraction.

## Result Acceptance

After generation, inspect the video if possible. If the background contains scenery, a floor, a wall, shadows, gradients, or any non-chroma color variation, treat the result as failed. Do not claim it is ready for sprite-sheet extraction. Ask the user whether to spend another paid retry using the failed-background retry prompt in `references/prompting.md`.

## References

- Read `references/xai-imagine.md` for API parameters, pricing notes, and output constraints.
- Read `references/prompting.md` for reusable prompt templates and action wording.
