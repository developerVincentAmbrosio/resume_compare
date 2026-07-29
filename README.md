# resume_compare
An LLM-driven web application designed to automatically compare job descriptions against one or multiple resumes. The tool analyzes skills, highlights critical gaps, and provides actionable recommendations to optimize candidate resumes for specific roles.

## Resume Compare Tool
An LLM-driven web application designed to automatically compare job descriptions against one or multiple resumes. The tool analyzes skills, highlights critical gaps, and provides actionable recommendations to optimize candidate resumes for specific roles.
------------------------------
## Table of Contents

* Features
* Tech Stack
* Getting Started
* Prerequisites
   * Local Setup
* Usage
* License

------------------------------
## Features

* Comprehensive Score: Generates an overall alignment score from 0 to 100.
* Skill Gap Analysis: Maps matching skills and highlights missing qualifications.
* Standout Highlights: Identifies unique candidate strengths that exceed requirements.
* Optimization Advice: Provides tailored feedback to better align the resume with the target job description.
* Multi-Format Upload: Accepts .txt, .pdf, and .docx file formats.
* Agentic Workflow: Powered by complex LLM orchestration for deep textual analysis.

------------------------------
## Tech Stack

* Language: Python
* Orchestration: LangGraph (for multi-step LLM analysis and reasoning)
* Frontend UI: Streamlit (for a lightweight, interactive web interface)
* AI Model: OpenAI GPT Models

------------------------------
## Getting Started## Prerequisites
You need an OpenAI API key to run the underlying language models.

# Set your OpenAI API key in your environment
export OPENAI_API_KEY="your-api-key-here"

## Local Setup
While the application is available as a web-based service, developers can run the interface locally using the following steps:

   1. Clone the repository:
   
   git clone https://github.com
   cd resume-compare-tool
   
   2. Install dependencies:
   
   pip install -r requirements.txt
   
   3. Launch the application:
   
   streamlit run app.py
   
   
------------------------------
## Usage

   1. Open the web interface in your browser.
   2. Paste the target Job Description into the designated text box.
   3. Upload one or more Resume files (.pdf, .txt, or .docx).
   4. Click the Analyze Resume button.
   5. Review the generated breakdown, score, and alignment tips.

------------------------------
## License
This project is licensed under the MIT License - see the LICENSE file for details.
------------------------------
If you want to expand this document, let me know:

* Do you have a live URL for the hosted app?
* What are the exact names of your core project files?
* Do you want to add a section for contributing guidelines?
