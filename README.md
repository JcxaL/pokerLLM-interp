# Poker GTO Interpreter using Large Language Models (LLMs)

## Project Overview
This project aims to bridge the gap between quantitative Game Theory Optimal (GTO) strategies and interpretability in No-Limit Texas Hold'em poker. Using a fine-tuned language model, we convert raw GTO outputs and poker data into strategic insights, providing players with understandable and actionable explanations of optimal poker strategies.

## Features
- **Data Extraction and Processing**: Scripts for parsing poker books and GTO outputs (PDFs, images, text).
- **LLM Summarization and Interpretation**: A pipeline for summarizing key poker strategies and integrating them into a chain of reasoning.
- **Prompt Tuning and Iteration**: Refinement of prompts and model responses based on test questions to improve clarity and accuracy.
  
## Project Structure
```plaintext
poker-LLM/
├── README.md                 # Project overview and setup instructions
├── requirements.txt          # Python dependencies
├── data/
│   ├── raw/                  # Raw data (original PDFs, images)
│   ├── processed/            # Processed data (JSON/CSV summaries)
│   └── examples/             # Example outputs from GPT summaries
├── notebooks/
│   ├── data_extraction.ipynb # Notebook for extracting and processing PDF data
│   ├── summarization.ipynb   # Notebook for summarizing data with GPT
│   └── testing.ipynb         # Notebook for testing and refining GPT responses
├── src/
│   ├── data_processing.py    # Scripts for data extraction and cleaning
│   ├── ocr_processing.py     # Scripts for OCR and text extraction from images
│   ├── gpt_integration.py    # Functions for interacting with GPT
│   └── evaluation.py         # Code for evaluating GPT responses and testing prompts
└── .gitignore                # Files to ignore in the repo
