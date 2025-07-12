from model import raster_handler
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox
from exceptions import RasterHandlerError, ControllerError

class MainController:
    def __init__(self, view):
        self.view = view
        self.raster_path = None
        self.band_names = []
        self.meta = None

    def open_raster(self):
        """Opens a raster file and loads its information"""
        try:
            filepath, _ = QFileDialog.getOpenFileName(
                self.view, 
                "Open raster file", 
                "", 
                "GeoTIFF (*.tif *.tiff);;All files (*)"
            )
            
            if not filepath:
                return  # User cancelled selection
            
            # Load raster information
            try:
                self.meta, self.band_names = raster_handler.load_raster(filepath)
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, "Error", f"Error loading raster:\n{str(e)}")
                return
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Unexpected error loading raster:\n{str(e)}")
                return
            
            # Update interface
            self.raster_path = filepath
            self.view.band_list.clear()
            
            for name in self.band_names:
                item = QListWidgetItem(name)
                item.setSelected(True)
                self.view.band_list.addItem(item)
            
            self.view.export_button.setEnabled(True)
            self.view.status_label.setText(f"Raster loaded: {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Unexpected error opening raster:\n{str(e)}")

    def export_selected_bands(self):
        """Exports selected bands to a new file"""
        try:
            # Check if there's a loaded raster
            if not self.raster_path:
                QMessageBox.warning(self.view, "Warning", "No raster has been loaded!")
                return
            
            # Check if there are selected bands
            selected_items = self.view.band_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self.view, "Warning", "Select at least one band!")
                return
            
            # Get indices of selected bands
            selected_indices = [self.view.band_list.row(item) for item in selected_items]
            
            # Read selected bands
            try:
                bands, meta, selected_band_names, band_metadata, file_metadata = raster_handler.read_selected_bands(self.raster_path, selected_indices)
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, "Error", f"Error reading selected bands:\n{str(e)}")
                return
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Unexpected error reading bands:\n{str(e)}")
                return
            
            # Request output path
            out_path, _ = QFileDialog.getSaveFileName(
                self.view, 
                "Save GeoTIFF", 
                "", 
                "GeoTIFF (*.tif *.tiff)"
            )
            
            if not out_path:
                self.view.status_label.setText("Export cancelled.")
                return
            
            # Export file
            try:
                raster_handler.export_tif(out_path, bands, meta, selected_band_names, band_metadata, file_metadata)
                self.view.status_label.setText(f"File exported: {out_path}")
                QMessageBox.information(self.view, "Success", f"File exported successfully:\n{out_path}")
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, "Error", f"Error exporting file:\n{str(e)}")
                self.view.status_label.setText("Export error.")
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Unexpected error during export:\n{str(e)}")
                self.view.status_label.setText("Export error.")
                
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Unexpected error during export:\n{str(e)}")
            self.view.status_label.setText("Export error.")
