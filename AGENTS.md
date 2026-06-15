# Repository Guidelines

## Project Structure & Module Organization

This repository contains `animeskill`, a Codex/Cursor-oriented skill for generating short chroma-key character animation clips with xAI Grok Imagine.

- `skills/animeskill/SKILL.md` is the primary Codex skill instruction file.
- `skills/animeskill/scripts/` contains executable helpers, currently the xAI video generator CLI.
- `skills/animeskill/references/` stores API and prompting notes loaded only when needed.
- `skills/animeskill/agents/openai.yaml` contains UI metadata for Codex skill listings.
- `.cursor/rules/` mirrors the workflow for Cursor users.
- `docs/agent-install-prompts.md` contains ready-to-send installation prompts for other agents.
- `install.ps1` installs the Codex skill directly from GitHub on Windows.

Keep skill instructions concise. Put detailed provider notes in `references/` and deterministic automation in `scripts/`.

## Build, Test, and Development Commands

- `python skills/animeskill/scripts/generate_xai_video.py --help`: inspect CLI options.
- `python skills/animeskill/scripts/generate_xai_video.py ... --dry-run`: validate inputs, build the prompt, and estimate cost without calling xAI.
- `powershell -ExecutionPolicy Bypass -File install.ps1`: test Windows skill installation from GitHub.
- `python C:\Users\nilso\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/animeskill`: validate Codex skill metadata when developing locally on this machine.

No package manager is required yet. Add one only when the project needs distributable tooling.

## Coding Style & Naming Conventions

Use plain Python 3 standard-library code for scripts unless a dependency clearly pays for itself. Keep files ASCII, use 4-space indentation, and prefer descriptive snake_case names.

Skill folder names must stay lowercase hyphen-case when new skills are added. This skill is intentionally named `animeskill` to match the user-facing invocation.

## Testing Guidelines

Use dry runs for routine validation. For paid API tests, set `XAI_API_KEY`, use `480x480`, `1s`, and pass `--yes` only after reviewing the cost estimate.

Do not commit generated videos, source character images, API responses with secrets, or temporary downloaded assets.

## Commit & Pull Request Guidelines

Use concise imperative commit messages such as `Add xAI video helper` or `Document agent install prompts`.

Pull requests should describe the workflow change, include dry-run output or validation notes, and call out any paid API test performed.

## Security & Configuration Tips

Store `XAI_API_KEY` in the local environment, never in files committed to the repo. Before generation, always show the estimated cost and ask for explicit confirmation.
