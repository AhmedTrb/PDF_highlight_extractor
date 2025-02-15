from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QListWidget, QLineEdit, QProgressBar, QTextEdit, QFrame
)
import sys
import os
from PySide6.QtGui import QFont, QPalette, QColor, QIcon
from PySide6.QtCore import Qt
from PDF_highlight_extractor import HighlightExtractorThread

class PDFHighlightExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_dark_theme()
        self.setWindowIcon(QIcon("./icon/contract.png"))

    def setup_dark_theme(self):
        # Set dark theme colors
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#1e1e1e"))
        palette.setColor(QPalette.WindowText, QColor("#ffffff"))
        palette.setColor(QPalette.Base, QColor("#2d2d2d"))
        palette.setColor(QPalette.AlternateBase, QColor("#353535"))
        palette.setColor(QPalette.Text, QColor("#ffffff"))
        palette.setColor(QPalette.Button, QColor("#353535"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.Highlight, QColor("#2979ff"))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))

        self.setPalette(palette)
        self.setStyleSheet("""
                    QWidget {
                        font-family: 'Arial', sans-serif;
                        font-size: 14px;
                    }
                    QPushButton {
                        padding: 8px 16px;
                        border-radius: 4px;
                        border: none;
                        background-color: #2979ff;
                        color: white;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #1565c0;
                    }
                    QPushButton:disabled {
                        background-color: #666666;
                    }
                    QLineEdit, QListWidget, QTextEdit {
                        padding: 8px;
                        border-radius: 4px;
                        border: 1px solid #424242;
                        background-color: #2d2d2d;
                        color: white;
                    }
                    /* List Widget specific styling */
                    QListWidget {
                        outline: none;
                        height: 450px
                    }
                    QListWidget::item {
                        padding-top: 8px;
                        padding-bottom: 8px;
                        padding-left: 8px;
                        padding-right: 8px;
                        border-radius: 4px;
                        margin: 2px 4px;
                    }
                    QListWidget::item:selected {
                        background-color: #2979ff;
                        color: white;
                    }
                    QListWidget::item:hover {
                        background-color: #1e1e1e;
                    }
                    QProgressBar {
                        border: 1px solid #424242;
                        border-radius: 4px;
                        text-align: center;
                    }
                    QProgressBar::chunk {
                        background-color: #2979ff;
                        border-radius: 3px;
                    }
                    QLabel {
                        color: #ffffff;
                    }

                    /* Scrollbar styling */
                    QScrollBar:vertical {
                        border: none;
                        background: #2d2d2d;
                        width: 8px;
                        margin: 0px;
                    }
                    QScrollBar::handle:vertical {
                        background: #666666;
                        min-height: 20px;
                        border-radius: 4px;
                    }
                    QScrollBar::handle:vertical:hover {
                        background: #888888;
                    }
                    QScrollBar::add-line:vertical {
                        height: 0px;
                    }
                    QScrollBar::sub-line:vertical {
                        height: 0px;
                    }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }

                    /* Horizontal scrollbar */
                    QScrollBar:horizontal {
                        border: none;
                        background: #2d2d2d;
                        height: 8px;
                        margin: 0px;
                    }
                    QScrollBar::handle:horizontal {
                        background: #666666;
                        min-width: 20px;
                        border-radius: 4px;
                    }
                    QScrollBar::handle:horizontal:hover {
                        background: #888888;
                    }
                    QScrollBar::add-line:horizontal {
                        width: 0px;
                    }
                    QScrollBar::sub-line:horizontal {
                        width: 0px;
                    }
                    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                        background: none;
                    }
                """)

    def init_ui(self):
        self.setWindowTitle("Highlight Extractor")
        self.setGeometry(200, 200, 800, 600)
        self.setMinimumWidth(600)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Highlight Extractor")
        title_label.setFont(QFont('Arial', 32, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Input section
        input_section = QFrame()
        input_layout = QHBoxLayout()

        self.folder_button = QPushButton("Select PDF Folder")
        self.folder_button.clicked.connect(self.select_folder)
        input_layout.addWidget(self.folder_button)

        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        self.folder_path.setPlaceholderText("No folder selected")
        input_layout.addWidget(self.folder_path)

        input_section.setLayout(input_layout)
        main_layout.addWidget(input_section)

        # File list
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.select_pdf)
        main_layout.addWidget(self.file_list)

        # Output section
        output_section = QFrame()
        output_layout = QHBoxLayout()

        self.output_folder_button = QPushButton("Select Output Folder")
        self.output_folder_button.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.output_folder_button)

        self.output_filename = QLineEdit("highlights.md")
        self.output_filename.setPlaceholderText("Enter output filename")
        output_layout.addWidget(self.output_filename)

        output_section.setLayout(output_layout)
        main_layout.addWidget(output_section)

        # Progress section
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Preview section
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setPlaceholderText("Highlights preview will appear here")
        main_layout.addWidget(self.preview_area)

        # Action buttons
        button_section = QFrame()
        button_layout = QHBoxLayout()

        self.extract_button = QPushButton("Extract Highlights")
        self.extract_button.clicked.connect(self.extract_highlights)
        self.extract_button.setEnabled(False)
        button_layout.addWidget(self.extract_button)

        self.save_button = QPushButton("Save to Markdown")
        self.save_button.clicked.connect(self.save_highlights)
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.save_button)

        button_section.setLayout(button_layout)
        main_layout.addWidget(button_section)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # Initialize variables
        self.pdf_folder = ""
        self.selected_pdf = ""
        self.output_folder = ""
        self.current_highlights = []

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select PDF Folder")
        if folder:
            self.pdf_folder = folder
            self.folder_path.setText(folder)
            self.file_list.clear()
            for file in os.listdir(folder):
                if file.lower().endswith(".pdf"):
                    self.file_list.addItem(file)

    def select_pdf(self, item):
        self.selected_pdf = os.path.join(self.pdf_folder, item.text())
        self.extract_button.setEnabled(True)
        self.preview_area.clear()
        self.status_label.clear()

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.status_label.setText(f"Output folder set to: {folder}")

    def extract_highlights(self):
        if not self.selected_pdf:
            self.show_error("Please select a PDF file first.")
            return

        self.progress_bar.setVisible(True)
        self.extract_button.setEnabled(False)
        self.preview_area.clear()

        self.extractor_thread = HighlightExtractorThread(self.selected_pdf)
        self.extractor_thread.progress.connect(self.update_progress)
        self.extractor_thread.finished.connect(self.process_highlights)
        self.extractor_thread.error.connect(self.show_error)
        self.extractor_thread.start()

    def update_progress(self, current, total):
        percentage = int((current / total) * 100)
        self.progress_bar.setValue(percentage)
        self.status_label.setText(f"Processing page {current} of {total}")

    def process_highlights(self, highlights):
        self.current_highlights = highlights
        self.preview_area.clear()

        if not highlights:
            self.show_error("No highlights found in the selected PDF.")
            return

        preview_text = ""
        for page, text in highlights:
            preview_text += f"**Page {page}**:\n - {text}\n\n"

        self.preview_area.setMarkdown(preview_text)
        self.save_button.setEnabled(True)
        self.extract_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Highlights extracted successfully!")

    def save_highlights(self):
        if not self.output_folder:
            self.show_error("Please select an output folder first.")
            return

        if not self.current_highlights:
            self.show_error("No highlights to save.")
            return

        output_path = os.path.join(self.output_folder, self.output_filename.text())
        try:
            with open(output_path, 'w', encoding='utf-8') as md_file:
                md_file.write(f"# Highlights from {os.path.basename(self.selected_pdf)}\n\n")
                for page, highlight in self.current_highlights:
                    md_file.write(f"**Page {page}**:\n")
                    md_file.write(f" - {highlight}\n")


            self.status_label.setText(f"Highlights saved to: {output_path}")
        except Exception as e:
            self.show_error(f"Error saving file: {str(e)}")

    def show_error(self, message):
        self.status_label.setText(f"Error: {message}")
        self.status_label.setStyleSheet("color: #ff5252;")
        self.progress_bar.setVisible(False)
        self.extract_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFHighlightExtractor()
    window.show()
    sys.exit(app.exec())