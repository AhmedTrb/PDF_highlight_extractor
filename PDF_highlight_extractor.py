import fitz  # PyMuPDF
import numpy as np
from PySide6.QtCore import Qt, QThread, Signal


class HighlightExtractorThread(QThread):
    progress = Signal(int, int)  # current, total
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path


    def categorize_highlight(self, color):
        """Categorizes highlights based on the closest color match using Euclidean distance."""
        # customize the categories of highlights as you
        color_mapping = {
            (0.5608, 0.8706, 0.9765): "Ideas & Insights",  # Light Blue
            (1.0, 0.9412, 0.4): "General Notes",  # Yellow
            (0.4902, 0.9412, 0.4): "Action Items / To-Do",  # Green
            (0.9686, 0.6, 0.8196): "Quotes & References",  # Pink
            (0.9216, 0.2863, 0.2863): "Critical Issues / Warnings"  # Red
        }

        # Convert color to a NumPy array for distance calculation
        color_array = np.array(color)

        # Find the closest color in the mapping using Euclidean distance
        best_match = min(color_mapping.keys(), key=lambda ref_color: np.linalg.norm(color_array - np.array(ref_color)))

        return color_mapping[best_match]

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
                        highlight_text = highlight_text.encode("utf-8", "ignore").decode("utf-8").replace("\n",
                                                                                                          " ").replace(
                            "�", " ")

                        # Extract annotation color
                        color_rgb = annot.colors.get("stroke", [0, 0, 0])  # Default black if undefined
                        category = self.categorize_highlight(color_rgb)

                        # Extract popup comment if it exists
                        comment = annot.info.get("content", "").strip() if annot.has_popup else ""

                        # Store structured highlight data
                        if highlight_text:
                            highlights.append({
                                "page": page_num + 1,
                                "text": highlight_text,
                                "category": category,
                                "comment": comment
                            })

            pdf_document.close()
            self.finished.emit(highlights)
        except Exception as e:
            self.error.emit(str(e))
