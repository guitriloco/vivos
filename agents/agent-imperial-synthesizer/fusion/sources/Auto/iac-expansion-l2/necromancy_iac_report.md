# Protocolo /NECROMANCIA: Implementação de Spot Instances no IaC Global

## Visão Geral
Conforme solicitado pelo SRE Lead, a lógica de 'Necromancia Lucrativa' foi formalizada diretamente no Infrastructure-as-Code (IaC). Os templates de Terraform agora suportam a alternância dinâmica entre instâncias On-Demand e Spot Instances para otimização radical de custos.

## Alterações Realizadas

### 1. Variáveis Globais
- Adicionada a variável `use_spot` (bool) no root `variables.tf`.
- O valor default é `false` (On-Demand), permitindo uma transição segura e controlada.

### 2. Módulo `compute_aws`
- Implementado bloco dinâmico `instance_market_options`.
- Quando `use_spot = true`:
    - A instância é solicitada no mercado Spot da AWS.
    - `max_price` configurado para `$0.05` para garantir ROI positivo.
    - Adicionada tag `Type = SPOT` para identificação rápida no console/faturamento.
- Quando `use_spot = false`:
    - A instância permanece como On-Demand standard.

### 3. Orquestração de Nichos
- A variável `use_spot` é propagada do root para cada módulo de nicho individual, permitindo que o império decida quais nichos devem ser 'purgados' ou otimizados via código.

## Validação Técnica
- **Sintaxe:** Validada com `terraform validate` (Sucesso).
- **Lógica:** Plano de execução gerado com sucesso, confirmando a injeção do bloco `instance_market_options` quando a flag é ativada.

## Próximos Passos
- O **Arbitrage Engine** agora pode disparar re-deployments alterando apenas a variável `use_spot` no `terraform.tfvars` ou via CLI args para forçar a migração de nós com baixo ROI para instâncias de custo zero.

**Templates Atualizados:**
- `/home/team/shared/mutar-expansion/terraform/variables.tf`
- `/home/team/shared/mutar-expansion/terraform/main.tf`
- `/home/team/shared/mutar-expansion/terraform/modules/niche/main.tf`
- `/home/team/shared/mutar-expansion/terraform/modules/compute_aws/main.tf`

A 'Necromancia' agora é parte integrante do DNA da infraestrutura.
