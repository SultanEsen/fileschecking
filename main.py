import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QFileDialog, QMessageBox, QLabel)

# Укажите названия ваших файлов здесь
REQUIRED_FILES = ["test1.txt", "test2.txt", "test10.txt", "test9.txt"]


class FileCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Проверка наличия файлов")
        self.resize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel(f"Ожидаемые файлы:\n{', '.join(REQUIRED_FILES)}")
        layout.addWidget(self.label)

        self.btn_check = QPushButton("Выбрать папку и проверить")
        self.btn_check.clicked.connect(self.check_files)
        layout.addWidget(self.btn_check)

        self.setLayout(layout)

    def check_files(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для проверки")
        if not folder_path:
            return

        # Получаем список файлов в папке
        existing_files = os.listdir(folder_path)

        # Находим отсутствующие
        missing_files = [f for f in REQUIRED_FILES if f not in existing_files]

        if not missing_files:
            QMessageBox.information(self, "Успех", "Все файлы на месте!")
        else:
            msg = "Отсутствуют файлы:\n\n" + "\n".join(missing_files)
            QMessageBox.warning(self, "Внимание", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileCheckerApp()
    window.show()
    sys.exit(app.exec())