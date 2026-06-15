# Prompting Guide

Use one compact prompt. Avoid long story context.

## Base Template

```text
Animate the provided character image into a {duration}-second {action} animation for a 2D game sprite sheet. Preserve the exact character identity, outfit, colors, proportions, and silhouette from the source image. Keep the full body centered and visible. Use a flat solid {chroma} chroma-key background only. No camera movement, no zoom, no scene cuts, no text, no extra characters, no props, no background shadows, no gradients. Clean readable motion, loop-friendly timing.
```

## Action Wording

- Walk: `side-view walk cycle with clear alternating steps`
- Run: `side-view run cycle with energetic leg and arm motion`
- Attack: `single quick melee attack wind-up, strike, and recovery`
- Hit: `brief impact reaction with recoil and recovery`
- Idle: `subtle breathing idle animation`
- Jump: `small jump upward and landing in place`
- Cast: `short spell-casting gesture with hands, no external effects unless requested`

If the user gives a custom action, keep it concise and insert it directly into the template.
