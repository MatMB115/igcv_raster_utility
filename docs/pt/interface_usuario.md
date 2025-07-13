# Interfaces de Usuário - IGCV Raster Utility

## Visão Geral

O IGCV Raster Utility oferece duas interfaces de usuário distintas para atender diferentes necessidades de uso:

1. **Interface Gráfica (GUI)**: Interface visual intuitiva para uso interativo
2. **Interface de Linha de Comando (CLI)**: Interface textual para processamento em lote e automação

## Interface Gráfica (GUI)

### Arquitetura da GUI

A interface gráfica é construída usando PyQt5 e segue o padrão MVC, onde a View (`main_window.py`) é responsável pela apresentação e interação com o usuário.

#### Componentes Principais

```
┌─────────────────────────────────────────────────────────────────┐
│                    IGCV Raster Tool - MVP                       │
├─────────────────────────────────────────────────────────────────┤
│  Idioma ▼                                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────┐  ┌─────────────────────────────────┐ │
│  │   PAINEL ESQUERDO     │  │        PAINEL DIREITO           │ │
│  │                       │  │                                 │ │
│  │ [Abrir Raster]        │  │  Metadados do Raster            │ │
│  │                       │  │ ┌─────────────────────────────┐ │ │
│  │ Bandas disponíveis:   │  │ │                             │ │ │
│  │    Band 1             │  │ │  [Informações detalhadas]   │ │ │
│  │    Band 2             │  │ │                             │ │ │
│  │    Band 3             │  │ │                             │ │ │
│  │    Band 4             │  │ └─────────────────────────────┘ │ │
│  │                       │  │                                 │ │
│  │   Preview             │  │                                 │ │
│  │   [Gerar Preview]     │  │                                 │ │
│  │ ┌─────────────────┐   │  │                                 │ │
│  │ │                 │   │  │                                 │ │
│  │ │   [Preview]     │   │  │                                 │ │
│  │ │                 │   │  │                                 │ │
│  │ └─────────────────┘   │  │                                 │ │
│  │                       │  │                                 │ │
│  │ [Exportar Selecionadas]  │                                 │ │
│  │                       │  │                                 │ │
│  │ Status: ...           │  │                                 │ │
│  └───────────────────────┘  └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Funcionalidades da GUI

#### 1. Carregamento de Arquivos

**Botão "Abrir Raster"**
- Abre diálogo de seleção de arquivos
- Filtra apenas arquivos GeoTIFF (.tif, .tiff)
- Valida arquivo antes do carregamento
- Exibe erro se arquivo for inválido

```python
def open_raster(self):
    filepath, _ = QFileDialog.getOpenFileName(
        self.view, 
        "Open raster file", 
        "", 
        "GeoTIFF (*.tif *.tiff);;All files (*)"
    )
```

#### 2. Seleção de Bandas

**Lista de Bandas**
- Exibe todas as bandas disponíveis no arquivo
- Suporte a seleção múltipla (Ctrl+Click)
- Mostra nomes das bandas extraídos dos metadados
- Fallback para "Band X" se nome não estiver disponível

```python
self.band_list = QListWidget()
self.band_list.setSelectionMode(QListWidget.MultiSelection)

for name in self.band_names:
    item = QListWidgetItem(name)
    item.setSelected(True)  # Seleção padrão
    self.band_list.addItem(item)
```

#### 3. Preview de Imagem

**Área de Preview**
- Gera visualização RGB das bandas selecionadas
- Suporte a 1-3 bandas para preview
- Downsampling automático para performance
- Normalização de valores para melhor visualização

```python
def generate_preview(self):
    selected_items = self.view.band_list.selectedItems()
    if len(selected_items) < 1 or len(selected_items) > 3:
        QMessageBox.warning(self.view, "Aviso", 
                          "Selecione 1 a 3 bandas para preview!")
        return
    
    selected_indices = [self.view.band_list.row(item) 
                       for item in selected_items]
    preview_array = raster_handler.generate_preview_image(
        self.raster_path, selected_indices)
    self.view.update_preview_image(preview_array)
```

#### 4. Reordenação de Bandas

**Botão "Reordenar"**
- Permite reordenar as bandas selecionadas antes da exportação
- Abre janela dedicada para reordenação
- Suporte a drag & drop para reordenação visual
- Botões para mover bandas para cima/baixo
- Opção de resetar para ordem original
- Confirmação da nova ordem

```python
def open_reorder_window(self):
    selected_items = self.view.band_list.selectedItems()
    if not selected_items:
        QMessageBox.warning(self.view, "Aviso", 
                          "Selecione pelo menos uma banda!")
        return
    
    selected_indices = [self.view.band_list.row(item) 
                       for item in selected_items]
    
    reorder_window = BandReorderWindow(
        parent=self.view,
        selected_bands=selected_indices,
        band_names=self.band_names
    )
    
    reorder_window.bands_reordered.connect(self._on_bands_reordered)
    reorder_window.exec_()
```

**Janela de Reordenação**
- Interface intuitiva com lista arrastável
- Visualização da ordem atual das bandas
- Botões de ação para mover bandas
- Confirmação ou cancelamento da operação
- Preservação da ordem na exportação

#### 5. Visualização de Metadados

**Painel de Metadados**
- Exibe informações detalhadas do arquivo raster
- Organizado em seções lógicas
- Informações geográficas e técnicas
- Atualização automática ao carregar arquivo

```python
def update_metadata_display(self, meta, band_names):
    metadata_text = []
    
    # Informações básicas
    metadata_text.append("[FILE] Informações Básicas")
    metadata_text.append(f"   Dimensões: {meta.get('width')} x {meta.get('height')}")
    metadata_text.append(f"   Número de bandas: {meta.get('count')}")
    metadata_text.append(f"   Tipo de dados: {meta.get('dtype')}")
    
    # Sistema de coordenadas
    metadata_text.append("[CRS] Sistema de Coordenadas")
    crs = meta.get('crs', None)
    if crs:
        metadata_text.append(f"   CRS: {crs}")
    
    # Bandas
    metadata_text.append("[BANDS] Bandas Disponíveis")
    for i, name in enumerate(band_names, 1):
        metadata_text.append(f"   {i}: {name}")
    
    self.metadata_text.setPlainText('\n'.join(metadata_text))
```

#### 6. Exportação de Dados

**Botão "Exportar Selecionadas"**
- Valida seleção de bandas
- Utiliza ordem reordenada se disponível
- Abre diálogo de salvamento
- Preserva metadados durante exportação
- Feedback de progresso e resultado

```python
def export_selected_bands(self):
    selected_items = self.view.band_list.selectedItems()
    if not selected_items:
        QMessageBox.warning(self.view, "Aviso", 
                          "Selecione pelo menos uma banda!")
        return
    
    selected_indices = [self.view.band_list.row(item) 
                       for item in selected_items]
    
    # Solicita caminho de saída
    out_path, _ = QFileDialog.getSaveFileName(
        self.view, "Save GeoTIFF", "", "GeoTIFF (*.tif *.tiff)")
    
    if out_path:
        # Processa exportação
        bands, meta, names, band_meta, file_meta = \
            raster_handler.read_selected_bands(self.raster_path, selected_indices)
        raster_handler.export_tif(out_path, bands, meta, names, 
                                 band_meta, file_meta)
        
        QMessageBox.information(self.view, "Sucesso", 
                              f"Arquivo exportado: {out_path}")
```

### Sistema de Tradução

#### Arquitetura de Tradução

A GUI suporta múltiplos idiomas usando o sistema de tradução do Qt:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        self.translator = QTranslator()
        self.current_language = 'pt_BR'  # idioma padrão
        self._load_language(self.current_language)
```

#### Carregamento de Traduções

```python
def _load_language(self, lang_code):
    translations_dir = os.path.join(os.path.dirname(__file__), 
                                   '..', 'translations')
    if lang_code == 'pt_BR':
        qm_file = os.path.join(translations_dir, 'igcv_pt_BR.qm')
    elif lang_code == 'en':
        qm_file = os.path.join(translations_dir, 'igcv_en.qm')
    
    if os.path.exists(qm_file):
        self.translator.load(qm_file)
        QCoreApplication.instance().installTranslator(self.translator)
```

#### Troca de Idioma

```python
def switch_language(self, lang_code):
    self._load_language(lang_code)
    self.current_language = lang_code
    self._retranslate_ui()  # Atualiza todos os textos
```

#### Uso de Traduções

```python
# Textos traduzíveis
self.setWindowTitle(self.tr("IGCV Raster Tool - MVP"))
self.open_button.setText(self.tr("Abrir Raster"))
self.export_button.setText(self.tr("Exportar Selecionadas"))
```

### Tratamento de Erros na GUI

#### Estratégias de Tratamento

1. **Validação Preventiva**
   ```python
   if not self.raster_path:
       QMessageBox.warning(self.view, self.view.tr("Aviso"), 
                          self.view.tr("Nenhum raster foi carregado!"))
       return
   ```

2. **Mensagens de Erro Amigáveis**
   ```python
   try:
       self.meta, self.band_names = raster_handler.load_raster(filepath)
   except RasterHandlerError as e:
       QMessageBox.critical(self.view, self.view.tr("Erro"), 
                          f"{self.view.tr('Erro ao carregar raster:')}\n{str(e)}")
       return
   ```

3. **Feedback de Status**
   ```python
   self.view.status_label.setText(self.view.tr(f"Raster carregado: {filepath}"))
   ```

## Interface de Linha de Comando (CLI)

### Arquitetura da CLI

A CLI é implementada no módulo `cli/cli_app.py` e utiliza o módulo `argparse` para parsing de argumentos.

#### Estrutura de Comandos

```bash
python main.py --cli [opções]
```

### Argumentos Disponíveis

#### Argumentos Obrigatórios

- `--input, -i`: Caminho do arquivo GeoTIFF de entrada

#### Argumentos Opcionais

- `--bands, -b`: Lista de bandas para exportar (1-based)
- `--output, -o`: Caminho do arquivo de saída
- `--list`: Apenas lista as bandas disponíveis

### Exemplos de Uso

#### 1. Listar Bandas Disponíveis

```bash
python main.py --cli --input image.tif --list
```

**Saída:**
```
File: image.tif
Available bands:
1: Red Band
2: Green Band
3: Blue Band
4: Near Infrared

Use --bands to choose bands and --output to export.
```

#### 2. Exportar Bandas Específicas

```bash
python main.py --cli --input image.tif --bands 1 3 4 --output output.tif
```

**Saída:**
```
File: image.tif
Available bands:
1: Red Band
2: Green Band
3: Blue Band
4: Near Infrared

File exported successfully: output.tif
```

#### 3. Apenas Listar Sem Exportar

```bash
python main.py --cli --input image.tif
```

### Implementação da CLI

#### Parsing de Argumentos

```python
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="IGCVRasterTool CLI: select and export bands from GeoTIFF rasters"
    )
    parser.add_argument('--input', '-i', required=True, 
                       help="Input GeoTIFF file path")
    parser.add_argument('--bands', '-b', nargs='+', type=int, 
                       help="Bands to export (1-based, e.g.: 1 3 4)")
    parser.add_argument('--output', '-o', 
                       help="Output GeoTIFF file path")
    parser.add_argument('--list', action='store_true', 
                       help="Only list bands from file")
    
    args = parser.parse_args(argv)
```

#### Validação de Entrada

```python
# Validação de arquivo de entrada
if not os.path.exists(args.input):
    raise FileOperationError(f"Input file not found: {args.input}")

if not os.path.isfile(args.input):
    raise FileOperationError(f"The specified path is not a file: {args.input}")

# Validação de bandas selecionadas
selected_indices = [b-1 for b in args.bands]  # conversão para 0-based
for b in selected_indices:
    if b < 0 or b >= len(band_names):
        raise ValidationError(f"Invalid band: {b+1}. Valid bands: 1-{len(band_names)}")

# Validação de arquivo de saída
if not args.output:
    raise ValidationError("Please specify output file with --output")

output_dir = os.path.dirname(args.output)
if output_dir and not os.path.exists(output_dir):
    raise FileOperationError(f"Output directory does not exist: {output_dir}")
```

#### Processamento de Dados

```python
# Carregamento de informações
meta, band_names = raster_handler.load_raster(args.input)

# Exibição de informações
print(f"File: {args.input}")
print("Available bands:")
for idx, name in enumerate(band_names):
    print(f"{idx+1}: {name}")

# Processamento se bandas foram especificadas
if args.bands:
    bands, meta, selected_band_names, band_metadata, file_metadata = \
        raster_handler.read_selected_bands(args.input, selected_indices)
    
    raster_handler.export_tif(args.output, bands, meta, 
                             selected_band_names, band_metadata, file_metadata)
    print(f"File exported successfully: {args.output}")
```

### Tratamento de Erros na CLI

#### Hierarquia de Exceções

```python
try:
    # Operações principais
    pass
except KeyboardInterrupt:
    print("\nOperation cancelled by user.")
    sys.exit(0)
except SystemExit:
    raise  # Mantém códigos de saída corretos
except (CLIError, ValidationError, FileOperationError, RasterHandlerError) as e:
    print(f"Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
```

#### Códigos de Saída

- **0**: Sucesso
- **1**: Erro de validação ou processamento
- **2**: Erro inesperado

## Comparação entre GUI e CLI

### GUI - Vantagens

1. **Usabilidade**
   - Interface intuitiva e visual
   - Feedback imediato
   - Preview de dados
   - Seleção visual de bandas

2. **Funcionalidades**
   - Visualização de metadados
   - Preview de imagens
   - Suporte multilíngue
   - Tratamento de erros amigável

3. **Casos de Uso**
   - Uso interativo
   - Exploração de dados
   - Processamento ocasional
   - Usuários não técnicos

### CLI - Vantagens

1. **Automação**
   - Processamento em lote
   - Integração com scripts
   - Automação de workflows
   - Processamento não supervisionado

2. **Performance**
   - Sem overhead de interface gráfica
   - Menor uso de memória
   - Execução mais rápida
   - Ideal para servidores

3. **Casos de Uso**
   - Processamento em lote
   - Automação de pipelines
   - Uso em servidores
   - Usuários técnicos

### Escolha da Interface

#### Use GUI quando:
- Trabalhando com poucos arquivos
- Precisa explorar dados
- Usuário não é técnico
- Precisa de preview visual

#### Use CLI quando:
- Processando muitos arquivos
- Automatizando workflows
- Executando em servidor
- Integrando com outros scripts

## Considerações de Usabilidade

### Princípios de Design

1. **Simplicidade**
   - Interface limpa e focada
   - Fluxo de trabalho intuitivo
   - Menos é mais

2. **Feedback**
   - Status claro das operações
   - Mensagens de erro úteis
   - Confirmação de ações importantes

3. **Consistência**
   - Padrões consistentes de interface
   - Comportamento previsível
   - Terminologia uniforme

4. **Acessibilidade**
   - Suporte a múltiplos idiomas
   - Atalhos de teclado
   - Interface responsiva

### Melhorias Futuras

#### GUI
- [ ] Thumbnails de bandas
- [ ] Drag & drop de arquivos
- [ ] Barra de progresso
- [ ] Atalhos de teclado
- [ ] Histórico de arquivos recentes

#### CLI
- [ ] Processamento em paralelo
- [ ] Opções de configuração avançadas
- [ ] Logging detalhado
- [ ] Modo verbose/quiet
- [ ] Suporte a wildcards

## Conclusão

As interfaces de usuário do IGCV Raster Utility foram projetadas para atender diferentes necessidades:

- **GUI**: Focada em usabilidade e interação visual
- **CLI**: Focada em automação e performance

Ambas as interfaces compartilham a mesma lógica de processamento através do Model, garantindo consistência nos resultados independentemente da interface escolhida. A arquitetura modular permite fácil manutenção e extensão de ambas as interfaces. 