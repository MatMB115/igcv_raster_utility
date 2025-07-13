import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from view.main_window import MainWindow
from controller.main_controller import MainController
from logger import setup_logger

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
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
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

