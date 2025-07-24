# run_mvp.py - Startup script for the MVP
import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def setup_venv():
    """Setup and activate virtual environment"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        result = subprocess.run([sys.executable, "-m", "venv", "venv"])
        if result.returncode != 0:
            print("❌ Failed to create virtual environment")
            return False
    
    # Determine the correct activation script path
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
    else:  # Unix/Linux/MacOS
        activate_script = venv_path / "bin" / "activate"
    
    if not activate_script.exists():
        print("❌ Virtual environment activation script not found")
        return False
    
    print("✅ Virtual environment ready")
    return str(activate_script)

def install_dependencies(python_path):
    """Install required dependencies in virtual environment"""
    print("📋 Checking dependencies...")
    
    # Check if key packages are installed
    result = subprocess.run([python_path, "-c", "import fastapi, streamlit"], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("📥 Installing dependencies...")
        install_result = subprocess.run([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
        if install_result.returncode != 0:
            print("❌ Failed to install dependencies")
            return False
    
    print("✅ Dependencies ready")
    return True

def check_ollama():
    """Check if Ollama is running and has the required model"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'llama3.2' not in result.stdout:
            print("⚠️  Warning: llama3.2 model not found. Installing...")
            subprocess.run(['ollama', 'pull', 'llama3.2'])
        return True
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first.")
        print("   Visit: https://ollama.ai/")
        return False

def start_backend(python_path):
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend on port 8001...")
    return subprocess.Popen([
        python_path, '-m', 'fastapi', 'run', 'stream.py', '--port', '8001'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def start_frontend(python_path):
    """Start the Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    return subprocess.Popen([
        python_path, '-m', 'streamlit', 'run', 'frontend.py', '--server.port', '8501'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    print("🎥 YouTube to Blog MVP Startup")
    print("=" * 40)
    
    # Setup virtual environment
    python_path = setup_venv()
    if not python_path:
        return
    
    # Install dependencies
    if not install_dependencies(python_path):
        return
    
    # Check prerequisites
    if not check_ollama():
        return
    
    try:
        # Start backend
        backend_process = start_backend(python_path)
        print("✅ Backend starting...")
        time.sleep(3)  # Give backend time to start
        
        # Start frontend
        frontend_process = start_frontend(python_path)
        print("✅ Frontend starting...")
        time.sleep(3)  # Give frontend time to start
        
        print("\n🌟 MVP is now running!")
        print("📝 Frontend: http://localhost:8501")
        print("🔧 Backend API: http://localhost:8001")
        print("📚 API Docs: http://localhost:8001/docs")
        print("\nPress Ctrl+C to stop both services")
        
        # Auto-open browser
        webbrowser.open("http://localhost:8501")
        
        # Wait for user interrupt
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down services...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ Services stopped successfully")
            
    except Exception as e:
        print(f"❌ Error starting services: {e}")
        return

if __name__ == "__main__":
    main()
