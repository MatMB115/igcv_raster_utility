# Documentation Index - IGCV Raster Utility

## Complete Documentation

This documentation provides a comprehensive overview of the IGCV Raster Utility project, from basic concepts to advanced technical details.

---

## Quick Start

### [Main README](README.md)
- Project overview
- Main features
- Basic installation and usage
- Feature roadmap

---

## Architecture and Design

### [System Architecture](architecture.md)
- **MVC Pattern** detailed
- **Architecture diagrams**
- **Data flow**
- **Design principles**
- **Error handling strategies**
- **Performance considerations**
- **Extensibility**

### [Raster Data Processing](raster_processing.md)
- **Main operations** (loading, reading, export)
- **Metadata preservation**
- **Performance optimizations**
- **Specific error handling**
- **Compatibility considerations**
- **Extension points**

---

## User Interfaces

### [User Interfaces](user_interface.md)
- **Graphical Interface (GUI)**
  - Components and functionalities
  - Translation system
  - Error handling
- **Command Line Interface (CLI)**
  - Arguments and options
  - Usage examples
  - Batch processing
- **Interface comparison**
- **Usability considerations**

---

## Development

### [Development Guide](development.md)
- **Development environment**
- **Code patterns** (PEP 8, docstrings, type hints)
- **Architecture patterns** (SRP, DIP, Strategy)
- **Error handling**
- **Logging system**
- **Testing** (unit, integration)
- **Extensibility**
- **Performance and optimization**
- **Documentation**
- **Contribution process**

---

## Planning

### [Development Roadmap](roadmap.md)
- **Phase 1**: Basic features
- **Phase 2**: Visualization and indices
- **Phase 3**: Advanced features
- **Phase 4**: Polish and documentation
- **Phase 5**: Expansion and integration
- **Feature prioritization**
- **General timeline**
- **Technical considerations**
- **Success metrics**
- **Risks and mitigations**

---

## Technical Documentation

### Project Structure
```
igcv_raster_utility/
├── main.py                 # Entry point
├── exceptions.py           # Exception hierarchy
├── logger.py              # Logging system
├── requirements.txt       # Dependencies
├── cli/                   # CLI interface
├── controller/            # Control logic
├── model/                 # Business logic
├── view/                  # Graphical interface
├── utils/                 # Utilities
├── translations/          # Translations
├── docs/                  # Documentation
├── logs/                  # Log files
└── assets/               # Resources
```

### Main Modules

#### `main.py`
- **Responsibility**: Application initialization
- **Features**: Mode detection (GUI/CLI), logging configuration, global error handling

#### `model/raster_handler.py`
- **Responsibility**: Raster data processing
- **Features**: Loading, selective reading, preview generation, export

#### `controller/main_controller.py`
- **Responsibility**: Business logic and coordination
- **Features**: State management, validation, coordination between View and Model

#### `view/main_window.py`
- **Responsibility**: User graphical interface
- **Features**: Main interface, band selection, metadata visualization, preview

#### `view/band_reorder_window.py`
- **Responsibility**: Band reordering window
- **Features**: Reordering interface, drag & drop, order validation

#### `cli/cli_app.py`
- **Responsibility**: Command line interface
- **Features**: Argument parsing, batch processing, parameter validation

---

## Features

### Implemented Features

#### Data Processing
- **GeoTIFF file loading**
- **Band selection and reading**
- **Complete metadata preservation**
- **GeoTIFF export**
- **RGB preview generation**

#### Interfaces
- **PyQt5 graphical interface**
- **Command line interface**
- **Multilingual support** (Portuguese/English)
- **Dynamic translation system**

#### Quality and Robustness
- **Comprehensive error handling**
- **Detailed logging system**
- **Input validation**
- **Well-structured MVC architecture**

---

## Technologies

### Technology Stack

#### Backend
- **Python 3.8+**: Main language
- **rasterio**: Raster data processing
- **numpy**: Numerical computation
- **matplotlib**: Advanced visualization (future - not currently used)

#### Frontend
- **PyQt5**: Graphical interface framework
- **Qt Translation System**: Translation system

#### Architecture
- **MVC Pattern**: Separation of concerns
- **Exception hierarchy**: Error handling
- **Logging system**: Monitoring and debugging

---

## Use Cases

### Typical Usage - GUI
1. **Load raster file** via "Open Raster" button
2. **View metadata** in right panel
3. **Select bands** in left panel list
4. **Reorder bands** (optional) via "Reorder" button
5. **Generate preview** of selected bands
6. **Export selected bands** to new file

### Typical Usage - CLI
```bash
# List available bands
python main.py --cli --input image.tif --list

# Export specific bands
python main.py --cli --input image.tif --bands 1 3 4 --output output.tif
```

---

## Troubleshooting

### Common Issues
- **File loading errors**: Check file format and permissions
- **Memory issues**: Large files may require more RAM
- **Translation issues**: Verify translation compilation
- **Export errors**: Check output directory permissions

### Debugging
- **Logs**: Check `logs/` directory for detailed information
- **Error messages**: User-friendly messages with technical details
- **Validation**: Input validation prevents many common errors

---

## 🤝 Contributing

### For Documentation
- **Corrections**: Open issues for documentation errors
- **Improvements**: Suggestions are welcome
- **Translations**: Help with English translations

### For Development
- Follow established patterns
- Add appropriate error handling
- Include logging for debugging
- Update documentation
- Add tests for new functionality

---

## Support

- **Issues**: Use GitHub issues system
- **Discussions**: Participate in project discussions
- **Documentation**: Check this documentation first

---

**Last update**: Documentation updated with band reordering functionality 