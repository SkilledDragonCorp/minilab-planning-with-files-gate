# Security Policy

**Built by [SkilledDragon LLC](https://skilleddragon.com)**

This is a **SkilledDragon educational minilab**, not a production product. We do **not** maintain these repos on a regular schedule and we do **not** operate a vulnerability response program for them.

## Contact

General questions: **hello@skilleddragon.com**  
Do not use a dedicated security mailbox for this repo — none exists.

## If you find an issue

- Prefer reporting **upstream** when the issue is in [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files).
- For something specific to this minilab’s scripts or CI, you may email hello@skilleddragon.com. There is **no SLA**, and we may not patch or reply quickly.

## Supported versions

Only the commit currently on `main` is considered current for this educational lab.

## Secret handling

- Never commit `.env`, API keys, or tokens.
- This lab is **keyless** — no API keys are required for CI or local pytest.
- Secrets, if you add any locally, must come only from environment variables.

## Tooling pins

| Control | Pin |
| --- | --- |
| Upstream | `OthmanAdi/planning-with-files` @ `ff349ebe322b4f86c3416a6fbcde515f1de32e8b` (MIT) |
| skills CLI | `skills@1.7.2` |
| gitleaks | `v8.30.1` (pre-commit hook + CI binary with SHA256 verify) |
| osv-scanner | `v2.7.0` (upstream Node lockfiles) |
| Python audit | `uv run pip-audit` |

## Hooks warning

The upstream skill ships lifecycle hook scripts. Review any `.claude/settings.json` changes before enabling hooks in a real project.

Use at your own risk. Pin versions, review the code, and treat this as sample material.
