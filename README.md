# VIVOS — Pre-Assembled Distributed Automation System (Phase 17)

A pre-assembled, verifiable automation package: one integrity-checked master bundle, a one-command
installer that refuses to install a tampered package, a documented pantheon of 35 agent roles, and
the part most repos leave out — a **truth register** stating exactly what is proven and what is not.

**Everything below is tied to a commit, a hash or an exit code. Claims that could not be reproduced
are listed as not verified, in this same README.**

---

## What's in this repository

| Path | What it is | Proof |
|---|---|---|
| `VIVOS_MASTER_BUNDLE/` | 52 files: `SHA256SUMS`, `verify_bundle.sh`, `install.sh`, `installer/vivos_master.sh`, `pantheon/` (index + 35 dossiers), `registry/`, `benchmark/`, `TRUTH_REGISTER.md`, `CAVEATS.md` | commit `77231f1` (PR #4) |
| `PANTHEON_AGENTES/` | 35 individual agent dossiers | commit `20d7de1` |
| `REGISTRO_AGENTES_V17.md` | agent registry | commit `3c3cbbf` |
| `SEAL_FINAL_V17.md` | closing seal: 5/5 deliverables, each with its evidence | commit `324b15d` (PR #5) |
| ~5,176 Python files across the tree | the system itself | `py_compile` sweep, 0 failures — PR #3, merged as `bed427b` |

## Verify it yourself (no trust required)

```bash
cd VIVOS_MASTER_BUNDLE
./verify_bundle.sh            # → "BUNDLE ÍNTEGRO — 51 arquivos verificados", exit 0
```

- **51 hashes** in `SHA256SUMS` (the sums file does not list itself — 52 files on disk).
- **The verifier fails when it should** — this is the part that makes it a proof instead of a stamp:

```bash
rm -rf /tmp/tb && cp -r . /tmp/tb && printf 'x' >> /tmp/tb/pantheon/01-engineer.md
/tmp/tb/verify_bundle.sh      # → "hash divergente: 1", FAILED, exit 1
touch /tmp/tb/ARQUIVO_INTRUSO.txt && /tmp/tb/verify_bundle.sh   # → detected, exit 1
```

- **The installer gates on the verifier before installing:**

```bash
./install.sh --dry-run        # verifies integrity first; aborts if the bundle is tampered
```

## The one measured performance number

**22.04–22.79 ns/op** — the in-memory arbitrage comparator (`benchmark/`), two independent sessions,
5×200,000 iterations, Xeon 2.90 GHz, 2 vCPU. This is **not** exchange execution latency: the engine
sends no orders; `execute_trade()` increments a counter.

## What is NOT verified

Stated plainly, because a claim you can't test is worse than no claim:

- **0.368 µs decision latency** — withdrawn. No reproducible origin; it is a literal in a legacy script, not a measurement.
- **PHI 1.618 Resonance Engine** — not verified; no such module exists in the tree.
- **Causal Collapse O(-t²)** — not verified; described, never measured.
- **7 Supreme Aggregates** — not verified.
- **35 fractal variants** — catalog entries only; functional value not verified.

## Known caveats (`VIVOS_MASTER_BUNDLE/CAVEATS.md`)

- The `EvolutionCore` class header was corrupted and reconstructed from usage (`mutation_factor = 0.01`); the file containing it is not in the bundle.
- `vivos_master.sh --dry-run` overestimates the file count (reports the whole tree; a real install copies ~1,881 files).
- Some counts in `REGISTRO_AGENTES_V17.md` are stale; the manifest (`VIVOS_SUPREME_MANIFEST.json`) is the authoritative one and is checked against disk by `verify_bundle.sh`.

## Status

Sealed and verified 2026-11-14 (`SEAL_FINAL_V17.md`). **Not for sale yet** — no checkout is
connected; this repository sells nothing today. Distribution will be via the cto.new marketplace
listing when it goes live.
