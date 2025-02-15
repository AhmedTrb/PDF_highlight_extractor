
import fitz  # PyMuPDF

from PySide6.QtCore import Qt, QThread, Signal



class HighlightExtractorThread(QThread):
    progress = Signal(int, int)  # current, total
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path

    def run(self):
        try:
            highlights = []
            pdf_document = fitz.open(self.pdf_path)
            total_pages = pdf_document.page_count

            for page_num in range(total_pages):
                self.progress.emit(page_num + 1, total_pages)
                page = pdf_document[page_num]

                for annot in page.annots():
                    if annot.type[0] == 8:  # Highlight annotation
                        # Extract highlighted text
                        highlight_text = page.get_text("text", clip=annot.rect, sort=True, flags=1).strip()
                        highlight_text = highlight_text.encode("utf-8", "ignore").decode("utf-8").replace("\n"," ").replace("�", " ")



                        # If there’s any highlight text, and a comment (or empty string)
                        if highlight_text:
                            highlights.append((page_num + 1, highlight_text))

            pdf_document.close()
            self.finished.emit(highlights)
        except Exception as e:
            self.error.emit(str(e))