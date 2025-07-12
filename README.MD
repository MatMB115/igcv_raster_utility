# IGCV Raster Utility (IGCVRasterTool)

A lightweight, user-friendly desktop application for processing, visualizing, and exporting satellite and similar multispectral raster datasets.
This tool was designed to support scientific workflows and dataset distribution, enabling fast band selection, index calculation (NDVI, EVI, NDRE, etc.), and export to common formats (GeoTIFF, PNG) with customizable band stacks.

## Features

* **Open and preview multispectral raster files** (GeoTIFF, Sentinel-2 tiles, etc.)
* **Select bands of interest** for export (e.g., RGB, NIR, Red Edge, SWIR)
* **Calculate spectral indices** such as NDVI, EVI, NDRE and add them to the export stack
* **Export as RGB/PNG** (quicklook) or **GeoTIFF** with the chosen bands and indices
* **Cross-platform GUI** (Windows, Linux, macOS) via PyQt5/PySide2
* **Multi-language support** (Portuguese and English) with Qt translation system
* **Designed for ease of use** in research, education, and dataset distribution
* **Robust error handling** with comprehensive exception management
* **Logging system** for debugging and monitoring

## Getting Started

### Requirements

* Python 3.8+
* [PyQt5](https://pypi.org/project/PyQt5/) or [PySide2](https://pypi.org/project/PySide2/)
* [rasterio](https://rasterio.readthedocs.io/)
* [numpy](https://numpy.org/)
* [matplotlib](https://matplotlib.org/) (for preview)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/igcv_raster_utility.git
cd igcv_raster_utility
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Compile translations (optional):
```bash
python compile_translations_simple.py
```

4. Run the application:
```bash
# GUI mode
python main.py

# CLI mode
python main.py --cli --input input.tif --bands 1 2 3 --output output.tif
```

## Usage

### GUI Mode
1. Open a raster file (GeoTIFF).
2. Preview bands and select which to export.
3. Optionally, calculate NDVI, EVI, NDRE and add them to your band stack.
4. Export your selection as a new GeoTIFF or as an RGB PNG quicklook.

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
├── compile_translations_simple.py # Translation compiler script
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

## Development

### Adding New Features
1. Follow the MVC pattern
2. Add appropriate exception handling
3. Include logging for debugging
4. Update documentation

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

TODO
