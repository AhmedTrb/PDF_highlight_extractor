# PDF Highlight Extractor

**PDF Highlight Extractor** is a Python-based desktop application that extracts highlighted text and comments from PDF files, organizes them, and outputs them into Markdown files. It categorizes highlights based on color or user-defined criteria, making it easier to structure and review important insights. Additionally, the application extracts comment popups, which are particularly useful for reflecting on ideas found in books. By displaying the original highlighted text alongside the associated comment, users can seamlessly connect key passages with their thoughts, making the review process more effective for readers, students, and professionals.

## User Interface :
<img src="https://github.com/user-attachments/assets/50adcde5-b5cc-466f-a0ad-d73f082382c0" width="600" />

## Motivation :
As someone who reads a lot of documents in PDF format—be it books, papers, slides, or other materials—I often found myself using the highlight tool in the Microsoft Edge PDF viewer. After reading, I would save the PDFs, but the highlights and notes would remain trapped within the document. Over time, this valuable information would get lost, and I rarely revisited or reflected on those notes. This felt like a missed opportunity for learning and deeper understanding.

To solve this problem, I decided to create a tool that could help me extract my highlights and notes from PDFs, organize them, and output them in a format that would be easy to review and reflect on. Although there are existing solutions, I wanted something custom-built to fit my specific needs and be fully adaptable to my workflow.

The result is a Python-based desktop application that extracts highlights and comments from PDF files. It organizes the data based on color or user-defined criteria and outputs everything into a Markdown file. Since I use Obsidian as my note-taking system, Markdown was the perfect format for me to store and structure these insights.

## Features :
- Extract Highlights: The application extracts all highlights and comments from PDF files.
- Categorize Highlights: Highlights are automatically categorized based on color or other user-defined criteria. This makes it easier to organize and review key insights.
- Extract Comment Popups: The application extracts all comments and associated popup text. This allows users to see reflections, annotations, or thoughts related to specific highlighted sections.
- Markdown Output: The extracted highlights and associated comments are saved in Markdown files, with each entry specifying the page number.
- Customizable: Built for personal use, so you can modify or extend it to meet your needs.
- Simple Input/Output: specify the folder containing your PDFs, select the file you want to process, and get the output in a separate folder.

## How to Use :
1.Clone the repository or download the files.
```bash
git clone https://github.com/AhmedTrb/PDF_highlight_extractor.git
```
2.Install the required dependencies by running
```bash
  pip install -r requirements.txt
```
3.Run application
```bash
  python app.py
```

4.Choose the folder containing the PDFs you want to process.

5.Select the PDF file from which you want to extract highlights.

5.The extracted highlights and notes will be saved in Markdown format in the specified output folder.

