import argparse
from model import raster_handler
import os
import sys
from exceptions import CLIError, ValidationError, FileOperationError, RasterHandlerError

def main(argv=None):
    try:
        parser = argparse.ArgumentParser(
            description="IGCVRasterTool CLI: selecione e exporte bandas de rasters GeoTIFF"
        )
        parser.add_argument('--input', '-i', required=True, help="Caminho do arquivo GeoTIFF de entrada")
        parser.add_argument('--bands', '-b', nargs='+', type=int, help="Bandas a exportar (1-baseadas, ex: 1 3 4). Omitir para listar bandas.")
        parser.add_argument('--output', '-o', help="Caminho do arquivo GeoTIFF de saída")
        parser.add_argument('--list', action='store_true', help="Apenas listar bandas do arquivo")

        args = parser.parse_args(argv)

        # Validação do arquivo de entrada
        if not os.path.exists(args.input):
            raise FileOperationError(f"Arquivo de entrada não encontrado: {args.input}")
        
        if not os.path.isfile(args.input):
            raise FileOperationError(f"O caminho especificado não é um arquivo: {args.input}")

        # Carregar informações do raster
        try:
            meta, band_names = raster_handler.load_raster(args.input)
        except RasterHandlerError as e:
            raise CLIError(f"Erro ao carregar o arquivo raster: {e}")
        except Exception as e:
            raise CLIError(f"Erro inesperado ao carregar o arquivo raster: {e}")

        print(f"Arquivo: {args.input}")
        print("Bandas disponíveis:")
        for idx, name in enumerate(band_names):
            print(f"{idx+1}: {name}")

        if args.list or not args.bands:
            print("\nUse --bands para escolher as bandas e --output para exportar.")
            return

        # Validação das bandas selecionadas
        selected_indices = [b-1 for b in args.bands]
        for b in selected_indices:
            if b < 0 or b >= len(band_names):
                raise ValidationError(f"Banda inválida: {b+1}. Bandas válidas: 1-{len(band_names)}")

        # Validação do arquivo de saída
        if not args.output:
            raise ValidationError("Por favor, especifique o arquivo de saída com --output")

        # Verificar se o diretório de saída existe
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            raise FileOperationError(f"Diretório de saída não existe: {output_dir}")

        # Ler bandas selecionadas
        try:
            bands, meta = raster_handler.read_selected_bands(args.input, selected_indices)
        except RasterHandlerError as e:
            raise CLIError(f"Erro ao ler as bandas selecionadas: {e}")
        except Exception as e:
            raise CLIError(f"Erro inesperado ao ler as bandas: {e}")

        # Exportar arquivo
        try:
            raster_handler.export_tif(args.output, bands, meta)
            print(f"Arquivo exportado com sucesso: {args.output}")
        except RasterHandlerError as e:
            raise CLIError(f"Erro ao exportar o arquivo: {e}")
        except Exception as e:
            raise CLIError(f"Erro inesperado ao exportar o arquivo: {e}")

    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        sys.exit(0)
    except SystemExit:
        # Re-raise SystemExit para manter códigos de saída corretos
        raise
    except (CLIError, ValidationError, FileOperationError, RasterHandlerError) as e:
        print(f"Erro: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
