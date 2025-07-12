"""
Exceções personalizadas para o projeto IGCV Raster Utility
"""

class IGCVRasterError(Exception):
    """Exceção base para todos os erros do projeto"""
    pass

class RasterHandlerError(IGCVRasterError):
    """Exceção para erros relacionados ao processamento de rasters"""
    pass

class ControllerError(IGCVRasterError):
    """Exceção para erros relacionados ao controller"""
    pass

class ViewError(IGCVRasterError):
    """Exceção para erros relacionados à interface gráfica"""
    pass

class CLIError(IGCVRasterError):
    """Exceção para erros relacionados à interface de linha de comando"""
    pass

class ValidationError(IGCVRasterError):
    """Exceção para erros de validação de dados"""
    pass

class FileOperationError(IGCVRasterError):
    """Exceção para erros de operações com arquivos"""
    pass 