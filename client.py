import sys
import requests
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox


class PDFValidatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Validator')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Выберите PDF файл для валидации:')
        layout.addWidget(self.label)

        self.button = QPushButton('Выбрать файл')
        self.button.clicked.connect(self.select_file)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите PDF файл", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    response = requests.post('https://pdfvalidator.up.railway.app/validate', files={'file': f})
                    if response.status_code == 200:
                        result = response.json()
                        if "message" in result:
                            QMessageBox.information(self, "Результат валидации", result["message"])
                        else:
                            barcodes_validation_result_text = json.dumps(result["barcodes_validation"], indent=4, ensure_ascii=False)
                            structure_validation_result_text = json.dumps(result["structure_validation"], indent=4, ensure_ascii=False)
                            QMessageBox.warning(self, "Результат валидации", f"{barcodes_validation_result_text}\n{structure_validation_result_text}")
                    else:
                        QMessageBox.critical(self, "Ошибка", "Ошибка при валидации файла")
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к серверу")
            
# Создание и запуск приложения
def main():
    app = QApplication(sys.argv)
    ex = PDFValidatorApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
