# LLM + RAG Automation API  

This project is a Python-based API service that dynamically retrieves and executes automation functions using **LLM + RAG (Retrieval-Augmented Generation)**.  

## Features  
Function registry with common automation tasks  
LLM + RAG for function retrieval  
Dynamic Python code generation for function execution  
REST API for function invocation  

## Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo


## Install dependencies:
pip install -r requirements.txt
## Usage
Start the API Server
uvicorn api_service:app --reload

## pip install -r requirements.txt
Usage
Start the API Server
uvicorn api_service:app --reload
## Test with cURL
curl -X POST "http://127.0.0.1:8000/execute" \
     -H "Content-Type: application/json" \
     -d "{\"prompt\": \"Open calculator\"}"

## Expected Response
{
  "function": "open_calculator",
  "code": "Generated Python code for execution"
}
## Future Enhancements
Logging and monitoring for function executions

Support for custom user-defined functions
