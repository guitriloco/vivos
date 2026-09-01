# Hiperpersonalizador - Sistema de Conteúdo Hiper-Personalizado

## Visão Geral

O Hiperpersonalizador é um sistema avançado de geração de conteúdo personalizado que utiliza inteligência artificial para criar experiências únicas para cada cliente com base em seu perfil individual, histórico e preferências.

## Arquitetura

```
HIPERPERSONALIZADOR/
├── backend/                 # Servidor Flask com API REST
│   ├── app.py              # Ponto de entrada da aplicação
│   ├── config.py           # Configurações da aplicação
│   ├── api/
│   │   ├── controllers/    # Controladores de negócio
│   │   ├── models/         # Modelos de dados
│   │   └── routes/         # Definições de rotas
│   ├── services/           # Serviços de integração (IA, etc)
│   └── utils/              # Funções utilitárias
├── frontend/               # Aplicação React
│   ├── src/
│   │   ├── App.js          # Componente principal
│   │   ├── App.css         # Estilos globais
│   │   └── ...
├── data/                   # Dados e bancos de dados
├── docs/                   # Documentação
├── tests/                  # Testes automatizados
└── requirements.txt        # Dependências do backend
```

## Funcionalidades

### Backend
- **API RESTful**: Endpoints para geração e histórico de conteúdo
- **Persistência de dados**: Banco de dados SQLite para histórico
- **Integração com IA**: Interfaces para Claude e Gemini
- **Personalização avançada**: Algoritmos de personalização baseados em perfil do usuário

### Frontend
- **Interface intuitiva**: Painel para inserção de dados do produto/cliente
- **Geração em tempo real**: Visualização imediata do conteúdo gerado
- **Histórico de gerações**: Acompanhamento de conteúdos anteriores
- **Responsividade**: Design adaptável para diferentes dispositivos

## Tecnologias Utilizadas

### Backend
- Python 3.8+
- Flask
- SQLite
- Google Generative AI SDK
- Requests

### Frontend
- React
- JavaScript ES6+
- CSS3

## Instalação e Configuração

### Backend

1. Instale as dependências:
```bash
pip install flask flask-cors python-dotenv google-generativeai requests
```

2. Configure as variáveis de ambiente:
```bash
# .env
GEMINI_API_KEY=sua_chave_do_gemini
CLAUDE_API_KEY=sua_chave_do_claude
SECRET_KEY=sua_chave_secreta
DATABASE_URL=sqlite:///hiperp.db
```

3. Execute o servidor:
```bash
cd backend
python app.py
```

### Frontend

1. Instale as dependências:
```bash
cd frontend
npm install
```

2. Execute o aplicativo:
```bash
npm start
```

## Endpoints da API

### Geração de Conteúdo
- `POST /api/v1/content/generate` - Gera conteúdo personalizado
- `GET /api/v1/content/history` - Recupera histórico de gerações

### Usuário
- `POST /api/v1/user/create` - Cria um novo usuário
- `GET /api/v1/user/profile` - Recupera perfil do usuário

### Analytics
- `GET /api/v1/analytics/performance` - Métricas de desempenho
- `GET /api/v1/analytics/conversions` - Taxas de conversão

## Segurança

- Autenticação baseada em API keys
- Sanitização de entradas
- Máscaras para dados sensíveis
- Limites de requisições (rate limiting)

## Próximos Passos

- Integração com mais provedores de IA
- Sistema de A/B testing avançado
- Dashboard de analytics completo
- Integração com plataformas de e-commerce
- Sistema de templates personalizáveis

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request