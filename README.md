# LLM + RAG Automation API  

This project is a Python-based API service that dynamically retrieves and executes automation functions using **LLM + RAG (Retrieval-Augmented Generation)**.  

## Features  
✔ Function registry with common automation tasks  
✔ LLM + RAG for function retrieval  
✔ Dynamic Python code generation for function execution  
✔ REST API for function invocation  

## Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Usage
Start the API Server
bash
Copy
Edit
uvicorn api_service:app --reload
Test with cURL
bash
Copy
Edit
curl -X POST "http://127.0.0.1:8000/execute" \
     -H "Content-Type: application/json" \
     -d "{\"prompt\": \"Open calculator\"}"
Expected Response
json
Copy
Edit
{
  "function": "open_calculator",
  "code": "Generated Python code for execution"
}
File Structure
bash
Copy
Edit
📂 project-root
├── automation_functions.py  # Predefined automation functions
├── function_retriever.py     # Function retrieval using RAG
├── code_generator.py         # Dynamic code generation
├── api_service.py            # FastAPI service
├── requirements.txt          # Dependencies
└── README.md                 # Project documentation
Future Enhancements
Logging and monitoring for function executions

Support for custom user-defined functions
