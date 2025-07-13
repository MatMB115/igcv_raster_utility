import sys
import os
if getattr(sys, 'frozen', False):
    base = sys._MEIPASS  # type: ignore
    os.environ.pop('PROJ_LIB', None)
    os.environ.pop('PROJ_DATA', None)
    os.environ['GDAL_DATA'] = os.path.join(base, 'gdal_data')
    os.environ['PROJ_DATA'] = os.path.join(base, 'proj_data')
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from view.main_window import MainWindow
from controller.main_controller import MainController
from logger import setup_logger

def resource_path(relative_path):
    """
    Função utilitária para obter o caminho absoluto para recursos.
    Funciona tanto para desenvolvimento quanto para aplicações congeladas.
    """
    if getattr(sys, 'frozen', False):
        # Se o aplicativo está congelado (PyInstaller, cx_Freeze, etc.)
        return os.path.join(sys._MEIPASS, relative_path)  # type: ignore
    else:
        # Se o aplicativo está em desenvolvimento
        return os.path.join(os.path.abspath('.'), relative_path)

def main():
    logger = setup_logger()
    logger.info("Starting IGCV Raster Utility application")
    
    try:
        if '--cli' in sys.argv:
            logger.info("Running CLI mode")
            argv = sys.argv[:]
            argv.remove('--cli')
            import cli.cli_app
            cli.cli_app.main(*argv)
        else:
            logger.info("Running GUI mode")
            app = QApplication(sys.argv)
            
            # Set application icon
            icon_path = resource_path('assets/icon.png')
            if os.path.exists(icon_path):
                app.setWindowIcon(QIcon(icon_path))
            
            main_window = MainWindow()
            controller = MainController(main_window)
            main_window.set_controller(controller)
            main_window.show()
            logger.info("Graphical interface started successfully")
            app.exec_()
    except ImportError as e:
        logger.error(f"Import error: {e}")
        print(f"Import error: {e}")
        print("Check if all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error in application: {e}", exc_info=True)
        print(f"Unexpected error in application: {e}")
        sys.exit(1)
    finally:
        logger.info("Application finished")

if __name__ == "__main__":
    main()

