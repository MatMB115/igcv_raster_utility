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
        """Abre um arquivo raster e carrega suas informações"""
        try:
            filepath, _ = QFileDialog.getOpenFileName(
                self.view, 
                "Abrir arquivo raster", 
                "", 
                "GeoTIFF (*.tif *.tiff);;Todos os arquivos (*)"
            )
            
            if not filepath:
                return  # Usuário cancelou a seleção
            
            # Carregar informações do raster
            try:
                self.meta, self.band_names = raster_handler.load_raster(filepath)
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, "Erro", f"Erro ao carregar o raster:\n{str(e)}")
                return
            except Exception as e:
                QMessageBox.critical(self.view, "Erro", f"Erro inesperado ao carregar o raster:\n{str(e)}")
                return
            
            # Atualizar interface
            self.raster_path = filepath
            self.view.band_list.clear()
            
            for name in self.band_names:
                item = QListWidgetItem(name)
                item.setSelected(True)
                self.view.band_list.addItem(item)
            
            self.view.export_button.setEnabled(True)
            self.view.status_label.setText(f"Raster carregado: {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self.view, "Erro", f"Erro inesperado ao abrir raster:\n{str(e)}")

    def export_selected_bands(self):
        """Exporta as bandas selecionadas para um novo arquivo"""
        try:
            # Verificar se há um raster carregado
            if not self.raster_path:
                QMessageBox.warning(self.view, "Aviso", "Nenhum raster foi carregado!")
                return
            
            # Verificar se há bandas selecionadas
            selected_items = self.view.band_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self.view, "Aviso", "Selecione ao menos uma banda!")
                return
            
            # Obter índices das bandas selecionadas
            selected_indices = [self.view.band_list.row(item) for item in selected_items]
            
            # Ler bandas selecionadas
            try:
                bands, meta = raster_handler.read_selected_bands(self.raster_path, selected_indices)
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, "Erro", f"Erro ao ler as bandas selecionadas:\n{str(e)}")
                return
            except Exception as e:
                QMessageBox.critical(self.view, "Erro", f"Erro inesperado ao ler as bandas:\n{str(e)}")
                return
            
            # Solicitar caminho de saída
            out_path, _ = QFileDialog.getSaveFileName(
                self.view, 
                "Salvar GeoTIFF", 
                "", 
                "GeoTIFF (*.tif *.tiff)"
            )
            
            if not out_path:
                self.view.status_label.setText("Exportação cancelada.")
                return
            
            # Exportar arquivo
            try:
                raster_handler.export_tif(out_path, bands, meta)
                self.view.status_label.setText(f"Arquivo exportado: {out_path}")
                QMessageBox.information(self.view, "Sucesso", f"Arquivo exportado com sucesso:\n{out_path}")
            except RasterHandlerError as e:
                QMessageBox.critical(self.view, "Erro", f"Erro ao exportar o arquivo:\n{str(e)}")
                self.view.status_label.setText("Erro na exportação.")
            except Exception as e:
                QMessageBox.critical(self.view, "Erro", f"Erro inesperado na exportação:\n{str(e)}")
                self.view.status_label.setText("Erro na exportação.")
                
        except Exception as e:
            QMessageBox.critical(self.view, "Erro", f"Erro inesperado na exportação:\n{str(e)}")
            self.view.status_label.setText("Erro na exportação.")
