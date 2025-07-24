# start_mvp.ps1 - PowerShell script to start the MVP
Write-Host "🎥 YouTube to Blog MVP Startup" -ForegroundColor Green
Write-Host "=" * 40 -ForegroundColor Green

# Check and setup Python virtual environment
Write-Host "🐍 Checking Python virtual environment..." -ForegroundColor Blue

if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment. Please check Python installation." -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Blue
& ".\venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment." -ForegroundColor Red
    exit 1
}

Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies." -ForegroundColor Red
        exit 1
    }

Write-Host "✅ Virtual environment ready with dependencies" -ForegroundColor Green

# Check if Ollama is installed
Write-Host "🤖 Checking Ollama..." -ForegroundColor Blue
try {
    $ollamaCheck = ollama list 2>$null
    if ($ollamaCheck -notcontains "llama3.2") {
        Write-Host "⚠️  Installing llama3.2 model..." -ForegroundColor Yellow
        ollama pull llama3.2
    }
    Write-Host "✅ Ollama ready with llama3.2 model" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama not found. Please install Ollama first." -ForegroundColor Red
    Write-Host "   Visit: https://ollama.ai/" -ForegroundColor Yellow
    exit 1
}

# Start backend in new window
Write-Host "🚀 Starting FastAPI backend..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; fastapi run stream.py --port 8001"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend in new window
Write-Host "🎨 Starting Streamlit frontend..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; streamlit run frontend.py --server.port 8501"

# Wait a moment for frontend to start
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "🌟 MVP is now running!" -ForegroundColor Green
Write-Host "📝 Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8001" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to open the frontend in your browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open browser
Start-Process "http://localhost:8501"

Write-Host "✅ Browser opened. You can now use the application!" -ForegroundColor Green
