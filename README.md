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
  scripts/configure_xai_key.py
  scripts/generate_xai_video.py
.cursor/rules/              # Cursor-facing workflow notes
```

## Requirements

- Python 3.10+.
- xAI API key with billing enabled.
- The key available through `XAI_API_KEY` or Animeskill config.

Recommended setup:

```powershell
python .\skills\animeskill\scripts\configure_xai_key.py
```

The script prompts for the key without echoing it and stores it outside the repo at `~/.animeskill/config.json`. Set `ANIMESKILL_CONFIG` if you need a custom config path.

Temporary PowerShell-only setup:


```powershell
$env:XAI_API_KEY = "xai-..."
```

That command affects only the current PowerShell session. User-level env also works, but some agent sandboxes may run under a different Windows user:

```powershell
[Environment]::SetEnvironmentVariable("XAI_API_KEY", "xai-...", "User")
```

## Install For Codex

On Windows, install directly from GitHub in any PowerShell directory:

```powershell
$script = "$env:TEMP\install-animeskill.ps1"
Invoke-WebRequest "https://raw.githubusercontent.com/nilsonleow/animeskill/main/install.ps1" -OutFile $script
powershell -ExecutionPolicy Bypass -File $script
```

Then configure the API key:

```powershell
python "$env:USERPROFILE\.codex\skills\animeskill\scripts\configure_xai_key.py"
```

If you already cloned this repository, you can also copy or symlink `skills/animeskill` into your Codex skills directory.

Then start a new Codex thread and invoke it with `$animeskill`, for example:

```text
Use $animeskill to animate @person.png into a 2-second side-view walk cycle on #00FF00 at 720x720.
```

## Install From An Agent Prompt

You can ask an agent with shell access to install Animeskill directly from GitHub. Give it this prompt:

```text
Install the Codex skill from https://github.com/nilsonleow/animeskill.

Steps:
1. On Windows, prefer downloading and running https://raw.githubusercontent.com/nilsonleow/animeskill/main/install.ps1.
2. Otherwise, clone or download the repository into a temporary directory.
3. Copy the folder skills/animeskill into my local Codex skills directory:
   - Windows: %USERPROFILE%\.codex\skills\animeskill
   - macOS/Linux: ~/.codex/skills/animeskill
4. If the destination folder already exists, replace it instead of copying into it; avoid creating nested paths like animeskill/animeskill.
5. Preserve the internal folders: SKILL.md, agents/, references/, and scripts/.
6. Do not copy generated videos, .env files, Git metadata, __pycache__, or other cache folders.
7. After installation, verify that SKILL.md exists in the destination.
8. Ask whether I want to configure the xAI API key now. If your shell supports interactive hidden input, run scripts/configure_xai_key.py from the installed skill and let me paste the key into the hidden prompt. If interactive input is not available, do not ask me to paste the key into chat; instead tell me the exact configure command to run locally.
9. Remind me that paid generations require cost confirmation.
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

## Managed Agent Policy Blocks

Some hosted or tenant-managed agents, including Codex running inside Cursor, may block uploading private workspace files to external services such as xAI. If that happens, Animeskill cannot bypass the policy.

Use one of these options:

- Run the CLI manually from your own terminal.
- Ask an admin to allow xAI or provide an approved internal gateway.
- Use only public/non-sensitive sample images that policy allows.
- Let the agent prepare a dry-run prompt and command, then run the paid command yourself.

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

## API Key Storage

Animeskill looks for the xAI key in this order:

1. `XAI_API_KEY`.
2. `ANIMESKILL_CONFIG`, if set.
3. `~/.animeskill/config.json`.

The config file contains only:

```json
{
  "xai_api_key": "xai-..."
}
```

Do not store this file inside a project repository.

## Cost Defaults

The skill estimates `grok-imagine-video` cost as:

- `480x480`: `$0.05/sec + $0.002` input image.
- `720x720`: `$0.07/sec + $0.002` input image.

Every retry can incur another charge.
