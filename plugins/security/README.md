# ajbm-security

Security guardrails for Claude Code. Blocks dangerous bash commands and sensitive file access.

## Installation

```bash
/plugin marketplace add ajbmachon/ajbm-skills
/plugin install ajbm-security@ajbm
```

## What It Does

The `smart-guard` PreToolUse hook blocks:

**Dangerous Bash Commands:**
- `rm -rf /` and similar destructive patterns
- Fork bombs
- Disk wiping commands

**Sensitive File Access:**
- `.env` files
- `.ssh/` directory and keys
- AWS/GCP/Azure credentials
- Private keys and certificates
- Password files

## Enable/Disable

Use native Claude Code plugin controls:

```bash
/plugin  # Opens plugin menu → Enable/Disable
```

- **Enable plugin** = security guardrails active
- **Disable plugin** = security guardrails inactive

## License

MIT
