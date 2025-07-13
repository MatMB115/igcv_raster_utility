from PyQt5.QtWidgets import (
    QMainWindow, QAction, QMenuBar, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox, QTextEdit, QSplitter, QGroupBox, QCheckBox
)
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QCoreApplication
from PyQt5.QtGui import QPixmap, QImage, QIcon
import os
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self, controller=None):
        try:
            super().__init__()
            self.controller = controller
            self.translator = QTranslator()
            self.current_language = 'pt_BR'  # padrão inicial
            self._load_language(self.current_language)
            self.setWindowTitle(self.tr("IGCV Raster Tool - MVP"))
            self.setMinimumSize(800, 600)
            
            # Set application icon
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.png')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))

            # MENU BAR
            try:
                menubar = self.menuBar()
                if menubar is not None:
                    language_menu = menubar.addMenu(self.tr("Idioma"))
                    if language_menu is not None:
                        self.action_portuguese = QAction(self.tr("Português"), self)
                        self.action_english = QAction(self.tr("English"), self)
                        language_menu.addAction(self.action_portuguese)
                        language_menu.addAction(self.action_english)
                    else:
                        self.action_portuguese = QAction(self.tr("Português"), self)
                        self.action_english = QAction(self.tr("English"), self)
                else:
                    self.action_portuguese = QAction(self.tr("Português"), self)
                    self.action_english = QAction(self.tr("English"), self)
                
                self.action_portuguese.triggered.connect(lambda: self.switch_language('pt_BR'))
                self.action_english.triggered.connect(lambda: self.switch_language('en'))
            except Exception as e:
                print(f"Erro ao criar menu: {e}")
                self.action_portuguese = QAction(self.tr("Português"), self)
                self.action_english = QAction(self.tr("English"), self)
                self.action_portuguese.triggered.connect(lambda: self.switch_language('pt_BR'))
                self.action_english.triggered.connect(lambda: self.switch_language('en'))
            
            try:
                # Create main splitter for left and right panels
                main_splitter = QSplitter(Qt.Orientation.Horizontal)
                
                # LEFT PANEL - Band selection
                left_panel = QWidget()
                left_layout = QVBoxLayout()
                
                self.open_button = QPushButton(self.tr("Abrir Raster"))
                self.open_button.clicked.connect(self._open_raster)

                self.band_list = QListWidget()
                self.band_list.setSelectionMode(QListWidget.MultiSelection)

                # Preview controls
                preview_group = QGroupBox(self.tr("Preview"))
                preview_layout = QVBoxLayout()
                
                self.preview_button = QPushButton(self.tr("Gerar Preview"))
                self.preview_button.clicked.connect(self._generate_preview)
                self.preview_button.setEnabled(False)
                
                self.preview_label = QLabel(self.tr("Selecione 1 a 3 bandas para preview"))
                self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.preview_label.setMinimumHeight(200)
                self.preview_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0; color: black;")
                
                preview_layout.addWidget(self.preview_button)
                preview_layout.addWidget(self.preview_label)
                preview_group.setLayout(preview_layout)
                
                self.export_button = QPushButton(self.tr("Exportar Selecionadas"))
                self.export_button.clicked.connect(self._export_selected_bands)
                self.export_button.setEnabled(False)

                self.status_label = QLabel(self.tr("Selecione um raster GeoTIFF."))
                self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                left_layout.addWidget(self.open_button)
                left_layout.addWidget(QLabel(self.tr("Bandas disponíveis:")))
                left_layout.addWidget(self.band_list)
                left_layout.addWidget(preview_group)
                left_layout.addWidget(self.export_button)
                left_layout.addWidget(self.status_label)
                left_panel.setLayout(left_layout)
                
                # RIGHT PANEL - Metadata display
                right_panel = QWidget()
                right_layout = QVBoxLayout()
                
                # Metadata group
                metadata_group = QGroupBox(self.tr("Metadados do Raster"))
                metadata_layout = QVBoxLayout()
                
                self.metadata_text = QTextEdit()
                self.metadata_text.setReadOnly(True)
                self.metadata_text.setMaximumHeight(400)
                self.metadata_text.setPlaceholderText(self.tr("Carregue um raster para ver os metadados..."))
                
                metadata_layout.addWidget(self.metadata_text)
                metadata_group.setLayout(metadata_layout)
                
                right_layout.addWidget(metadata_group)
                right_layout.addStretch()  # Add stretch to push metadata to top
                right_panel.setLayout(right_layout)
                
                # Add panels to splitter
                main_splitter.addWidget(left_panel)
                main_splitter.addWidget(right_panel)
                main_splitter.setSizes([400, 400])  # Equal initial sizes
                
                self.setCentralWidget(main_splitter)
                
            except Exception as e:
                QMessageBox.critical(self, self.tr("Erro"), f"{self.tr('Erro ao criar interface:')}\n{str(e)}")
                raise
                
        except Exception as e:
            print(f"Erro crítico na inicialização da janela principal: {e}")
            raise

    def _load_language(self, lang_code):
        """Carrega o arquivo de tradução .qm correspondente ao idioma."""
        translations_dir = os.path.join(os.path.dirname(__file__), '..', 'translations')
        if lang_code == 'pt_BR':
            qm_file = os.path.join(translations_dir, 'igcv_pt_BR.qm')
        elif lang_code == 'en':
            qm_file = os.path.join(translations_dir, 'igcv_en.qm')
        else:
            return
        if os.path.exists(qm_file):
            self.translator.load(qm_file)
            QCoreApplication.instance().installTranslator(self.translator)
        else:
            QCoreApplication.instance().removeTranslator(self.translator)

    def switch_language(self, lang_code):
        """Alterna o idioma da interface e reinicializa os textos."""
        self._load_language(lang_code)
        self.current_language = lang_code
        self._retranslate_ui()

    def _retranslate_ui(self):
        """Atualiza os textos da interface após troca de idioma."""
        self.setWindowTitle(self.tr("IGCV Raster Tool - MVP"))
        menubar = self.menuBar()
        if menubar:
            menubar.clear()
            language_menu = menubar.addMenu(self.tr("Idioma"))
            self.action_portuguese = QAction(self.tr("Português"), self)
            self.action_english = QAction(self.tr("English"), self)
            language_menu.addAction(self.action_portuguese)
            language_menu.addAction(self.action_english)
            self.action_portuguese.triggered.connect(lambda: self.switch_language('pt_BR'))
            self.action_english.triggered.connect(lambda: self.switch_language('en'))
        self.open_button.setText(self.tr("Abrir Raster"))
        self.export_button.setText(self.tr("Exportar Selecionadas"))
        self.status_label.setText(self.tr("Selecione um raster GeoTIFF."))
        
        # Update metadata group title and placeholder text
        central_widget = self.centralWidget()
        if isinstance(central_widget, QSplitter):
            right_panel = central_widget.widget(1)
            if right_panel:
                metadata_group = right_panel.layout().itemAt(0).widget()
                if isinstance(metadata_group, QGroupBox):
                    metadata_group.setTitle(self.tr("Metadados do Raster"))
                    # Update metadata text placeholder
                    metadata_layout = metadata_group.layout()
                    if metadata_layout:
                        metadata_text = metadata_layout.itemAt(0).widget()
                        if hasattr(metadata_text, 'setPlaceholderText'):
                            metadata_text.setPlaceholderText(self.tr("Carregue um raster para ver os metadados..."))
        
        # Update band list label
        left_panel = central_widget.widget(0)
        if left_panel:
            layout = left_panel.layout()
            if layout:
                label = layout.itemAt(1).widget()
                if isinstance(label, QLabel):
                    label.setText(self.tr("Bandas disponíveis:"))
        
        # Update preview group title and labels
        if left_panel:
            layout = left_panel.layout()
            if layout:
                preview_group = layout.itemAt(3).widget()  # Preview group is at index 3
                if isinstance(preview_group, QGroupBox):
                    preview_group.setTitle(self.tr("Preview"))
                    # Update preview button and label
                    preview_layout = preview_group.layout()
                    if preview_layout:
                        preview_button = preview_layout.itemAt(0).widget()
                        if isinstance(preview_button, QPushButton):
                            preview_button.setText(self.tr("Gerar Preview"))
                        preview_label = preview_layout.itemAt(1).widget()
                        if isinstance(preview_label, QLabel) and not preview_label.pixmap():
                            preview_label.setText(self.tr("Selecione 1 a 3 bandas para preview"))
        
        # Re-update metadata display if there's loaded data
        if hasattr(self, 'controller') and self.controller and hasattr(self.controller, 'meta') and self.controller.meta:
            self.controller.view.update_metadata_display(self.controller.meta, self.controller.band_names)
        else:
            # If no metadata is loaded, update the placeholder text
            self.metadata_text.setPlaceholderText(self.tr("Carregue um raster para ver os metadados..."))

    def set_controller(self, controller):
        """Define o controller da view"""
        try:
            self.controller = controller
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erro"), f"{self.tr('Erro ao definir controller:')}\n{str(e)}")

    def update_metadata_display(self, meta, band_names):
        """Atualiza a exibição dos metadados"""
        try:
            if not meta:
                self.metadata_text.setPlainText(self.tr("Nenhum raster carregado."))
                return
            
            metadata_text = []
            
            # Basic file information
            metadata_text.append(f"[FILE] {self.tr('Informações Básicas')}")
            metadata_text.append(f"   {self.tr('Dimensões')}: {meta.get('width', 'N/A')} x {meta.get('height', 'N/A')}")
            metadata_text.append(f"   {self.tr('Número de bandas')}: {meta.get('count', 'N/A')}")
            metadata_text.append(f"   {self.tr('Tipo de dados')}: {meta.get('dtype', 'N/A')}")
            metadata_text.append("")
            
            # Coordinate system information
            metadata_text.append(f"[CRS] {self.tr('Sistema de Coordenadas')}")
            crs = meta.get('crs', None)
            if crs:
                metadata_text.append(f"   {self.tr('CRS')}: {crs}")
                if hasattr(crs, 'to_string'):
                    metadata_text.append(f"   {self.tr('WKT')}: {crs.to_string()}")
            else:
                metadata_text.append(f"   {self.tr('CRS')}: {self.tr('Não definido')}")
            metadata_text.append("")
            
            # Geographic transformation
            metadata_text.append(f"[GEO] {self.tr('Transformação Geográfica')}")
            transform = meta.get('transform', None)
            if transform:
                metadata_text.append(f"   {self.tr('Transform')}: {transform}")
                # Extract individual components safely
                try:
                    if hasattr(transform, '__iter__'):
                        transform_list = list(transform)
                        if len(transform_list) >= 6:
                            a, b, c, d, e, f = transform_list[:6]
                            metadata_text.append(f"   {self.tr('Pixel Size X')}: {abs(a):.6f}")
                            metadata_text.append(f"   {self.tr('Pixel Size Y')}: {abs(e):.6f}")
                            metadata_text.append(f"   {self.tr('Upper Left X')}: {c:.6f}")
                            metadata_text.append(f"   {self.tr('Upper Left Y')}: {f:.6f}")
                        else:
                            metadata_text.append(f"   {self.tr('Transform inválida')}: {len(transform_list)} valores")
                    else:
                        metadata_text.append(f"   {self.tr('Transform não iterável')}: {type(transform)}")
                except Exception as e:
                    metadata_text.append(f"   {self.tr('Erro ao processar transform')}: {str(e)}")
            else:
                metadata_text.append(f"   {self.tr('Transform')}: {self.tr('Não definido')}")
            metadata_text.append("")
            
            # NoData information
            metadata_text.append(f"[DATA] {self.tr('Valores de Dados')}")
            nodata = meta.get('nodata', None)
            if nodata is not None:
                metadata_text.append(f"   {self.tr('NoData')}: {nodata}")
            else:
                metadata_text.append(f"   {self.tr('NoData')}: {self.tr('Não definido')}")
            metadata_text.append("")
            
            # Band information
            metadata_text.append(f"[BANDS] {self.tr('Informações das Bandas')}")
            for i, name in enumerate(band_names):
                metadata_text.append(f"   {self.tr('Banda')} {i+1}: {name}")
            metadata_text.append("")
            
            # Additional metadata
            metadata_text.append(f"[META] {self.tr('Metadados Adicionais')}")
            for key, value in meta.items():
                if key not in ['width', 'height', 'count', 'dtype', 'crs', 'transform', 'nodata']:
                    metadata_text.append(f"   {key}: {value}")
            
            self.metadata_text.setPlainText("\n".join(metadata_text))
            
        except Exception as e:
            self.metadata_text.setPlainText(f"{self.tr('Erro ao carregar metadados:')} {str(e)}")

    def update_preview_image(self, preview_array):
        """Atualiza a imagem de preview com o array de visualização"""
        try:
            if preview_array is None:
                self.preview_label.setText(self.tr("Erro ao gerar preview"))
                return
            
            # Convert numpy array to QImage
            height, width, channels = preview_array.shape
            bytes_per_line = channels * width
            
            # Create QImage from numpy array
            q_image = QImage(preview_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Create QPixmap and scale to fit label
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale pixmap to fit label while maintaining aspect ratio
            label_size = self.preview_label.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.setText("")  # Clear text
            
        except Exception as e:
            self.preview_label.setText(f"{self.tr('Erro ao exibir preview:')} {str(e)}")

    def _open_raster(self):
        """Método interno para abrir raster"""
        try:
            if self.controller:
                self.controller.open_raster()
            else:
                QMessageBox.warning(self, self.tr("Erro"), self.tr("Controller não inicializado"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erro"), f"{self.tr('Erro ao abrir raster:')}\n{str(e)}")

    def _generate_preview(self):
        """Método interno para gerar preview RGB"""
        try:
            if self.controller:
                self.controller.generate_preview()
            else:
                QMessageBox.warning(self, self.tr("Erro"), self.tr("Controller não inicializado"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erro"), f"{self.tr('Erro ao gerar preview:')}\n{str(e)}")

    def _export_selected_bands(self):
        """Método interno para exportar bandas selecionadas"""
        try:
            if self.controller:
                self.controller.export_selected_bands()
            else:
                QMessageBox.warning(self, self.tr("Erro"), self.tr("Controller não inicializado"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erro"), f"{self.tr('Erro ao exportar bandas:')}\n{str(e)}")

    def change_to_portuguese(self):
        """Muda o idioma para português"""
        try:
            QMessageBox.information(self, self.tr("Idioma"), self.tr("Funcionalidade de idioma: Português (em desenvolvimento)"))
        except Exception as e:
            print(f"Erro ao mudar para português: {e}")

    def change_to_english(self):
        """Muda o idioma para inglês"""
        try:
            QMessageBox.information(self, self.tr("Language"), self.tr("Language switch: English (under development)"))
        except Exception as e:
            print(f"Erro ao mudar para inglês: {e}")

    def closeEvent(self, event):
        """Tratamento do evento de fechamento da janela"""
        try:
            event.accept()
        except Exception as e:
            print(f"Erro ao fechar janela: {e}")
            event.accept()
