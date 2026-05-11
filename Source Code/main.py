import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from UI import Window
from database import database
from databaseOriginal import database_original

def main():
    app = QApplication(sys.argv)

    if not database_original():
        QMessageBox.critical(None, "Error", "Failed to open database")

    if not database():
        QMessageBox.critical(None, "Error", "Failed to open database")

    window = Window()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
