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
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro ao carregar raster:')}\n{str(e)}")
                return
            except Exception as e:
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado ao carregar raster:')}\n{str(e)}")
                return
            
            # Update interface
            self.raster_path = filepath
            self.view.band_list.clear()
            
            for name in self.band_names:
                item = QListWidgetItem(name)
                item.setSelected(True)
                self.view.band_list.addItem(item)
            
            self.view.export_button.setEnabled(True)
            self.view.preview_button.setEnabled(True)
            self.view.status_label.setText(self.view.tr(f"Raster carregado: {filepath}"))
            
            # Update metadata display
            self.view.update_metadata_display(self.meta, self.band_names)
            
        except Exception as e:
            QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado ao abrir raster:')}\n{str(e)}")

    def export_selected_bands(self):
        """Exports selected bands to a new file"""
        try:
            # Check if there's a loaded raster
            if not self.raster_path:
                QMessageBox.warning(self.view, self.view.tr("Aviso"), self.view.tr("Nenhum raster foi carregado!"))
                return
            
            # Check if there are selected bands
            selected_items = self.view.band_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self.view, self.view.tr("Aviso"), self.view.tr("Selecione pelo menos uma banda!"))
                return
            
            # Get indices of selected bands
            selected_indices = [self.view.band_list.row(item) for item in selected_items]
            
            # Read selected bands
            try:
                bands, meta, selected_band_names, band_metadata, file_metadata = raster_handler.read_selected_bands(self.raster_path, selected_indices)
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro ao ler bandas selecionadas:')}\n{str(e)}")
                return
            except Exception as e:
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado ao ler bandas:')}\n{str(e)}")
                return
            
            # Request output path
            out_path, _ = QFileDialog.getSaveFileName(
                self.view, 
                "Save GeoTIFF", 
                "", 
                "GeoTIFF (*.tif *.tiff)"
            )
            
            if not out_path:
                self.view.status_label.setText(self.view.tr("Exportação cancelada."))
                return
            
            # Export file
            try:
                raster_handler.export_tif(out_path, bands, meta, selected_band_names, band_metadata, file_metadata)
                self.view.status_label.setText(f"{self.view.tr('Arquivo exportado:')} {out_path}")
                QMessageBox.information(self.view, self.view.tr("Sucesso"), f"{self.view.tr('Arquivo exportado com sucesso:')}\n{out_path}")
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro ao exportar arquivo:')}\n{str(e)}")
                self.view.status_label.setText(self.view.tr("Erro na exportação."))
            except Exception as e:
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado durante exportação:')}\n{str(e)}")
                self.view.status_label.setText(self.view.tr("Erro na exportação."))
                
        except Exception as e:
            QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado durante exportação:')}\n{str(e)}")
            self.view.status_label.setText(self.view.tr("Erro na exportação."))

    def generate_preview(self):
        """Generates RGB preview from selected bands"""
        try:
            # Check if there's a loaded raster
            if not self.raster_path:
                QMessageBox.warning(self.view, self.view.tr("Aviso"), self.view.tr("Nenhum raster foi carregado!"))
                return
            
            # Check if 1 to 3 bands are selected
            selected_items = self.view.band_list.selectedItems()
            if len(selected_items) < 1 or len(selected_items) > 3:
                QMessageBox.warning(self.view, self.view.tr("Aviso"), self.view.tr("Selecione 1 a 3 bandas para preview!"))
                return
            
            # Get indices of selected bands
            selected_indices = [self.view.band_list.row(item) for item in selected_items]
            
            # Generate preview
            try:
                preview_array = raster_handler.generate_preview_image(self.raster_path, selected_indices)
                self.view.update_preview_image(preview_array)
                self.view.status_label.setText(self.view.tr("Preview gerado com sucesso!"))
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro ao gerar preview:')}\n{str(e)}")
                self.view.status_label.setText(self.view.tr("Erro no preview."))
            except Exception as e:
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado ao gerar preview:')}\n{str(e)}")
                self.view.status_label.setText(self.view.tr("Erro no preview."))
                
        except Exception as e:
            QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado durante preview:')}\n{str(e)}")
            self.view.status_label.setText(self.view.tr("Erro no preview."))
