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
2. Build a concise prompt using `references/prompting.md`.
3. Estimate cost and request confirmation.
4. Use `scripts/generate_xai_video.py` when possible:

```bash
python skills/animeskill/scripts/generate_xai_video.py \
  --image person.png \
  --action "walk cycle, side view" \
  --duration 2 \
  --size 720x720 \
  --chroma "#00FF00" \
  --output out/walk_720.mp4
```

5. Save the downloaded MP4. Do not perform chroma cleanup, sprite-sheet conversion, or heavy post-processing unless explicitly requested.

## Prompt Rules

Keep prompts specific and restrictive:

- Preserve the exact character identity, silhouette, outfit, colors, and proportions from the source image.
- Center the full character in frame.
- Use a flat, solid chroma-key background with the selected hex color.
- Avoid camera movement, zoom, cuts, text, props, extra characters, shadows on the background, and background gradients.
- Ask for readable game-animation motion suitable for sprite-sheet extraction.

## References

- Read `references/xai-imagine.md` for API parameters, pricing notes, and output constraints.
- Read `references/prompting.md` for reusable prompt templates and action wording.
