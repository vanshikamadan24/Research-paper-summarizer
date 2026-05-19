import os
import sys
import traceback
from summarizer import ResearchPaperSummarizer

def test():
    try:
        from reportlab.pdfgen import canvas
        dummy_pdf = "dummy.pdf"
        c = canvas.Canvas(dummy_pdf)
        c.drawString(100, 750, "This is a test research paper. " * 50)
        c.showPage()
        c.save()
        
        print("Testing summarization...")
        summarizer = ResearchPaperSummarizer()
        result = summarizer.summarize(dummy_pdf, detail_level="Brief")
        print("Success! Result:")
        print(result)
        
        print("\nTesting QA...")
        ans = summarizer.answer_question("What is this paper about?")
        print("QA Answer:", ans)
    except Exception as e:
        print("An error occurred!")
        traceback.print_exc()

if __name__ == "__main__":
    test()
