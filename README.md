# 🎥 YouTube to Blog MVP

Convert any YouTube video into a well-structured blog post using AI! This MVP combines a Streamlit frontend with a FastAPI backend, powered by LangChain and local Ollama for video-to-blog conversion.

## 🏗️ Architecture

```
Frontend (Streamlit) → Backend (FastAPI) → LangChain → Ollama (llama3.2)
                                      ↓
                               YouTube Transcript API
```

## ✨ Features

-  **Simple UI**: Clean Streamlit interface for easy YouTube URL input
-  **Real-time Processing**: See progress as your video is converted
-  **AI-Powered**: Uses LangChain with local Ollama (llama3.2) for content generation
-  **Structured Output**: Generates well-formatted blog posts with headings
-  **Download Support**: Export your blog as Markdown
-  **Error Handling**: Comprehensive error messages and validation

## 🚀 Quick Start

### Prerequisites

1. **Python 3.13+** installed
2. **Ollama** installed with llama3.2 model
   ```bash
   # Install Ollama from https://ollama.ai/
   ollama pull llama3.2
   ```

### Installation

1. **Clone or navigate to the project directory**
2. **The startup scripts will automatically handle virtual environment and dependencies**

### 🎯 Running the MVP

#### Option 1: Automatic Startup (Recommended)

**Both scripts will automatically:**

-  ✅ Create a Python virtual environment if it doesn't exist
-  ✅ Activate the virtual environment
-  ✅ Install all required dependencies
-  ✅ Check Ollama and install llama3.2 model if needed
-  ✅ Start both backend and frontend services

```bash
# Windows PowerShell (Recommended)
.\start_mvp.ps1

# Cross-platform Python script
python run_mvp.py
```

#### Option 2: Manual Setup

If you prefer manual control:

1. **Create and activate virtual environment**:

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Start services manually**:

   ```bash
   # Terminal 1 - Backend
   fastapi run stream.py --port 8001

   # Terminal 2 - Frontend
   streamlit run frontend.py --server.port 8501
   ```

4. **Open your browser** to `http://localhost:8501`

## 🔧 Virtual Environment Benefits

The automated scripts ensure:

-  ✅ **Isolated dependencies** - No conflicts with system Python packages
-  ✅ **Consistent environment** - Same setup across different machines
-  ✅ **Easy cleanup** - Just delete the `venv` folder to remove everything
-  ✅ **Reproducible builds** - Exact dependency versions from requirements.txt

1. **Start the backend** (Terminal 1):

   ```bash
   fastapi run stream.py --port 8001
   ```

2. **Start the frontend** (Terminal 2):

   ```bash
   streamlit run frontend.py --server.port 8501
   ```

3. **Open your browser** to `http://localhost:8501`

## 📱 How to Use

1. **Enter YouTube URL**: Paste any YouTube video URL with available transcripts
2. **Generate Blog**: Click the "Generate Blog Post" button
3. **Wait for Processing**: The AI will extract transcript and generate content
4. **Read & Download**: View your blog post and download as Markdown

## 🔧 API Endpoints

-  `GET /` - API information
-  `GET /health` - Health check
-  `POST /generate-blog` - Generate blog from YouTube URL
-  `GET /docs` - Interactive API documentation

## 📁 Project Structure

```
├── frontend.py              # Streamlit frontend
├── stream.py               # FastAPI backend
├── run_mvp.py             # Python startup script
├── start_mvp.ps1          # PowerShell startup script
├── main.py                # CLI version (existing)
├── requirements.txt       # Dependencies
├── agents/
│   ├── yt_tool.py        # YouTube transcript extraction
│   ├── blog_researcher.py # Blog outline generation
│   └── blog_writer.py    # Blog content generation
└── config/
    └── llm_config.py     # Ollama configuration
```

## 🎨 Screenshots

The MVP provides:

-  Clean input interface for YouTube URLs
-  Real-time progress indicators
-  Markdown-formatted blog output
-  Download functionality
-  Error handling and troubleshooting

## 🔍 Troubleshooting

### Common Issues

1. **Port 8000 already in use**

   -  The MVP uses port 8001 for backend to avoid conflicts

2. **Cannot connect to backend**

   -  Ensure FastAPI is running: `fastapi run stream.py --port 8001`
   -  Check if Ollama is running: `ollama list`

3. **Virtual environment issues**

   -  If manual setup: ensure virtual environment is activated
   -  Delete `venv` folder and re-run startup script to recreate
   -  On Windows: ensure execution policy allows PowerShell scripts

4. **Transcript not available**

   -  Some videos don't have transcripts
   -  Try videos with auto-generated captions

5. **Slow generation**

   -  Local Ollama processing can take 1-3 minutes depending on video length
   -  Consider using a more powerful model if available

6. **PowerShell execution policy (Windows)**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Health Checks

-  Backend health: `http://localhost:8001/health`
-  Test transcript: `http://localhost:8001/test-transcript/{video_id}`
-  Virtual environment: Check if `venv` folder exists and contains packages

## 🚀 Future Enhancements

-  **Video length optimization** - Handle longer videos
-  **Multiple language support** - Support non-English videos
-  **Custom prompts** - Allow users to customize blog style
-  **Batch processing** - Process multiple videos
-  **Export formats** - PDF, HTML, etc.
-  **User authentication** - Save and manage blog posts

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
