# Mapa Geral dos Projetos - Documentos AI

## Visão Geral

Este repositório contém 5 projetos inter-relacionados para processamento e classificação automática de documentos:

1. **Document_Classifier_GUI** - Interface gráfica para classificação de documentos
2. **Configurable_Document_Processor** - Processador configurável de documentos
3. **Classification_History_Tracker** - Rastreamento de histórico de classificações
4. **Local_Model_Trainer** - Treinamento de modelos locais de IA
5. **Document_Backup_Manager** - Gerenciamento de backups de documentos

## Estrutura do Projeto

```
Projetos_Documentos_AI/
├── Document_Classifier_GUI/
│   ├── README.md
│   ├── main.py
│   ├── gui.py
│   └── classifier.py
├── Configurable_Document_Processor/
│   ├── README.md
│   ├── main.py
│   ├── config_processor.py
│   └── profiles/
├── Classification_History_Tracker/
│   ├── README.md
│   ├── main.py
│   ├── database.py
│   └── analytics.py
├── Local_Model_Trainer/
│   ├── README.md
│   ├── main.py
│   ├── trainer.py
│   └── models/
└── Document_Backup_Manager/
    ├── README.md
    ├── main.py
    ├── backup_manager.py
    └── logs/
```

## Integração Entre Projetos

Os projetos podem ser usados individualmente ou combinados para formar um sistema completo:

- Document_Backup_Manager protege os documentos antes de qualquer processamento
- Configurable_Document_Processor define as regras de processamento
- Document_Classifier_GUI fornece a interface para interação humana
- Classification_History_Tracker registra todas as classificações
- Local_Model_Trainer melhora continuamente os modelos com base no histórico

## Próximos Passos

1. Implementar o esqueleto básico de cada projeto
2. Definir interfaces comuns para integração
3. Criar testes unitários para cada componente
4. Estabelecer pipeline de integração contínua