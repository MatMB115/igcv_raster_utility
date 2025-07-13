# Development Guide - IGCV Raster Utility

## Overview

This document provides guidance for developers who want to contribute to the IGCV Raster Utility project or extend its functionalities.

## Development Environment

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, Linux, macOS
- **Git**: For version control
- **IDE**: VS Code, PyCharm, or Cursor

### Initial Setup

1. **Repository Clone**
   ```bash
   git clone https://github.com/your-username/igcv_raster_utility.git
   cd igcv_raster_utility
   ```

2. **Virtual Environment Creation**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Dependency Installation**
   ```bash
   pip install -r requirements.txt
   ```

4. **Translation Compilation**
   ```bash
   python utils/compile_translations.py
   ```

### Project Structure

```
igcv_raster_utility/
├── main.py                 # Application entry point
├── exceptions.py           # Exception hierarchy
├── logger.py              # Logging system
├── requirements.txt       # Python dependencies
├── cli/                   # Command line interface
│   └── cli_app.py
├── controller/            # Control logic (MVC)
│   └── main_controller.py
├── model/                 # Business logic (MVC)
│   └── raster_handler.py
├── view/                  # Graphical interface (MVC)
│   ├── main_window.py     # Main window
│   └── band_reorder_window.py # Band reordering window
├── utils/                 # Utilities
│   └── compile_translations.py
├── translations/          # Translation files
│   ├── igcv_en.ts
│   ├── igcv_pt_BR.ts
│   └── README.md
├── docs/                  # Documentation
├── logs/                  # Log files
└── assets/               # Resources (icons, etc.)
    └── icon.png
```

## Code Patterns

### Python Conventions

#### 1. PEP 8 - Code Style

```python
# Good
def process_raster_data(file_path, band_indices):
    """Processes raster data from specified file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return process_bands(file_path, band_indices)

# Bad
def processRasterData(filePath,bandIndices):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"File not found: {filePath}")
    return processBands(filePath,bandIndices)
```

#### 2. Docstrings

```python
def load_raster(filepath):
    """
    Loads basic information from a raster file.
    
    Args:
        filepath (str): Path to the raster file
        
    Returns:
        tuple: (meta, band_names) - metadata and band names
        
    Raises:
        RasterHandlerError: If there's an error loading the raster
        
    Example:
        >>> meta, names = load_raster("image.tif")
        >>> print(f"Bands: {len(names)}")
        Bands: 4
    """
```

#### 3. Type Hints

```python
from typing import List, Tuple, Dict, Optional
import numpy as np

def read_selected_bands(
    filepath: str, 
    selected_indices: List[int]
) -> Tuple[List[np.ndarray], Dict, List[str], List[Dict], Dict]:
    """
    Reads specific bands from a raster file.
    
    Args:
        filepath: Path to the raster file
        selected_indices: List of band indices (0-based)
        
    Returns:
        Tuple containing: (bands, meta, band_names, band_metadata, file_metadata)
    """
```

### Architecture Patterns

#### 1. Single Responsibility Principle (SRP)

```python
# Good - Each class has a single responsibility
class RasterLoader:
    """Responsible only for loading raster data."""
    
class MetadataExtractor:
    """Responsible only for extracting metadata."""
    
class BandProcessor:
    """Responsible only for processing bands."""

# Bad - Class with multiple responsibilities
class RasterHandler:
    """Does everything: loads, processes, exports, etc."""
```

#### 2. Dependency Inversion Principle (DIP)

```python
# Good - Depends on abstractions
class RasterProcessor:
    def __init__(self, loader: RasterLoader, exporter: RasterExporter):
        self.loader = loader
        self.exporter = exporter
    
    def process(self, filepath: str) -> None:
        data = self.loader.load(filepath)
        result = self.process_data(data)
        self.exporter.export(result)

# Bad - Depends on concrete implementations
class RasterProcessor:
    def __init__(self):
        self.loader = RasterLoader()  # Concrete dependency
        self.exporter = RasterExporter()  # Concrete dependency
```

#### 3. Strategy Pattern

```python
# Interface for different processing strategies
class ProcessingStrategy:
    def process(self, data: np.ndarray) -> np.ndarray:
        raise NotImplementedError

class NormalizationStrategy(ProcessingStrategy):
    def process(self, data: np.ndarray) -> np.ndarray:
        return (data - data.min()) / (data.max() - data.min())

class PercentileStrategy(ProcessingStrategy):
    def __init__(self, min_percentile: float = 2, max_percentile: float = 98):
        self.min_percentile = min_percentile
        self.max_percentile = max_percentile
    
    def process(self, data: np.ndarray) -> np.ndarray:
        p_min, p_max = np.percentile(data, (self.min_percentile, self.max_percentile))
        return np.clip((data - p_min) / (p_max - p_min), 0, 1)
```

## Error Handling

### Exception Hierarchy

```python
class IGCVRasterError(Exception):
    """Base exception for all project errors"""
    pass

class RasterHandlerError(IGCVRasterError):
    """Raster processing errors"""
    pass

class ControllerError(IGCVRasterError):
    """Business logic errors"""
    pass

class ViewError(IGCVRasterError):
    """Graphical interface errors"""
    pass

class CLIError(IGCVRasterError):
    """Command line interface errors"""
    pass

class ValidationError(IGCVRasterError):
    """Data validation errors"""
    pass

class FileOperationError(IGCVRasterError):
    """File I/O errors"""
    pass
```

### Error Handling Patterns

#### 1. Defensive Programming

```python
def load_raster(filepath: str) -> Tuple[Dict, List[str]]:
    """Loads raster information with comprehensive error handling."""
    
    # Input validation
    if not filepath:
        raise ValidationError("File path cannot be empty")
    
    if not os.path.exists(filepath):
        raise FileOperationError(f"File not found: {filepath}")
    
    try:
        with rasterio.open(filepath) as src:
            meta = src.meta.copy()
            band_names = extract_band_names(src)
            return meta, band_names
            
    except rasterio.RasterioIOError as e:
        raise RasterHandlerError(f"Error reading raster file: {e}")
    except Exception as e:
        raise RasterHandlerError(f"Unexpected error loading raster: {e}")
```

#### 2. Graceful Degradation

```python
def extract_band_names(src) -> List[str]:
    """Extracts band names with fallback to defaults."""
    band_names = []
    
    for i in range(1, src.count + 1):
        try:
            # Try to get band name from metadata
            name = src.tags(i).get('name', f'Band {i}')
            band_names.append(name)
        except Exception:
            # Fallback to default name
            logger.warning(f"Band {i} without name, using default")
            band_names.append(f'Band {i}')
    
    return band_names
```

## Logging System

### Configuration

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    """Configures the logging system."""
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('logs/igcv_raster.log', maxBytes=1024*1024, backupCount=5),
            logging.StreamHandler()
        ]
    )
    
    # Set specific logger levels
    logging.getLogger('rasterio').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
```

### Usage Patterns

```python
import logging

logger = logging.getLogger(__name__)

def process_bands(filepath: str, band_indices: List[int]):
    """Processes selected bands with detailed logging."""
    
    logger.info(f"Starting band processing for {filepath}")
    logger.debug(f"Processing bands: {band_indices}")
    
    try:
        for band_index in band_indices:
            logger.debug(f"Processing band {band_index}")
            # Processing logic here
            
        logger.info("Band processing completed successfully")
        
    except Exception as e:
        logger.error(f"Error processing bands: {e}", exc_info=True)
        raise
```

## Testing

### Unit Testing

```python
import unittest
from unittest.mock import Mock, patch
import numpy as np

class TestRasterHandler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_filepath = "test_data/sample.tif"
        self.test_indices = [0, 1, 2]
    
    def test_load_raster_success(self):
        """Test successful raster loading."""
        with patch('rasterio.open') as mock_open:
            mock_src = Mock()
            mock_src.meta = {'width': 100, 'height': 100, 'count': 3}
            mock_src.tags.return_value = {'name': 'Test Band'}
            mock_open.return_value.__enter__.return_value = mock_src
            
            meta, band_names = load_raster(self.test_filepath)
            
            self.assertEqual(meta['width'], 100)
            self.assertEqual(len(band_names), 3)
    
    def test_load_raster_file_not_found(self):
        """Test raster loading with non-existent file."""
        with self.assertRaises(FileOperationError):
            load_raster("non_existent.tif")
```

### Integration Testing

```python
class TestEndToEnd(unittest.TestCase):
    
    def test_complete_workflow(self):
        """Test complete workflow from file loading to export."""
        # Test data setup
        test_input = "test_data/input.tif"
        test_output = "test_data/output.tif"
        
        # Execute workflow
        controller = MainController(Mock())
        controller.open_raster(test_input)
        controller.export_selected_bands(test_output)
        
        # Verify results
        self.assertTrue(os.path.exists(test_output))
        # Additional verification logic
```

## Performance Optimization

### Memory Management

```python
def read_bands_efficiently(filepath: str, band_indices: List[int]) -> List[np.ndarray]:
    """Reads bands efficiently with memory management."""
    
    bands = []
    
    with rasterio.open(filepath) as src:
        for band_idx in band_indices:
            # Read only necessary bands
            band_data = src.read(band_idx + 1)
            bands.append(band_data)
            
            # Explicit memory cleanup for large arrays
            if band_data.nbytes > 100 * 1024 * 1024:  # 100MB
                import gc
                gc.collect()
    
    return bands
```

### Processing Optimization

```python
def process_large_raster(filepath: str, chunk_size: int = 1024):
    """Processes large rasters in chunks."""
    
    with rasterio.open(filepath) as src:
        for ji, window in src.block_windows(1):
            # Process data in chunks
            data = src.read(window=window)
            processed_data = process_chunk(data)
            
            # Yield results to avoid memory accumulation
            yield processed_data
```

## Documentation

### Code Documentation

```python
def calculate_ndvi(nir_band: np.ndarray, red_band: np.ndarray) -> np.ndarray:
    """
    Calculates the Normalized Difference Vegetation Index (NDVI).
    
    NDVI is calculated using the formula: (NIR - RED) / (NIR + RED)
    where NIR is the near-infrared band and RED is the red band.
    
    Args:
        nir_band: Numpy array of the near-infrared band
        red_band: Numpy array of the red band
        
    Returns:
        Numpy array containing NDVI values ranging from -1 to 1
        
    Raises:
        ValueError: If bands have different dimensions
        
    Example:
        >>> ndvi = calculate_ndvi(nir_data, red_data)
        >>> print(f"NDVI range: {ndvi.min():.3f} to {ndvi.max():.3f}")
    """
    
    if nir_band.shape != red_band.shape:
        raise ValueError("Bands must have the same dimensions")
    
    # Avoid division by zero
    denominator = nir_band + red_band
    denominator[denominator == 0] = 1e-10
    
    return (nir_band - red_band) / denominator
```

### API Documentation

```python
class RasterHandler:
    """
    Handles raster data processing operations.
    
    This class provides methods for loading, processing, and exporting
    raster data with comprehensive error handling and metadata preservation.
    
    Attributes:
        supported_formats (List[str]): List of supported file formats
        
    Example:
        >>> handler = RasterHandler()
        >>> meta, bands = handler.load_raster("image.tif")
        >>> handler.export_tif("output.tif", bands, meta)
    """
    
    def __init__(self):
        self.supported_formats = ['.tif', '.tiff']
```

## Contribution Process

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/new-functionality
   ```
3. **Make changes following the established patterns**
4. **Add tests for new functionality**
5. **Update documentation**
6. **Run tests and ensure they pass**
7. **Submit a pull request**

### Code Review Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] Functions have proper docstrings
- [ ] Type hints are included where appropriate
- [ ] Error handling is comprehensive
- [ ] Logging is implemented for debugging
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No performance regressions

### Commit Message Convention

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(raster): add band reordering functionality`
- `fix(export): resolve metadata preservation issue`
- `docs(api): update function documentation`
- `test(handler): add unit tests for load_raster`

## Building Executables

### Prerequisites

Before building executables, ensure you have the following installed:

- **PyInstaller**: `pip install pyinstaller`
- **All project dependencies**: `pip install -r requirements.txt`
- **GDAL and PROJ data**: These are automatically included with rasterio

### Building for Linux

```bash
pyinstaller --noconfirm --onefile --windowed \
  --add-data "translations:translations" \
  --add-data "/home/maysu-lp/Documentos/github/igcv_raster_utility/local/lib/python3.8/site-packages/rasterio/gdal_data:gdal_data" \
  --add-data "/home/maysu-lp/Documentos/github/igcv_raster_utility/local/lib/python3.8/site-packages/rasterio/proj_data:proj_data" \
  --hidden-import rasterio.sample \
  --hidden-import rasterio.vrt \
  --hidden-import rasterio._features \
  main.py
```

### Building for Windows

```bash
pyinstaller --noconfirm --onefile --windowed \
  --add-data "translations;translations" \
  --add-data "C:\path\to\your\env\Lib\site-packages\rasterio\gdal_data;gdal_data" \
  --add-data "C:\path\to\your\env\Lib\site-packages\rasterio\proj_data;proj_data" \
  --hidden-import rasterio.sample \
  --hidden-import rasterio.vrt \
  --hidden-import rasterio._features \
  main.py
```

### Building for macOS

```bash
pyinstaller --noconfirm --onefile --windowed \
  --add-data "translations:translations" \
  --add-data "/path/to/your/env/lib/python3.x/site-packages/rasterio/gdal_data:gdal_data" \
  --add-data "/path/to/your/env/lib/python3.x/site-packages/rasterio/proj_data:proj_data" \
  --hidden-import rasterio.sample \
  --hidden-import rasterio.vrt \
  --hidden-import rasterio._features \
  main.py
```

### Important Notes

#### GDAL and PROJ Data Paths

The paths to `gdal_data` and `proj_data` directories vary depending on your Python environment and operating system. To find the correct paths automatically:

```bash
# Use the provided utility script
python utils/find_rasterio_paths.py
```

This script will:
- Find your rasterio installation path
- Locate the GDAL and PROJ data directories
- Generate a ready-to-use PyInstaller command with the correct paths

Alternatively, you can find the paths manually:

```bash
# Find rasterio installation path
python -c "import rasterio; print(rasterio.__file__)"

# Then locate gdal_data and proj_data relative to that path
# Usually they are in the same directory as rasterio's __init__.py
```

#### Troubleshooting

If you encounter issues with rasterio in the compiled executable, refer to the [rasterio FAQ](https://rasterio.readthedocs.io/en/stable/faq.html) for common solutions:

1. **Missing GDAL drivers**: Ensure all necessary GDAL drivers are included
2. **PROJ database issues**: Verify PROJ data is properly bundled
3. **File format support**: Some formats may require additional GDAL drivers

#### Alternative Build Options

For debugging or development builds, you can use:

```bash
# Debug build (shows console window)
pyinstaller --noconfirm --onefile \
  --add-data "translations:translations" \
  --hidden-import rasterio.sample \
  --hidden-import rasterio.vrt \
  --hidden-import rasterio._features \
  main.py

# Directory build (faster for testing)
pyinstaller --noconfirm --onedir --windowed \
  --add-data "translations:translations" \
  --hidden-import rasterio.sample \
  --hidden-import rasterio.vrt \
  --hidden-import rasterio._features \
  main.py
```

### Output

The compiled executable will be created in the `dist/` directory:
- **Linux**: `dist/main` (executable file)
- **Windows**: `dist/main.exe` (executable file)
- **macOS**: `dist/main` (executable file)

## Conclusion

This development guide provides the foundation for contributing to the IGCV Raster Utility project. Following these patterns ensures code quality, maintainability, and consistency across the codebase.

For additional questions or clarifications, please refer to the project documentation or open an issue on GitHub. 