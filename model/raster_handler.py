import rasterio
import os
from rasterio.errors import RasterioIOError, RasterioError
from exceptions import RasterHandlerError

def load_raster(filepath):
    """
    Carrega informações básicas de um arquivo raster.
    
    Args:
        filepath (str): Caminho para o arquivo raster
        
    Returns:
        tuple: (meta, band_names) - metadados e nomes das bandas
        
    Raises:
        RasterHandlerError: Se houver erro ao carregar o raster
    """
    try:
        if not os.path.exists(filepath):
            raise RasterHandlerError(f"Arquivo não encontrado: {filepath}")
        
        if not os.path.isfile(filepath):
            raise RasterHandlerError(f"O caminho especificado não é um arquivo: {filepath}")
        
        with rasterio.open(filepath) as src:
            meta = src.meta
            band_names = [f'Banda {i+1}' for i in range(src.count)]
        return meta, band_names
        
    except RasterioIOError as e:
        raise RasterHandlerError(f"Erro de I/O ao abrir o arquivo raster: {e}")
    except RasterioError as e:
        raise RasterHandlerError(f"Erro ao processar o arquivo raster: {e}")
    except Exception as e:
        raise RasterHandlerError(f"Erro inesperado ao carregar o raster: {e}")

def read_selected_bands(filepath, selected_indices):
    """
    Lê bandas específicas de um arquivo raster.
    
    Args:
        filepath (str): Caminho para o arquivo raster
        selected_indices (list): Lista de índices das bandas a ler (0-baseados)
        
    Returns:
        tuple: (bands, meta) - lista de bandas e metadados atualizados
        
    Raises:
        RasterHandlerError: Se houver erro ao ler as bandas
    """
    try:
        if not os.path.exists(filepath):
            raise RasterHandlerError(f"Arquivo não encontrado: {filepath}")
        
        with rasterio.open(filepath) as src:
            # Validar índices das bandas
            if not selected_indices:
                raise RasterHandlerError("Nenhuma banda foi selecionada")
            
            for idx in selected_indices:
                if idx < 0 or idx >= src.count:
                    raise RasterHandlerError(f"Índice de banda inválido: {idx}. Bandas disponíveis: 0-{src.count-1}")
            
            bands = []
            for i in selected_indices:
                try:
                    band = src.read(i+1)  # rasterio usa índices 1-baseados
                    bands.append(band)
                except Exception as e:
                    raise RasterHandlerError(f"Erro ao ler banda {i+1}: {e}")
            
            meta = src.meta.copy()
            meta.update({'count': len(selected_indices)})
            
        return bands, meta
        
    except RasterioIOError as e:
        raise RasterHandlerError(f"Erro de I/O ao ler as bandas: {e}")
    except RasterioError as e:
        raise RasterHandlerError(f"Erro ao processar as bandas: {e}")
    except RasterHandlerError:
        # Re-raise nossas exceções personalizadas
        raise
    except Exception as e:
        raise RasterHandlerError(f"Erro inesperado ao ler as bandas: {e}")

def export_tif(out_path, bands, meta):
    """
    Exporta bandas para um arquivo GeoTIFF.
    
    Args:
        out_path (str): Caminho para o arquivo de saída
        bands (list): Lista de arrays numpy das bandas
        meta (dict): Metadados do raster
        
    Raises:
        RasterHandlerError: Se houver erro ao exportar o arquivo
    """
    try:
        if not bands:
            raise RasterHandlerError("Nenhuma banda fornecida para exportação")
        
        # Verificar se o diretório de saída existe
        output_dir = os.path.dirname(out_path)
        if output_dir and not os.path.exists(output_dir):
            raise RasterHandlerError(f"Diretório de saída não existe: {output_dir}")
        
        # Verificar se o arquivo de saída já existe e se é gravável
        if os.path.exists(out_path):
            if not os.access(out_path, os.W_OK):
                raise RasterHandlerError(f"Sem permissão de escrita no arquivo: {out_path}")
        
        with rasterio.open(out_path, 'w', **meta) as dst:
            for i, band in enumerate(bands, start=1):
                try:
                    dst.write(band, i)
                except Exception as e:
                    raise RasterHandlerError(f"Erro ao escrever banda {i}: {e}")
                    
    except RasterioIOError as e:
        raise RasterHandlerError(f"Erro de I/O ao exportar o arquivo: {e}")
    except RasterioError as e:
        raise RasterHandlerError(f"Erro ao processar a exportação: {e}")
    except RasterHandlerError:
        # Re-raise nossas exceções personalizadas
        raise
    except Exception as e:
        raise RasterHandlerError(f"Erro inesperado ao exportar o arquivo: {e}")
