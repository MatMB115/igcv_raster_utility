from PyQt5.QtWidgets import (
    QMainWindow, QAction, QMenuBar, QVBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QCoreApplication
import os

class MainWindow(QMainWindow):
    def __init__(self, controller=None):
        try:
            super().__init__()
            self.controller = controller
            self.translator = QTranslator()
            self.current_language = 'pt_BR'  # padrão inicial
            self._load_language(self.current_language)
            self.setWindowTitle(self.tr("IGCV Raster Tool - MVP"))
            self.setMinimumSize(400, 300)

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
                self.open_button = QPushButton(self.tr("Abrir Raster"))
                self.open_button.clicked.connect(self._open_raster)

                self.band_list = QListWidget()
                self.band_list.setSelectionMode(QListWidget.MultiSelection)

                self.export_button = QPushButton(self.tr("Exportar Selecionadas"))
                self.export_button.clicked.connect(self._export_selected_bands)
                self.export_button.setEnabled(False)

                self.status_label = QLabel(self.tr("Selecione um raster GeoTIFF."))
                self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                layout = QVBoxLayout()
                layout.addWidget(self.open_button)
                layout.addWidget(QLabel(self.tr("Bandas disponíveis:")))
                layout.addWidget(self.band_list)
                layout.addWidget(self.export_button)
                layout.addWidget(self.status_label)

                container = QWidget()
                container.setLayout(layout)
                self.setCentralWidget(container)
                
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
        layout = self.centralWidget().layout()
        if layout:
            label = layout.itemAt(1).widget()
            if isinstance(label, QLabel):
                label.setText(self.tr("Bandas disponíveis:"))

    def set_controller(self, controller):
        """Define o controller da view"""
        try:
            self.controller = controller
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erro"), f"{self.tr('Erro ao definir controller:')}\n{str(e)}")

    def _open_raster(self):
        """Método interno para abrir raster"""
        try:
            if self.controller:
                self.controller.open_raster()
            else:
                QMessageBox.warning(self, self.tr("Erro"), self.tr("Controller não inicializado"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erro"), f"{self.tr('Erro ao abrir raster:')}\n{str(e)}")

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
