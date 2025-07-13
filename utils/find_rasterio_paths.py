#!/usr/bin/env python3
"""
Utility script to find GDAL and PROJ data paths for rasterio installation.
This helps users determine the correct paths for PyInstaller compilation.
"""

import os
import sys
from pathlib import Path


def find_rasterio_paths():
    """Find the paths to rasterio's GDAL and PROJ data directories."""
    
    try:
        import rasterio
        rasterio_path = Path(rasterio.__file__).parent
        print(f"Rasterio installation path: {rasterio_path}")
        
        # Look for gdal_data and proj_data directories
        gdal_data_path = None
        proj_data_path = None
        
        # Check in rasterio directory
        potential_gdal = rasterio_path / "gdal_data"
        potential_proj = rasterio_path / "proj_data"
        
        if potential_gdal.exists():
            gdal_data_path = potential_gdal
        if potential_proj.exists():
            proj_data_path = potential_proj
        
        # Check in parent directory (common location)
        parent_gdal = rasterio_path.parent / "gdal_data"
        parent_proj = rasterio_path.parent / "proj_data"
        
        if not gdal_data_path and parent_gdal.exists():
            gdal_data_path = parent_gdal
        if not proj_data_path and parent_proj.exists():
            proj_data_path = parent_proj
        
        # Check in site-packages
        site_packages = Path(rasterio_path).parent
        site_gdal = site_packages / "gdal_data"
        site_proj = site_packages / "proj_data"
        
        if not gdal_data_path and site_gdal.exists():
            gdal_data_path = site_gdal
        if not proj_data_path and site_proj.exists():
            proj_data_path = site_proj
        
        print("\nFound paths:")
        if gdal_data_path:
            print(f"GDAL data: {gdal_data_path}")
        else:
            print("GDAL data: NOT FOUND")
            
        if proj_data_path:
            print(f"PROJ data: {proj_data_path}")
        else:
            print("PROJ data: NOT FOUND")
        
        # Generate PyInstaller command
        print("\n" + "="*60)
        print("PYINSTALLER COMMAND TEMPLATE:")
        print("="*60)
        
        separator = ";" if sys.platform.startswith("win") else ":"
        
        cmd = f'pyinstaller --noconfirm --onefile --windowed \\\n'
        cmd += f'  --add-data "translations{separator}translations" \\\n'
        
        if gdal_data_path:
            cmd += f'  --add-data "{gdal_data_path}{separator}gdal_data" \\\n'
        else:
            cmd += f'  --add-data "PATH_TO_GDAL_DATA{separator}gdal_data" \\\n'
            
        if proj_data_path:
            cmd += f'  --add-data "{proj_data_path}{separator}proj_data" \\\n'
        else:
            cmd += f'  --add-data "PATH_TO_PROJ_DATA{separator}proj_data" \\\n'
            
        cmd += f'  --hidden-import rasterio.sample \\\n'
        cmd += f'  --hidden-import rasterio.vrt \\\n'
        cmd += f'  --hidden-import rasterio._features \\\n'
        cmd += f'  main.py'
        
        print(cmd)
        
        if not gdal_data_path or not proj_data_path:
            print("\n" + "="*60)
            print("TROUBLESHOOTING:")
            print("="*60)
            print("If GDAL or PROJ data paths are not found:")
            print("1. Check if rasterio is properly installed")
            print("2. Try reinstalling rasterio: pip install --force-reinstall rasterio")
            print("3. Check the rasterio documentation for your platform")
            print("4. Manual paths may be needed for your specific environment")
        
    except ImportError:
        print("Error: rasterio is not installed.")
        print("Please install it first: pip install rasterio")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    find_rasterio_paths() 