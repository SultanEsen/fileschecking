import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QFileDialog, QMessageBox, QLabel, QComboBox)

# Конфигурация: списки файлов
FILE_CONFIGS = {
    "Вариант 1": ["Seminar.txt", "test1.txt", "test3.txt"],
    "Вариант 2": ["image.png", "video.mp4"],
}


class FileCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Проверка наличия и порядка файлов")
        self.resize(400, 250)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите тип проверки:"))

        self.combo = QComboBox()
        self.combo.addItems(FILE_CONFIGS.keys())
        layout.addWidget(self.combo)

        self.btn_check = QPushButton("Выбрать папку и проверить")
        self.btn_check.clicked.connect(self.check_files)
        layout.addWidget(self.btn_check)

        self.setLayout(layout)

    def check_files(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if not folder_path:
            return

        required_files = FILE_CONFIGS[self.combo.currentText()]
        existing_files_map = {}  # Словарь {имя: время_изменения}

        # 1. Сначала проверяем наличие всех файлов
        missing = []
        for f in required_files:
            full_path = os.path.join(folder_path, f)
            if not os.path.exists(full_path):
                missing.append(f)
            else:
                existing_files_map[f] = os.path.getmtime(full_path)

        if missing:
            QMessageBox.critical(self, "Ошибка", f"Отсутствуют файлы:\n{', '.join(missing)}")
            return

        # 2. Проверяем хронологию (порядок в списке)
        # Сравниваем: время[0] <= время[1] <= время[2] ...
        errors = []
        for i in range(len(required_files) - 1):
            file_current = required_files[i]
            file_next = required_files[i + 1]

            if existing_files_map[file_current] > existing_files_map[file_next]:
                errors.append(f"'{file_current}' создан позже, чем '{file_next}'")

        if errors:
            QMessageBox.warning(self, "Нарушение порядка",
                                "Файлы найдены, но нарушена хронология создания:\n\n" + "\n".join(errors))
        else:
            QMessageBox.information(self, "Успех", "Все файлы на месте и порядок соблюден!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileCheckerApp()
    window.show()
    sys.exit(app.exec())