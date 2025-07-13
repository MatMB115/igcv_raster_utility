# IGCV Raster Utility - Documentation

This folder contains the English documentation for the IGCV Raster Utility project.

## Documentation Structure

```
docs/en/
├── README.md          # This file
├── index.md           # Documentation index (in development)
├── architecture.md    # System architecture (in development)
├── development.md     # Development guide (in development)
├── user_interface.md  # User interfaces (in development)
├── raster_processing.md # Raster data processing (in development)
└── roadmap.md         # Development roadmap (in development)
```

## Language Status

### Portuguese (pt/)
- **Complete**: All documentation available in Portuguese
- **Updated**: Includes all implemented features
- **Detailed**: Complete technical documentation with examples

### English (en/)
- **In Development**: Translation in progress
- **Priority**: Basic documentation will be translated first
- **Timeline**: Complete translation planned for future versions

## Current Status

### Available in English
- **Basic project overview** (this file)
- **Interface translations** (GUI and CLI support English)

### In Development
- **Technical documentation**: Being translated from Portuguese
- **User guides**: Will be available in both languages
- **API documentation**: Planned for future versions

## Translation Process

### Development Workflow
1. **Development**: New features documented in Portuguese first
2. **Review**: Documentation reviewed and tested
3. **Translation**: Translation to English
4. **Validation**: Technical review of translation

### Maintenance
- Portuguese documentation is the primary source
- Changes applied first in Portuguese
- English translations updated as needed

## Quick Index

### Portuguese Documentation (Complete)
- **[README](../pt/README.md)**: Project overview
- **[Index](../pt/indice.md)**: Complete documentation navigation
- **[Architecture](../pt/arquitetura.md)**: System design and structure
- **[Development](../pt/desenvolvimento.md)**: Developer guide (includes compilation instructions)
- **[User Interface](../pt/interface_usuario.md)**: GUI and CLI
- **[Raster Processing](../pt/processamento_raster.md)**: Raster data operations
- **[Roadmap](../pt/roadmap.md)**: Development planning

### English Documentation (In Development)
- **This file**: Basic overview
- **[Development](development.md)**: Developer guide (includes compilation instructions)
- **Technical docs**: Coming soon
- **User guides**: Coming soon

### Quick Compilation Reference
For building executables, see the **Compilation de Executáveis** section in:
- **[Portuguese Development Guide](../pt/desenvolvimento.md#compilação-de-executáveis)**
- **[English Development Guide](development.md#building-executables)**

Or use the utility script: `python utils/find_rasterio_paths.py`

## Features

### Implemented Features
- **Raster file loading**: GeoTIFF support with metadata extraction
- **Band selection**: Multiple band selection with visual interface
- **Band reordering**: Visual interface for reordering bands before export
- **Preview generation**: RGB preview from selected bands
- **Data export**: GeoTIFF export with metadata preservation
- **Multilingual support**: Portuguese and English interface
- **Command line interface**: CLI for batch processing
- **Error handling**: Comprehensive error management

### Technical Features
- **MVC Architecture**: Clean separation of concerns
- **Signal-based communication**: Qt signals for component communication
- **Memory optimization**: Selective band reading
- **Metadata preservation**: Complete metadata handling
- **Logging system**: Detailed logging for debugging

## 🤝 Contributing

### For Documentation
- **Corrections**: Open issues for documentation errors
- **Improvements**: Suggestions are welcome
- **Translations**: Help with English translations

### For Development
- Use Portuguese documentation as reference
- Keep documentation updated when adding features
- Follow established patterns

## Support

- **Issues**: Use GitHub issues system
- **Discussions**: Participate in project discussions
- **Documentation**: Check this documentation first

---

**Last update**: Documentation updated with band reordering functionality 