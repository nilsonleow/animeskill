# Agent Install Prompts

Use these prompts when asking Codex, Cursor, or another coding agent to install Animeskill from GitHub.

## Codex Skill Install

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

## Cursor Rule Install

```text
Install the Animeskill Cursor rule from https://github.com/nilsonleow/animeskill.

Steps:
1. Clone or download the repository into a temporary directory.
2. Copy .cursor/rules/animeskill.mdc into this project's .cursor/rules/ directory.
3. If this project does not have .cursor/rules/, create it.
4. Do not copy generated videos, .env files, or Git metadata.
5. Confirm the rule file path when done.
```

## Verification Prompt

```text
Verify that Animeskill is installed correctly.

Check:
1. The Codex skill exists at ~/.codex/skills/animeskill or %USERPROFILE%\.codex\skills\animeskill.
2. SKILL.md, agents/openai.yaml, references/, and scripts/generate_xai_video.py are present.
3. The CLI help command runs:
   python <skill-path>/scripts/generate_xai_video.py --help
4. No API call is made during verification.
```
