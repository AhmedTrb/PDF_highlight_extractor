# PDF Highlight Extractor

**PDF Highlight Extractor** is a Python-based desktop application that extracts highlighted text and comments from PDF files, organizes them, and outputs them into Markdown files. It categorizes highlights based on color or user-defined criteria, making it easier to structure and review important insights. Additionally, the application extracts comment popups, which are particularly useful for reflecting on ideas found in books. By displaying the original highlighted text alongside the associated comment, users can seamlessly connect key passages with their thoughts, making the review process more effective for readers, students, and professionals.

## User Interface :
<img src="https://github.com/user-attachments/assets/50adcde5-b5cc-466f-a0ad-d73f082382c0" width="600" />

## Motivation :
As someone who reads a lot of documents in PDF format (books, papers, slides, etc.), 
I often find myself using the highlight tool in the Microsoft Edge PDF viewer. After finishing my reading, 
I save these files, but the notes and highlights remain trapped within the documents. Over time, this information is lost, 
and I rarely go back to review or write them down. This, I felt, was a missed opportunity for learning and reflection.

So, I decided to build a tool that could solve this problem. The goal was to create something that would allow me to extract highlights and notes from my PDFs,
organize them, and output them in a format that I could easily use for review and reflection. Although there are solutions already available online,
I wanted something custom-built that could cater to my specific needs and that I could tweak as I liked.

This Python app extracts highlights from PDF files, identifies the page numbers where the highlights were taken, 
and outputs them in Markdown format. Since I use Obsidian as my note-taking system, Markdown was the ideal output format for me.

## Features :
- Extract Highlights: The application extracts all highlights and comments from PDF files.
- Markdown Output: The extracted highlights and associated comments are saved in Markdown files, with each entry specifying the page number.
- Customizable: Built for personal use, so you can modify or extend it to meet your needs.
- Simple Input/Output: specify the folder containing your PDFs, select the file you want to process, and get the output in a separate folder.

## How to Use :
1.Clone the repository or download the files.
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



## Motivation Behind Building :

I created this tool because I found myself often losing track of the valuable notes and highlights I made during my reading.
While solutions exist, I wanted something tailored to my workflow. By exporting the highlights to Markdown,
I can now easily organize and review my notes, especially in Obsidian, where I keep all my study and reflection notes.

This project has helped me stay more organized and intentional with my reading, and I hope it will be helpful to others who face the same challenge!
