# AUTOMATION ENGINE — Nectar Suprema
## Módulo: Execution Core for Sales Automation

**Módulo de IA:** `automation-engine`  
**Função:** Executor autônomo de automação de vendas — conduz a jornada completa do lead ao pós-venda  
**Uso:** Webhooks, sequências de email, remarketing, CRM, pixels de rastreamento  
**Status:** ✅ Ativo  
**Versão:** 1.0.0  
**Integrado com:** Nexus Core, Sovereign Entity, Mirror Protocol, Nov API

---

## 1. Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                  AUTOMATION ENGINE                       │
│                                                          │
│  wf_lead_capture  → wf_purchase  → wf_remarketing       │
│         ↓                ↓              ↓               │
│  Webhooks Handler  →  CRM Update  →  Pixel Fire         │
│         ↓                ↓              ↓               │
│  Email Sequence   →  Delivery    →  Schedule Manager   │
│                                                          │
│  Comandos: /automatizar, /novo-nicho, /status-vendas   │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Workflows

| WF | Nome | Trigger | Plataforma |
|---|---|---|---|
| WF-01 | Lead Capture | Form submit | Kiwify/Hotmart landing |
| WF-02 | Purchase Confirmed | Webhook compra.aprovada | Kiwify/Hotmart |
| WF-03 | Remarketing Non-Buyer | Cron D+8 sem compra | Internal |
| WF-04 | Cart Abandoned | Pixel event | Facebook/Google |
| WF-05 | Post-Sale Upsell | D+3 after purchase | Internal |

---

## 3. Comandos

| Comando | Descrição |
|---|---|
| `/automatizar [nicho]` | Ativar automação completa para novo nicho |
| `/status-vendas` | Ver métricas de automação (conversões, envios) |
| `/novo-nicho [nome]` | Configurar automação para nicho específico |
| `/parar-automatizacao` | Desativar workflows ativos |
| `/testar-webhook [kiwify\|hotmart]` | Simular webhook para teste |
| `/verificar-fila` | Checar emails pendentes na fila |
| `/trigger-sequencia [email] [dia]` | Forçar envio de email específico |

---

## 4. Estrutura de Pastas

```
automation-engine/
├── webhooks/
│   ├── kiwify_handler.py      # Webhook Kiwify
│   ├── hotmart_handler.py     # Webhook Hotmart
│   └── webhook_router.py      # Roteador central
├── email/
│   ├── sender.py             # Motor de envio
│   ├── templates/            # Templates PHP/HTML
│   └── scheduler.py          # Gerenciador de fila
├── crm/
│   └── rdstation.py          # Cliente RD Station API
├── pixel/
│   ├── facebook.py           # Facebook Pixel
│   └── google_analytics.py   # GA4 Events
├── commands/
│   ├── automate.py           # /automatizar
│   ├── status.py             # /status-vendas
│   ├── niche.py              # /novo-nicho
│   └── test.py               # /testar-webhook
├── nexus_integration.py      # Integração Nexus Core
├── mirror_logger.py          # Mirror Protocol logging
├── automation_core.py        # Controladora central
└── AUTOMATION_ENGINE.md      # Este arquivo
```

---

## 5. Integrações

### Nexus Core
- Busca dados de leads no Nexus Core
- Reporta conversões para análise preditiva
- Consulta pipeline de vendas

### Sovereign Entity
- Executa comandos autonomously
- Opera sem intervenção humana
- Reporta status para dashboard

### Mirror Protocol
- Log de todas as ações em `mirror-protocol/`
- Auto-reflexão: analisa métricas e otimiza
- Preserva histórico de workflows

### Nov API
- Exposto como endpoint FastAPI `/automations/*`
- Webhook receiver integrado
- Status endpoint `/automations/status`

---

## 6. Configuração

### Nichos Suportados
- `energia-solar` — energia solar fotovoltaica
- `acessorios-celular` — capas, chargers, cabos
- `iluminacao-led` — tiras LED, painéis
- `pets` — produtos para animais
- `organizacao` — organizadores domésticos
- `generic` — template padrão

### Variáveis de Ambiente
```
KIWIFY_API_KEY
KIWIFY_PRODUCT_ID
HOTMART_WEBHOOK_TOKEN
HOTMART_PRODUCT_ID
RD_STATION_API_KEY
RD_STATION_WORKSPACE_UUID
SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
FACEBOOK_PIXEL_ID
FACEBOOK_ACCESS_TOKEN
```

---

## 7. Endpoints (via Nov API)

```
POST /automations/webhook/kiwify     → Receber webhook Kiwify
POST /automations/webhook/hotmart    → Receber webhook Hotmart
POST /automations/lead              → Capturar lead
GET  /automations/status             → Status geral
GET  /automations/queue             → Emails na fila
POST /automations/send/[email]      → Forçar envio
```

---

*Automation Engine — Nectar Suprema*
*Versão 1.0.0 — 2025*