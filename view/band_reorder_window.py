from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, 
    QListWidget, QListWidgetItem, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
import os

class BandReorderWindow(QDialog):
    """Janela para reordenar as bandas selecionadas antes da exportação"""
    
    # Sinal emitido quando a reordenação é confirmada
    bands_reordered = pyqtSignal(list)  # Lista com os índices reordenados
    
    def __init__(self, parent=None, selected_bands=None, band_names=None):
        super().__init__(parent)
        self.selected_bands = selected_bands or []
        self.band_names = band_names or []
        self.reordered_indices = []
        
        self.setWindowTitle(self.tr("Reordenar Bandas"))
        self.setMinimumSize(400, 300)
        self.setModal(True)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self._setup_ui()
        self._populate_bands()
        
    def _setup_ui(self):
        """Configura a interface da janela"""
        layout = QVBoxLayout()
        
        # Título e instruções
        title_label = QLabel(self.tr("Reordenar Bandas para Exportação"))
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        instruction_label = QLabel(self.tr("Arraste as bandas para reordená-las. A ordem será mantida na exportação."))
        instruction_label.setWordWrap(True)
        instruction_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(instruction_label)
        
        # Grupo das bandas
        bands_group = QGroupBox(self.tr("Ordem das Bandas"))
        bands_layout = QVBoxLayout()
        
        self.bands_list = QListWidget()
        self.bands_list.setDragDropMode(QListWidget.InternalMove)
        self.bands_list.setSelectionMode(QListWidget.SingleSelection)
        bands_layout.addWidget(self.bands_list)
        
        bands_group.setLayout(bands_layout)
        layout.addWidget(bands_group)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        self.move_up_button = QPushButton(self.tr("Mover para Cima"))
        self.move_up_button.clicked.connect(self._move_up)
        self.move_up_button.setEnabled(False)
        
        self.move_down_button = QPushButton(self.tr("Mover para Baixo"))
        self.move_down_button.clicked.connect(self._move_down)
        self.move_down_button.setEnabled(False)
        
        self.reset_button = QPushButton(self.tr("Resetar Ordem"))
        self.reset_button.clicked.connect(self._reset_order)
        
        buttons_layout.addWidget(self.move_up_button)
        buttons_layout.addWidget(self.move_down_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.reset_button)
        
        layout.addLayout(buttons_layout)
        
        # Botões de confirmação
        confirm_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton(self.tr("Cancelar"))
        self.cancel_button.clicked.connect(self.reject)
        
        self.confirm_button = QPushButton(self.tr("Confirmar Ordem"))
        self.confirm_button.clicked.connect(self._confirm_order)
        self.confirm_button.setDefault(True)
        
        confirm_layout.addStretch()
        confirm_layout.addWidget(self.cancel_button)
        confirm_layout.addWidget(self.confirm_button)
        
        layout.addLayout(confirm_layout)
        
        self.setLayout(layout)
        
        # Conectar sinais
        self.bands_list.itemSelectionChanged.connect(self._update_move_buttons)
        
    def _populate_bands(self):
        """Popula a lista com as bandas selecionadas"""
        self.bands_list.clear()
        for i, band_index in enumerate(self.selected_bands):
            if 0 <= band_index < len(self.band_names):
                band_name = self.band_names[band_index]
                item = QListWidgetItem(f"{i+1}. {band_name}")
                item.setData(int(Qt.UserRole), band_index)
                self.bands_list.addItem(item)
        self.reordered_indices = self.selected_bands.copy()
        
    def _update_move_buttons(self):
        """Atualiza o estado dos botões de mover baseado na seleção"""
        current_row = self.bands_list.currentRow()
        self.move_up_button.setEnabled(current_row > 0)
        self.move_down_button.setEnabled(current_row >= 0 and current_row < self.bands_list.count() - 1)
        
    def _move_up(self):
        """Move a banda selecionada para cima"""
        current_row = self.bands_list.currentRow()
        if current_row > 0:
            item = self.bands_list.takeItem(current_row)
            self.bands_list.insertItem(current_row - 1, item)
            self.bands_list.setCurrentRow(current_row - 1)
            self._update_order()
            
    def _move_down(self):
        """Move a banda selecionada para baixo"""
        current_row = self.bands_list.currentRow()
        if current_row < self.bands_list.count() - 1:
            item = self.bands_list.takeItem(current_row)
            self.bands_list.insertItem(current_row + 1, item)
            self.bands_list.setCurrentRow(current_row + 1)
            self._update_order()
            
    def _reset_order(self):
        """Reseta a ordem para a original"""
        self._populate_bands()
        self.bands_list.setCurrentRow(0)
        
    def _update_order(self):
        """Atualiza a lista de índices reordenados"""
        self.reordered_indices = []
        for i in range(self.bands_list.count()):
            item = self.bands_list.item(i)
            if item is not None:
                original_index = item.data(int(Qt.UserRole))
                self.reordered_indices.append(original_index)
            
    def _confirm_order(self):
        """Confirma a ordem e emite o sinal"""
        self._update_order()
        self.bands_reordered.emit(self.reordered_indices)
        self.accept()
        
    def get_reordered_indices(self):
        """Retorna os índices reordenados"""
        return self.reordered_indices.copy() 