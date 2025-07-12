"""
Centralized logging system for the IGCV Raster Utility project
"""

import logging
import os
from datetime import datetime

def setup_logger(name='igcv_raster_utility', level=logging.INFO):
    """
    Configures the logger for the project
    
    Args:
        name (str): Logger name
        level: Logging level (default: INFO)
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid handler duplication
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # File handler
    log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Message format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
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