# SNAPSHOT COMPLETO DA MÁQUINA — IMPÉRIO VIVOS

- **Data (UTC):** 2026-09-01 07:53:23
- **Tamanho:** 892 MB | **Arquivos:** ~39.200 | **Nenhum arquivo > 90 MB**

## Estrutura
- `shared/` — workspace completo da equipe (/home/team/shared)
- `agents/` — todos os homes dos agentes (34), incluindo workspaces próprios (IMPERIAL_MIRROR, MIRROR_V2, workspace, YIELD-SIPHON, fusion, etc.)
- `database/` — estado do banco de dados do time em JSON: tasks.json (kanban completo com resultados), agents.json (roster), config.json

## Excluídos por segurança
- `.git` (histórios — os repos originais já estão no GitHub guitriloco/*)
- Credenciais: .git-credentials, .netrc, .ssh, *.pem, *.key, id_rsa*, .env*, .config/gh, .claude*, .mcp.json
- Caches: __pycache__, *.pyc, .run (logs)
- **Scan de segredos executado:** nenhum match (Stripe/GitHub/AWS/Slack/privkeys)

## Estado no momento
- Tarefas: 21 done / 8 in-progress / 0 review
- Membros: 34 agentes; 5 working (engineer, imperial-synthesizer, master-orchestrator, sovereign-integrator, vault-guardian)
- Repos conectados: 68 (guitriloco/*)
- Finance: plano FREE — sem Stripe, nenhum produto/pagamento real
