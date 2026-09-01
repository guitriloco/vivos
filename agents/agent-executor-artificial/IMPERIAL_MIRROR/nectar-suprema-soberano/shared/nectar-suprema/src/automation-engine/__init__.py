# Automation Engine — Nexus Module
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   AUTOMATION ENGINE — SOVEREIGN MODULE                       ║
║                         Nexu$ Automa+ion Core v1.0                           ║
║                                                                              ║
║  Função: Motor central de automação de vendas e jornada do cliente          ║
║  Uso: Execução autônoma de workflows de marketing, CRM e entrega            ║
║  Status: ✅ Ativo                                                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝

MÓDULOS:
  ├── webhooks/     → Receptor de webhooks Kiwify/Hotmart + Pixel events
  ├── email/        → Motor de envio e templates de email
  ├── scheduler/    → Queue de emails agendados + cron workers
  ├── crm/          → Integração RD Station + tags + scoring
  ├── pixel/        → Facebook Pixel + Google Analytics events
  └── commands/     → Comandos do sistema (GitHub Issues compatible)

JORNADA DO CLIENTE:
  Lead → Captura → Nutrição (7 dias) → Compra → Entrega → Upsell → Remarketing

NICHOS SUPORTADOS:
  energia_solar | acessorios_celular | iluminacao_led | pets | organizacao

EXEMPLO DE USO:
  from automation_engine import AutomationEngine
  engine = AutomationEngine(niche='energia_solar')
  engine.capture_lead(email='cliente@teste.com', name='João', utm_params={...})
  engine.process_purchase(email='cliente@teste.com', platform='kiwify', amount=97)
"""

from .engine import AutomationEngine
from .workflows import WorkflowRunner
from .niche_config import NICHE_CONFIGS

__all__ = ['AutomationEngine', 'WorkflowRunner', 'NICHE_CONFIGS']