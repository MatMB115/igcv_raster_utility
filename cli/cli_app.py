import argparse
from model import raster_handler
import os
import sys
from exceptions import CLIError, ValidationError, FileOperationError, RasterHandlerError

def main(argv=None):
    try:
        parser = argparse.ArgumentParser(
            description="IGCVRasterTool CLI: select and export bands from GeoTIFF rasters"
        )
        parser.add_argument('--input', '-i', required=True, help="Input GeoTIFF file path")
        parser.add_argument('--bands', '-b', nargs='+', type=int, help="Bands to export (1-based, e.g.: 1 3 4). Omit to list bands.")
        parser.add_argument('--output', '-o', help="Output GeoTIFF file path")
        parser.add_argument('--list', action='store_true', help="Only list bands from file")

        args = parser.parse_args(argv)

        # Input file validation
        if not os.path.exists(args.input):
            raise FileOperationError(f"Input file not found: {args.input}")
        
        if not os.path.isfile(args.input):
            raise FileOperationError(f"The specified path is not a file: {args.input}")

        # Load raster information
        try:
            meta, band_names = raster_handler.load_raster(args.input)
        except RasterHandlerError as e:
            raise CLIError(f"Error loading raster file: {e}")
        except Exception as e:
            raise CLIError(f"Unexpected error loading raster file: {e}")

        print(f"File: {args.input}")
        print("Available bands:")
        for idx, name in enumerate(band_names):
            print(f"{idx+1}: {name}")

        if args.list or not args.bands:
            print("\nUse --bands to choose bands and --output to export.")
            return

        # Band selection validation
        selected_indices = [b-1 for b in args.bands]
        for b in selected_indices:
            if b < 0 or b >= len(band_names):
                raise ValidationError(f"Invalid band: {b+1}. Valid bands: 1-{len(band_names)}")

        # Output file validation
        if not args.output:
            raise ValidationError("Please specify output file with --output")

        # Check if output directory exists
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            raise FileOperationError(f"Output directory does not exist: {output_dir}")

        # Read selected bands
        try:
            bands, meta, selected_band_names, band_metadata, file_metadata = raster_handler.read_selected_bands(args.input, selected_indices)
        except RasterHandlerError as e:
            raise CLIError(f"Error reading selected bands: {e}")
        except Exception as e:
            raise CLIError(f"Unexpected error reading bands: {e}")

        # Export file
        try:
            raster_handler.export_tif(args.output, bands, meta, selected_band_names, band_metadata, file_metadata)
            print(f"File exported successfully: {args.output}")
        except RasterHandlerError as e:
            raise CLIError(f"Error exporting file: {e}")
        except Exception as e:
            raise CLIError(f"Unexpected error exporting file: {e}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except SystemExit:
        # Re-raise SystemExit to maintain correct exit codes
        raise
    except (CLIError, ValidationError, FileOperationError, RasterHandlerError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
