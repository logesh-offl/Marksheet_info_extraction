📄 Marksheet Information Extraction
An AI-powered pipeline that extracts and organizes student data from marksheet images using PaddleOCR for text detection, Gemini AI for intelligent text categorization, and MongoDB for structured data storage.

🚀 Overview
This project automates the process of reading marksheets and extracting valuable student data (e.g., name, roll number, subject-wise marks). It eliminates manual data entry and leverages modern AI tools for reliable and scalable information extraction.

🧠 Workflow
📷 Image Input: Upload a scanned marksheet image.

🔍 Text Detection: PaddleOCR extracts raw text from the image.

🤖 Text Categorization: Gemini AI processes and classifies the text into fields like Name, Roll No., Subjects, Marks, etc.

🗃️ Database Storage: The structured data is stored in a MongoDB collection for future retrieval and analysis.

🛠️ Tech Stack
🐍 Python

📦 PaddleOCR – For high-accuracy Optical Character Recognition

🤖 Gemini AI – For context-aware classification of extracted text

🍃 MongoDB – For storing extracted data in structured format

🧪 Jupyter Notebook / Streamlit (optional for UI)
