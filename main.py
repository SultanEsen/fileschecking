import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QFileDialog, QMessageBox, QLabel, QComboBox)

# Конфигурация: словари с наборами файлов
FILE_CONFIGS = {
    "Local SOPs": ["test10.txt", "test100.txt"],
    "FF Events": ["image.png", "video.mp4", "logo.svg"],
    "International events": ["config.ini", "settings.json", "auth.key", "config1.ini", "settings1.json", "auth1.key",
                             "config2.ini", "settings2.json", "auth2.key"]
}


class FileCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CheckBox")
        self.resize(350, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Choose type:"))

        # Выпадающий список
        self.combo = QComboBox()
        self.combo.addItems(FILE_CONFIGS.keys())
        layout.addWidget(self.combo)

        self.btn_check = QPushButton("Choose folder to check")
        self.btn_check.clicked.connect(self.check_files)
        layout.addWidget(self.btn_check)

        self.setLayout(layout)

    def check_files(self):
        # Получаем список для выбранного варианта
        selected_key = self.combo.currentText()
        required_files = FILE_CONFIGS[selected_key]

        folder_path = QFileDialog.getExistingDirectory(self, "Choose folder")
        if not folder_path:
            return

        existing_files = os.listdir(folder_path)
        missing_files = [f for f in required_files if f not in existing_files]

        if not missing_files:
            QMessageBox.information(self, "Success", f"[{selected_key}]\nAll files are here!")
        else:
            msg = f"[{selected_key}]\nMissing files:\n\n" + "\n".join(missing_files)
            QMessageBox.warning(self, "Notice", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileCheckerApp()
    window.show()
    sys.exit(app.exec())