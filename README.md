# LLM Hallucination Detection System

## Overview
An evidence-based, multi-agent system designed to identify and assess potentially hallucinated claims in LLM-generated answers.

The system extracts factual claims, retrieves relevant evidence, verifies claims and identifies cases requiring manual review.
<img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/68833db9-97a1-4a0b-8ae0-9350e50acc7d" />

<img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/05a8c0a8-1d1d-4850-aa6d-94fba092c084" />


## Architecture

1. **Claim Extraction Agent** – Extracts individual claims from generated answers.
2. **Evidence Retrieval Agent** – Retrieves relevant evidence from the local evidence index.
3. **Verification Agent** – Evaluates claims against retrieved evidence.
4. **Correction Agent** – Supports evidence-based correction when sufficient evidence is available.
5. **Pipeline** – Coordinates the complete verification workflow.

## Technology Stack
- Python
- PyTorch
- Sentence Transformers
- FAISS
- spaCy
- Pandas
- Hugging Face Transformers

## Project Structure

```text
hallucination-detection-in-llms/
├── agents/
│   ├── claim_extractor.py
│   └── correction_agent.py
├── data/
├── pipeline.py
├── retriever_agent.py
├── verifier_agent.py
├── correction_agent.py
├── vector_search.py
├── build_evidence.py
├── build_index.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Riyarathore12/hallucination-detection-in-llms.git
cd hallucination-detection-in-llms
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python pipeline.py
```

Enter a question and an LLM-generated answer when prompted.

## Verification Outcomes

The system can identify claims that need further review when retrieved evidence does not sufficiently establish or contradict a claim.

## Current Limitations

- Retrieval quality affects verification accuracy.
- Relevant but incomplete evidence may result in REVIEW_REQUIRED.
- Some claims may require manual verification.
- Automatic correction should only be attempted when sufficient supporting evidence is available.

## Research Focus

This project explores evidence-based verification and multi-agent approaches to reducing factual hallucinations in Large Language Models.

## Author

Riya Rathore  
Integrated M.Tech – Computational and Data Science  
VIT Bhopal University

GitHub: https://github.com/Riyarathore12
