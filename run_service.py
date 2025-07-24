import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def setup_venv():
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("Creating virtual environment...")
        result = subprocess.run([sys.executable, "-m", "venv", "venv"])
        if result.returncode != 0:
            print("Failed to create virtual environment")
            return False
    
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
    else:  # Linux
        activate_script = venv_path / "bin" / "activate"
    
    if not activate_script.exists():
        print("Virtual environment activation script not found")
        return False
    
    print("Virtual environment ready")
    return str(activate_script)

def install_dependencies(python_path):
    print("Checking dependencies...")
    
    result = subprocess.run([python_path, "-c", "import fastapi, streamlit"], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Installing dependencies...")
        install_result = subprocess.run([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
        if install_result.returncode != 0:
            print("Failed to install dependencies")
            return False
    
    print("Dependencies ready")
    return True

def start_backend(python_path):
    print("Starting FastAPI backend on port 8001...")
    return subprocess.Popen([
        python_path, '-m', 'fastapi', 'run', 'stream.py', '--port', '8001'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def start_frontend(python_path):
    print("Starting Streamlit frontend...")
    return subprocess.Popen([
        python_path, '-m', 'streamlit', 'run', 'frontend.py', '--server.port', '8501'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    print("YouTube to Blog MVP Startup")
    print("=" * 40)
    
    python_path = setup_venv()
    if not python_path:
        return
    
    if not install_dependencies(python_path):
        return
    
    try:
        backend_process = start_backend(python_path)
        print("Backend starting...")
        time.sleep(5) 
        
        frontend_process = start_frontend(python_path)
        print("Frontend starting...")
        time.sleep(5) 
        
        print("\nMVP is now running!")
        print("Frontend: http://localhost:8501")
        print("Backend API: http://localhost:8001")
        print("API Docs: http://localhost:8001/docs")
        print("\nPress Ctrl+C to stop both services")
        
        webbrowser.open("http://localhost:8501")
        
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\nShutting down services...")
            backend_process.terminate()
            frontend_process.terminate()
            print("Services stopped successfully")
            
    except Exception as e:
        print(f"Error starting services: {e}")
        return

if __name__ == "__main__":
    main()
