# Integração Claude-Gemini

Esta pasta contém os arquivos necessários para integrar o Claude Code com a API do Gemini, ampliando as capacidades de IA disponíveis durante suas sessões.

## Arquivos Criados

1. **gemini_api_integration.py** - Classe principal para integração com a API do Gemini
2. **instrucoes_gemini_integration.md** - Instruções detalhadas para configuração
3. **exemplo_integracao.py** - Exemplo prático de uso da integração
4. **testar_integracao.py** - Script para testar a conexão com a API

## Como Configurar

### Passo 1: Obter uma chave da API do Gemini

1. Acesse o [Google AI Studio](https://aistudio.google.com/)
2. Faça login com sua conta Google
3. Clique em "Get API Key" para criar uma nova chave
4. Anote sua chave da API

### Passo 2: Configurar a variável de ambiente

Execute o seguinte comando no seu terminal para definir a variável de ambiente:

No Windows (cmd):
```
setx GEMINI_API_KEY "sua_chave_da_api_aqui"
```

No Windows (PowerShell):
```
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "sua_chave_da_api_aqui", "User")
```

### Passo 3: Testar a conexão

Após configurar a variável de ambiente, reinicie seu terminal e execute:
```
python testar_integracao.py
```

## Como Usar

Depois de configurar a chave da API, você pode usar a integração em seus próprios scripts:

```python
from gemini_api_integration import GeminiAPIIntegration

# Inicializa a integração
integration = GeminiAPIIntegration()

# Usa a API para gerar conteúdo
prompt = "Seu prompt aqui"
response = integration.generate_content(prompt)
print(response)
```

## Benefícios da Integração

- Combina as forças do Claude (análise de código, raciocínio lógico) com o Gemini (criatividade, raciocínio diverso)
- Permite alternar entre diferentes modelos de IA conforme a necessidade
- Expande significativamente as capacidades disponíveis durante sessões de desenvolvimento
- Oferece flexibilidade para tarefas específicas que podem ser melhor executadas por um modelo ou outro

## Considerações

- Certifique-se de manter sua chave da API segura e não compartilhá-la
- Esteja ciente dos limites de uso da API do Gemini
- A conexão com a API requer uma conexão ativa com a internet