"""
Sistema de logging centralizado para o projeto IGCV Raster Utility
"""

import logging
import os
from datetime import datetime

def setup_logger(name='igcv_raster_utility', level=logging.INFO):
    """
    Configura o logger para o projeto
    
    Args:
        name (str): Nome do logger
        level: Nível de logging (default: INFO)
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Criar diretório de logs se não existir
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Handler para arquivo
    log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name='igcv_raster_utility'):
    """
    Obtém o logger configurado
    
    Args:
        name (str): Nome do logger
        
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(name) 