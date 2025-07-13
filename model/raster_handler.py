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
            
            # Normalize each band to 0-255 range
            normalized_preview = np.zeros_like(preview_array, dtype=np.uint8)
            
            for i in range(3):
                band_data = preview_array[:, :, i]
                
                # Skip if band is all zeros or all same value
                if np.all(band_data == 0) or np.all(band_data == band_data.flat[0]):
                    normalized_preview[:, :, i] = 0
                    continue
                
                # Remove zeros for percentile calculation (if they're not meaningful data)
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
