# Animeskill

Animeskill is a reusable agent skill for turning a static character image into a short chroma-key animation clip for later sprite-sheet conversion. The first provider target is xAI Grok Imagine image-to-video.

Current project constraints:

- Durations: `1`, `2`, or `3` seconds.
- Sizes: `480x480` or `720x720`.
- Chroma keys: `#00FF00` or `#FF00FF`.
- Output: MP4 video, no special post-processing by default.

## Repository Layout

```text
skills/animeskill/
  SKILL.md                  # Codex skill instructions
  agents/openai.yaml        # Codex UI metadata
  references/               # Provider and prompting notes
  scripts/generate_xai_video.py
.cursor/rules/              # Cursor-facing workflow notes
```

## Requirements

- Python 3.10+.
- xAI API key with billing enabled.
- `XAI_API_KEY` set in your shell before paid generation.

PowerShell:

```powershell
$env:XAI_API_KEY = "xai-..."
```

That command affects only the current PowerShell session. To make the key available to future agent shells, set it as a user environment variable and restart the agent app:

```powershell
[Environment]::SetEnvironmentVariable("XAI_API_KEY", "xai-...", "User")
```

## Install For Codex

Copy or symlink `skills/animeskill` into your Codex skills directory.

PowerShell copy example:

```powershell
Copy-Item -Recurse .\skills\animeskill "$env:USERPROFILE\.codex\skills\animeskill"
```

Then start a new Codex thread and invoke it with `$animeskill`, for example:

```text
Use $animeskill to animate @person.png into a 2-second side-view walk cycle on #00FF00 at 720x720.
```

## Install From An Agent Prompt

You can ask an agent with shell access to install Animeskill directly from GitHub. Give it this prompt:

```text
Install the Codex skill from https://github.com/nilsonleow/animeskill.

Steps:
1. Clone or download the repository into a temporary directory.
2. Copy the folder skills/animeskill into my local Codex skills directory:
   - Windows: %USERPROFILE%\.codex\skills\animeskill
   - macOS/Linux: ~/.codex/skills/animeskill
3. If the destination folder already exists, replace it instead of copying into it; avoid creating nested paths like animeskill/animeskill.
4. Preserve the internal folders: SKILL.md, agents/, references/, and scripts/.
5. Do not copy generated videos, .env files, or Git metadata.
6. After installation, verify that SKILL.md exists in the destination.
7. Tell me how to set XAI_API_KEY and remind me that paid generations require cost confirmation.
```

For Cursor, use this prompt:

```text
Install the Animeskill Cursor rule from https://github.com/nilsonleow/animeskill.

Steps:
1. Clone or download the repository into a temporary directory.
2. Copy .cursor/rules/animeskill.mdc into this project's .cursor/rules/ directory.
3. If this project does not have .cursor/rules/, create it.
4. Do not copy generated videos, .env files, or Git metadata.
5. Confirm the rule file path when done.
```

## Install For Cursor

Copy or keep `.cursor/rules/animeskill.mdc` in the target project. Cursor should then apply the workflow when you ask for Animeskill-style character animation.

## CLI Usage

Dry-run first to validate the prompt and estimate cost:

```powershell
python .\skills\animeskill\scripts\generate_xai_video.py `
  --image .\person.png `
  --action "side-view walk cycle with clear alternating steps" `
  --duration 2 `
  --size 720x720 `
  --chroma "#00FF00" `
  --output .\out\walk.mp4 `
  --dry-run
```

Run a paid generation after reviewing the estimate:

```powershell
python .\skills\animeskill\scripts\generate_xai_video.py `
  --image .\person.png `
  --action "side-view walk cycle with clear alternating steps" `
  --duration 2 `
  --size 720x720 `
  --chroma "#00FF00" `
  --output .\out\walk.mp4
```

Use `--yes` only when automation should skip the interactive cost confirmation.

## Cost Defaults

The skill estimates `grok-imagine-video` cost as:

- `480x480`: `$0.05/sec + $0.002` input image.
- `720x720`: `$0.07/sec + $0.002` input image.

Every retry can incur another charge.
