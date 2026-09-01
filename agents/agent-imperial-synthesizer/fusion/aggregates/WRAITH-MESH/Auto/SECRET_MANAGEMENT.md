# Empire Security — Secret Management Runbook

## Incident: PAT Exposed in Message History

**Date:** 2026-05-04
**Exposure:** A GitHub PAT was inadvertently shared in team chat messages. The token value has been scrubbed from git history via `git filter-repo`.
**Status:** ⚠️ Requires manual revocation at GitHub Settings

---

## Immediate Actions Required (Manual)

### 1. Revoke the exposed PAT
Go to: **https://github.com/settings/tokens**

1. Log in as `guitriloco`
2. Find the token associated with this account (it will be the one listed as `guitriloco`)
3. Click **Revoke** — confirm immediately

### 2. Generate a replacement fine-grained PAT (if needed for external tool access)
Go to: **https://github.com/settings/tokens/new**

- **Name:** `empire-ci-2025`
- **Expiration:** 30 days
- **Scopes:** `repo` (for git operations), `workflow` (for Actions)
- **Repository access:** Only `guitriloco/Auto`
- Store the new token in **GitHub Actions Secrets** using `gh secret set` or a vault — **never in chat or code**

---

## Current Pipeline Security Posture

The vulnerability scanning pipeline in `guitriloco/Auto` uses **zero custom secrets**:

| Mechanism | Why It's Safe |
|-----------|--------------|
| `GITHUB_TOKEN` (auto-injected) | Provided by GitHub Actions at runtime — never stored in code, chat, or secrets |
| `gh` CLI authenticated session | Stored locally at `~/.config/gh/hosts.yml` — not in repo |
| No hardcoded credentials | Workflow uses `${{ github.token }}` and `${{ secrets.GITHUB_TOKEN }}` |

The `AUTOREPO_GH_TOKEN` GitHub Actions secret was **deleted** as it was redundant.

---

## Vault Integration (Recommended)

For long-term secret management, integrate **HashiCorp Vault** or **GitHub Advanced Security**:

### Option A: GitHub Advanced Security (GHAS) + Secrets Scanning
- Enable secret scanning at: `https://github.com/guitriloco/Auto/settings/security_analysis`
- Push protection will block commits containing detected secrets

### Option B: HashiCorp Vault
```bash
# Store PAT in Vault
vault kv put secret/empire/github token="ghp_NEW_TOKEN_HERE"

# Retrieve at runtime in CI
vault kv get -field=token secret/empire/github
```

---

## Don'ts (Permanent Policy)

| ❌ Never Do | ✅ Instead |
|-------------|-----------|
| Paste PATs in team chat | Use `gh secret set` via authenticated CLI |
| Store PATs in environment variables in code | Use GitHub Actions Secrets or Vault |
| Commit `.env`, `config.json` with credentials | Add to `.gitignore`, use secret manager |
| Use the same PAT across repos | Use fine-grained PATs scoped per-repo |
