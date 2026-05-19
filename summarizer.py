import os
from dotenv import load_dotenv
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from concurrent.futures import ThreadPoolExecutor

load_dotenv(override=True)

class ResearchPaperSummarizer:
    def __init__(self, api_key: str = None):
        kwargs = {
            "model": "gemini-2.5-flash",
            "temperature": 0.2,
        }
        if api_key:
            kwargs["google_api_key"] = api_key

        self.llm = ChatGoogleGenerativeAI(**kwargs)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=400,
        )
        self.extracted_text = ""

    def load_pdf(self, pdf_path: str) -> str:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        text = "\n\n".join(doc.page_content for doc in docs)
        return text

    def chunk_text(self, text: str):
        return self.text_splitter.split_text(text)
    
    def summarize_chunk(self, chunk: str) -> str:
        prompt = PromptTemplate(
            template="""
You are an expert research assistant.
Summarize the following section of a research paper in concise technical language.

TEXT:
{chunk}
""",
            input_variables=["chunk"],
        )

        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"chunk": chunk})

    def generate_final_report(self, partial_summaries: str, detail_level: str = "Standard") -> str:
        prompt = PromptTemplate(
            template="""
You are an expert academic research assistant.

Using the intermediate summaries below, create a well-structured report in Markdown.
The user has requested the detail level to be: {detail_level}
Adjust the length and depth of your explanation based on this detail level.

Intermediate Summaries:
{summaries}

Create the following sections:

# Executive Summary
Provide an overview.

# Key Contributions
List the main novel ideas.

# Problem Statement
What problem does the paper solve?

# Methodology
Explain the proposed approach.

# Experimental Results
Summarize datasets, metrics, and outcomes.

# Limitations
Mention weaknesses or constraints.

# Future Work
Potential improvements and extensions.

# Important Keywords
List up to 10 relevant technical keywords.
""",
            input_variables=["summaries", "detail_level"],
        )

        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"summaries": partial_summaries, "detail_level": detail_level})

    def summarize(self, pdf_path: str, detail_level: str = "Standard") -> str:
        text = self.load_pdf(pdf_path)
        self.extracted_text = text

        if len(text.strip()) < 100:
            return "The uploaded PDF does not contain enough extractable text."

        chunks = self.chunk_text(text)

        partial_summaries = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            partial_summaries = list(executor.map(self.summarize_chunk, chunks))

        combined = "\n\n".join(partial_summaries)
        return self.generate_final_report(combined, detail_level=detail_level)

    def answer_question(self, question: str) -> str:
        if not self.extracted_text:
            return "No document text available. Please summarize a document first."
            
        prompt = PromptTemplate(
            template="""
You are an extremely knowledgeable AI research assistant.
Answer the user's question based strictly on the content of the research paper provided below.
If the answer is not contained in the text, say "I could not find the answer to that in the paper."

PAPER CONTENT:
{text}

USER QUESTION:
{question}
""",
            input_variables=["text", "question"],
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"text": self.extracted_text, "question": question})