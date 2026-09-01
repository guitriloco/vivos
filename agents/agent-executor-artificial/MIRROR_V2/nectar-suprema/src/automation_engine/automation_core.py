"""
automation_core.py — Automation Engine Core
Nectar Suprema — Execution Module for Sales Automation

Integra com: Nexus Core, Sovereign Entity, Mirror Protocol, Nov API
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

# ─────────────────────────────────────────────────────────────────────────────
# Tipos e Enum
# ─────────────────────────────────────────────────────────────────────────────

class WorkflowStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Platform(Enum):
    KIWIFY = "kiwify"
    HOTMART = "hotmart"
    RDSTATION = "rdstation"
    FACEBOOK = "facebook"
    GOOGLE = "google"
    SMTP = "smtp"

class Niche(Enum):
    ENERGIA_SOLAR = "energia-solar"
    ACESSORIOS_CELULAR = "acessorios-celular"
    ILUMINACAO_LED = "iluminacao-led"
    PETS = "pets"
    ORGANIZACAO = "organizacao"
    GENERIC = "generic"

# ─────────────────────────────────────────────────────────────────────────────
# Workflow Types
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class WorkflowResult:
    workflow_id: str
    status: WorkflowStatus
    email: str
    actions_triggered: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class Lead:
    email: str
    name: str
    niche: Niche = Niche.GENERIC
    lifecycle_stage: str = "lead"
    tags: List[str] = field(default_factory=list)
    utm_source: str = ""
    utm_medium: str = ""
    utm_campaign: str = ""
    utm_content: str = ""
    score: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

# ─────────────────────────────────────────────────────────────────────────────
# AutomationCore — Controladora Central
# ─────────────────────────────────────────────────────────────────────────────

class AutomationCore:
    """
    AutomationCore — Motor de automação de vendas.
    Executa workflows de forma autônoma e integra com todos os módulos do NS.
    """

    def __init__(self, niche: Niche = Niche.GENERIC):
        self.niche = niche
        self.log_file = self._get_log_path()
        self.queue_file = self._get_queue_path()
        self.conversions_file = self._get_conversions_path()

        self.kiwify_api_key = os.getenv("KIWIFY_API_KEY", "")
        self.hotmart_token = os.getenv("HOTMART_WEBHOOK_TOKEN", "")
        self.rdstation_key = os.getenv("RD_STATION_API_KEY", "")
        self.rdstation_workspace = os.getenv("RD_STATION_WORKSPACE_UUID", "")
        self.fb_pixel_id = os.getenv("FACEBOOK_PIXEL_ID", "")
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.seudominio.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")

        self._setup_logging()

    # ─────────────────────────────────────────────────────────────────────────
    # WORKFLOWS
    # ─────────────────────────────────────────────────────────────────────────

    def wf01_lead_capture(self, name: str, email: str, utm_params: Dict[str, str] = None) -> WorkflowResult:
        """
        WF-01: Captura de Lead (isca digital)
        1. Cadastra no CRM (RD Station)
        2. Envia Email-01 Boas-vindas
        3. Agenda sequência 7 dias (D+2 a D+8)
        4. Trigger Facebook Pixel Lead
        """
        self.log("WF-01", f"Lead capturado: {email}", {"name": name, "utm": utm_params or {}})

        result = WorkflowResult(
            workflow_id="WF-01",
            status=WorkflowStatus.ACTIVE,
            email=email,
            actions_triggered=["crm_register", "email_01_sent", "sequence_scheduled", "pixel_lead"]
        )

        try:
            # 1. CRM — criar lead
            self._crm_register_lead(email, name, utm_params or {})
            result.actions_triggered.append("crm_register_ok")

            # 2. Enviar Email-01
            self._send_email(email, name, template="email_01_boasvindas", subject="Sua lista chegou! 📦")
            result.actions_triggered.append("email_01_sent_ok")

            # 3. Agendar sequência 7 dias
            self._schedule_email_sequence(email, name)
            result.actions_triggered.append("sequence_scheduled_ok")

            # 4. Trigger Pixel
            self._pixel_fire("Lead", {"content_category": "lead_quente"})
            result.actions_triggered.append("pixel_fired_ok")

            result.status = WorkflowStatus.COMPLETED
            self.log("WF-01", f"WF-01 completo: {email}", result.actions_triggered)

        except Exception as e:
            result.status = WorkflowStatus.FAILED
            result.metadata["error"] = str(e)
            self.log("WF-01-ERROR", str(e), {"email": email})

        return result

    def wf02_purchase_confirmed(
        self,
        email: str,
        name: str,
        product: str,
        price: float,
        platform: Platform
    ) -> WorkflowResult:
        """
        WF-02: Compra Confirmada
        1. Atualizar CRM (status=comprador, tags)
        2. Enviar email de confirmação + entrega
        3. Cancelar sequências ativas de venda
        4. Trigger Facebook Pixel Purchase
        5. Log de conversão
        """
        self.log("WF-02", f"Compra confirmada: {email} | Plataforma: {platform.value}", {
            "product": product,
            "price": price
        })

        result = WorkflowResult(
            workflow_id="WF-02",
            status=WorkflowStatus.ACTIVE,
            email=email,
            metadata={"product": product, "price": price, "platform": platform.value}
        )

        try:
            # 1. CRM update
            self._crm_update_purchase(email)
            result.actions_triggered.append("crm_updated_ok")

            # 2. Email confirmação
            self._send_email(
                email, name,
                template="purchase_confirmation",
                subject=f"🎉 Sua compra foi confirmada! Acesso imediato",
                product=product, platform=platform.value
            )
            result.actions_triggered.append("confirmation_email_sent")

            # 3. Cancelar sequências ativas
            self._cancel_active_sequences(email)
            result.actions_triggered.append("sequences_cancelled")

            # 4. Pixel Purchase
            self._pixel_fire("Purchase", {"value": price, "currency": "BRL"})
            result.actions_triggered.append("pixel_purchase_fired")

            # 5. Log conversão
            self._log_conversion(email, price, platform.value)
            result.actions_triggered.append("conversion_logged")

            result.status = WorkflowStatus.COMPLETED
            self.log("WF-02", f"WF-02 completo: {email}", result.actions_triggered)

        except Exception as e:
            result.status = WorkflowStatus.FAILED
            result.metadata["error"] = str(e)
            self.log("WF-02-ERROR", str(e), {"email": email})

        return result

    def wf03_remarketing_nonbuyer(self, email: str, name: str) -> WorkflowResult:
        """
        WF-03: Remarketing — Lead que completou sequência sem comprar
        1. Mover tag para remarketing_1
        2. Agenda sequência D+10, D+14, D+21
        """
        self.log("WF-03", f"Iniciando remarketing: {email}")

        result = WorkflowResult(
            workflow_id="WF-03",
            status=WorkflowStatus.ACTIVE,
            email=email
        )

        try:
            # 1. CRM: atualizar tag
            self._crm_replace_tag(email, "wf_01_ativo", "remarketing_1")
            result.actions_triggered.append("crm_tag_updated")

            # 2. Agenda sequência remarketing
            self._schedule_remarketing_sequence(email, name)
            result.actions_triggered.append("remarketing_sequence_scheduled")

            result.status = WorkflowStatus.COMPLETED

        except Exception as e:
            result.status = WorkflowStatus.FAILED
            result.metadata["error"] = str(e)

        return result

    def wf04_cart_abandoned(self, email: str, name: str, cart_value: float) -> WorkflowResult:
        """
        WF-04: Carrinho Abandonado
        1. Adicionar tag carrinho_abandonado
        2. Email em 1h
        3. Email em 24h (urgência)
        """
        self.log("WF-04", f"Carrinho abandonado: {email} | Valor: {cart_value}")

        result = WorkflowResult(
            workflow_id="WF-04",
            status=WorkflowStatus.ACTIVE,
            email=email,
            metadata={"cart_value": cart_value}
        )

        try:
            # 1. CRM tag
            self._crm_add_tag(email, "carrinho_abandonado")
            result.actions_triggered.append("crm_tag_added")

            # 2. Email 1h
            self._schedule_email(
                email, name,
                template="email_carrinho_abandonado",
                subject="Esqueceu algo? 🔥",
                send_at=datetime.now() + timedelta(hours=1)
            )
            result.actions_triggered.append("recovery_email_1h_scheduled")

            # 3. Email 24h
            self._schedule_email(
                email, name,
                template="email_carrinho_urgencia",
                subject="Ainda está lá... mas não por muito tempo ⏰",
                send_at=datetime.now() + timedelta(hours=24)
            )
            result.actions_triggered.append("recovery_email_24h_scheduled")

            result.status = WorkflowStatus.COMPLETED

        except Exception as e:
            result.status = WorkflowStatus.FAILED
            result.metadata["error"] = str(e)

        return result

    def wf05_post_sale_upsell(self, email: str, name: str, product: str) -> WorkflowResult:
        """
        WF-05: Upsell pós-venda
        1. Email upsell D+3
        2. Email cross-sell D+7
        """
        self.log("WF-05", f"Upsell pós-venda: {email}")

        result = WorkflowResult(
            workflow_id="WF-05",
            status=WorkflowStatus.ACTIVE,
            email=email,
            metadata={"product": product}
        )

        try:
            self._schedule_email(
                email, name,
                template="email_upsell",
                subject="Um presente só pra você... 🎁",
                send_at=datetime.now() + timedelta(days=3)
            )
            result.actions_triggered.append("upsell_email_scheduled")

            self._schedule_email(
                email, name,
                template="email_cross_sell",
                subject="Você conhece outro nicho? 👀",
                send_at=datetime.now() + timedelta(days=7)
            )
            result.actions_triggered.append("cross_sell_email_scheduled")

            result.status = WorkflowStatus.COMPLETED

        except Exception as e:
            result.status = WorkflowStatus.FAILED
            result.metadata["error"] = str(e)

        return result

    # ─────────────────────────────────────────────────────────────────────────
    # HANDLERS DE WEBHOOK
    # ─────────────────────────────────────────────────────────────────────────

    def handle_kiwify_webhook(self, data: Dict[str, Any]) -> WorkflowResult:
        """Processa webhook Kiwify"""
        event = data.get("event", "")
        email = data.get("email") or data.get("customer", {}).get("email", "")
        name = data.get("customer", {}).get("name", "")
        product = data.get("product", {}).get("name", "Lista Quente")
        price = float(data.get("amount") or data.get("product", {}).get("price", 97))

        if event == "compra.aprovada":
            return self.wf02_purchase_confirmed(email, name, product, price, Platform.KIWIFY)
        elif event == "compra.reprovada":
            return self._wf02_rejected(email)
        elif event == "acesso.concedido":
            return self._wf02_access_granted(email, name, product, Platform.KIWIFY)

        return WorkflowResult("WF-KIWIFY", WorkflowStatus.FAILED, email, [], {"error": f"Evento desconhecido: {event}"})

    def handle_hotmart_webhook(self, data: Dict[str, Any]) -> WorkflowResult:
        """Processa webhook Hotmart"""
        event = data.get("event") or data.get("event_type", "")

        # Normalizar estrutura Hotmart
        hotmart_data = self._normalize_hotmart_data(data)
        email = hotmart_data.get("email", "")
        name = hotmart_data.get("name", "")
        product = hotmart_data.get("product", "Lista Quente")
        price = float(hotmart_data.get("price", 97))

        event = self._normalize_hotmart_event(event)

        if event == "PURCHASE_APPROVED":
            return self.wf02_purchase_confirmed(email, name, product, price, Platform.HOTMART)
        elif event == "PURCHASE_REFUNDED":
            return self._wf02_rejected(email)
        elif event == "MEMBER_ACCESS_PROVIDED":
            return self._wf02_access_granted(email, name, product, Platform.HOTMART)

        return WorkflowResult("WF-HOTMART", WorkflowStatus.FAILED, email, [], {"error": f"Evento desconhecido: {event}"})

    # ─────────────────────────────────────────────────────────────────────────
    # COMANDOS
    # ─────────────────────────────────────────────────────────────────────────

    def command_automate(self, niche: str) -> Dict[str, Any]:
        """
        /automatizar [nicho]
        Ativa automação completa para novo nicho
        """
        self.niche = Niche(niche) if niche in [e.value for e in Niche] else Niche.GENERIC
        self.log("CMD-AUTOMATE", f"Automação ativada para nicho: {self.niche.value}")

        return {
            "status": "ok",
            "niche": self.niche.value,
            "workflows_activated": ["WF-01", "WF-02", "WF-03", "WF-04", "WF-05"],
            "message": f"Automação ativada para nicho: {self.niche.value}"
        }

    def command_status(self) -> Dict[str, Any]:
        """
        /status-vendas
        Retorna métricas de automação
        """
        stats = self._get_stats()
        queue = self._get_queue()

        return {
            "status": "ok",
            "niche": self.niche.value,
            "timestamp": datetime.now().isoformat(),
            "stats": stats,
            "queue_size": len(queue),
            "pending_emails": [e["email"] for e in queue if e.get("status") == "pending"]
        }

    def command_trigger_sequence(self, email: str, day: int) -> Dict[str, Any]:
        """
        /trigger-sequencia [email] [dia]
        Força envio de email específico
        """
        templates = {
            1: ("email_01_boasvindas", "Sua lista chegou! 📦"),
            2: ("email_02_problema", "Você se identifica com isso?"),
            3: ("email_03_solucao", "O que você precisa pra fazer dropshipping funcionar"),
            4: ("email_04_provasocial", "Olha o que está acontecendo com quem já usa 📣"),
            5: ("email_05_urgencia", "Isso expira em breve ⚠️"),
            6: ("email_06_fechamento", "Última chamada 🚨"),
            7: ("email_07_final", "Última chance 🚨"),
        }

        if day not in templates:
            return {"status": "error", "message": f"Dia {day} não existe. Use 1-7."}

        template, subject = templates[day]
        try:
            self._send_email(email, "Cliente", template=template, subject=subject)
            return {"status": "ok", "email": email, "day": day, "template": template}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ─────────────────────────────────────────────────────────────────────────
    # HELPERS PRIVADOS
    # ─────────────────────────────────────────────────────────────────────────

    def _crm_register_lead(self, email: str, name: str, utm_params: Dict) -> None:
        """Registra lead no RD Station"""
        # Implementação: POST para RD Station API
        self.log("CRM", f"Registrando lead: {email}", {"name": name, "utm": utm_params})
        # Em produção: chamada HTTP real

    def _crm_update_purchase(self, email: str) -> None:
        """Atualiza lead para status comprador"""
        self.log("CRM", f"Atualizando para comprador: {email}")

    def _crm_add_tag(self, email: str, tag: str) -> None:
        self.log("CRM", f"Adicionando tag {tag} a {email}")

    def _crm_replace_tag(self, email: str, old_tag: str, new_tag: str) -> None:
        self.log("CRM", f"Trocando tag {old_tag} → {new_tag} em {email}")

    def _cancel_active_sequences(self, email: str) -> None:
        self.log("CANCEL", f"Cancelando sequências ativas: {email}")

    def _send_email(self, email: str, name: str, template: str, subject: str, **kwargs) -> None:
        """Envia email imediato via SMTP"""
        self.log("EMAIL", f"Enviando {template} para {email}: {subject}")

    def _schedule_email(self, email: str, name: str, template: str, subject: str, send_at: datetime) -> None:
        """Agenda email para data futura"""
        queue = self._get_queue()
        queue.append({
            "id": f"email_{len(queue)}_{datetime.now().timestamp()}",
            "email": email,
            "name": name,
            "template": template,
            "subject": subject,
            "send_at": send_at.isoformat(),
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            **kwargs
        })
        self._save_queue(queue)
        self.log("SCHEDULE", f"Email agendado: {template} para {email} em {send_at.isoformat()}")

    def _schedule_email_sequence(self, email: str, name: str) -> None:
        """Agenda sequência 7 dias"""
        sequence = {
            2: ("email_02_problema", "Você se identifica com isso?"),
            4: ("email_03_solucao", "O que você precisa pra fazer dropshipping funcionar"),
            5: ("email_04_provasocial", "Olha o que está acontecendo com quem já usa 📣"),
            6: ("email_05_urgencia", "Isso expira em breve ⚠️"),
            7: ("email_06_fechamento", "Última chamada 🚨"),
            8: ("email_07_final", "Última chance 🚨"),
        }
        for day, (template, subject) in sequence.items():
            send_at = datetime.now() + timedelta(days=day)
            self._schedule_email(email, name, template, subject, send_at)

    def _schedule_remarketing_sequence(self, email: str, name: str) -> None:
        """Agenda sequência remarketing D+10, D+14, D+21"""
        sequence = {
            10: ("email_remarketing_01", "Uma oferta exclusiva pra você..."),
            14: ("email_remarketing_02", "Como o João fez R$5.000 em 30 dias"),
            21: ("email_remarketing_03", "É agora ou nunca ⏰"),
        }
        for day, (template, subject) in sequence.items():
            send_at = datetime.now() + timedelta(days=day)
            self._schedule_email(email, name, template, subject, send_at)

    def _pixel_fire(self, event_name: str, data: Dict[str, Any]) -> None:
        """Dispara pixel Facebook"""
        self.log("PIXEL", f"Facebook Pixel: {event_name}", data)

    def _log_conversion(self, email: str, price: float, platform: str) -> None:
        """Log de conversão para métricas"""
        self.log("CONVERSION", f"Conversão: {email} | R$ {price} | {platform}")

    def _wf02_rejected(self, email: str) -> WorkflowResult:
        self._crm_add_tag(email, "reembolsado")
        return WorkflowResult("WF-02", WorkflowStatus.COMPLETED, email, ["tag_added"])

    def _wf02_access_granted(self, email: str, name: str, product: str, platform: Platform) -> WorkflowResult:
        self._send_email(email, name, "product_access", "Seu acesso está pronto! 🚀", product=product, platform=platform.value)
        return WorkflowResult("WF-02", WorkflowStatus.COMPLETED, email, ["access_email_sent"])

    def _normalize_hotmart_event(self, event: str) -> str:
        mapping = {
            "purchase.approved": "PURCHASE_APPROVED",
            "subscription.approved": "SUBSCRIPTION_APPROVED",
            "purchase.refunded": "PURCHASE_REFUNDED",
            "product.access.granted": "MEMBER_ACCESS_PROVIDED",
        }
        return mapping.get(event, event)

    def _normalize_hotmart_data(self, data: Dict) -> Dict:
        return {
            "email": data.get("data", {}).get("email") or data.get("email", ""),
            "name": data.get("data", {}).get("name") or data.get("name", ""),
            "product": data.get("data", {}).get("product", {}).get("name") or data.get("product_name", ""),
            "price": data.get("data", {}).get("price", {}).get("value") or data.get("amount", 97),
        }

    # ─────────────────────────────────────────────────────────────────────────
    # FILE HELPERS
    # ─────────────────────────────────────────────────────────────────────────

    def _get_log_path(self) -> str:
        base = "/home/team/shared/nectar-suprema/logs"
        os.makedirs(base, exist_ok=True)
        return f"{base}/automation_{datetime.now().strftime('%Y-%m')}.json"

    def _get_queue_path(self) -> str:
        base = "/home/team/shared/nectar-suprema/logs"
        os.makedirs(base, exist_ok=True)
        return f"{base}/email_queue.json"

    def _get_conversions_path(self) -> str:
        base = "/home/team/shared/nectar-suprema/logs"
        os.makedirs(base, exist_ok=True)
        return f"{base}/conversions_{datetime.now().strftime('%Y-%m')}.json"

    def _get_queue(self) -> List[Dict]:
        if os.path.exists(self.queue_file):
            return json.load(open(self.queue_file))
        return []

    def _save_queue(self, queue: List[Dict]) -> None:
        json.dump(queue, open(self.queue_file, "w"), indent=2, ensure_ascii=False)

    def _get_stats(self) -> Dict:
        conv_file = self.conversions_file
        if os.path.exists(conv_file):
            conversions = json.load(open(conv_file))
            total = len(conversions)
            revenue = sum(c.get("price", 0) for c in conversions)
            return {"total_conversions": total, "total_revenue": revenue}
        return {"total_conversions": 0, "total_revenue": 0}

    def _setup_logging(self) -> None:
        os.makedirs("/home/team/shared/nectar-suprema/logs", exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            handlers=[
                logging.FileHandler("/home/team/shared/nectar-suprema/logs/automation.log"),
                logging.StreamHandler()
            ]
        )

    def log(self, tag: str, message: str, context: Dict = None) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tag": tag,
            "message": message,
            "context": context or {},
            "niche": self.niche.value
        }
        if os.path.exists(os.path.dirname(self.log_file)):
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        logging.info(f"[{tag}] {message} | {context}")

# ─────────────────────────────────────────────────────────────────────────────
# Instância Global
# ─────────────────────────────────────────────────────────────────────────────

automation_core = AutomationCore()

def get_core() -> AutomationCore:
    return automation_core