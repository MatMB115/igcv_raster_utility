import rasterio
import os
import numpy as np
from rasterio.errors import RasterioIOError, RasterioError
from rasterio.windows import Window
from rasterio.enums import Resampling
from exceptions import RasterHandlerError

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
    try:
        if not os.path.exists(filepath):
            raise RasterHandlerError(f"File not found: {filepath}")
        
        if not os.path.isfile(filepath):
            raise RasterHandlerError(f"The specified path is not a file: {filepath}")
        
        with rasterio.open(filepath) as src:
            meta = src.meta
            band_names = []
            
            for i in range(src.count):
                band_idx = i + 1  # rasterio uses 1-based indices
                band_name = f'Band {band_idx}'  # default fallback
                
                try:
                    # Try to get band name from tags
                    tags = src.tags(band_idx)
                    
                    # Check different possible keys for band names
                    possible_keys = [
                        'name', 'band_name', 'description', 'title',
                        'BANDNAME', 'DESCRIPTION', 'TITLE',
                        'Name', 'BandName', 'Description'
                    ]
                    
                    for key in possible_keys:
                        if key in tags and tags[key].strip():
                            band_name = tags[key].strip()
                            break
                    
                    # If not found in tags, try to get band description
                    if band_name == f'Band {band_idx}':
                        desc = src.descriptions[band_idx - 1] if src.descriptions else None
                        if desc and desc.strip():
                            band_name = desc.strip()
                            
                except Exception:
                    # If there's any error trying to get the name, keep the fallback
                    pass
                
                band_names.append(band_name)
                
        return meta, band_names
        
    except RasterioIOError as e:
        raise RasterHandlerError(f"I/O error opening raster file: {e}")
    except RasterioError as e:
        raise RasterHandlerError(f"Error processing raster file: {e}")
    except Exception as e:
        raise RasterHandlerError(f"Unexpected error loading raster: {e}")

def read_selected_bands(filepath, selected_indices):
    """
    Reads specific bands from a raster file.
    
    Args:
        filepath (str): Path to the raster file
        selected_indices (list): List of band indices to read (0-based)
        
    Returns:
        tuple: (bands, meta, selected_band_names, band_metadata, file_metadata) - list of bands, updated metadata, selected band names, band metadata and file metadata
        
    Raises:
        RasterHandlerError: If there's an error reading the bands
    """
    try:
        if not os.path.exists(filepath):
            raise RasterHandlerError(f"File not found: {filepath}")
        
        with rasterio.open(filepath) as src:
            # Validate band indices
            if not selected_indices:
                raise RasterHandlerError("No bands were selected")
            
            for idx in selected_indices:
                if idx < 0 or idx >= src.count:
                    raise RasterHandlerError(f"Invalid band index: {idx}. Available bands: 0-{src.count-1}")
            
            bands = []
            selected_band_names = []
            band_metadata = []
            
            for i in selected_indices:
                try:
                    band_idx = i + 1  # rasterio uses 1-based indices
                    band = src.read(band_idx)
                    bands.append(band)
                    
                    # Get selected band name
                    band_name = f'Band {band_idx}'  # default fallback
                    
                    try:
                        # Try to get band name from tags
                        tags = src.tags(band_idx)
                        
                        # Check different possible keys for band names
                        possible_keys = [
                            'name', 'band_name', 'description', 'title',
                            'BANDNAME', 'DESCRIPTION', 'TITLE',
                            'Name', 'BandName', 'Description'
                        ]
                        
                        for key in possible_keys:
                            if key in tags and tags[key].strip():
                                band_name = tags[key].strip()
                                break
                        
                        # If not found in tags, try to get band description
                        if band_name == f'Band {band_idx}':
                            desc = src.descriptions[band_idx - 1] if src.descriptions else None
                            if desc and desc.strip():
                                band_name = desc.strip()
                                
                    except Exception:
                        # If there's any error trying to get the name, keep the fallback
                        pass
                    
                    selected_band_names.append(band_name)
                    
                    # Preserve band metadata
                    band_meta = {
                        'tags': dict(src.tags(band_idx)) if src.tags(band_idx) else {},
                        'description': src.descriptions[band_idx - 1] if src.descriptions and band_idx - 1 < len(src.descriptions) else None,
                        'nodata': src.nodata,
                        'dtype': src.dtypes[band_idx - 1] if band_idx - 1 < len(src.dtypes) else src.dtypes[0],
                        'index': band_idx
                    }
                    band_metadata.append(band_meta)
                    
                except Exception as e:
                    raise RasterHandlerError(f"Error reading band {i+1}: {e}")
            
            # Capture ALL metadata from the original file
            file_metadata = {
                'tags': dict(src.tags()) if src.tags() else {},  # Global file tags
                'descriptions': list(src.descriptions) if src.descriptions else [],  # Global descriptions
                'colorinterp': list(src.colorinterp) if hasattr(src, 'colorinterp') and src.colorinterp else [],
                'scales': list(src.scales) if hasattr(src, 'scales') and src.scales else [],
                'offsets': list(src.offsets) if hasattr(src, 'offsets') and src.offsets else [],
                'units': list(src.units) if hasattr(src, 'units') and src.units else [],
                'masks': list(src.masks) if hasattr(src, 'masks') and src.masks else [],
            }
            
            # Preserve ALL important metadata from the original file
            meta = src.meta.copy()
            
            # Update only the band count, preserving everything else
            meta.update({
                'count': len(selected_indices),
                'dtype': bands[0].dtype if bands else meta.get('dtype'),
            })
            
            # Ensure important geographic metadata is preserved
            if 'transform' not in meta and hasattr(src, 'transform'):
                meta['transform'] = src.transform
            if 'crs' not in meta and hasattr(src, 'crs'):
                meta['crs'] = src.crs
            if 'nodata' not in meta and hasattr(src, 'nodata'):
                meta['nodata'] = src.nodata
            
            # Preserve compression and tiling settings if they exist
            if 'compress' not in meta:
                meta['compress'] = 'lzw'
            if 'tiled' not in meta:
                meta['tiled'] = True
            if 'blockxsize' not in meta:
                meta['blockxsize'] = 256
            if 'blockysize' not in meta:
                meta['blockysize'] = 256
            
        return bands, meta, selected_band_names, band_metadata, file_metadata
        
    except RasterioIOError as e:
        raise RasterHandlerError(f"I/O error reading bands: {e}")
    except RasterioError as e:
        raise RasterHandlerError(f"Error processing bands: {e}")
    except RasterHandlerError:
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        raise RasterHandlerError(f"Unexpected error reading bands: {e}")

def generate_preview_image(filepath, band_indices, max_size=500):
    """
    Generates a color visualization preview from selected bands with downsampling for performance.
    
    Note: This function creates a visual representation using the selected bands as color channels
    (similar to RGB), but does not represent real natural colors. It's for visualization purposes only.
    
    Args:
        filepath (str): Path to the raster file
        band_indices (list): List of 1-3 band indices (0-based) for preview
        max_size (int): Maximum size for preview (width or height)
        
    Returns:
        numpy.ndarray: Preview image array (height, width, 3) with values 0-255
        
    Raises:
        RasterHandlerError: If there's an error generating the preview
    """
    try:
        if len(band_indices) < 1 or len(band_indices) > 3:
            raise RasterHandlerError("Preview requires 1 to 3 bands")
        
        if not os.path.exists(filepath):
            raise RasterHandlerError(f"File not found: {filepath}")
        
        with rasterio.open(filepath) as src:
            # Validate band indices
            for idx in band_indices:
                if idx < 0 or idx >= src.count:
                    raise RasterHandlerError(f"Invalid band index: {idx}. Available bands: 0-{src.count-1}")
            
            # Calculate downsampling factor
            width, height = src.width, src.height
            scale_factor = max(width, height) / max_size
            scale_factor = max(1, int(scale_factor))  # At least 1 (no upsampling)
            
            # Calculate window size for preview
            preview_width = width // scale_factor
            preview_height = height // scale_factor
            
            # Ensure minimum size
            preview_width = max(100, preview_width)
            preview_height = max(100, preview_height)
            
            # Read the selected bands with downsampling
            band_data_list = []
            for band_idx in band_indices:
                try:
                    # Read band with downsampling
                    band_data = src.read(band_idx + 1, 
                                        out_shape=(preview_height, preview_width),
                                        resampling=Resampling.average)
                    band_data_list.append(band_data)
                except Exception as e:
                    raise RasterHandlerError(f"Error reading band {band_idx + 1}: {e}")
            
            # Compose preview array based on number of bands
            if len(band_indices) == 1:
                # Single band: grayscale visualization (same band for all channels)
                preview_array = np.stack([band_data_list[0], band_data_list[0], band_data_list[0]], axis=-1)
            elif len(band_indices) == 2:
                # Two bands: channel1=band1, channel2=band2, channel3=band1
                preview_array = np.stack([band_data_list[0], band_data_list[1], band_data_list[0]], axis=-1)
            else:
                # Three bands: channel1=band1, channel2=band2, channel3=band3
                preview_array = np.stack(band_data_list, axis=-1)
            
            # Handle NoData values
            nodata = src.nodata
            if nodata is not None:
                # Create mask for NoData values
                mask = np.any(preview_array == nodata, axis=-1)
                # Replace NoData with 0 for visualization
                preview_array[mask] = 0
            
            # Normalize each band to 0-255 range with improved handling for float64 data
            normalized_preview = np.zeros_like(preview_array, dtype=np.uint8)
            
            for i in range(3):
                band_data = preview_array[:, :, i]
                
                # Handle NaN and infinite values
                band_data = np.nan_to_num(band_data, nan=0.0, posinf=0.0, neginf=0.0)
                
                # Skip if band is all zeros or all same value
                if np.all(band_data == 0) or np.all(band_data == band_data.flat[0]):
                    normalized_preview[:, :, i] = 0
                    continue
                
                # For float64 data, use more robust normalization
                if band_data.dtype == np.float64:
                    # Remove outliers using more aggressive percentiles
                    valid_data = band_data[np.isfinite(band_data) & (band_data != 0)]
                    
                    if len(valid_data) > 0:
                        # Use 1-99 percentile for better handling of extreme values
                        p1, p99 = np.percentile(valid_data, (1, 99))
                        
                        # If percentiles are too close, use min/max
                        if p99 - p1 < 1e-10:
                            p1, p99 = np.min(valid_data), np.max(valid_data)
                        
                        # Avoid division by zero
                        if p99 > p1:
                            # Normalize to 0-255 with clipping
                            normalized = np.clip((band_data - p1) / (p99 - p1) * 255, 0, 255)
                        else:
                            # If all values are the same, set to middle gray
                            normalized = np.full_like(band_data, 128, dtype=np.uint8)
                    else:
                        # If no valid data, set to black
                        normalized = np.zeros_like(band_data, dtype=np.uint8)
                else:
                    # For other data types, use original logic
                    non_zero_data = band_data[band_data != 0]
                    if len(non_zero_data) > 0:
                        # Use 2-98 percentile for better contrast
                        p2, p98 = np.percentile(non_zero_data, (2, 98))
                        
                        # Avoid division by zero
                        if p98 > p2:
                            # Normalize to 0-255
                            normalized = np.clip((band_data - p2) / (p98 - p2) * 255, 0, 255)
                        else:
                            # If all values are the same, set to middle gray
                            normalized = np.full_like(band_data, 128, dtype=np.uint8)
                    else:
                        # If all values are zero, set to black
                        normalized = np.zeros_like(band_data, dtype=np.uint8)
                
                normalized_preview[:, :, i] = normalized.astype(np.uint8)
            
            return normalized_preview
            
    except RasterioIOError as e:
        raise RasterHandlerError(f"I/O error generating preview: {e}")
    except RasterioError as e:
        raise RasterHandlerError(f"Error processing preview: {e}")
    except RasterHandlerError:
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        raise RasterHandlerError(f"Unexpected error generating preview: {e}")

def detect_data_issues(filepath, band_indices):
    """
    Detect potential issues in raster data that might cause preview problems.
    
    Args:
        filepath (str): Path to the raster file
        band_indices (list): List of band indices (0-based) to analyze
        
    Returns:
        dict: Issues detected and recommendations
    """
    try:
        with rasterio.open(filepath) as src:
            issues = {
                'has_issues': False,
                'issues': [],
                'recommendations': [],
                'band_details': {}
            }
            
            total_pixels = src.width * src.height
            
            for i, band_idx in enumerate(band_indices):
                band_data = src.read(band_idx + 1)
                band_issues = []
                band_recommendations = []
                
                # Check for NaN values
                nan_count = np.sum(np.isnan(band_data))
                if nan_count > 0:
                    nan_percent = (nan_count / total_pixels) * 100
                    band_issues.append(f"NaN values: {nan_count} pixels ({nan_percent:.2f}%)")
                    band_recommendations.append("Convert NaN to NoData (-9999)")
                
                # Check for infinite values
                inf_count = np.sum(np.isinf(band_data))
                if inf_count > 0:
                    inf_percent = (inf_count / total_pixels) * 100
                    band_issues.append(f"Infinite values: {inf_count} pixels ({inf_percent:.2f}%)")
                    band_recommendations.append("Convert infinite values to NoData (-9999)")
                
                # Check for extreme values in float64
                if band_data.dtype == np.float64:
                    valid_data = band_data[np.isfinite(band_data)]
                    if len(valid_data) > 0:
                        min_val = np.min(valid_data)
                        max_val = np.max(valid_data)
                        
                        # Check for very large or very small values
                        if abs(min_val) > 1e6 or abs(max_val) > 1e6:
                            band_issues.append(f"Extreme values: min={min_val:.2e}, max={max_val:.2e}")
                            band_recommendations.append("Consider data scaling or clipping")
                        
                        # Check for very small range (might cause preview issues)
                        if max_val - min_val < 1e-10:
                            band_issues.append("Very small data range - might cause preview issues")
                            band_recommendations.append("Check if data needs scaling")
                
                # Check for NoData issues
                nodata = src.nodata
                if nodata is None:
                    # Check if there are suspicious patterns that might indicate NoData
                    zero_count = np.sum(band_data == 0)
                    zero_percent = (zero_count / total_pixels) * 100
                    
                    if zero_percent > 50:  # More than 50% zeros
                        band_issues.append(f"High zero count: {zero_count} pixels ({zero_percent:.2f}%) - might be NoData")
                        band_recommendations.append("Consider setting NoData to 0")
                
                # Store band details
                issues['band_details'][f'band_{band_idx + 1}'] = {
                    'issues': band_issues,
                    'recommendations': band_recommendations,
                    'dtype': str(band_data.dtype),
                    'shape': band_data.shape,
                    'nan_count': int(nan_count),
                    'inf_count': int(inf_count)
                }
                
                # Add to overall issues
                if band_issues:
                    issues['has_issues'] = True
                    issues['issues'].extend([f"Banda {band_idx + 1}: {issue}" for issue in band_issues])
                    issues['recommendations'].extend(band_recommendations)
            
            # Remove duplicates from recommendations
            issues['recommendations'] = list(set(issues['recommendations']))
            
            return issues
            
    except Exception as e:
        return {
            'has_issues': True,
            'issues': [f"Error analyzing data: {str(e)}"],
            'recommendations': ["Unable to analyze data issues"],
            'band_details': {}
        }

def debug_band_statistics(filepath, band_indices):
    """
    Debug function to show statistics for selected bands.
    
    Args:
        filepath (str): Path to the raster file
        band_indices (list): List of band indices (0-based) to analyze
        
    Returns:
        dict: Statistics for each band
    """
    try:
        with rasterio.open(filepath) as src:
            stats = {}
            
            for i, band_idx in enumerate(band_indices):
                band_data = src.read(band_idx + 1)
                
                # Basic statistics
                band_stats = {
                    'min': float(np.min(band_data)),
                    'max': float(np.max(band_data)),
                    'mean': float(np.mean(band_data)),
                    'std': float(np.std(band_data)),
                    'dtype': str(band_data.dtype),
                    'shape': band_data.shape,
                    'nan_count': int(np.sum(np.isnan(band_data))),
                    'inf_count': int(np.sum(np.isinf(band_data))),
                    'zero_count': int(np.sum(band_data == 0)),
                    'unique_values': int(len(np.unique(band_data)))
                }
                
                # Percentiles
                valid_data = band_data[np.isfinite(band_data)]
                if len(valid_data) > 0:
                    percentiles = np.percentile(valid_data, [1, 5, 25, 50, 75, 95, 99])
                    band_stats.update({
                        'p1': float(percentiles[0]),
                        'p5': float(percentiles[1]),
                        'p25': float(percentiles[2]),
                        'p50': float(percentiles[3]),
                        'p75': float(percentiles[4]),
                        'p95': float(percentiles[5]),
                        'p99': float(percentiles[6])
                    })
                
                stats[f'band_{band_idx + 1}'] = band_stats
            
            return stats
            
    except Exception as e:
        return {'error': str(e)}

def apply_data_corrections(filepath, band_indices, output_path=None):
    """
    Apply automatic corrections to raster data to fix common issues.
    
    Args:
        filepath (str): Path to the input raster file
        band_indices (list): List of band indices (0-based) to process
        output_path (str, optional): Output file path. If None, creates a temporary file.
        
    Returns:
        str: Path to the corrected file
        
    Raises:
        RasterHandlerError: If there's an error applying corrections
    """
    try:
        if output_path is None:
            # Create output path with "_corrected" suffix
            base_path = os.path.splitext(filepath)[0]
            output_path = f"{base_path}_corrected.tif"
        
        with rasterio.open(filepath) as src:
            # Read all bands to preserve metadata
            all_bands = []
            for i in range(src.count):
                band_data = src.read(i + 1)
                all_bands.append(band_data)
            
            # Apply corrections to selected bands
            for band_idx in band_indices:
                if 0 <= band_idx < len(all_bands):
                    band_data = all_bands[band_idx]
                    
                    # Convert NaN and infinite values to -9999
                    band_data = np.nan_to_num(band_data, nan=-9999.0, posinf=-9999.0, neginf=-9999.0)
                    
                    # Update the band data
                    all_bands[band_idx] = band_data
            
            # Prepare metadata for export
            export_meta = src.meta.copy()
            export_meta['nodata'] = -9999.0  # Set NoData value
            
            # Export corrected file
            with rasterio.open(output_path, 'w', **export_meta) as dst:
                for i, band in enumerate(all_bands, start=1):
                    dst.write(band, i)
                    
                    # Preserve band names if available
                    try:
                        band_name = src.tags(i).get('name', f'Band {i}')
                        dst.update_tags(i, name=band_name)
                        dst.set_band_description(i, band_name)
                    except Exception:
                        pass
            
            return output_path
            
    except Exception as e:
        raise RasterHandlerError(f"Error applying data corrections: {e}")

def export_tif(out_path, bands, meta, band_names=None, band_metadata=None, file_metadata=None):
    """
    Exports bands to a GeoTIFF file.
    
    Args:
        out_path (str): Path to the output file
        bands (list): List of numpy arrays of bands
        meta (dict): Raster metadata
        band_names (list, optional): List of band names to preserve
        band_metadata (list, optional): List of band metadata to preserve
        file_metadata (dict, optional): Global file metadata to preserve
        
    Raises:
        RasterHandlerError: If there's an error exporting the file
    """
    try:
        if not bands:
            raise RasterHandlerError("No bands provided for export")
        
        # Check if output directory exists
        output_dir = os.path.dirname(out_path)
        if output_dir and not os.path.exists(output_dir):
            raise RasterHandlerError(f"Output directory does not exist: {output_dir}")
        
        # Check if output file already exists and is writable
        if os.path.exists(out_path):
            if not os.access(out_path, os.W_OK):
                raise RasterHandlerError(f"No write permission for file: {out_path}")
        
        # Ensure metadata is correct
        export_meta = meta.copy()
        if 'dtype' not in export_meta and bands:
            export_meta['dtype'] = bands[0].dtype
        
        with rasterio.open(out_path, 'w', **export_meta) as dst:
            # Preserve global file tags if they exist
            if file_metadata and file_metadata.get('tags'):
                try:
                    dst.update_tags(**file_metadata['tags'])
                except Exception:
                    # If unable to preserve global tags, continue
                    pass
            
            for i, band in enumerate(bands, start=1):
                try:
                    dst.write(band, i)
                    
                    # Preserve band name if provided
                    if band_names and i <= len(band_names):
                        band_name = band_names[i-1]
                        # Set band name in tags
                        dst.update_tags(i, name=band_name)
                        # Set band description
                        dst.set_band_description(i, band_name)
                    
                    # Preserve additional band metadata if provided
                    if band_metadata and i <= len(band_metadata):
                        band_meta = band_metadata[i-1]
                        
                        # Preserve original tags
                        if band_meta.get('tags'):
                            for key, value in band_meta['tags'].items():
                                if key != 'name':  # Avoid overwriting the name already set
                                    dst.update_tags(i, **{key: value})
                        
                        # Preserve description if not set by name
                        if not band_names or i > len(band_names):
                            if band_meta.get('description'):
                                dst.set_band_description(i, band_meta['description'])
                    
                    # Preserve specific band metadata if available
                    if file_metadata:
                        # Preserve color interpretation
                        if file_metadata.get('colorinterp') and i <= len(file_metadata['colorinterp']):
                            try:
                                dst.colorinterp = file_metadata['colorinterp'][:len(bands)]
                            except Exception:
                                pass
                        
                        # Preserve scales
                        if file_metadata.get('scales') and i <= len(file_metadata['scales']):
                            try:
                                dst.scales = file_metadata['scales'][:len(bands)]
                            except Exception:
                                pass
                        
                        # Preserve offsets
                        if file_metadata.get('offsets') and i <= len(file_metadata['offsets']):
                            try:
                                dst.offsets = file_metadata['offsets'][:len(bands)]
                            except Exception:
                                pass
                        
                        # Preserve units
                        if file_metadata.get('units') and i <= len(file_metadata['units']):
                            try:
                                dst.units = file_metadata['units'][:len(bands)]
                            except Exception:
                                pass
                        
                except Exception as e:
                    raise RasterHandlerError(f"Error writing band {i}: {e}")
                    
    except RasterioIOError as e:
        raise RasterHandlerError(f"I/O error exporting file: {e}")
    except RasterioError as e:
        raise RasterHandlerError(f"Error processing export: {e}")
    except RasterHandlerError:
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        raise RasterHandlerError(f"Unexpected error exporting file: {e}")
