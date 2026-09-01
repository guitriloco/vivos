# Sistema Autônomo de Tráfego Pago — AETHER FLOW TRAFFIC
## IA Decide Onde Investir Baseado em Lucro Real

---

## 1. ARQUITETURA DO SISTEMA AUTÔNOMO

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AETHER FLOW TRAFFIC — MOTOR AUTÔNOMO                 │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CAMADA DE DADOS                               │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │    │
│  │  │ Meta Ads   │  │ TikTok Ads  │  │ Kiwify API  │             │    │
│  │  │ API        │  │ API         │  │ (vendas)    │             │    │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │    │
│  │         │                │                │                     │    │
│  │         └────────────────┼────────────────┘                     │    │
│  │                          ▼                                      │    │
│  │  ┌─────────────────────────────────────────────────────────┐   │    │
│  │  │              DATA LAKE (Google Sheets / BigQuery)         │   │    │
│  │  │  - Custo por dia                                        │   │    │
│  │  │  - Receitas por campanha                                 │   │    │
│  │  │  - ROAS real-time                                       │   │    │
│  │  │  - CPL, CPA, CTR                                        │   │    │
│  │  └─────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    MOTOR DE DECISÃO IA                           │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │                   ALGORITMO                              │    │    │
│  │  │                                                          │    │    │
│  │  │  SE ROAS > 3x por 3 dias consecutivos                   │    │    │
│  │  │  ENTÃO: +50% budget automãtico                          │    │    │    │
│  │  │                                                          │    │    │
│  │  │  SE ROAS < 2x por 2 dias consecutivos                   │    │    │    │
│  │  │  ENTÃO: -30% budget + pausar pior audience              │    │    │    │
│  │  │                                                          │    │    │
│  │  │  SE CPL > R$ 5 por 1 dia                                │    │    │    │
│  │  │  ENTÃO: pausar campanha + escalar alternativa          │    │    │    │
│  │  │                                                          │    │    │
│  │  │  SE ROAS > 5x por 5 dias                                │    │    │    │
│  │  │  ENTÃO: duplicar campaign (escalação agressiva)         │    │    │
│  │  │                                                          │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    EXECUÇÃO AUTOMÁTICA                            │    │
│  │  ┌─────────────────┐  ┌─────────────────┐                     │    │
│  │  │ Meta Ads API    │  │ TikTok Ads API  │                     │    │
│  │  │ (ajuste budget) │  │ (ajuste budget) │                     │    │
│  │  └─────────────────┘  └─────────────────┘                     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. REGRAS DE DECISÃO AUTÔNOMA

### 2.1 Regras Primárias (Lucro > 3x)

| Condição | Ação Automática | Justificativa |
|---|---|---|
| ROAS > 5x por 5 dias | +100% budget | Lucro excepcional, escalar agressivamente |
| ROAS > 4x por 3 dias | +50% budget | Bom desempenho, aumentar presença |
| ROAS > 3x por 3 dias | +20% budget | Meta atingida, crescimento estável |

### 2.2 Regras de Alerta (Lucro 2-3x)

| Condição | Ação Automática | Justificativa |
|---|---|---|
| ROAS 2-3x por 3 dias | Manter budget | Desempenho acceptable, monitorar |
| ROAS 2-3x + CTR caindo | -20% budget | Possível fadiga, reduzir exposição |
| ROAS < 2x por 2 dias | -30% budget | Baixo desempenho, cortar gastos |

### 2.3 Regras de Emergência (Lucro < 2x)

| Condição | Ação Automática | Justificativa |
|---|---|---|
| ROAS < 1.5x por 2 dias | Pausar campanha | Prejuízo, não desperdiçar mais |
| CPL > R$ 8 por 1 dia | Pausar + escalar alternativa | Custo muito alto |
| Relevance Score < 4 | Pausar creative | Publicidade não ressoa |

---

## 3. HIERARQUIA DE PRIORIZAÇÃO

### 3.1 Ordem de Alocação de Budget

```
1º (MAIOR PRIORIDADE) — Campanhas com ROAS > 4x
   → Recebem até 60% do budget total
   
2º (MÉDIA PRIORIDADE) — Campanhas com ROAS 2-4x
   → Recebem até 30% do budget total
   
3º (TESTE) — Campanhas novas
   → Recebem até 10% do budget total (teste A/B)
```

### 3.2 Distribuição Automática de Budget

| Situação da Conta | Alocação FB/IG | Alocação TikTok | Alocação Teste |
|---|---|---|---|
| ROAS geral > 4x | 50% | 40% | 10% |
| ROAS geral 2-4x | 60% | 30% | 10% |
| ROAS geral < 2x | 70% | 20% | 10% |
| Em recuperação | 80% | 10% | 10% |

---

## 4. MÉTRICAS PARA DECISÃO DA IA

### 4.1 Dados de Input (来源)

```python
# Pseudocódigo do sistema

class CampaignMetrics:
    diaria:
        - custo_total
        - receita_total
        - roas = receita / custo
        - cpl = custo / leads
        - cpa = custo / compras
        - ctr = cliques / impressoes
        - impressions
        
    acumulada (7 dias):
        - roas_medio
        - tendencia (crescendo/estavel/decrescendo)
        - desvio_padrao_roas
```

### 4.2 Algoritmo de Decisão

```python
def avaliar_campaign(campaign):
    roas = campaign.roas_7_dias
    tendencia = campaign.tendencia_roas
    cpl = campaign.cpl_dia
    
    # Regra 1: Super performers
    if roas > 4 and tendencia == 'crescendo':
        return 'ESCALAR_AGRESSIVO'  # +50% budget
        
    # Regra 2: Performers sólidos
    elif roas > 3 and tendencia != 'decrescendo':
        return 'ESCALAR_MODERADO'  # +20% budget
        
    # Regra 3: Em dúvida
    elif roas > 2:
        if cpl < 5:
            return 'MANTER'  # Manter budget
        else:
            return 'REDUZIR'  # -20% budget
            
    # Regra 4: Perigos
    elif roas < 2:
        if tendencia == 'decrescendo':
            return 'PAUSAR'  # Pausar imediatamente
        else:
            return 'REDUZIR_AGRESSIVO'  # -50% budget
            
    # Regra 5: Experimento novo
    elif campaign.dias < 7:
        return 'TESTAR'  # Manter para coletar dados
```

---

## 5. SISTEMA DE FEEDBACK LOOP

```
┌─────────────────────────────────────────────────────────────────┐
│                      FEEDBACK LOOP CONTÍNUO                      │
│                                                                   │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐ │
│  │ COLETA   │ ──▶ │ ANALISA │ ──▶ │ DECIDE   │ ──▶ │ EXECUTA │ │
│  │ dados    │     │ ROAS    │     │ ação     │     │ muda    │ │
│  └──────────┘     └──────────┘     └──────────┘     └─────────┘ │
│       ▲                                                      │   │
│       │                                                      │   │
│       └──────────────────────────────────────────────────────┘   │
│                        24 horas (loop diário)                     │
└─────────────────────────────────────────────────────────────────┘
```

### 5.1 Ciclo de Execução

| Horário | Ação |
|---|---|
| 00:00 | Coletar dados do dia anterior |
| 06:00 | IA analisa métricas e calcula decisões |
| 07:00 | Executar ajustes de budget (se necessários) |
| 12:00 | Checkpoint intermediário (verificar anomalias) |
| 18:00 | Relatório de desempenho |
| 00:00 | Iniciar próximo ciclo |

---

## 6. INTEGRAÇÃO COM PLATAFORMAS

### 6.1 Meta Ads API

```python
# Configuração de budget automãtico
def ajustar_budget_meta(campaign_id, novo_budget):
    meta.api.update_campaign_budget(
        campaign_id=campaign_id,
        daily_budget=novo_budget
    )
```

### 6.2 TikTok Ads API

```python
# Configuração de budget automãtico
def ajustar_budget_tiktok(campaign_id, novo_budget):
    tiktok.api.update_campaign_budget(
        campaign_id=campaign_id,
        budget_mode='daily',
        daily_budget=novo_budget
    )
```

### 6.3 Kiwify/Hotmart (Receita)

```python
# Buscar dados de venda
def coletar_receita(periodo):
    return kiwify.api.get_sales({
        'period': periodo,
        'campaign': 'all'  # ou filtrar por UTM
    })
```

---

## 7. PAINEL DE MONITORAMENTO

### 7.1 Dashboard em Tempo Real

```
┌──────────────────────────────────────────────────────────────┐
│               AETHER FLOW TRAFFIC — PAINEL                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  SALDO DISPONÍVEL: R$ 5.000,00                              │
│  BUDGET DO DIA:    R$ 500,00                                │
│                                                              │
│  ┌─────────────────┬────────┬────────┬───────────────────┐   │
│  │ CAMPANHA        │ ROAS   │ BUDGET │ AÇÃO IA           │   │
│  ├─────────────────┼────────┼────────┼───────────────────┤   │
│  │ Solar_VSL      │ 4.7x   │ R$200  │ +50% → R$ 300    │   │
│  │ Solar_Isca     │ 3.2x   │ R$100  │ +20% → R$ 120    │   │
│  │ Cell_Acessorios│ 1.8x   │ R$50   │ ⚠️ PAUSAR        │   │
│  │ Retargeting     │ 5.1x   │ R$100  │ +100% → R$ 200  │   │
│  └─────────────────┴────────┴────────┴───────────────────┘   │
│                                                              │
│  ÚLTIMA DECISÃO: 2025-05-12 08:00                           │
│  PRÓXIMA ANÁLISE: 2025-05-12 18:00                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 7.2 Alertas Automáticos

| Tipo | Condição | Ação |
|---|---|---|
| 🚨 CRÍTICO | ROAS < 1x | Pausar + notificar |
| ⚠️ ATENÇÃO | ROAS < 2x | Reduzir + notificar |
| ✅ OK | ROAS > 3x | Continuar normal |
| 🎯 EXCELENTE | ROAS > 5x | Escalar + notificar |

---

## 8. CONFIGURAÇÃO DE LIMITS

### 8.1 Proteções de Budget

```python
LIMITS = {
    # Budget por campanha
    'max_budget_por_campanha': 500,  # R$ 500/dia por campanha
    'min_budget_por_campanha': 20,    # R$ 20/dia (manter teste)
    
    # Ajuste por ciclo
    'max_increase_percent': 100,      # Máximo +100% por dia
    'max_decrease_percent': 50,       # Máximo -50% por dia
    
    # Tempo mínimo
    'min_dias_teste': 3,             # Mínimo 3 dias para avaliar
    'min_gasto_para_decisao': 150,   # R$ 150 gasto mínimo para decisão
    
    # Emergência
    'limite_cpl_emergencia': 8,      # CPL acima disso = pausar
    'limite_roas_emergencia': 1.5,   # ROAS abaixo disso = pausar
}
```

---

## 9. IMPLEMENTAÇÃO TÉCNICA

### 9.1 Stack Tecnológico

| Componente | Ferramenta |
|---|---|
| IA/Motor de Decisão | Python + pandas |
| Automação | Zapier / Make (n8n) |
| Base de Dados | Google Sheets ou BigQuery |
| Visualização | Looker Studio (gratuito) |
| Execução API | Meta Marketing API + TikTok API |

### 9.2 Fluxo de Implementação

```
SEMANA 1-2: Setup
- [ ] Configurar Google Sheets como data lake
- [ ] Conectar Meta Ads API (leitura)
- [ ] Conectar TikTok Ads API (leitura)
- [ ] Criar dashboard Looker Studio

SEMANA 3-4: Motor
- [ ] Desenvolver script Python de decisão
- [ ] Testar lógica com dados históricos
- [ ] Configurar automatização (Zapier)

SEMANA 5-6: Execução
- [ ] Ativar ajustes manuais (supervisão)
- [ ] Validar decisões da IA
- [ ] Ajustar regras se necessário

SEMANA 7+: Autonomia Total
- [ ] IA decide e executa sem supervisão
- [ ] Revisão semanal humana
- [ ] Otimização contínua
```

---

## 10. MÃO-NA-MASSA: PRIMEIROS PASSOS

### 10.1 Para Começar Hoje

1. **Criar planilha Google Sheets** com colunas:
   - Data, Campanha, Custo, Receita, ROAS, CPL, CTR, Impressões

2. **Exportar dados** do Meta Ads Manager (últimos 30 dias)

3. **Importar dados de vendas** da Kiwify (UTMs configuradas)

4. **Calcular ROAS real** por campanha

5. **Aplicar regras**:
   - ROAS > 3x → +20% budget
   - ROAS < 2x → -30% budget
   - ROAS < 1.5x → Pausar

---

## 11. EXEMPLO PRÁTICO

### Situação Real:

```
Campanha: Solar_VSL
Budget atual: R$ 100/dia

Dia 1: Custo R$ 100 → Receita R$ 350 → ROAS 3.5x ✓
Dia 2: Custo R$ 100 → Receita R$ 380 → ROAS 3.8x ✓
Dia 3: Custo R$ 100 → Receita R$ 420 → ROAS 4.2x ✓

Decisão IA (após 3 dias com ROAS > 3x):
→ +20% budget = R$ 120/dia

Dia 4: Custo R$ 120 → Receita R$ 520 → ROAS 4.3x ✓
Dia 5: Custo R$ 120 → Receita R$ 560 → ROAS 4.7x ✓

Decisão IA (após 5 dias com ROAS > 4x):
→ +50% budget = R$ 180/dia

Dia 6-10: Continua escalando até atingir limit de R$ 500/dia
```

---

## 12. MANUAL DE OPERAÇÃO

### 12.1 Supervisão Humana

| Frequência | O que revisar |
|---|---|
| Diário (5 min) | Dashboard, exceções |
| Semanal (30 min) | Performance geral, ajustar regras |
| Mensal (1 hora) | Análise profunda, estratégia |

### 12.2 Quando Intervir Manualmente

- Nova campanha de lanzamiento (primeiros 7 dias)
- Events externos (feriados, promoções)
- Queda generalizada de ROAS (mercado)
- Bugs ou erros de tracking

---

*Documento preparado pelo agente de Growth Hacking*
*Versão 1.0 — Sistema Autônomo de Tráfego*
*Maio 2025*

*Baseado na arquitetura AETHER FLOW para sistemas autônomos*