# Guia de Desenvolvimento - IGCV Raster Utility

## Visão Geral

Este documento fornece orientações para desenvolvedores que desejam contribuir para o projeto IGCV Raster Utility ou estender suas funcionalidades.

## Ambiente de Desenvolvimento

### Requisitos do Sistema

- **Python**: 3.8 ou superior
- **Sistema Operacional**: Windows, Linux, macOS
- **Git**: Para controle de versão
- **IDE**: VS Code, PyCharm, ou Cursor

### Configuração Inicial

1. **Clone do Repositório**
   ```bash
   git clone https://github.com/your-username/igcv_raster_utility.git
   cd igcv_raster_utility
   ```

2. **Criação de Ambiente Virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Instalação de Dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Compilação de Traduções**
   ```bash
   python utils/compile_translations.py
   ```

### Estrutura do Projeto

```
igcv_raster_utility/
├── main.py                 # Ponto de entrada da aplicação
├── exceptions.py           # Hierarquia de exceções
├── logger.py              # Sistema de logging
├── requirements.txt       # Dependências Python
├── cli/                   # Interface de linha de comando
│   └── cli_app.py
├── controller/            # Lógica de controle (MVC)
│   └── main_controller.py
├── model/                 # Lógica de negócio (MVC)
│   └── raster_handler.py
├── view/                  # Interface gráfica (MVC)
│   └── main_window.py
├── utils/                 # Utilitários
│   └── compile_translations.py
├── translations/          # Arquivos de tradução
│   ├── igcv_en.ts
│   ├── igcv_pt_BR.ts
│   └── README.md
├── docs/                  # Documentação
├── logs/                  # Arquivos de log
└── assets/               # Recursos (ícones, etc.)
    └── icon.png
```

## Padrões de Código

### Convenções Python

#### 1. PEP 8 - Estilo de Código

```python
# ✅ Bom
def process_raster_data(file_path, band_indices):
    """Processa dados raster do arquivo especificado."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    return process_bands(file_path, band_indices)

# ❌ Ruim
def processRasterData(filePath,bandIndices):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filePath}")
    return processBands(filePath,bandIndices)
```

#### 2. Docstrings

```python
def load_raster(filepath):
    """
    Carrega informações básicas de um arquivo raster.
    
    Args:
        filepath (str): Caminho para o arquivo raster
        
    Returns:
        tuple: (meta, band_names) - metadados e nomes das bandas
        
    Raises:
        RasterHandlerError: Se houver erro no carregamento
        
    Example:
        >>> meta, names = load_raster("image.tif")
        >>> print(f"Bandas: {len(names)}")
        Bandas: 4
    """
```

#### 3. Type Hints

```python
from typing import List, Tuple, Dict, Optional
import numpy as np

def read_selected_bands(
    filepath: str, 
    selected_indices: List[int]
) -> Tuple[List[np.ndarray], Dict, List[str], List[Dict], Dict]:
    """
    Lê bandas específicas de um arquivo raster.
    
    Args:
        filepath: Caminho para o arquivo raster
        selected_indices: Lista de índices das bandas (0-based)
        
    Returns:
        Tuple contendo: (bands, meta, band_names, band_metadata, file_metadata)
    """
```

### Padrões de Arquitetura

#### 1. Princípio da Responsabilidade Única (SRP)

```python
# ✅ Bom - Cada classe tem uma responsabilidade
class RasterLoader:
    """Responsável apenas por carregar dados raster."""
    
class MetadataExtractor:
    """Responsável apenas por extrair metadados."""
    
class BandProcessor:
    """Responsável apenas por processar bandas."""

# ❌ Ruim - Classe com múltiplas responsabilidades
class RasterHandler:
    """Faz tudo: carrega, processa, exporta, etc."""
```

#### 2. Inversão de Dependência (DIP)

```python
# ✅ Bom - Depende de abstrações
class RasterProcessor:
    def __init__(self, loader: RasterLoader, exporter: RasterExporter):
        self.loader = loader
        self.exporter = exporter
    
    def process(self, filepath: str) -> None:
        data = self.loader.load(filepath)
        result = self.process_data(data)
        self.exporter.export(result)

# ❌ Ruim - Depende de implementações concretas
class RasterProcessor:
    def __init__(self):
        self.loader = RasterLoader()  # Dependência concreta
        self.exporter = RasterExporter()  # Dependência concreta
```

#### 3. Padrão Strategy

```python
# Interface para diferentes estratégias de processamento
class ProcessingStrategy:
    def process(self, data: np.ndarray) -> np.ndarray:
        raise NotImplementedError

class NormalizationStrategy(ProcessingStrategy):
    def process(self, data: np.ndarray) -> np.ndarray:
        return (data - data.min()) / (data.max() - data.min())

class PercentileStrategy(ProcessingStrategy):
    def __init__(self, min_percentile: float = 2, max_percentile: float = 98):
        self.min_percentile = min_percentile
        self.max_percentile = max_percentile
    
    def process(self, data: np.ndarray) -> np.ndarray:
        p_min, p_max = np.percentile(data, (self.min_percentile, self.max_percentile))
        return np.clip((data - p_min) / (p_max - p_min), 0, 1)

# Uso do padrão
class RasterProcessor:
    def __init__(self, strategy: ProcessingStrategy):
        self.strategy = strategy
    
    def process_raster(self, data: np.ndarray) -> np.ndarray:
        return self.strategy.process(data)
```

## Tratamento de Erros

### Hierarquia de Exceções

```python
class IGCVRasterError(Exception):
    """Exceção base para todos os erros do projeto."""
    pass

class RasterHandlerError(IGCVRasterError):
    """Erros relacionados ao processamento de rasters."""
    pass

class ValidationError(IGCVRasterError):
    """Erros de validação de dados."""
    pass

class FileOperationError(IGCVRasterError):
    """Erros de operações com arquivos."""
    pass
```

### Boas Práticas

#### 1. Exceções Específicas

```python
# ✅ Bom - Exceção específica
def load_raster(filepath: str) -> Tuple[Dict, List[str]]:
    if not os.path.exists(filepath):
        raise FileOperationError(f"Arquivo não encontrado: {filepath}")
    
    try:
        with rasterio.open(filepath) as src:
            return src.meta, get_band_names(src)
    except rasterio.RasterioIOError as e:
        raise RasterHandlerError(f"Erro ao abrir raster: {e}")

# ❌ Ruim - Exceção genérica
def load_raster(filepath: str) -> Tuple[Dict, List[str]]:
    if not os.path.exists(filepath):
        raise Exception(f"Arquivo não encontrado: {filepath}")
    
    with rasterio.open(filepath) as src:
        return src.meta, get_band_names(src)
```

#### 2. Context Managers

```python
# ✅ Bom - Uso de context managers
def process_raster(filepath: str) -> np.ndarray:
    with rasterio.open(filepath) as src:
        data = src.read(1)
        return process_data(data)

# ❌ Ruim - Gerenciamento manual
def process_raster(filepath: str) -> np.ndarray:
    src = rasterio.open(filepath)
    try:
        data = src.read(1)
        return process_data(data)
    finally:
        src.close()
```

## Sistema de Logging

### Configuração

```python
import logging
from logger import setup_logger

# Configuração do logger
logger = setup_logger('my_module')

def my_function():
    logger.info("Iniciando processamento")
    try:
        # Processamento
        logger.debug("Dados processados com sucesso")
    except Exception as e:
        logger.error(f"Erro no processamento: {e}", exc_info=True)
        raise
```

### Níveis de Log

```python
# DEBUG - Informações detalhadas para desenvolvimento
logger.debug(f"Processando banda {band_index}")

# INFO - Informações gerais sobre o progresso
logger.info(f"Arquivo carregado: {filepath}")

# WARNING - Situações que merecem atenção
logger.warning(f"Banda {band_index} sem nome, usando padrão")

# ERROR - Erros que impedem operação normal
logger.error(f"Falha ao carregar arquivo: {filepath}")

# CRITICAL - Erros críticos que podem causar falha do sistema
logger.critical("Falha crítica no sistema de arquivos")
```

## Extensibilidade

### Adicionando Novos Formatos

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
import numpy as np

class RasterFormatHandler(ABC):
    """Interface para handlers de diferentes formatos raster."""
    
    @abstractmethod
    def can_read(self, filepath: str) -> bool:
        """Verifica se o handler pode ler o arquivo."""
        pass
    
    @abstractmethod
    def load_raster(self, filepath: str) -> Tuple[Dict, List[str]]:
        """Carrega informações do raster."""
        pass
    
    @abstractmethod
    def read_bands(self, filepath: str, indices: List[int]) -> List[np.ndarray]:
        """Lê bandas específicas."""
        pass
    
    @abstractmethod
    def export_raster(self, filepath: str, bands: List[np.ndarray], 
                     meta: Dict) -> None:
        """Exporta dados para o formato."""
        pass

class GeoTIFFHandler(RasterFormatHandler):
    """Handler para arquivos GeoTIFF."""
    
    def can_read(self, filepath: str) -> bool:
        return filepath.lower().endswith(('.tif', '.tiff'))
    
    def load_raster(self, filepath: str) -> Tuple[Dict, List[str]]:
        # Implementação específica para GeoTIFF
        pass
    
    def read_bands(self, filepath: str, indices: List[int]) -> List[np.ndarray]:
        # Implementação específica para GeoTIFF
        pass
    
    def export_raster(self, filepath: str, bands: List[np.ndarray], 
                     meta: Dict) -> None:
        # Implementação específica para GeoTIFF
        pass

class ENVIHandler(RasterFormatHandler):
    """Handler para arquivos ENVI."""
    
    def can_read(self, filepath: str) -> bool:
        return filepath.lower().endswith('.hdr')
    
    # Implementações específicas para ENVI...

# Factory para seleção automática do handler
class RasterHandlerFactory:
    _handlers: List[RasterFormatHandler] = [
        GeoTIFFHandler(),
        ENVIHandler(),
    ]
    
    @classmethod
    def get_handler(cls, filepath: str) -> RasterFormatHandler:
        for handler in cls._handlers:
            if handler.can_read(filepath):
                return handler
        raise ValueError(f"Nenhum handler encontrado para: {filepath}")
```

### Adicionando Novos Processamentos

```python
class RasterProcessor:
    """Processador de dados raster com plugins."""
    
    def __init__(self):
        self.processors = {}
    
    def register_processor(self, name: str, processor: callable):
        """Registra um novo processador."""
        self.processors[name] = processor
    
    def process(self, data: np.ndarray, processor_name: str, **kwargs) -> np.ndarray:
        """Executa um processador específico."""
        if processor_name not in self.processors:
            raise ValueError(f"Processador não encontrado: {processor_name}")
        
        return self.processors[processor_name](data, **kwargs)

# Exemplo de processadores
def normalize_processor(data: np.ndarray, min_val: float = 0, 
                       max_val: float = 1) -> np.ndarray:
    """Normaliza dados para o intervalo especificado."""
    data_min, data_max = data.min(), data.max()
    return (data - data_min) / (data_max - data_min) * (max_val - min_val) + min_val

def clip_processor(data: np.ndarray, min_val: float, max_val: float) -> np.ndarray:
    """Corta dados para o intervalo especificado."""
    return np.clip(data, min_val, max_val)

# Uso
processor = RasterProcessor()
processor.register_processor('normalize', normalize_processor)
processor.register_processor('clip', clip_processor)

# Processamento
result = processor.process(data, 'normalize', min_val=0, max_val=255)
result = processor.process(result, 'clip', min_val=0, max_val=255)
```

## Performance e Otimização

### Profiling

```python
import cProfile
import pstats
from pstats import SortKey

def profile_function(func, *args, **kwargs):
    """Perfila uma função específica."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = func(*args, **kwargs)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats(SortKey.TIME)
    stats.print_stats(10)  # Top 10 funções mais lentas
    
    return result

# Uso
result = profile_function(load_raster, "large_file.tif")
```

### Otimizações Comuns

#### 1. Leitura Eficiente

```python
# ✅ Bom - Leitura seletiva
def read_bands_efficient(filepath: str, indices: List[int]) -> List[np.ndarray]:
    with rasterio.open(filepath) as src:
        return [src.read(i + 1) for i in indices]

# ❌ Ruim - Leitura de todas as bandas
def read_bands_inefficient(filepath: str, indices: List[int]) -> List[np.ndarray]:
    with rasterio.open(filepath) as src:
        all_bands = src.read()  # Carrega todas as bandas
        return [all_bands[i] for i in indices]
```

#### 2. Processamento em Chunks

```python
def process_large_raster(filepath: str, chunk_size: int = 1024):
    """Processa raster grande em chunks."""
    with rasterio.open(filepath) as src:
        for ji, window in src.block_windows(1):
            data = src.read(window=window)
            processed = process_chunk(data)
            # Salvar resultado...
```

#### 3. Cache de Metadados

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_raster_metadata(filepath: str) -> Dict:
    """Cache de metadados para evitar leituras repetidas."""
    with rasterio.open(filepath) as src:
        return src.meta
```

## Documentação

### Docstrings

```python
def calculate_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    """
    Calcula o Índice de Vegetação por Diferença Normalizada (NDVI).
    
    O NDVI é calculado usando a fórmula: (NIR - RED) / (NIR + RED)
    onde NIR é a banda do infravermelho próximo e RED é a banda vermelha.
    
    Args:
        red_band: Array numpy da banda vermelha
        nir_band: Array numpy da banda do infravermelho próximo
        
    Returns:
        Array numpy com valores NDVI no intervalo [-1, 1]
        
    Raises:
        ValueError: Se as bandas têm dimensões diferentes
        ZeroDivisionError: Se a soma NIR + RED for zero em algum pixel
        
    Example:
        >>> red = np.array([[100, 150], [200, 250]])
        >>> nir = np.array([[200, 300], [400, 500]])
        >>> ndvi = calculate_ndvi(red, nir)
        >>> print(ndvi)
        [[0.33333333 0.33333333]
         [0.33333333 0.33333333]]
        
    Note:
        Valores NDVI típicos:
        - -1 a 0: Água, nuvens, neve
        - 0 a 0.2: Solo exposto, rochas
        - 0.2 a 0.5: Vegetação esparsa
        - 0.5 a 1.0: Vegetação densa
    """
    if red_band.shape != nir_band.shape:
        raise ValueError("As bandas devem ter as mesmas dimensões")
    
    numerator = nir_band - red_band
    denominator = nir_band + red_band
    
    # Evita divisão por zero
    denominator = np.where(denominator == 0, 1e-10, denominator)
    
    return numerator / denominator
```

### Documentação de API

```python
class RasterProcessor:
    """
    Processador principal de dados raster.
    
    Esta classe fornece métodos para carregar, processar e exportar
    dados raster em diferentes formatos.
    
    Attributes:
        supported_formats (List[str]): Lista de formatos suportados
        max_file_size (int): Tamanho máximo de arquivo em bytes
        
    Example:
        >>> processor = RasterProcessor()
        >>> meta, bands = processor.load("image.tif")
        >>> processed = processor.normalize(bands[0])
        >>> processor.export("output.tif", [processed], meta)
    """
    
    def __init__(self, max_file_size: int = 1024**3):
        """
        Inicializa o processador.
        
        Args:
            max_file_size: Tamanho máximo de arquivo permitido
        """
        self.max_file_size = max_file_size
        self.supported_formats = ['.tif', '.tiff']
```

## Contribuição

### Processo de Contribuição

1. **Fork** do repositório
2. **Criação** de branch para feature
3. **Desenvolvimento** seguindo padrões
4. **Documentação** das mudanças
5. **Pull Request** com descrição detalhada

### Checklist de Pull Request

- [ ] Código segue PEP 8
- [ ] Documentação atualizada
- [ ] Logs apropriados adicionados
- [ ] Tratamento de erros implementado
- [ ] Compatibilidade mantida

## Conclusão

Este guia fornece as bases para desenvolvimento e contribuição no projeto IGCV Raster Utility. Seguindo estes padrões e práticas, você pode:

Para dúvidas específicas ou sugestões de melhoria, consulte a documentação técnica ou abra uma issue no repositório. 