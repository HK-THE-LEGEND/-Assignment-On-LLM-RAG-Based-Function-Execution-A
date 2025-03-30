import os
import webbrowser
import psutil
import subprocess

# Application Control
def open_chrome():
    webbrowser.open("https://www.google.com")

def open_calculator():
    # Windows example; change for your OS if needed
    os.system("calc")

def open_notepad():
    os.system("notepad")

def echo(message):
    print(message)
    return message
# Additional functions (example)
def open_file_explorer():
    os.system("explorer")

# System Monitoring
def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_ram_usage():
    return f"RAM Usage: {psutil.virtual_memory().percent}%"

# Command Execution
def run_command(command: str):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output}"