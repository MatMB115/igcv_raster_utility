# Raster Data Processing - IGCV Raster Utility

## Overview

The IGCV Raster Utility provides comprehensive raster data processing capabilities focused on efficiency, metadata preservation, and user-friendly operations. This document describes the main processing operations, optimization strategies, and technical implementation details.

## Main Operations

### 1. Raster Loading (`load_raster`)

**Purpose**: Loads basic information from a raster file without loading all data into memory.

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
    """
```

#### Loading Process

1. **File Validation**
   ```python
   if not os.path.exists(filepath):
       raise RasterHandlerError(f"File not found: {filepath}")
   
   if not filepath.lower().endswith(('.tif', '.tiff')):
       raise RasterHandlerError("Only GeoTIFF files are supported")
   ```

2. **Metadata Extraction**
   ```python
   with rasterio.open(filepath) as src:
       meta = src.meta.copy()
       
       # Extract band names
       band_names = []
       for i in range(1, src.count + 1):
           try:
               name = src.tags(i).get('name', f'Band {i}')
               band_names.append(name)
           except Exception:
               band_names.append(f'Band {i}')
   ```

3. **Metadata Structure**
   ```python
   meta = {
       'driver': 'GTiff',
       'width': src.width,
       'height': src.height,
       'count': src.count,
       'dtype': src.dtypes[0],
       'crs': src.crs,
       'transform': src.transform,
       'nodata': src.nodata,
       'compress': src.compression,
       'tiled': src.is_tiled,
       'blockxsize': src.blockxsize,
       'blockysize': src.blockysize
   }
   ```

#### Preserved Metadata

- **Geographic Information**: CRS, transform, nodata values
- **Raster Properties**: Dimensions, data type, number of bands
- **Compression Settings**: `compress`, `tiled`

### 2. Selective Band Reading (`read_selected_bands`)

**Purpose**: Reads specific bands from a raster file, respecting reordering order if applicable.

```python
def read_selected_bands(filepath, selected_indices):
    """
    Reads specific bands from a raster file.
    
    Args:
        filepath (str): Path to the raster file
        selected_indices (list): List of band indices (0-based) or reordered order
        
    Returns:
        tuple: (bands, meta, selected_band_names, band_metadata, file_metadata)
    """
```

#### Selective Reading Process

1. **Index Validation**
   ```python
   for idx in selected_indices:
       if idx < 0 or idx >= src.count:
           raise RasterHandlerError(f"Invalid band index: {idx}")
   ```

2. **Band Reading**
   ```python
   bands = []
   selected_band_names = []
   band_metadata = []
   
   for i in selected_indices:
       band_idx = i + 1  # conversion to 1-based
       band = src.read(band_idx)
       bands.append(band)
   ```

3. **Per-Band Metadata Preservation**
   ```python
   band_meta = {
       'tags': dict(src.tags(band_idx)),
       'description': src.descriptions[band_idx - 1],
       'nodata': src.nodata,
       'dtype': src.dtypes[band_idx - 1],
       'index': band_idx
   }
   band_metadata.append(band_meta)
   ```

4. **Global Metadata Capture**
   ```python
   file_metadata = {
       'tags': dict(src.tags()),
       'descriptions': list(src.descriptions),
       'colorinterp': list(src.colorinterp),
       'scales': list(src.scales),
       'offsets': list(src.offsets),
       'units': list(src.units),
       'masks': list(src.masks),
   }
   ```

### 3. Preview Generation (`generate_preview_image`)

```python
def generate_preview_image(filepath, band_indices, max_size=500):
    """
    Generates a color visualization of selected bands for preview.
    
    Note: This function creates a visual representation using bands as color
    channels (similar to RGB), but does not represent real natural colors.
    
    Args:
        filepath (str): Path to the raster file
        band_indices (list): Band indices (1-3 bands)
        max_size (int): Maximum preview size
        
    Returns:
        numpy.ndarray: Normalized visualization array (0-255)
    """
```

#### Preview Generation Process

1. **Input Validation**
   ```python
   if len(band_indices) < 1 or len(band_indices) > 3:
       raise RasterHandlerError("Preview requires 1 to 3 bands")
   ```

2. **Downsampling Calculation**
   ```python
   width, height = src.width, src.height
   scale_factor = max(width, height) / max_size
   scale_factor = max(1, int(scale_factor))
   
   preview_width = width // scale_factor
   preview_height = height // scale_factor
   ```

3. **Downsampled Reading**
   ```python
   band_data = src.read(band_idx + 1, 
                       out_shape=(preview_height, preview_width),
                       resampling=Resampling.average)
   ```

4. **Visualization Composition**
   ```python
   if len(band_indices) == 1:
       # Single band: grayscale visualization
       preview_array = np.stack([band_data_list[0], 
                               band_data_list[0], 
                               band_data_list[0]], axis=-1)
   elif len(band_indices) == 2:
       # Two bands: channel1=band1, channel2=band2, channel3=band1
       preview_array = np.stack([band_data_list[0], 
                               band_data_list[1], 
                               band_data_list[0]], axis=-1)
   else:
       # Three bands: channel1=band1, channel2=band2, channel3=band3
       preview_array = np.stack(band_data_list, axis=-1)
   ```

5. **Value Normalization**
   ```python
   for i in range(3):
       band_data = preview_array[:, :, i]
       
       # Remove zeros for percentile calculation
       non_zero_data = band_data[band_data != 0]
       
       if len(non_zero_data) > 0:
           p2, p98 = np.percentile(non_zero_data, (2, 98))
           
           if p98 > p2:
               normalized = np.clip((band_data - p2) / (p98 - p2) * 255, 0, 255)
           else:
               normalized = np.full_like(band_data, 128, dtype=np.uint8)
   ```

### 4. Band Reordering

**Purpose**: Allows reordering selected bands before export, maintaining the custom order in the final file.

**Features**:
- Visual interface for reordering
- Drag & drop for intuitive reordering
- Buttons to move bands up/down
- Reset to original order
- Order preservation in export

**Reordering Process**:
1. **Band Selection**: User selects bands in main interface
2. **Window Opening**: "Reorder" button opens dedicated window
3. **Visual Reordering**: Interface allows drag and drop bands
4. **Confirmation**: User confirms new order
5. **Application**: Order is applied in next export

**Export Integration**:
```python
# Controller checks if reordered order exists
if self.reordered_indices is not None:
    selected_indices = self.reordered_indices
    self.view.status_label.setText("Using reordered band order.")
else:
    selected_indices = [self.view.band_list.row(item) for item in selected_items]
```

### 5. GeoTIFF Export (`export_tif`)

```python
def export_tif(out_path, bands, meta, band_names=None, 
               band_metadata=None, file_metadata=None):
    """
    Exports bands to GeoTIFF file with metadata preservation.
    
    Args:
        out_path (str): Output file path
        bands (list): List of numpy arrays of bands
        meta (dict): Raster metadata
        band_names (list): Band names
        band_metadata (list): Per-band metadata
        file_metadata (dict): Global file metadata
    """
```

#### Export Process

1. **Output Validation**
   ```python
   if not bands:
       raise RasterHandlerError("No bands provided for export")
   
   output_dir = os.path.dirname(out_path)
   if output_dir and not os.path.exists(output_dir):
       raise RasterHandlerError(f"Output directory does not exist: {output_dir}")
   ```

2. **Metadata Preparation**
   ```python
   export_meta = meta.copy()
   if 'dtype' not in export_meta and bands:
       export_meta['dtype'] = bands[0].dtype
   ```

3. **Writing with rasterio**
   ```python
   with rasterio.open(out_path, 'w', **export_meta) as dst:
       # Global tags preservation
       if file_metadata and file_metadata.get('tags'):
           dst.update_tags(**file_metadata['tags'])
       
       # Band writing
       for i, band in enumerate(bands, start=1):
           dst.write(band, i)
   ```

4. **Per-Band Metadata Preservation**
   ```python
   # Band name
   if band_names and i <= len(band_names):
       dst.update_tags(i, name=band_names[i-1])
       dst.set_band_description(i, band_names[i-1])
   
   # Additional metadata
   if band_metadata and i <= len(band_metadata):
       band_meta = band_metadata[i-1]
       if band_meta.get('tags'):
           dst.update_tags(i, **band_meta['tags'])
   ```

## Performance Optimizations

### Memory Management

#### Problem: Loading all bands consumes too much memory
**Solution**: Selective reading of only necessary bands

```python
# Inefficient - loads all bands
with rasterio.open(filepath) as src:
    all_bands = src.read()  # Loads all bands

# Efficient - loads only selected bands
with rasterio.open(filepath) as src:
    selected_bands = []
    for band_idx in selected_indices:
        band = src.read(band_idx + 1)
        selected_bands.append(band)
```

### Preview Optimization

#### Downsampling Strategy
- **Large files**: Automatic downsampling for preview
- **Performance**: Faster interface response
- **Memory**: Reduced memory usage for visualization

```python
def calculate_downsample_factor(width, height, max_size):
    """Calculates optimal downsampling factor."""
    scale_factor = max(width, height) / max_size
    return max(1, int(scale_factor))
```

### Processing Efficiency

#### Chunked Processing
For very large files, process data in chunks:

```python
def process_large_raster(filepath, chunk_size=1024):
    """Processes large rasters in chunks."""
    with rasterio.open(filepath) as src:
        for ji, window in src.block_windows(1):
            data = src.read(window=window)
            processed = process_chunk(data)
            yield processed
```

## Error Handling

### Specific Error Types

```python
class RasterHandlerError(IGCVRasterError):
    """Raster processing specific errors"""
    pass

class ValidationError(IGCVRasterError):
    """Data validation errors"""
    pass

class FileOperationError(IGCVRasterError):
    """File I/O errors"""
    pass
```

### Error Recovery Strategies

1. **Input Validation**
   ```python
   def validate_file_path(filepath):
       if not filepath:
           raise ValidationError("File path cannot be empty")
       if not os.path.exists(filepath):
           raise FileOperationError(f"File not found: {filepath}")
   ```

2. **Band Index Validation**
   ```python
   def validate_band_indices(indices, max_bands):
       for idx in indices:
           if idx < 0 or idx >= max_bands:
               raise ValidationError(f"Invalid band index: {idx}")
   ```

3. **Fallback for Band Names**
   ```python
   # Fallback for band names
   try:
       name = src.tags(i).get('name', f'Band {i}')
   except Exception:
       name = f'Band {i}'
   ```

## Metadata Preservation

### Preserved Per-Band Metadata

The system preserves comprehensive metadata for each band:

- **Name**: Unique band identifier
- **Description**: Detailed band description
- **Index**: Position in band sequence
- **Tags**: Custom metadata tags
- **Data Type**: Band data type
- **NoData Value**: NoData value for the band

### Preserved File Metadata

Global file metadata is also preserved:

- **Coordinate Reference System**: Geographic projection
- **Transform**: Geographic transformation matrix
- **Compression**: Compression settings
- **Tiling**: Tiling configuration
- **Global Tags**: File-level metadata tags

### Metadata Structure

```python
# Per-band metadata structure
band_metadata = {
    'name': 'Red Band',
    'description': 'Red spectral band',
    'index': 1,
    'tags': {'wavelength': '650nm'},
    'dtype': 'uint16',
    'nodata': 0
}

# File metadata structure
file_metadata = {
    'crs': 'EPSG:32632',
    'transform': Affine(...),
    'compression': 'lzw',
    'tiled': True,
    'tags': {'software': 'IGCV Raster Utility'}
}
```

## Compatibility Considerations

### Supported Formats

- **Primary**: GeoTIFF (.tif, .tiff)
- **Future**: Additional formats planned

### Data Type Support

- **Integer**: uint8, uint16, uint32, int16, int32
- **Float**: float32, float64
- **Complex**: complex64, complex128

### Coordinate Systems

- **Geographic**: WGS84, NAD83, etc.
- **Projected**: UTM, State Plane, etc.
- **Custom**: User-defined CRS

## Extension Points

### Custom Processing

The system is designed for extensibility:

```python
class CustomProcessor:
    def process_bands(self, bands, metadata):
        """Custom band processing logic."""
        # Implementation here
        return processed_bands
```

### New Export Formats

```python
def export_custom_format(out_path, bands, meta):
    """Export to custom format."""
    # Implementation here
    pass
```

### Metadata Extensions

```python
def extend_metadata(metadata, custom_data):
    """Extend metadata with custom information."""
    metadata.update(custom_data)
    return metadata
```

## Conclusion

The IGCV Raster Utility raster processing system provides:

- **Efficient Processing**: Selective reading and memory optimization
- **Metadata Preservation**: Complete metadata handling
- **User-Friendly Operations**: Intuitive interfaces and error handling
- **Extensibility**: Easy addition of new features
- **Robustness**: Comprehensive error handling and validation

This processing system forms the foundation for reliable and efficient raster data manipulation, supporting both interactive and automated workflows. 