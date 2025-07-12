import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.main_controller import MainController
from logger import setup_logger

def main():
    # Configurar logging
    logger = setup_logger()
    logger.info("Iniciando aplicação IGCV Raster Utility")
    
    try:
        if '--cli' in sys.argv:
            logger.info("Executando modo CLI")
            argv = sys.argv[:]
            argv.remove('--cli')
            import cli.cli_app
            cli.cli_app.main(*argv)
        else:
            logger.info("Executando modo GUI")
            app = QApplication(sys.argv)
            main_window = MainWindow()  # Criar MainWindow sem controller
            controller = MainController(main_window)  # Criar controller com referência à view
            main_window.set_controller(controller)  # Conectar controller à view
            main_window.show()
            logger.info("Interface gráfica iniciada com sucesso")
            app.exec_()
    except ImportError as e:
        logger.error(f"Erro de importação: {e}")
        print(f"Erro de importação: {e}")
        print("Verifique se todas as dependências estão instaladas: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado na aplicação: {e}", exc_info=True)
        print(f"Erro inesperado na aplicação: {e}")
        sys.exit(1)
    finally:
        logger.info("Aplicação finalizada")

if __name__ == "__main__":
    main()

