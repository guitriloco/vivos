# 📖 MANUAL DE OPERAÇÃO DO IMPÉRIO DEVOPS

Este manual fornece as instruções necessárias para operar, monitorar e expandir a infraestrutura soberana de 540 nós.

---

## 1. Primeiros Passos
### Requisitos
- Acesso SSH aos Regional Hubs.
- Python 3.8+ instalado nos nós de controle.
- Docker e Docker Compose para os ativos.

### Instalação da Base
Para sincronizar o ambiente local com o estado do Império:
```bash
git clone https://github.com/guitriloco/Auto.git
cd Auto
tar -xzvf EMPIRE_BACKUP_APOGEU.tar.gz
```

---

## 2. Operações de Segurança
### Ativar o WAF Global
O WAF protege os 45 Hubs Regionais contra ataques DDoS e Brute Force.
```bash
./empire_waf.sh apply
```
*Ações suportadas: `apply`, `rollback`, `status`.*

### Auditoria de Conformidade (LGPD/GDPR)
O sistema verifica automaticamente se os nós seguem as políticas de soberania.
```bash
# OPA (Open Policy Agent) roda via pipeline ou manualmente
# Verifique os relatórios em:
cat synthesis/synthesis_report_l2.json
```

---

## 3. Inteligência e Agregação
### Executar Agregador SINTESE L2
Coleta dados bio-financeiros de toda a frota em < 0.1s.
```bash
python3 scripts_v2/synthesis_aggregator_l2.py
```

### Motor de Arbitragem (Auto-Scaling)
Inicia o loop de decisão que escala os ativos baseado em lucro e performance.
```bash
python3 scripts_v2/arbitrage_engine_v2_1.py --interval 15 --service active-asset
```

---

## 4. Auto-Cura (Self-Healing)
### Protocolo Lucrative Necromancy
Monitora nós lentos e os converte em instâncias Spot ou os encerra se o ROI for negativo.
```bash
python3 infrastructure_scripts/lucrative_necromancy.py
```

---

## 5. Monitoramento
### Dashboard de Status
Gere o JSON de telemetria para o dashboard executivo:
```bash
python3 empire_dashboard_v2.py
```
Visualize os resultados no Grafana (Porta 3000) usando o arquivo `monitoring/velocity_dashboard.json`.

---
**EM CASO DE CRISE: Execute o backup imediato.**
`./infrastructure_scripts/backup.sh`
