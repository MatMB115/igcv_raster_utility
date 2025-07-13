# IGCV Raster Utility (IGCVRasterTool) - pt-BR

Uma aplicação desktop leve e amigável para processamento, visualização e exportação de datasets raster multiespectrais de satélite e similares.
Esta ferramenta foi projetada para suportar workflows científicos e distribuição de datasets, permitindo seleção rápida de bandas, cálculo de índices (NDVI, EVI, NDRE, etc.) e exportação para formatos comuns (GeoTIFF, PNG) com empilhamentos de bandas personalizáveis.

## Funcionalidades Implementadas

### Funcionalidades Principais
- [x] **Abrir e carregar arquivos raster multiespectrais** (formato GeoTIFF)
- [x] **Selecionar bandas de interesse** para exportação (interface de seleção múltipla)
- [x] **Reordenar bandas** antes da exportação com interface visual drag & drop
- [x] **Exportar bandas selecionadas como GeoTIFF** com preservação de metadados
- [x] **GUI multiplataforma** (Windows, Linux, macOS) via PyQt5
- [x] **Suporte multilíngue** (Português e Inglês) com sistema de tradução Qt
- [x] **Interface de linha de comando (CLI)** para processamento em lote
- [x] **Tratamento robusto de erros** com gerenciamento abrangente de exceções
- [x] **Sistema de logging** para debugging e monitoramento
- [x] **Preservação de metadados** (nomes das bandas, tags, descrições, CRS, transform, etc.)

### Funcionalidades Técnicas
- [x] **Arquitetura MVC** (padrão Model-View-Controller)
- [x] **Classes de exceção customizadas** para diferentes tipos de erro
- [x] **Validação de arquivos** e recuperação de erros
- [x] **Extração de nomes de bandas** de várias fontes de metadados
- [x] **Preservação de metadados geográficos** (CRS, transform, valores nodata)
- [x] **Configurações de compressão e tiling** preservadas
- [x] **Sistema de compilação de traduções** com ferramentas Qt

## Funcionalidades Faltantes (TODO)

### Funcionalidades Principais
- [ ] **Seleção avançada de bandas** (interface de seleção aprimorada)

### Interface do Usuário
- [x] **Miniaturas de preview de bandas** na interface de seleção
- [ ] **Diálogo de opções de exportação** (compressão, configurações de qualidade)
- [ ] **Lista de arquivos recentes** no menu
- [ ] **Atalhos de teclado** para operações comuns
- [ ] **Barra de status** com progresso das operações

### Funcionalidades Avançadas
- [ ] **Exibição de estatísticas das bandas** (min, max, média, desvio padrão)
- [ ] **Visualização de histograma** para bandas selecionadas
- [ ] **Presets de combinação de bandas** (RGB, cor falsa, etc.)
- [ ] **Opções de conversão de sistema de coordenadas**

### Documentação e Testes
- [ ] **Testes unitários** para funcionalidades principais
- [ ] **Testes de integração** para GUI e CLI
- [ ] **Manual do usuário** com screenshots
- [ ] **Documentação da API** para desenvolvedores
- [ ] **Datasets de exemplo** para testes

## Começando

### Requisitos

* Python 3.8+
* [PyQt5](https://pypi.org/project/PyQt5/) >= 5.15.0
* [rasterio](https://rasterio.readthedocs.io/) >= 1.3.0
* [numpy](https://numpy.org/) >= 1.21.0

### Instalação

## Uso

### Modo GUI
1. Abra um arquivo raster (GeoTIFF) usando o botão "Abrir Raster"
2. Visualize as bandas disponíveis na lista (atualmente mostra apenas nomes das bandas)
3. Selecione quais bandas exportar (seleção múltipla suportada)
4. Reordene as bandas se necessário usando o botão "Reordenar"
5. Exporte sua seleção como um novo GeoTIFF com metadados preservados

### Modo CLI
```bash
# Listar bandas disponíveis
python main.py --cli --input input.tif --list

# Exportar bandas específicas
python main.py --cli --input input.tif --bands 1 3 4 --output output.tif
```

## Tratamento de Erros

A aplicação inclui tratamento abrangente de erros:

### Tipos de Exceção
- **IGCVRasterError**: Exceção base para todos os erros do projeto
- **RasterHandlerError**: Erros relacionados ao processamento raster
- **ControllerError**: Erros no controlador da aplicação
- **ViewError**: Erros na interface gráfica
- **CLIError**: Erros na interface de linha de comando
- **ValidationError**: Erros de validação de dados
- **FileOperationError**: Erros de I/O de arquivos

### Logging
- Todas as operações são logadas no diretório `logs/`
- Logging em console e arquivo com timestamps
- Diferentes níveis de log (INFO, WARNING, ERROR, DEBUG)

### Recuperação de Erros
- Tratamento gracioso de erros de arquivo não encontrado
- Validação de parâmetros de entrada
- Mensagens de erro amigáveis ao usuário
- Limpeza automática em caso de erros

## Estrutura do Projeto

```
igcv_raster_utility/
├── main.py                 # Ponto de entrada da aplicação
├── exceptions.py           # Classes de exceção customizadas
├── logger.py              # Configuração de logging
├── requirements.txt       # Dependências Python
├── utils/
│   └── compile_translations.py # Script compilador de traduções
├── cli/
│   └── cli_app.py        # Interface de linha de comando
├── controller/
│   └── main_controller.py # Controlador da aplicação
├── model/
│   └── raster_handler.py  # Lógica de processamento raster
├── view/
│   ├── main_window.py     # Implementação da GUI
│   └── band_reorder_window.py # Interface de reordenação de bandas
├── translations/          # Arquivos de tradução
│   ├── igcv_en.ts        # Traduções em inglês (fonte)
│   ├── igcv_pt_BR.ts     # Traduções em português (fonte)
│   └── README.md         # Documentação de tradução
├── docs/                  # Documentação
│   ├── README.md         # Visão geral da documentação
│   ├── pt/               # Documentação em português
│   └── en/               # Documentação em inglês
└── logs/                  # Logs da aplicação
```

## Documentação

O projeto inclui documentação abrangente organizada por idioma:

### Estrutura da Documentação
- **[Visão Geral da Documentação](docs/README.md)**: Guia completo da documentação
- **[Documentação em Português](docs/pt/)**: Documentação técnica completa
- **[Documentação em Inglês](docs/en/)**: Documentação em desenvolvimento

### Documentação Disponível
- **Guia de Arquitetura**: Design do sistema e padrão MVC
- **Guia de Desenvolvimento**: Diretrizes para contribuição e desenvolvimento
- **Guia de Interface do Usuário**: Documentação da GUI e CLI
- **Guia de Processamento Raster**: Detalhes técnicos do processamento de dados
- **Roadmap**: Planejamento de desenvolvimento e funcionalidades futuras

### Suporte Multilíngue
- **Interface**: Disponível em português e inglês
- **Documentação**: Completa em português, inglês em desenvolvimento
- **Sistema de Tradução**: Tradução baseada em Qt com ferramentas de compilação

## Por que esta ferramenta?

A maioria das ferramentas GIS desktop são muito pesadas ou muito genéricas para workflows científicos simples ou de publicação de dados.
**IGCVRasterTool** é focado em velocidade, simplicidade e reprodutibilidade para sensoriamento remoto, criação de datasets de ML e projetos educacionais.

## Roadmap de Desenvolvimento

### Fase 1: Funcionalidades Principais (Atual)
- [x] Carregamento básico de raster e seleção de bandas
- [x] Exportação GeoTIFF com preservação de metadados
- [x] Interfaces CLI e GUI
- [x] Suporte multilíngue
- [x] Tratamento de erros e logging
- [x] Reordenação de bandas com interface visual

### Fase 2: Visualização e Índices (Próxima)
- [x] Miniaturas de preview de bandas
- [ ] RGB/PNG para visualizações rápidas
- [ ] Exibição básica de estatísticas

### Fase 3: Funcionalidades Avançadas (Futuro)
- [ ] Opções avançadas de exportação

### Fase 4: Polimento e Documentação (Futuro)
- [ ] Testes abrangentes
- [ ] Documentação do usuário
- [ ] Otimização de performance
- [ ] Formatos adicionais de exportação

## Contribuindo

### Adicionando Novas Funcionalidades
1. Siga o padrão MVC
2. Adicione tratamento apropriado de exceções
3. Inclua logging para debugging
4. Atualize a documentação
5. Adicione testes para nova funcionalidade

### Traduções
- A aplicação suporta múltiplos idiomas usando o sistema de tradução do Qt
- Arquivos de tradução estão no diretório `translations/`
- Veja `translations/README.md` para instruções detalhadas sobre como compilar e atualizar traduções

### Testes
- Teste com vários formatos GeoTIFF
- Verifique cenários de tratamento de erros
- Verifique funcionalidade de logging
- Teste funcionalidade de troca de idioma

## Licença

[GNU3.0](LICENSE)

## Citação

TODO: Adicionar informações de citação para uso acadêmico

---

# IGCV Raster Utility (IGCVRasterTool) - En-US

A lightweight, user-friendly desktop application for processing, visualizing, and exporting satellite and similar multispectral raster datasets.
This tool was designed to support scientific workflows and dataset distribution, enabling fast band selection, index calculation (NDVI, EVI, NDRE, etc.), and export to common formats (GeoTIFF, PNG) with customizable band stacks.

## ✅ Implemented Features

### Core Functionality
- [x] **Open and load multispectral raster files** (GeoTIFF format)
- [x] **Select bands of interest** for export (multi-selection interface)
- [x] **Reorder bands** before export with visual drag & drop interface
- [x] **Export selected bands as GeoTIFF** with metadata preservation
- [x] **Cross-platform GUI** (Windows, Linux, macOS) via PyQt5
- [x] **Multi-language support** (Portuguese and English) with Qt translation system
- [x] **Command-line interface (CLI)** for batch processing
- [x] **Robust error handling** with comprehensive exception management
- [x] **Logging system** for debugging and monitoring
- [x] **Metadata preservation** (band names, tags, descriptions, CRS, transform, etc.)

### Technical Features
- [x] **MVC architecture** (Model-View-Controller pattern)
- [x] **Custom exception classes** for different error types
- [x] **File validation** and error recovery
- [x] **Band name extraction** from various metadata sources
- [x] **Geographic metadata preservation** (CRS, transform, nodata values)
- [x] **Compression and tiling settings** preservation
- [x] **Translation compilation system** with Qt tools

## ❌ Missing Features (TODO)

### Core Functionality
- [ ] **Advanced band selection** (enhanced selection interface)

### User Interface
- [x] **Band preview thumbnails** in the selection interface
- [ ] **Export options dialog** (compression, quality settings)
- [ ] **Recent files list** in menu
- [ ] **Keyboard shortcuts** for common operations
- [ ] **Status bar** with operation progress

### Advanced Features
- [ ] **Band statistics** display (min, max, mean, std)
- [ ] **Histogram visualization** for selected bands
- [ ] **Band combination presets** (RGB, false color, etc.)
- [ ] **Coordinate system conversion** options

### Documentation & Testing
- [ ] **Unit tests** for core functionality
- [ ] **Integration tests** for GUI and CLI
- [ ] **User manual** with screenshots
- [ ] **API documentation** for developers
- [ ] **Example datasets** for testing

## Getting Started

### Requirements

* Python 3.8+
* [PyQt5](https://pypi.org/project/PyQt5/) >= 5.15.0
* [rasterio](https://rasterio.readthedocs.io/) >= 1.3.0
* [numpy](https://numpy.org/) >= 1.21.0

### Installation

## Usage

### GUI Mode
1. Open a raster file (GeoTIFF) using the "Open Raster" button
2. Preview available bands in the list (currently shows band names only)
3. Select which bands to export (multi-selection supported)
4. Reorder bands if needed using the "Reorder" button
5. Export your selection as a new GeoTIFF with preserved metadata

### CLI Mode
```bash
# List available bands
python main.py --cli --input input.tif --list

# Export specific bands
python main.py --cli --input input.tif --bands 1 3 4 --output output.tif
```

## Error Handling

The application includes comprehensive error handling:

### Exception Types
- **IGCVRasterError**: Base exception for all project errors
- **RasterHandlerError**: Errors related to raster processing
- **ControllerError**: Errors in the application controller
- **ViewError**: Errors in the graphical interface
- **CLIError**: Errors in command-line interface
- **ValidationError**: Data validation errors
- **FileOperationError**: File I/O errors

### Logging
- All operations are logged to `logs/` directory
- Console and file logging with timestamps
- Different log levels (INFO, WARNING, ERROR, DEBUG)

### Error Recovery
- Graceful handling of file not found errors
- Validation of input parameters
- User-friendly error messages
- Automatic cleanup on errors

## Project Structure

```
igcv_raster_utility/
├── main.py                 # Application entry point
├── exceptions.py           # Custom exception classes
├── logger.py              # Logging configuration
├── requirements.txt       # Python dependencies
├── utils/
│   └── compile_translations.py # Translation compiler script
├── cli/
│   └── cli_app.py        # Command-line interface
├── controller/
│   └── main_controller.py # Application controller
├── model/
│   └── raster_handler.py  # Raster processing logic
├── view/
│   ├── main_window.py     # GUI implementation
│   └── band_reorder_window.py # Band reordering interface
├── translations/          # Translation files
│   ├── igcv_en.ts        # English translations (source)
│   ├── igcv_pt_BR.ts     # Portuguese translations (source)
│   └── README.md         # Translation documentation
├── docs/                  # Documentation
│   ├── README.md         # Documentation overview
│   ├── pt/               # Portuguese documentation
│   └── en/               # English documentation
└── logs/                  # Application logs
```

## Documentation

The project includes comprehensive documentation organized by language:

### Documentation Structure
- **[Documentation Overview](docs/README.md)**: Complete documentation guide
- **[Portuguese Documentation](docs/pt/)**: Complete technical documentation
- **[English Documentation](docs/en/)**: Documentation in development

### Available Documentation
- **Architecture Guide**: System design and MVC pattern
- **Development Guide**: Contributing and development guidelines
- **User Interface Guide**: GUI and CLI documentation
- **Raster Processing Guide**: Technical details of data processing
- **Roadmap**: Development planning and future features

### Multilingual Support
- **Interface**: Available in Portuguese and English
- **Documentation**: Complete in Portuguese, English in development
- **Translation System**: Qt-based translation with compilation tools

## Why this tool?

Most desktop GIS tools are too heavy or too generic for simple scientific or data publishing workflows.
**IGCVRasterTool** is focused on speed, simplicity, and reproducibility for remote sensing, ML dataset creation, and educational projects.

## Development Roadmap

### Phase 1: Core Features (Current)
- [x] Basic raster loading and band selection
- [x] GeoTIFF export with metadata preservation
- [x] CLI and GUI interfaces
- [x] Multi-language support
- [x] Error handling and logging
- [x] Band reordering with visual interface

### Phase 2: Visualization & Indices (Next)
- [x] Band preview thumbnails
- [ ] RGB/PNG for quicklooks
- [ ] Basic statistics display

### Phase 3: Advanced Features (Future)
- [ ] Advanced export options

### Phase 4: Polish & Documentation (Future)
- [ ] Comprehensive testing
- [ ] User documentation
- [ ] Performance optimization
- [ ] Additional export formats

## Contributing

### Adding New Features
1. Follow the MVC pattern
2. Add appropriate exception handling
3. Include logging for debugging
4. Update documentation
5. Add tests for new functionality

### Translations
- The application supports multiple languages using Qt's translation system
- Translation files are in `translations/` directory
- See `translations/README.md` for detailed instructions on how to compile and update translations

### Testing
- Test with various GeoTIFF formats
- Verify error handling scenarios
- Check logging functionality
- Test translation switching functionality

## License

[GNU3.0](LICENSE)

## Citation

TODO: Add citation information for academic use
