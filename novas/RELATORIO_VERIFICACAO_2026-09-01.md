# RELATÓRIO DE VERIFICAÇÃO DE INTEGRIDADE — SNAPSHOT guitriloco/vivos

**Data:** 2026-09-01 08:18 UTC | **Método:** clone fresco do GitHub + `diff -rq` recursivo contra a árvore de staging da máquina

## Branch `machine-state-snapshot` (workspace /home/team/shared) — ✅ 100%
- Arquivos: **1.844 / 1.844** idênticos
- Diferenças de conteúdo: **0**
- Commit verificado: `d4e352e`

## Branch `main` (máquina completa) — ✅ 100% (após correção)
- Verificação inicial: 39.199 / 39.204 arquivos idênticos, **0 diferenças de conteúdo**
- **5 arquivos** estavam ausentes: `agents/agent-engineer/oi/build_sandbox/` (CMakeLists.txt, wraith_engine.cpp, main.cpp, +1) e `agents/agent-engineer/oi/mutation_logs/mutation_1777255606_wraith_engine.cpp`
- **Causa:** `.gitignore` aninhado do repositório `oi` (clone dentro do home do agente) silenciosamente excluiu `build_sandbox/` e `mutation_logs/` do `git add`
- **Correção:** `git add -A -f` (força inclusão ignorando gitignores aninhados) — commit de correção no histórico
- Diretórios vazios (1.141 entradas "Only in"): comportamento normal do git — não rastreia diretórios sem arquivos; **nenhum arquivo afetado**

## Segurança
- Segredo detectado pelo GitHub Push Protection em `PHASE_13_SYNC_ENGINE.py:47` (token GitHub App `ghs_` de fase antiga): **redigido** nos snapshots e nas fontes vivas antes do push
- Excluídos do snapshot por design: `.git` (histórico), credenciais (`.git-credentials`, `.netrc`, `.ssh`, `*.pem`, `*.key`, `.env*`, `.claude*`, `.mcp.json`), caches (`__pycache__`, `*.pyc`, `.run`)

## Backup redundante
- Mesmas branches limpas também em `guitriloco/NECTAR_SYNC_TEST` (privado): `machine-state-snapshot` @ `d4e352e`, `full-machine-state` @ `612d8d9`+correções
