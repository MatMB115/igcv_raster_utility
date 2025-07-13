# Processamento de Dados Raster - IGCV Raster Utility

## Visão Geral

O processamento de dados raster é o núcleo funcional do IGCV Raster Utility. Este módulo é responsável por todas as operações relacionadas à leitura, manipulação e escrita de arquivos GeoTIFF, incluindo a preservação completa de metadados durante as operações.

## Arquitetura do Processamento

### Componente Principal: `model/raster_handler.py`

O `raster_handler.py` é o módulo central que encapsula toda a lógica de processamento raster. Ele fornece uma interface limpa e bem definida para:

- Carregamento de informações de raster
- Leitura seletiva de bandas
- Geração de previews
- Exportação com preservação de metadados

## Operações Principais

### 1. Carregamento de Raster (`load_raster`)

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
    """
```

#### Processo de Carregamento

1. **Validação de Arquivo**
   ```python
   if not os.path.exists(filepath):
       raise RasterHandlerError(f"File not found: {filepath}")
   
   if not os.path.isfile(filepath):
       raise RasterHandlerError(f"The specified path is not a file: {filepath}")
   ```

2. **Abertura com rasterio**
   ```python
   with rasterio.open(filepath) as src:
       meta = src.meta
       band_names = []
   ```

3. **Extração de Nomes de Bandas**
   ```python
   for i in range(src.count):
       band_idx = i + 1  # rasterio usa índices 1-based
       band_name = f'Band {band_idx}'  # fallback padrão
       
       # Tentativa de extrair nome de tags
       tags = src.tags(band_idx)
       possible_keys = ['name', 'band_name', 'description', 'title']
       
       for key in possible_keys:
           if key in tags and tags[key].strip():
               band_name = tags[key].strip()
               break
   ```

#### Metadados Extraídos

- **Dimensões**: `width`, `height`
- **Número de bandas**: `count`
- **Tipo de dados**: `dtype`
- **Sistema de coordenadas**: `crs`
- **Transformação geográfica**: `transform`
- **Valores NoData**: `nodata`
- **Configurações de compressão**: `compress`, `tiled`

### 2. Leitura Seletiva de Bandas (`read_selected_bands`)

```python
def read_selected_bands(filepath, selected_indices):
    """
    Lê bandas específicas de um arquivo raster.
    
    Args:
        filepath (str): Caminho para o arquivo raster
        selected_indices (list): Lista de índices das bandas (0-based)
        
    Returns:
        tuple: (bands, meta, selected_band_names, band_metadata, file_metadata)
    """
```

#### Processo de Leitura Seletiva

1. **Validação de Índices**
   ```python
   for idx in selected_indices:
       if idx < 0 or idx >= src.count:
           raise RasterHandlerError(f"Invalid band index: {idx}")
   ```

2. **Leitura de Bandas**
   ```python
   bands = []
   selected_band_names = []
   band_metadata = []
   
   for i in selected_indices:
       band_idx = i + 1  # conversão para 1-based
       band = src.read(band_idx)
       bands.append(band)
   ```

3. **Preservação de Metadados por Banda**
   ```python
   band_meta = {
       'tags': dict(src.tags(band_idx)),
       'description': src.descriptions[band_idx - 1],
       'nodata': src.nodata,
       'dtype': src.dtypes[band_idx - 1],
       'index': band_idx
   }
   band_metadata.append(band_meta)
   ```

4. **Captura de Metadados Globais**
   ```python
   file_metadata = {
       'tags': dict(src.tags()),
       'descriptions': list(src.descriptions),
       'colorinterp': list(src.colorinterp),
       'scales': list(src.scales),
       'offsets': list(src.offsets),
       'units': list(src.units),
       'masks': list(src.masks),
   }
   ```

### 3. Geração de Preview (`generate_preview_image`)

```python
def generate_preview_image(filepath, band_indices, max_size=500):
    """
    Gera uma visualização colorida das bandas selecionadas para preview.
    
    Nota: Esta função cria uma representação visual usando as bandas como canais
    de cor (similar ao RGB), mas não representa cores naturais reais.
    
    Args:
        filepath (str): Caminho para o arquivo raster
        band_indices (list): Índices das bandas (1-3 bandas)
        max_size (int): Tamanho máximo do preview
        
    Returns:
        numpy.ndarray: Array de visualização normalizado (0-255)
    """
```

#### Processo de Geração de Preview

1. **Validação de Entrada**
   ```python
   if len(band_indices) < 1 or len(band_indices) > 3:
       raise RasterHandlerError("Preview requires 1 to 3 bands")
   ```

2. **Cálculo de Downsampling**
   ```python
   width, height = src.width, src.height
   scale_factor = max(width, height) / max_size
   scale_factor = max(1, int(scale_factor))
   
   preview_width = width // scale_factor
   preview_height = height // scale_factor
   ```

3. **Leitura com Downsampling**
   ```python
   band_data = src.read(band_idx + 1, 
                       out_shape=(preview_height, preview_width),
                       resampling=Resampling.average)
   ```

4. **Composição de Visualização**
   ```python
   if len(band_indices) == 1:
       # Banda única: visualização em escala de cinza
       preview_array = np.stack([band_data_list[0], 
                               band_data_list[0], 
                               band_data_list[0]], axis=-1)
   elif len(band_indices) == 2:
       # Duas bandas: canal1=banda1, canal2=banda2, canal3=banda1
       preview_array = np.stack([band_data_list[0], 
                               band_data_list[1], 
                               band_data_list[0]], axis=-1)
   else:
       # Três bandas: canal1=banda1, canal2=banda2, canal3=banda3
       preview_array = np.stack(band_data_list, axis=-1)
   ```

5. **Normalização de Valores**
   ```python
   for i in range(3):
       band_data = preview_array[:, :, i]
       
       # Remove zeros para cálculo de percentil
       non_zero_data = band_data[band_data != 0]
       
       if len(non_zero_data) > 0:
           p2, p98 = np.percentile(non_zero_data, (2, 98))
           
           if p98 > p2:
               normalized = np.clip((band_data - p2) / (p98 - p2) * 255, 0, 255)
           else:
               normalized = np.full_like(band_data, 128, dtype=np.uint8)
   ```

### 4. Exportação de GeoTIFF (`export_tif`)

```python
def export_tif(out_path, bands, meta, band_names=None, 
               band_metadata=None, file_metadata=None):
    """
    Exporta bandas para arquivo GeoTIFF com preservação de metadados.
    
    Args:
        out_path (str): Caminho do arquivo de saída
        bands (list): Lista de arrays numpy das bandas
        meta (dict): Metadados do raster
        band_names (list): Nomes das bandas
        band_metadata (list): Metadados por banda
        file_metadata (dict): Metadados globais do arquivo
    """
```

#### Processo de Exportação

1. **Validação de Saída**
   ```python
   if not bands:
       raise RasterHandlerError("No bands provided for export")
   
   output_dir = os.path.dirname(out_path)
   if output_dir and not os.path.exists(output_dir):
       raise RasterHandlerError(f"Output directory does not exist: {output_dir}")
   ```

2. **Preparação de Metadados**
   ```python
   export_meta = meta.copy()
   if 'dtype' not in export_meta and bands:
       export_meta['dtype'] = bands[0].dtype
   ```

3. **Escrita com rasterio**
   ```python
   with rasterio.open(out_path, 'w', **export_meta) as dst:
       # Preservação de tags globais
       if file_metadata and file_metadata.get('tags'):
           dst.update_tags(**file_metadata['tags'])
       
       # Escrita de bandas
       for i, band in enumerate(bands, start=1):
           dst.write(band, i)
   ```

4. **Preservação de Metadados por Banda**
   ```python
   # Nome da banda
   if band_names and i <= len(band_names):
       dst.update_tags(i, name=band_names[i-1])
       dst.set_band_description(i, band_names[i-1])
   
   # Metadados adicionais
   if band_metadata and i <= len(band_metadata):
       band_meta = band_metadata[i-1]
       
       for key, value in band_meta['tags'].items():
           if key != 'name':
               dst.update_tags(i, **{key: value})
   ```

## Preservação de Metadados

### Metadados de Arquivo Preservados

1. **Informações Geográficas**
   - **CRS**: Sistema de coordenadas de referência
   - **Transform**: Matriz de transformação geográfica
   - **Bounds**: Limites geográficos do raster

2. **Informações Técnicas**
   - **Nodata**: Valores que representam dados ausentes
   - **Compressão**: Algoritmo de compressão (LZW por padrão)
   - **Tiling**: Configuração de blocos (256x256 por padrão)

3. **Tags Globais**
   - Metadados gerais do arquivo
   - Informações de criação e processamento
   - Dados de licenciamento e uso

### Metadados por Banda Preservados

1. **Identificação**
   - **Nome**: Identificador único da banda
   - **Descrição**: Informações detalhadas
   - **Índice**: Posição na sequência de bandas

2. **Características Técnicas**
   - **Tipo de dados**: Formato dos valores (uint8, float32, etc.)
   - **Escalas**: Fatores de escala para conversão
   - **Offsets**: Valores de deslocamento
   - **Unidades**: Unidades de medida dos valores

3. **Interpretação Visual**
   - **Colorinterp**: Interpretação de cor (red, green, blue, gray, etc.)
   - **Masks**: Máscaras de dados válidos
   - **Tags específicas**: Metadados customizados

## Otimizações de Performance

### 1. Leitura Seletiva

**Problema**: Carregar todas as bandas consome muita memória
**Solução**: Leitura apenas das bandas necessárias

```python
# ❌ Ineficiente - carrega todas as bandas
all_bands = src.read()

# ✅ Eficiente - carrega apenas bandas selecionadas
selected_bands = []
for idx in selected_indices:
    band = src.read(idx + 1)
    selected_bands.append(band)
```

### 2. Downsampling para Preview

**Problema**: Arquivos grandes tornam preview lento
**Solução**: Redução de resolução para visualização

```python
# Cálculo de fator de escala
scale_factor = max(width, height) / max_size
scale_factor = max(1, int(scale_factor))

# Leitura com downsampling
band_data = src.read(band_idx + 1, 
                    out_shape=(preview_height, preview_width),
                    resampling=Resampling.average)
```

### 3. Gerenciamento de Memória

**Problema**: Vazamentos de memória com arquivos grandes
**Solução**: Uso de context managers

```python
# ✅ Uso correto - liberação automática
with rasterio.open(filepath) as src:
    data = src.read(1)
    # src é automaticamente fechado ao sair do bloco

# ❌ Uso incorreto - pode causar vazamentos
src = rasterio.open(filepath)
data = src.read(1)
# src pode não ser fechado se houver exceção
```

### 4. Validação Precoce

**Problema**: Processamento de dados inválidos
**Solução**: Validação antes do processamento pesado

```python
# Validação de arquivo
if not os.path.exists(filepath):
    raise RasterHandlerError(f"File not found: {filepath}")

# Validação de índices
for idx in selected_indices:
    if idx < 0 or idx >= src.count:
        raise RasterHandlerError(f"Invalid band index: {idx}")
```

## Tratamento de Erros

### Tipos de Erro Específicos

1. **RasterioIOError**
   - Arquivo não encontrado
   - Problemas de permissão
   - Formato não suportado

2. **RasterioError**
   - Dados corrompidos
   - Metadados inválidos
   - Problemas de georreferenciamento

3. **ValidationError**
   - Índices de banda inválidos
   - Parâmetros incorretos
   - Dados inconsistentes

### Estratégias de Recuperação

1. **Fallbacks Inteligentes**
   ```python
   # Fallback para nomes de banda
   band_name = f'Band {band_idx}'  # padrão
   
   # Tentativa de extrair nome real
   try:
       tags = src.tags(band_idx)
       if 'name' in tags:
           band_name = tags['name']
   except Exception:
       pass  # mantém o padrão
   ```

2. **Validação Gradual**
   ```python
   # Validação básica primeiro
   if not os.path.exists(filepath):
       raise RasterHandlerError(f"File not found: {filepath}")
   
   # Validação de formato
   try:
       with rasterio.open(filepath) as src:
           pass
   except rasterio.RasterioIOError as e:
       raise RasterHandlerError(f"Invalid raster file: {e}")
   ```

3. **Logging Detalhado**
   ```python
   logger = get_logger()
   logger.info(f"Loading raster: {filepath}")
   logger.debug(f"File size: {os.path.getsize(filepath)} bytes")
   ```

## Considerações de Compatibilidade

### Formatos Suportados

- **Entrada**: GeoTIFF (.tif, .tiff)
- **Saída**: GeoTIFF com metadados preservados
- **Compressão**: LZW, DEFLATE, JPEG
- **Tiling**: Suportado e recomendado

### Limitações Atuais

1. **Formatos**
   - Apenas GeoTIFF suportado
   - Não suporta outros formatos raster (ENVI, HDF, etc.)

2. **Tamanho**
   - Limitado pela RAM disponível
   - Não implementa processamento por chunks

3. **Funcionalidades**
   - Sem reprojeção automática
   - Sem cálculo de índices espectrais
   - Sem filtros espaciais

## Extensibilidade

### Pontos de Extensão

1. **Novos Formatos**
   ```python
   class RasterFormatHandler:
       def can_read(self, filepath):
           pass
       
       def load_raster(self, filepath):
           pass
       
       def export_raster(self, data, filepath):
           pass
   ```

2. **Novos Processamentos**
   ```python
   class RasterProcessor:
       def process_bands(self, bands, parameters):
           pass
       
       def calculate_index(self, bands, formula):
           pass
   ```

3. **Novos Algoritmos de Preview**
   ```python
   class PreviewGenerator:
       def generate_preview(self, bands, method):
           pass
   ```

## Conclusão

O sistema de processamento raster do IGCV Raster Utility foi projetado para ser:

- **Robusto**: Tratamento abrangente de erros
- **Eficiente**: Otimizações de performance
- **Flexível**: Preservação completa de metadados
- **Extensível**: Arquitetura preparada para crescimento

Este módulo fornece uma base sólida para processamento de dados raster, com foco na preservação de metadados e facilidade de uso, permitindo workflows científicos confiáveis e reprodutíveis. 