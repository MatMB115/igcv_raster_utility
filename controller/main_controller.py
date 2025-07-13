from model import raster_handler
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox
from exceptions import RasterHandlerError, ControllerError
from view.band_reorder_window import BandReorderWindow

class MainController:
    def __init__(self, view):
        self.view = view
        self.raster_path = None
        self.band_names = []
        self.meta = None
        self.reordered_indices = None  # Armazena a ordem reordenada das bandas

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
            self.view.reorder_button.setEnabled(True)
            self.view.status_label.setText(self.view.tr(f"Raster carregado: {filepath}"))
            
            # Reset reordered indices
            self.reordered_indices = None
            
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
            
            # Get indices of selected bands (use reordered indices if available)
            if self.reordered_indices is not None:
                selected_indices = self.reordered_indices
                self.view.status_label.setText(self.view.tr("Usando ordem reordenada das bandas."))
            else:
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
            
            # Check for data issues before generating preview
            issues = raster_handler.detect_data_issues(self.raster_path, selected_indices)
            
            if issues['has_issues']:
                # Show warning with issues and offer corrections
                warning_text = f"{self.view.tr('Problemas detectados nos dados:')}\n\n"
                for issue in issues['issues']:
                    warning_text += f"• {issue}\n"
                
                warning_text += f"\n{self.view.tr('Recomendações:')}\n"
                for rec in issues['recommendations']:
                    warning_text += f"• {rec}\n"
                
                warning_text += f"\n{self.view.tr('Para gerar o preview, serão aplicadas correções automáticas nos dados desta amostra (por exemplo, definição de NoData ou ajuste do tipo de dado).')}"
                warning_text += "\n\n" + self.view.tr('Se você escolher "Sim", os dados corrigidos serão salvos como uma nova amostra e estarão disponíveis tanto para visualização quanto para exportação.')
                warning_text += "\n" + self.view.tr('Se você escolher "Não", as correções serão feitas apenas para o preview e não afetarão os dados originais ou exportação.')
                warning_text += f"\n\n{self.view.tr('Deseja aplicar e salvar as correções automáticas?')}"
                
                reply = QMessageBox.question(
                    self.view, 
                    self.view.tr("Problemas Detectados"), 
                    warning_text
                )
                
                if reply == QMessageBox.Yes:
                    try:
                        # Apply corrections
                        corrected_path = raster_handler.apply_data_corrections(self.raster_path, selected_indices)
                        
                        # Generate preview with corrected file
                        preview_array = raster_handler.generate_preview_image(corrected_path, selected_indices)
                        self.view.update_preview_image(preview_array)
                        self.view.status_label.setText(self.view.tr("Preview gerado com arquivo corrigido!"))
                        
                        # Show info about corrected file
                        QMessageBox.information(
                            self.view, 
                            self.view.tr("Arquivo Corrigido"), 
                            f"{self.view.tr('Arquivo corrigido salvo como:')}\n{corrected_path}"
                        )
                        return
                        
                    except Exception as e:
                        QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro ao aplicar correções:')}\n{str(e)}")
                        return
            
            # Generate preview normally
            try:
                preview_array = raster_handler.generate_preview_image(self.raster_path, selected_indices)
                self.view.update_preview_image(preview_array)
                self.view.status_label.setText(self.view.tr("Preview gerado com sucesso!"))
            except RasterHandlerError as e:
                # Show debug information for preview errors
                debug_stats = raster_handler.debug_band_statistics(self.raster_path, selected_indices)
                debug_info = f"Erro: {str(e)}\n\nEstatísticas das bandas:\n"
                for band_name, stats in debug_stats.items():
                    if isinstance(stats, dict) and 'error' not in stats:
                        debug_info += f"\n{band_name}:\n"
                        for key, value in stats.items():
                            debug_info += f"  {key}: {value}\n"
                
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro ao gerar preview:')}\n{debug_info}")
                self.view.status_label.setText(self.view.tr("Erro no preview."))
            except Exception as e:
                QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado ao gerar preview:')}\n{str(e)}")
                self.view.status_label.setText(self.view.tr("Erro no preview."))
                
        except Exception as e:
            QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado durante preview:')}\n{str(e)}")
            self.view.status_label.setText(self.view.tr("Erro no preview."))

    def open_reorder_window(self):
        """Abre a janela de reordenação de bandas"""
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
            
            # Create and show reorder window
            reorder_window = BandReorderWindow(
                parent=self.view,
                selected_bands=selected_indices,
                band_names=self.band_names
            )
            
            # Connect the signal
            reorder_window.bands_reordered.connect(self._on_bands_reordered)
            
            # Show the window
            if reorder_window.exec_() == BandReorderWindow.Accepted:
                self.view.status_label.setText(self.view.tr("Ordem das bandas atualizada!"))
            else:
                self.view.status_label.setText(self.view.tr("Reordenação cancelada."))
                
        except Exception as e:
            QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro inesperado ao abrir janela de reordenação:')}\n{str(e)}")
            self.view.status_label.setText(self.view.tr("Erro na reordenação."))

    def _on_bands_reordered(self, reordered_indices):
        """Callback chamado quando as bandas são reordenadas"""
        try:
            self.reordered_indices = reordered_indices
            self.view.status_label.setText(self.view.tr("Ordem das bandas atualizada!"))
        except Exception as e:
            QMessageBox.critical(self.view, self.view.tr("Erro"), f"{self.view.tr('Erro ao processar reordenação:')}\n{str(e)}")
