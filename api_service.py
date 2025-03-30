import inspect
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from function_retriever import retrieve_function
from code_generator import generate_code
import automation_functions
from custom_functions import custom_functions

# Set up logging: logs will be saved to "execution.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="execution.log",
    filemode="a"
)

app = FastAPI()

# Request model for executing functions (with optional parameters)
class ExecuteRequest(BaseModel):
    prompt: str
    args: list = []    # Optional positional arguments
    kwargs: dict = {}  # Optional keyword arguments

@app.post("/execute")
def execute_function(request: ExecuteRequest):
    """
    Generates the Python code snippet for invoking the retrieved function.
    """
    function_name = retrieve_function(request.prompt)
    if function_name:
        generated_code = generate_code(function_name)
        return {"function": function_name, "code": generated_code}
    raise HTTPException(status_code=404, detail="No matching function found")

@app.post("/execute_and_run")
def execute_and_run(request: ExecuteRequest):
    """
    Retrieves and directly executes the function.
    Checks both the default registry (automation_functions) and custom functions.
    Uses provided args/kwargs if the function requires parameters.
    If the prompt exactly matches a custom function name, that is used.
    """
    # First, check if the prompt exactly matches a custom function name.
    if request.prompt in custom_functions:
        function_name = request.prompt
    else:
        function_name = retrieve_function(request.prompt)
    
    if function_name:
        func = None
        # Check default functions first
        if hasattr(automation_functions, function_name):
            func = getattr(automation_functions, function_name)
            registry = "default"
        elif function_name in custom_functions:
            # For custom functions, assume they're defined in globals()
            func = globals().get(function_name)
            registry = "custom"
        else:
            logging.error(f"Function {function_name} not found in any registry")
            raise HTTPException(status_code=500, detail="Function not found in registry")

        try:
            sig = inspect.signature(func)
            num_params = len(sig.parameters)
            logging.info(f"Function {function_name} requires {num_params} parameters.")

            # Execute with parameters if required, otherwise with no arguments
            if num_params > 0:
                logging.info(f"Executing {registry} function: {function_name} with args: {request.args} and kwargs: {request.kwargs}")
                result = func(*request.args, **request.kwargs)
            else:
                logging.info(f"Executing {registry} function: {function_name} without parameters")
                result = func()

            logging.info(f"Executed {function_name} successfully. Result: {result}")
            return {"function": function_name, "status": "Executed", "result": result}
        except Exception as e:
            logging.error(f"Error executing {function_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Error executing function: {e}")
    raise HTTPException(status_code=404, detail="No matching function found")

@app.get("/logs")
def get_logs():
    """
    Retrieves the last 20 lines from the execution log.
    """
    try:
        with open("execution.log", "r") as f:
            lines = f.readlines()
        return {"logs": lines[-20:]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading logs: {e}")

# Request model for adding custom functions
class AddFunctionRequest(BaseModel):
    function_name: str
    description: str
    code: str  # The complete Python code defining the function

@app.post("/add_function")
def add_function(request: AddFunctionRequest):
    """
    Adds a new custom function.
    The provided code is executed so that the function is defined globally,
    and then stored in the custom functions registry.
    """
    try:
        # Execute the user-provided code so that the function becomes available in globals()
        exec(request.code, globals())
        custom_functions[request.function_name] = request.code
        logging.info(f"Added custom function: {request.function_name}")
        return {"message": f"Function '{request.function_name}' added successfully."}
    except Exception as e:
        logging.error(f"Error adding function {request.function_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding function: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
