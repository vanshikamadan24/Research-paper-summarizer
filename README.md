AI Research Assistant is an AI-powered application that helps users analyze academic research papers efficiently. Users can upload research papers in PDF format, generate structured summaries, and interact with the paper using an intelligent chat interface powered by Google Gemini.

#Features-
Upload and analyze research papers in PDF format
Generate AI-powered summaries
Choose different summary detail levels
Chat with uploaded research papers
Interactive and clean user interface
Fast PDF processing and response generation
Google Gemini API integration
Streamlit-based web application

#Tech Stack
Frontend-
Streamlit
HTML/CSS
Backend-
Python
AI and NLP
Google Gemini API
LangChain
PDF Processing
PyPDF2 / PDF loaders

#Project Structure
ai-research-assistant/
│
├── app.py
├── summarizer.py
├── requirements.txt
├── README.md
├── .env
├── utils/
├── assets/
└── venv/
#Installation
1. Clone the Repository
git clone https://github.com/your-username/ai-research-assistant.git
cd ai-research-assistant
2. Create a Virtual Environment
Windows
python -m venv venv
macOS/Linux
python3 -m venv venv
3. Activate the Virtual Environment
Windows
venv\Scripts\activate
macOS/Linux
source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the root directory and add your Google Gemini API key.

GOOGLE_API_KEY=your_google_gemini_api_key

Get your API key from Google AI Studio:

Google AI Studio

Running the Application

Start the Streamlit server:

streamlit run app.py

The application will run locally at:

http://localhost:8501
Usage
Launch the application
Upload a research paper in PDF format
Enter your Google Gemini API key
Select the summary detail level
Click on "Generate Summary"
Read the generated summary report
Navigate to "Chat with Paper"
Ask questions related to the uploaded paper
Example Use Cases
Research paper summarization
Literature review assistance
Academic learning and revision
Research insights extraction
Question answering from academic PDFs
Requirements

Install all dependencies using:
pip install -r requirements.txt
