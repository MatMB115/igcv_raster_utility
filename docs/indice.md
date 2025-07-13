# Índice da Documentação - IGCV Raster Utility

## 📚 Documentação Completa

Esta documentação fornece uma visão abrangente do projeto IGCV Raster Utility, desde conceitos básicos até detalhes técnicos avançados.

---

## 🚀 Início Rápido

### [README Principal](README.md)
- Visão geral do projeto
- Características principais
- Instalação e uso básico
- Roadmap de funcionalidades

---

## 🏗️ Arquitetura e Design

### [Arquitetura do Sistema](arquitetura.md)
- **Padrão MVC** detalhado
- **Diagramas de arquitetura**
- **Fluxo de dados**
- **Princípios de design**
- **Estratégias de tratamento de erros**
- **Considerações de performance**
- **Extensibilidade**

### [Processamento de Dados Raster](processamento_raster.md)
- **Operações principais** (carregamento, leitura, exportação)
- **Preservação de metadados**
- **Otimizações de performance**
- **Tratamento de erros específicos**
- **Considerações de compatibilidade**
- **Pontos de extensão**

---

## 🖥️ Interfaces de Usuário

### [Interfaces de Usuário](interface_usuario.md)
- **Interface Gráfica (GUI)**
  - Componentes e funcionalidades
  - Sistema de tradução
  - Tratamento de erros
- **Interface de Linha de Comando (CLI)**
  - Argumentos e opções
  - Exemplos de uso
  - Processamento em lote
- **Comparação entre interfaces**
- **Considerações de usabilidade**

---

## 👨‍💻 Desenvolvimento

### [Guia de Desenvolvimento](desenvolvimento.md)
- **Ambiente de desenvolvimento**
- **Padrões de código** (PEP 8, docstrings, type hints)
- **Padrões de arquitetura** (SRP, DIP, Strategy)
- **Tratamento de erros**
- **Sistema de logging**
- **Testes** (unitários, integração)
- **Extensibilidade**
- **Performance e otimização**
- **Documentação**
- **Processo de contribuição**

---

## 📋 Planejamento

### [Roadmap de Desenvolvimento](roadmap.md)
- **Fase 1**: Funcionalidades básicas ✅
- **Fase 2**: Visualização e índices 🔄
- **Fase 3**: Recursos avançados 📋
- **Fase 4**: Polimento e documentação 📋
- **Fase 5**: Expansão e integração 📋
- **Priorização de funcionalidades**
- **Cronograma geral**
- **Considerações técnicas**
- **Métricas de sucesso**
- **Riscos e mitigações**

---

## 📖 Documentação Técnica

### Estrutura do Projeto
```
igcv_raster_utility/
├── main.py                 # Ponto de entrada
├── exceptions.py           # Hierarquia de exceções
├── logger.py              # Sistema de logging
├── requirements.txt       # Dependências
├── cli/                   # Interface CLI
├── controller/            # Lógica de controle
├── model/                 # Lógica de negócio
├── view/                  # Interface gráfica
├── utils/                 # Utilitários
├── translations/          # Traduções
├── docs/                  # Documentação
├── logs/                  # Arquivos de log
└── assets/               # Recursos
```

### Módulos Principais

#### `main.py`
- **Responsabilidade**: Inicialização da aplicação
- **Funcionalidades**: Detecção de modo (GUI/CLI), configuração de logging, tratamento de erros globais

#### `model/raster_handler.py`
- **Responsabilidade**: Processamento de dados raster
- **Funcionalidades**: Carregamento, leitura seletiva, geração de previews, exportação

#### `controller/main_controller.py`
- **Responsabilidade**: Lógica de negócio e coordenação
- **Funcionalidades**: Gerenciamento de estado, validação, coordenação entre View e Model

#### `view/main_window.py`
- **Responsabilidade**: Interface gráfica do usuário
- **Funcionalidades**: Interface principal, seleção de bandas, visualização de metadados, preview

#### `cli/cli_app.py`
- **Responsabilidade**: Interface de linha de comando
- **Funcionalidades**: Parsing de argumentos, processamento em lote, validação de parâmetros

---

## 🔧 Funcionalidades

### Funcionalidades Implementadas ✅

#### Processamento de Dados
- **Carregamento de arquivos GeoTIFF**
- **Seleção e leitura de bandas**
- **Preservação completa de metadados**
- **Exportação GeoTIFF**
- **Geração de previews RGB**

#### Interfaces
- **Interface gráfica com PyQt5**
- **Interface de linha de comando**
- **Suporte multilíngue** (Português/Inglês)
- **Sistema de tradução dinâmica**

#### Qualidade e Robustez
- **Tratamento abrangente de erros**
- **Sistema de logging detalhado**
- **Validação de entrada**
- **Arquitetura MVC bem estruturada**

---

## 🛠️ Tecnologias

### Stack Tecnológico

#### Backend
- **Python 3.8+**: Linguagem principal
- **rasterio**: Processamento de dados raster
- **numpy**: Computação numérica
- **matplotlib**: Visualização avançada (futuro - não usado atualmente)

#### Frontend
- **PyQt5**: Framework de interface gráfica
- **Qt Translation System**: Sistema de tradução

#### Arquitetura
- **Padrão MVC**: Separação de responsabilidades
- **Hierarquia de exceções**: Tratamento de erros
- **Sistema de logging**: Monitoramento e debugging

---

## 📊 Casos de Uso

### Uso Típico - GUI
1. **Carregar arquivo raster** via botão "Abrir Raster"
2. **Visualizar metadados** no painel direito
3. **Selecionar bandas** na lista do painel esquerdo
4. **Gerar preview** das bandas selecionadas
5. **Exportar bandas** selecionadas para novo arquivo

### Uso Típico - CLI
```bash
# Listar bandas disponíveis
python main.py --cli --input image.tif --list

# Exportar bandas específicas
python main.py --cli --input image.tif --bands 1 3 4 --output output.tif
```

---

## 🔍 Troubleshooting

### Problemas Comuns

#### Erro ao Carregar Arquivo
- **Verificar**: Formato do arquivo (.tif, .tiff)
- **Verificar**: Permissões de leitura
- **Verificar**: Integridade do arquivo

#### Erro de Tradução
- **Verificar**: Arquivos .qm compilados
- **Executar**: `python utils/compile_translations.py`

#### Performance Lenta
- **Verificar**: Tamanho do arquivo
- **Verificar**: Memória disponível
- **Considerar**: Usar CLI para arquivos grandes

---

## 🤝 Contribuição

### Como Contribuir
1. **Fork** do repositório
2. **Criação** de branch para feature
3. **Desenvolvimento** seguindo padrões
4. **Testes** da funcionalidade
5. **Documentação** das mudanças
6. **Pull Request** com descrição detalhada

### Padrões de Contribuição
- **PEP 8**: Estilo de código Python
- **Docstrings**: Documentação inline
- **Type Hints**: Anotações de tipo
- **Testes**: Cobertura adequada
- **Logging**: Registro de operações

---

## 📞 Suporte

### Recursos de Ajuda
- **Issues**: Para bugs e solicitações de features
- **Documentação**: Este conjunto de documentos
- **Logs**: Arquivos em `logs/` para debugging
- **Exemplos**: Casos de uso no README

### Comunidade
- **GitHub**: Repositório principal
- **Discussions**: Para dúvidas e discussões
- **Wiki**: Documentação adicional (futuro)

---

## 📈 Métricas e Status

### Status do Projeto
- **Versão atual**: MVP (Fase 1)
- **Status**: Estável e funcional
- **Próxima versão**: v2.0 (Fase 2)

### Funcionalidades por Status
- ✅ **Implementadas**: 15 funcionalidades
- 🔄 **Em desenvolvimento**: 8 funcionalidades
- 📋 **Planejadas**: 25+ funcionalidades

---

## 🔗 Links Úteis

### Documentação Externa
- [PyQt5 Documentation](https://doc.qt.io/qtforpython/)
- [rasterio Documentation](https://rasterio.readthedocs.io/)
- [NumPy Documentation](https://numpy.org/doc/)

### Recursos Relacionados
- [GeoTIFF Specification](https://gdal.org/drivers/raster/gtiff.html)
- [Qt Translation System](https://doc.qt.io/qt-5/internationalization.html)
- [Python Logging](https://docs.python.org/3/library/logging.html)

---

## 📝 Notas de Versão

### v1.0 (MVP) - Concluída
- ✅ Funcionalidades básicas de processamento raster
- ✅ Interface gráfica e linha de comando
- ✅ Sistema de tradução
- ✅ Tratamento de erros robusto

### v2.0 (Em Desenvolvimento)
- 🔄 Thumbnails de bandas
- 🔄 Cálculo de índices espectrais
- 🔄 Melhorias na visualização

---

*Esta documentação é mantida atualizada com o desenvolvimento do projeto. Para dúvidas específicas, consulte os documentos individuais ou abra uma issue no repositório.* 