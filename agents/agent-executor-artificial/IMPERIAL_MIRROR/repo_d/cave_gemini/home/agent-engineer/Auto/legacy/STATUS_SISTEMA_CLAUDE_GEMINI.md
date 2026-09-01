# Sistema de Fusão Claude-Gemini

Este sistema combina as capacidades do Claude e do Gemini para oferecer respostas mais completas e equilibradas através de um mecanismo de fusão inteligente de respostas.

## Estrutura do Sistema

- **FUSAO_EXTREMA/** - Pasta principal com os componentes de fusão
  - `arsenal/intelligence_fusion.py` - Motor de fusão principal
  - `arsenal/logger_system.py` - Sistema de logging
  - `entidades/` - Configurações de modelos e pesos
  - `main_fusion_orchestrator.py` - Orquestrador principal
- **gemini_api_integration.py** - Integração com a API do Gemini
- **README_INTEGRACAO.md** - Documentação original

## Funcionalidades

- Fusão inteligente de respostas de Claude e Gemini
- Classificação automática de tipos de tarefas
- Ponderação adaptativa conforme o tipo de tarefa
- Sistema de logging para auditoria
- Suporte para tarefas técnicas, criativas, analíticas e de resolução de problemas

## Como Usar

### Configuração Inicial

1. O sistema já está instalado e funcional
2. Para usar a API do Gemini, configure sua chave:
   ```
   setx GEMINI_API_KEY "sua_chave_da_api_aqui"
   ```
3. Reinicie seu terminal após configurar a chave

### Uso Básico

```python
import sys
sys.path.insert(0, r'C:\Users\Usuário\FUSAO_EXTREMA')

from arsenal.intelligence_fusion import create_fusion_engine
from arsenal.logger_system import get_fusion_logger

# Criar componentes
engine = create_fusion_engine()
logger = get_fusion_logger()

# Usar o sistema de fusão
claude_resp = "Resposta do Claude"
gemini_resp = "Resposta do Gemini"
result = engine.fuse_responses(claude_resp, gemini_resp, 'technical')
```

## Scripts de Demonstração

- `demo_fusao_completa_funcional.py` - Demonstração completa
- `teste_integracao_claude_gemini.py` - Teste da integração
- `guia_integracao_claude_gemini.py` - Guia de uso
- `inicio_rapido_simples.py` - Início rápido

## Estado Atual

- ✅ Componentes principais: FUNCIONANDO
- ✅ Motor de fusão: OPERACIONAL
- ✅ Sistema de logging: ATIVO
- ⚠️ API do Gemini: CHAVE PENDENTE (funcionalidade completa após configuração)

O sistema está completamente instalado e pronto para uso. Apenas a integração com a API do Gemini requer a configuração da chave para funcionar plenamente.