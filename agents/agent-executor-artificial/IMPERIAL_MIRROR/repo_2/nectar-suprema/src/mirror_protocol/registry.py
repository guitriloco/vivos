import httpx
import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Automation Registry — Habilidades Registradas
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Skill:
    """Representa uma habilidade/comando registrado no sistema"""
    name: str
    module: str
    description: str
    commands: List[str]
    status: str = "active"
    version: str = "1.0"
    registered_at: str = ""

@dataclass
class CommandExecution:
    """Log de execução de comando"""
    command: str
    skill: str
    args: Dict[str, Any]
    result_status: str
    timestamp: str
    duration_ms: float
    error: Optional[str] = None

class ExpansionRegistry:
    """
    ExpansionRegistry — Registro central de habilidades do Nectar Suprema.
    Mantém registro de todos os módulos, comandos e habilidades registradas.
    """

    def __init__(self):
        self.remote_callbacks: Dict[str, List[str]] = {
            "PROTOCOL_START": [],
            "PROTOCOL_COMPLETE": [],
            "ANOMALY_DETECTED": []
        }

        # Registro de habilidades
        self.skills: Dict[str, Skill] = {}
        self.executions: List[CommandExecution] = []

        # Inicializar habilidades padrão
        self._register_default_skills()

    def _register_default_skills(self) -> None:
        """Registra habilidades padrão do sistema"""

        # Automation Engine Skills
        self.register_skill(Skill(
            name="automation_engine",
            module="automation-engine",
            description="Motor de automação de vendas — workflows de lead, compra, remarketing e pós-venda",
            commands=[
                "/automatizar [nicho]",
                "/status-vendas",
                "/novo-nicho [nome]",
                "/parar-automatizacao",
                "/testar-webhook [kiwify|hotmart]",
                "/verificar-fila",
                "/trigger-sequencia [email] [dia]"
            ],
            status="active",
            registered_at=datetime.now().isoformat()
        ))

        self.register_skill(Skill(
            name="market_scanner",
            module="automation-engine/market_scanner",
            description="Scanner de mercado — tendências, concorrentes, fornecedores e oportunidades",
            commands=[
                "/scanner-mercado [nicho]",
                "/scanner-trending",
                "/scanner-concorrencia [nicho]",
                "/scanner-fornecedores [nicho]",
                "/scanner-relatorio [nicho]"
            ],
            status="active",
            registered_at=datetime.now().isoformat()
        ))

        self.register_skill(Skill(
            name="vvv_vault",
            module="automation-engine/vvv_vault",
            description="VVV Vault — proteção ZK de listas de fornecedores com criptografia e assinatura",
            commands=[
                "/vault-criptografar [arquivo]",
                "/vault-descriptografar [arquivo]",
                "/vault-verificar [arquivo]",
                "/vault-listar",
                "/vault-exportar [arquivo]"
            ],
            status="active",
            registered_at=datetime.now().isoformat()
        ))

        # Nexus Core Skills
        self.register_skill(Skill(
            name="nexus_core",
            module="nexus-core/core_v5_singularity",
            description="Nexus Core v5 — Hub preditivo de dados com auto-healing",
            commands=["/nexus-predict [input]"],
            status="active",
            registered_at=datetime.now().isoformat()
        ))

        # Sovereign Reality Skills
        self.register_skill(Skill(
            name="sovereign_reality",
            module="sovereign-entity/Sovereign_Reality",
            description="Sovereign Reality 3.0 — Unified orchestrator for global dominance",
            commands=[
                "/expandir-total [nicho]",
                "/conquista-global",
                "/pulse-status",
                "/optimize-core",
                "/vault-seal-all"
            ],
            status="active",
            registered_at=datetime.now().isoformat()
        ))

        print(f"[REGISTRY] {len(self.skills)} habilidades registradas")

    def register_skill(self, skill: Skill) -> None:
        """Registra nova habilidade"""
        self.skills[skill.name] = skill
        print(f"[REGISTRY] Habilidade registrada: {skill.name} | Comandos: {skill.commands}")

    def get_skill(self, name: str) -> Optional[Skill]:
        """Retorna habilidade por nome"""
        return self.skills.get(name)

    def list_skills(self) -> List[Dict]:
        """Lista todas as habilidades registradas"""
        return [asdict(s) for s in self.skills.values()]

    def list_commands(self) -> List[Dict]:
        """Lista todos os comandos disponíveis"""
        result = []
        for skill in self.skills.values():
            for cmd in skill.commands:
                result.append({
                    "command": cmd,
                    "skill": skill.name,
                    "module": skill.module,
                    "description": skill.description
                })
        return result

    def log_execution(self, command: str, skill: str, args: Dict, result_status: str, duration_ms: float, error: Optional[str] = None) -> None:
        """Registra execução de comando no audit trail"""
        exec_entry = CommandExecution(
            command=command,
            skill=skill,
            args=args,
            result_status=result_status,
            timestamp=datetime.now().isoformat(),
            duration_ms=duration_ms,
            error=error
        )
        self.executions.append(exec_entry)

        # Manter últimos 1000 registros
        self.executions = self.executions[-1000:]

        # Salvar em arquivo
        log_dir = "/home/team/shared/nectar-suprema/logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = f"{log_dir}/registry_executions.json"
        with open(log_file, "a") as f:
            f.write(json.dumps(asdict(exec_entry), ensure_ascii=False) + "\n")

    def get_executions(self, limit: int = 50) -> List[Dict]:
        """Retorna histórico de execuções"""
        return [asdict(e) for e in self.executions[-limit:]]

    # ─────────────────────────────────────────────────────────────────────────
    # Remote Callbacks
    # ─────────────────────────────────────────────────────────────────────────

    def register_remote(self, event: str, url: str):
        if event in self.remote_callbacks:
            if url not in self.remote_callbacks[event]:
                self.remote_callbacks[event].append(url)
                print(f"[REGISTRY] Remote callback registered for {event}: {url}")

    async def broadcast(self, event: str, data: Any):
        print(f"[REGISTRY] Broadcasting {event} to {len(self.remote_callbacks[event])} remote nodes.")
        async with httpx.AsyncClient() as client:
            tasks = []
            for url in self.remote_callbacks[event]:
                tasks.append(client.post(url, json={"event": event, "data": data}))
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for i, res in enumerate(results):
                    if isinstance(res, Exception):
                        print(f"[REGISTRY] Error broadcasting to {self.remote_callbacks[event][i]}: {res}")

registry = ExpansionRegistry()
