from src.controller.app_controller import AppController
from src.view.main_window import MainWindow


if __name__ == "__main__":
    controller = AppController()
    app = MainWindow(controller)
    app.mainloop()

