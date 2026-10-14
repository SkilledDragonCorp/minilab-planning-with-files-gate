# minilab-planning-with-files-gate

Crash-proof planning lab: [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) plans on disk that survive `/clear` and compaction, plus an opt-in `--gated` completion gate that can emit block JSON until all phases finish.

**Built by SkilledDragon LLC — architecture-led software engineering · [skilleddragon.com](https://skilleddragon.com)**

## What was built

- Vendors upstream at `ff349ebe322b4f86c3416a6fbcde515f1de32e8b` (v3.9.0 line / master pin).
- Installs the skill into `.claude/skills/planning-with-files/` via pinned `skills@1.7.2` (`-a claude-code --copy`).
- Lab skill `.claude/skills/plan-survives-clear/` teaches the recovery ritual.
- Pytest proves: init → phase-status → fresh process recovers from files → advisory check → gated `--gate` block/allow.
- Upstream CI cohort from `.github/workflows/tests.yml` at the pin: `scripts/upstream-pytest.sh` and `scripts/upstream-vitest.sh`.

## What was tested + results

| Suite | Command | Expectation |
| --- | --- | --- |
| Lab | `uv run pytest -q` | All lab tests green (keyless) |
| Upstream pytest | `bash scripts/upstream-pytest.sh` | Verbatim `tests.yml` pytest job |
| Upstream vitest | `bash scripts/upstream-vitest.sh` | Pi + OpenCode + DSH npm/vitest jobs |
| Security | gitleaks v8.30.1, osv-scanner v2.7.0, skill frontmatter, no mirrors | Clean |

See CI on `main` after push for the recorded green run.

## Setup

```bash
# Prerequisites: Python 3.12+, uv, Bun, Node 22 (for upstream vitest)
git clone https://github.com/SkilledDragonCorp/minilab-planning-with-files-gate.git
cd minilab-planning-with-files-gate
cp .env.example .env   # no API keys; DISABLE_TELEMETRY=1
uv sync --group dev
bash scripts/fetch-upstream.sh
bash scripts/install-skill.sh
uv run pytest -q
```

Upstream one-liner (documented; lab uses the pinned local form above):

```bash
npx skills add OthmanAdi/planning-with-files --skill planning-with-files -g
```

Lab install (exact):

```bash
DISABLE_TELEMETRY=1 bun --bun x skills@1.7.2 add ./vendor/planning-with-files \
  --skill planning-with-files -a claude-code -y --copy
```

## Tutorial

1. **Install** — `bash scripts/install-skill.sh`
2. **Init** — `bash .claude/skills/planning-with-files/scripts/init-session.sh`
3. **Work** — edit code; mark phases with `phase-status.sh N complete`
4. **`/clear`** — wipe chat context (or start a new shell with no memory)
5. **Recover** — read `task_plan.md` / `progress.md` first; run `check-complete.sh`
6. **Gate (opt-in)** — `init-session.sh --gated "Gated Run"` then `echo '{}' | check-complete.sh --gate` until phases are done

### Hooks warning

The upstream skill ships lifecycle hook scripts. Review any `.claude/settings.json` changes before enabling them in a real project.

## Using these skills in Claude Code and Cursor

Both Claude Code and Cursor read agent skills from **`.claude/skills/<name>/SKILL.md`**.

- This lab installs `planning-with-files` and ships `plan-survives-clear` under that path only.
- Do **not** create `.cursor/skills` or `.agents/skills` mirrors.
- After install, open the project in Claude Code or Cursor; the skills appear from `.claude/skills/`.
- Before `/clear` or compaction, write state to disk; after, read files first (see `plan-survives-clear`).

## API keys

None. No API keys are required for CI or local lab tests.

| Key | Where | Cost |
| --- | --- | --- |
| — | — | Free / keyless |

## Telemetry

- No telemetry env var in the upstream skill scripts at the pin.
- Skills CLI telemetry is disabled via `DISABLE_TELEMETRY=1` (and `DO_NOT_TRACK=1` in CI / `.env.example`).

## License

MIT (lab). Upstream [planning-with-files](https://github.com/OthmanAdi/planning-with-files) is MIT.
