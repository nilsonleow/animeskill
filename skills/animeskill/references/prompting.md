# Prompting Guide

Use one compact prompt. Avoid long story context.

## Base Template

```text
Animate the provided character image into a {duration}-second {action} animation for a 2D game sprite sheet. Preserve the exact character identity, outfit, colors, proportions, and silhouette from the source image. Keep the full body centered and visible. This is a technical green-screen asset, not an illustrated scene. Every background pixel from edge to edge must be exactly the same flat solid {chroma} color. Only two visual layers are allowed: the animated character and the pure chroma background. The character must not cast anything onto the background. No contact shadows, ambient shadows, cast shadows, floor, wall, room, scenery, reflections, glow, outlines, ground plane, horizon line, texture, particles, lighting falloff, noise, gradients, vignettes, or color variation. No camera movement, no zoom, no scene cuts, no text, no extra characters, no props. Clean readable motion, loop-friendly timing.
```

## Failed Background Retry

If the result has scenery, a floor, a wall, shadows, gradients, or any non-chroma background, treat the generation as failed. Do not present it as complete. Ask the user whether to spend another paid retry, then reuse the base template and add:

```text
Previous attempt failed because the background was not clean chroma key. Correct this strictly: the entire canvas background must be a uniform {chroma} matte with no environment, no floor, no wall, no lighting, and no shadows. If needed, simplify the motion rather than adding any scene detail.
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
