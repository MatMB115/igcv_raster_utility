# IGCV Raster Utility (IGCVRasterTool)

A lightweight, user-friendly desktop application for processing, visualizing, and exporting satellite and similar multispectral raster datasets.
This tool was designed to support scientific workflows and dataset distribution, enabling fast band selection, index calculation (NDVI, EVI, NDRE, etc.), and export to common formats (GeoTIFF, PNG) with customizable band stacks.

## ✅ Implemented Features

### Core Functionality
- [x] **Open and load multispectral raster files** (GeoTIFF format)
- [x] **Select bands of interest** for export (multi-selection interface)
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
- [ ] **Advanced band selection** (drag & drop, band reordering)

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
4. Export your selection as a new GeoTIFF with preserved metadata

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
│   └── main_window.py     # GUI implementation
├── translations/          # Translation files
│   ├── igcv_en.ts        # English translations (source)
│   ├── igcv_pt_BR.ts     # Portuguese translations (source)
│   └── README.md         # Translation documentation
└── logs/                  # Application logs
```

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

### Phase 2: Visualization & Indices (Next)
- [ ] Band preview thumbnails
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
