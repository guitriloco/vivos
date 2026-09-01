# Automation Engine — Nectar Suprema
## Habilidades de Automação e Comandos

### Módulos

| Módulo | Descrição | Comandos |
|---|---|---|
| `automation_core.py` | Workflows de automação de vendas (WF-01 a WF-05) | `/automatizar`, `/status-vendas`, `/trigger-sequencia` |
| `market_scanner.py` | Scanner de mercado e tendências | `/scanner-mercado`, `/scanner-trending`, `/scanner-relatorio` |
| `vvv_vault.py` | Cofre ZK para proteção de listas de fornecedores | `/vault-criptografar`, `/vault-listar`, `/vault-verificar` |

### Arquitetura

```
automation-engine/
├── automation_core.py     → Controladora de workflows (PHP + Python)
├── market_scanner.py      → Scanner de tendências e oportunidades
├── vvv_vault.py           → Proteção ZK de listas de fornecedores
├── mirror_integration.py  → Integração com Mirror Protocol
├── nexus_integration.py    → Integração com Nexus Core
└── commands/
    └── handlers.py        → Processadores de comandos
```

### Habilidades Registradas (mirror-protocol/registry.py)

- **automation_engine**: WF-01 a WF-05, webhooks Kiwify/Hotmart, CRM RD Station
- **market_scanner**: scan_niche(), scan_trending(), analyze_competition(), get_full_report()
- **vvv_vault**: encrypt_supplier_list(), decrypt_supplier_list(), verify_integrity()

### Uso via CLI

```bash
# Market Scanner
python market_scanner.py --niche energia-solar
python market_scanner.py --trending
python market_scanner.py --report pets

# VVV Vault
python vvv_vault.py --list
python vvv_vault.py --verify /path/to/file.vault.enc

# Automation Core (via API)
POST /automations/wf01_lead_capture
POST /automations/wf02_purchase_confirmed
```

### Workflows

| WF | Descrição |
|---|---|
| WF-01 | Lead Capture → CRM + Email-01 + Sequência 7 dias |
| WF-02 | Compra Confirmada → CRM update + Entrega + Pixel |
| WF-03 | Remarketing → Não-comprou D+8 → Sequência D+10/14/21 |
| WF-04 | Carrinho Abandonado → Email 1h + 24h |
| WF-05 | Upsell Pós-Venda → D+3 + D+7 |

### Logs

```
/home/team/shared/nectar-suprema/logs/automation_{YYYY-MM}.json
/home/team/shared/nectar-suprema/logs/market_scanner.log
/home/team/shared/nectar-suprema/logs/vvv_vault.log
/home/team/shared/nectar-suprema/logs/registry_executions.json
```

---

*Automation Engine — Nectar Suprema v1.0 — 2025*