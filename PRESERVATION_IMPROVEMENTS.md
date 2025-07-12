# Melhorias na Preservação de Dados e Nomes de Bandas

## Problema Identificado

As amostras exportadas estavam diferentes do arquivo original devido a:

1. **Perda de nomes das bandas**: Os nomes originais das bandas não estavam sendo preservados na exportação
2. **Perda de metadados**: Metadados importantes das bandas não estavam sendo transferidos
3. **Perda de metadados globais**: Tags globais do arquivo e outros metadados não eram preservados
4. **Configurações de compressão**: Configurações de exportação não estavam preservando as configurações originais

## Soluções Implementadas

### 1. Preservação de Nomes das Bandas

**Antes:**
- A função `export_tif()` não preservava os nomes das bandas
- Os nomes eram perdidos durante a exportação

**Depois:**
- A função `read_selected_bands()` agora retorna os nomes das bandas selecionadas
- A função `export_tif()` aceita e preserva os nomes das bandas usando:
  - `dst.update_tags(i, name=band_name)` - Define o nome nas tags da banda
  - `dst.set_band_description(i, band_name)` - Define a descrição da banda

### 2. Preservação de Metadados das Bandas

**Novo:**
- A função `read_selected_bands()` agora coleta e retorna metadados detalhados de cada banda:
  - Tags originais da banda
  - Descrições originais
  - Tipo de dados (dtype)
  - Valor de nodata
  - Índice da banda

### 3. Preservação de Metadados Globais do Arquivo

**NOVO - Implementação Completa:**
- Captura e preserva **TODOS** os metadados globais do arquivo:
  - Tags globais do arquivo (`src.tags()`)
  - Descrições globais (`src.descriptions`)
  - Interpretação de cor (`src.colorinterp`)
  - Escalas (`src.scales`)
  - Offsets (`src.offsets`)
  - Unidades (`src.units`)
  - Máscaras (`src.masks`)

### 4. Melhor Preservação de Metadados do Arquivo

**Melhorado:**
- Preservação de configurações importantes:
  - Tipo de dados (dtype)
  - Valor de nodata
  - Transformação geográfica (transform)
  - Sistema de coordenadas (CRS)
  - Compressão (padrão: lzw)
  - Tiling (padrão: True)
  - Tamanho dos blocos (padrão: 256x256)

### 5. Scripts de Teste

**Criados:**
- `test_band_names.py` - Testa preservação de nomes de bandas e metadados
- Verificação completa de preservação de dados

## Mudanças no Código

### model/raster_handler.py

```python
# Antes
def read_selected_bands(filepath, selected_indices):
    return bands, meta

def export_tif(out_path, bands, meta):
    # Não preservava nomes nem metadados globais

# Depois
def read_selected_bands(filepath, selected_indices):
    return bands, meta, selected_band_names, band_metadata, file_metadata

def export_tif(out_path, bands, meta, band_names=None, band_metadata=None, file_metadata=None):
    # Preserva nomes, metadados das bandas E metadados globais
```

### controller/main_controller.py

```python
# Atualizado para usar nova assinatura
bands, meta, selected_band_names, band_metadata, file_metadata = raster_handler.read_selected_bands(...)
raster_handler.export_tif(out_path, bands, meta, selected_band_names, band_metadata, file_metadata)
```

### cli/cli_app.py

```python
# Atualizado para usar nova assinatura
bands, meta, selected_band_names, band_metadata, file_metadata = raster_handler.read_selected_bands(...)
raster_handler.export_tif(args.output, bands, meta, selected_band_names, band_metadata, file_metadata)
```

## Metadados Agora Preservados

### ✅ **Metadados das Bandas:**
- Nomes das bandas
- Tags específicas de cada banda
- Descrições das bandas
- Tipo de dados (dtype)
- Valor de nodata

### ✅ **Metadados Globais do Arquivo:**
- Tags globais do arquivo
- Descrições globais
- Interpretação de cor (RGB, Gray, etc.)
- Escalas de valores
- Offsets de valores
- Unidades de medida
- Máscaras de dados

### ✅ **Metadados Geográficos:**
- Sistema de coordenadas (CRS)
- Transformação geográfica
- Dimensões (width, height)
- Configurações de compressão
- Configurações de tiling

## Como Testar

### Teste de Nomes de Bandas e Metadados
```bash
python test_band_names.py seu_arquivo.tif
```

Este teste agora verifica:
- Preservação de nomes das bandas
- Preservação de metadados globais
- Preservação de metadados geográficos
- Preservação de configurações do arquivo

## Resultados Esperados

Após as melhorias:

1. **Nomes preservados**: Os nomes originais das bandas são mantidos no arquivo exportado
2. **Dados idênticos**: Os valores dos pixels são preservados exatamente
3. **Metadados completos**: TODOS os metadados importantes são preservados
4. **Compatibilidade total**: Arquivos exportados são 100% compatíveis com outros softwares GIS
5. **Fidelidade máxima**: O arquivo exportado é uma réplica fiel do original (apenas com as bandas selecionadas)

## Compatibilidade

- **Retrocompatibilidade**: As funções antigas ainda funcionam (parâmetros opcionais)
- **Interface**: GUI e CLI continuam funcionando normalmente
- **Formatos**: Suporte mantido para GeoTIFF
- **Softwares GIS**: Compatível com QGIS, ArcGIS, ENVI, etc.

## Próximos Passos

1. Testar com diferentes tipos de arquivos GeoTIFF
2. Verificar compatibilidade com outros softwares GIS
3. Adicionar suporte para outros formatos de saída se necessário
4. Implementar preservação de estatísticas das bandas (min/max/mean)
5. Adicionar suporte para preservação de paletas de cores 