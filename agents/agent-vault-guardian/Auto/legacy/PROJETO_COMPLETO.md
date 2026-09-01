# Projeto Documentos AI - Sistema Completo

## Visão Geral

Este projeto implementa um ecossistema completo de processamento e classificação automática de documentos, composto por 5 módulos interconectados que trabalham em conjunto para automatizar tarefas de gerenciamento de documentos.

## Componentes do Sistema

### 1. Document_Classifier_GUI
- **Função**: Interface gráfica para classificação de documentos
- **Características**:
  - Interface intuitiva com arrastar e soltar (drag-and-drop)
  - Visualização em tempo real das classificações
  - Conexão com a API local para classificação por IA
  - Suporte a múltiplos formatos de documento

### 2. Configurable_Document_Processor
- **Função**: Processador configurável de documentos
- **Características**:
  - Perfis personalizados de processamento
  - Regras de negócio configuráveis
  - Suporte a múltiplos formatos de documento
  - Templates de classificação
  - Integração com diferentes APIs de IA

### 3. Classification_History_Tracker
- **Função**: Rastreamento e análise de histórico de classificações
- **Características**:
  - Banco de dados SQLite para armazenamento de histórico
  - Análise estatística de acurácia
  - Relatórios de desempenho
  - Sistema de feedback para correção de classificações
  - Dashboard de métricas

### 4. Local_Model_Trainer
- **Função**: Treinamento de modelos locais de IA
- **Características**:
  - Treinamento de modelos com base em dados históricos
  - Avaliação de acurácia do modelo
  - Exportação de modelos treinados
  - Comparação entre modelos
  - Pipeline de treinamento automatizado

### 5. Document_Backup_Manager
- **Função**: Gerenciamento de backups de documentos
- **Características**:
  - Cópias de segurança automáticas antes de operações
  - Sistema de restauração de arquivos
  - Verificação de integridade dos backups
  - Política configurável de retenção
  - Registro de operações de backup

## Integração entre Componentes

Os componentes trabalham em conjunto da seguinte forma:

1. **Document_Backup_Manager** protege os documentos antes de qualquer processamento
2. **Configurable_Document_Processor** define as regras de processamento
3. **Document_Classifier_GUI** fornece a interface para interação humana
4. **Classification_History_Tracker** registra todas as classificações
5. **Local_Model_Trainer** melhora continuamente os modelos com base no histórico

## Tecnologias Utilizadas

- **Linguagem**: Python 3.8+
- **Bibliotecas Principais**:
  - PyMuPDF (para extração de texto de PDFs)
  - Requests (para comunicação com APIs)
  - SQLite3 (para banco de dados local)
  - Pandas (para análise de dados)
  - Matplotlib (para visualizações)
  - Scikit-learn (para machine learning)
  - Joblib (para serialização de modelos)
  - Tkinter (para interface gráfica)

## Configuração e Execução

O sistema utiliza um arquivo de configuração central (config.json) que define:
- Chaves de API e endpoints
- Diretórios de entrada e saída
- Configurações de modelo
- Parâmetros de funcionamento

## Benefícios do Sistema

- **Automação**: Reduz o tempo manual necessário para classificar documentos
- **Aprendizado Contínuo**: O sistema melhora com o tempo com base em feedback
- **Segurança**: Sistema de backup garante que documentos não sejam perdidos
- **Personalização**: Configurações adaptáveis para diferentes necessidades
- **Monitoramento**: Histórico e métricas permitem acompanhamento de desempenho
- **Escalabilidade**: Arquitetura modular permite expansão e manutenção fácil

## Estado Atual do Projeto

Todos os 5 componentes foram implementados com sucesso e passaram no teste de integração. O sistema está pronto para ser utilizado e pode ser expandido com novas funcionalidades conforme necessário.