# User Interfaces - IGCV Raster Utility

## Overview

The IGCV Raster Utility offers two distinct user interfaces to meet different usage needs:

1. **Graphical Interface (GUI)**: Intuitive visual interface for interactive use
2. **Command Line Interface (CLI)**: Textual interface for batch processing and automation

## Graphical Interface (GUI)

### GUI Architecture

The graphical interface is built using PyQt5 and follows the MVC pattern, where the View (`main_window.py`) is responsible for presentation and user interaction.

#### Main Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    IGCV Raster Tool - MVP                       │
├─────────────────────────────────────────────────────────────────┤
│  Language ▼                                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────┐  ┌─────────────────────────────────┐ │
│  │   LEFT PANEL          │  │        RIGHT PANEL              │ │
│  │                       │  │                                 │ │
│  │ [Open Raster]         │  │  Raster Metadata                │ │
│  │                       │  │ ┌─────────────────────────────┐ │ │
│  │ Available bands:      │  │ │                             │ │ │
│  │    Band 1             │  │ │  [Detailed Information]     │ │ │
│  │    Band 2             │  │ │                             │ │ │
│  │    Band 3             │  │ │                             │ │ │
│  │    Band 4             │  │ └─────────────────────────────┘ │ │
│  │                       │  │                                 │ │
│  │   Preview             │  │                                 │ │
│  │   [Generate Preview]  │  │                                 │ │
│  │ ┌─────────────────┐   │  │                                 │ │
│  │ │                 │   │  │                                 │ │
│  │ │   [Preview]     │   │  │                                 │ │
│  │ │                 │   │  │                                 │ │
│  │ └─────────────────┘   │  │                                 │ │
│  │                       │  │                                 │ │
│  │ [Reorder]             │  │                                 │ │
│  │ [Export Selected]     │  │                                 │ │
│  │                       │  │                                 │ │
│  │ Status: ...           │  │                                 │ │
│  └───────────────────────┘  └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### GUI Features

#### 1. File Loading

**"Open Raster" Button**
- Opens file selection dialog
- Filters only GeoTIFF files (.tif, .tiff)
- Validates file before loading
- Displays error if file is invalid

```python
def open_raster(self):
    filepath, _ = QFileDialog.getOpenFileName(
        self.view, 
        "Open raster file", 
        "", 
        "GeoTIFF (*.tif *.tiff);;All files (*)"
    )
```

#### 2. Band Selection

**Band List**
- Displays all available bands in the file
- Supports multiple selection (Ctrl+Click)
- Shows band names extracted from metadata
- Fallback to "Band X" if name not available

```python
self.band_list = QListWidget()
self.band_list.setSelectionMode(QListWidget.MultiSelection)

for name in self.band_names:
    item = QListWidgetItem(name)
    item.setSelected(True)  # Default selection
    self.band_list.addItem(item)
```

#### 3. Band Reordering

**"Reorder" Button**
- Allows reordering selected bands before export
- Opens dedicated reordering window
- Supports drag & drop for visual reordering
- Buttons to move bands up/down
- Option to reset to original order
- Confirmation of new order

```python
def open_reorder_window(self):
    selected_items = self.view.band_list.selectedItems()
    if not selected_items:
        QMessageBox.warning(self.view, "Warning", 
                          "Select at least one band!")
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

**Reordering Window**
- Intuitive interface with draggable list
- Visualization of current band order
- Action buttons for moving bands
- Confirmation or cancellation of operation
- Order preservation in export

#### 4. Image Preview

**Preview Area**
- Generates RGB visualization of selected bands
- Supports 1-3 bands for preview
- Automatic downsampling for performance
- Value normalization for better visualization

```python
def generate_preview(self):
    selected_items = self.view.band_list.selectedItems()
    if len(selected_items) < 1 or len(selected_items) > 3:
        QMessageBox.warning(self.view, "Warning", 
                          "Select 1 to 3 bands for preview!")
        return
    
    selected_indices = [self.view.band_list.row(item) 
                       for item in selected_items]
    preview_array = raster_handler.generate_preview_image(
        self.raster_path, selected_indices)
    self.view.update_preview_image(preview_array)
```

#### 5. Metadata Visualization

**Metadata Panel**
- Displays detailed file raster information
- Organized in logical sections
- Geographic and technical information
- Automatic update when loading file

```python
def update_metadata_display(self, meta, band_names):
    metadata_text = []
    
    # Basic information
    metadata_text.append("[FILE] Basic Information")
    metadata_text.append(f"   Dimensions: {meta.get('width')} x {meta.get('height')}")
    metadata_text.append(f"   Number of bands: {meta.get('count')}")
    metadata_text.append(f"   Data type: {meta.get('dtype')}")
    
    # Coordinate system
    metadata_text.append("[CRS] Coordinate System")
    crs = meta.get('crs', None)
    if crs:
        metadata_text.append(f"   CRS: {crs}")
    
    # Bands
    metadata_text.append("[BANDS] Available Bands")
    for i, name in enumerate(band_names, 1):
        metadata_text.append(f"   {i}: {name}")
    
    self.metadata_text.setPlainText('\n'.join(metadata_text))
```

#### 6. Data Export

**"Export Selected" Button**
- Validates band selection
- Uses reordered order if available
- Opens save dialog
- Preserves metadata during export
- Progress and result feedback

```python
def export_selected_bands(self):
    selected_items = self.view.band_list.selectedItems()
    if not selected_items:
        QMessageBox.warning(self.view, "Warning", 
                          "Select at least one band!")
        return
    
    selected_indices = [self.view.band_list.row(item) 
                       for item in selected_items]
    
    # Request output path
    out_path, _ = QFileDialog.getSaveFileName(
        self.view, "Save GeoTIFF", "", "GeoTIFF (*.tif *.tiff)")
    
    if out_path:
        # Process export
        bands, meta, names, band_meta, file_meta = \
            raster_handler.read_selected_bands(self.raster_path, selected_indices)
        raster_handler.export_tif(out_path, bands, meta, 
                                 band_meta, file_meta)
        
        QMessageBox.information(self.view, "Success", 
                              f"File exported: {out_path}")
```

### Translation System

#### Translation Architecture

The GUI supports multiple languages using Qt's translation system:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        self.translator = QTranslator()
        self.current_language = 'pt_BR'  # default language
        self._load_language(self.current_language)
```

#### Translation Loading

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

#### Language Switching

```python
def switch_language(self, lang_code):
    self._load_language(lang_code)
    self.current_language = lang_code
    self._retranslate_ui()  # Updates all texts
```

#### Translation Usage

```python
# Translatable texts
self.setWindowTitle(self.tr("IGCV Raster Tool - MVP"))
self.open_button.setText(self.tr("Open Raster"))
self.export_button.setText(self.tr("Export Selected"))
```

### GUI Error Handling

#### Handling Strategies

1. **Preventive Validation**
   ```python
   if not self.raster_path:
       QMessageBox.warning(self.view, self.view.tr("Warning"), 
                          self.view.tr("No raster loaded!"))
       return
   ```

2. **User-Friendly Error Messages**
   ```python
   try:
       self.meta, self.band_names = raster_handler.load_raster(filepath)
   except RasterHandlerError as e:
       QMessageBox.critical(self.view, self.view.tr("Error"), 
                          f"{self.view.tr('Error loading raster:')}\n{str(e)}")
       return
   ```

3. **Status Feedback**
   ```python
   self.view.status_label.setText(self.view.tr(f"Raster loaded: {filepath}"))
   ```

## Command Line Interface (CLI)

### CLI Architecture

The CLI is implemented in the `cli/cli_app.py` module and uses the `argparse` module for argument parsing.

#### Command Structure

```bash
python main.py --cli [options]
```

### Available Arguments

#### Required Arguments

- `--input, -i`: Input GeoTIFF file path

#### Optional Arguments

- `--bands, -b`: List of bands to export (1-based)
- `--output, -o`: Output file path
- `--list`: Only list available bands

### Usage Examples

#### 1. List Available Bands

```bash
python main.py --cli --input image.tif --list
```

**Output:**
```
File: image.tif
Available bands:
1: Red Band
2: Green Band
3: Blue Band
4: Near Infrared

Use --bands to choose bands and --output to export.
```

#### 2. Export Specific Bands

```bash
python main.py --cli --input image.tif --bands 1 3 4 --output output.tif
```

**Output:**
```
File: image.tif
Available bands:
1: Red Band
2: Green Band
3: Blue Band
4: Near Infrared

File exported successfully: output.tif
```

#### 3. List Only Without Export

```bash
python main.py --cli --input image.tif
```

### CLI Implementation

#### Argument Parsing

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

#### Input Validation

```python
# Input file validation
if not os.path.exists(args.input):
    raise FileOperationError(f"Input file not found: {args.input}")

if not os.path.isfile(args.input):
    raise FileOperationError(f"The specified path is not a file: {args.input}")

# Selected bands validation
selected_indices = [b-1 for b in args.bands]  # conversion to 0-based
for b in selected_indices:
    if b < 0 or b >= len(band_names):
        raise ValidationError(f"Invalid band: {b+1}. Valid bands: 1-{len(band_names)}")

# Output file validation
if not args.output:
    raise ValidationError("Please specify output file with --output")

output_dir = os.path.dirname(args.output)
if output_dir and not os.path.exists(output_dir):
    raise FileOperationError(f"Output directory does not exist: {output_dir}")
```

#### Data Processing

```python
# Load information
meta, band_names = raster_handler.load_raster(args.input)

# Display information
print(f"File: {args.input}")
print("Available bands:")
for idx, name in enumerate(band_names):
    print(f"{idx+1}: {name}")

# Process if bands were specified
if args.bands:
    bands, meta, selected_band_names, band_metadata, file_metadata = \
        raster_handler.read_selected_bands(args.input, selected_indices)
    
    raster_handler.export_tif(args.output, bands, meta, 
                             selected_band_names, band_metadata, file_metadata)
    print(f"File exported successfully: {args.output}")
```

### CLI Error Handling

#### Exception Hierarchy

```python
try:
    # Main operations
    pass
except KeyboardInterrupt:
    print("\nOperation cancelled by user.")
    sys.exit(0)
except SystemExit:
    raise  # Maintains correct exit codes
except (CLIError, ValidationError, FileOperationError, RasterHandlerError) as e:
    print(f"Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
```

#### Exit Codes

- **0**: Success
- **1**: Validation or processing error
- **2**: Unexpected error

## GUI vs CLI Comparison

### GUI - Advantages

1. **Usability**
   - Intuitive and visual interface
   - Immediate feedback
   - Data preview
   - Visual band selection

2. **Features**
   - Metadata visualization
   - Image preview
   - Multilingual support
   - User-friendly error handling

3. **Use Cases**
   - Interactive use
   - Data exploration
   - Occasional processing
   - Non-technical users

### CLI - Advantages

1. **Automation**
   - Batch processing
   - Script integration
   - Workflow automation
   - Unsupervised processing

2. **Performance**
   - No GUI overhead
   - Lower memory usage
   - Faster execution
   - Ideal for servers

3. **Use Cases**
   - Batch processing
   - Pipeline automation
   - Server usage
   - Technical users

### Interface Choice

#### Use GUI when:
- Working with few files
- Need to explore data
- User is not technical
- Need visual preview

#### Use CLI when:
- Processing many files
- Automating workflows
- Running on server
- Integrating with other scripts

## Usability Considerations

### Design Principles

1. **Simplicity**
   - Clean and focused interface
   - Intuitive workflow
   - Less is more

2. **Feedback**
   - Clear operation status
   - Useful error messages
   - Important action confirmation

3. **Consistency**
   - Consistent interface patterns
   - Predictable behavior
   - Uniform terminology

4. **Accessibility**
   - Multilingual support
   - Keyboard shortcuts
   - Responsive interface

### Future Improvements

#### GUI
- [ ] Band thumbnails
- [ ] File drag & drop
- [ ] Progress bar
- [ ] Keyboard shortcuts
- [ ] Recent files history

#### CLI
- [ ] Parallel processing
- [ ] Advanced configuration options
- [ ] Detailed logging
- [ ] Verbose/quiet mode
- [ ] Wildcard support

## Conclusion

The IGCV Raster Utility user interfaces were designed to meet different needs:

- **GUI**: Focused on usability and visual interaction
- **CLI**: Focused on automation and performance

Both interfaces share the same processing logic through the Model, ensuring consistent results regardless of the chosen interface. The modular architecture allows easy maintenance and extension of both interfaces. 