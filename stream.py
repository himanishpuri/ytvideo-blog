from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
from agents.yt_tool import get_transcript
from agents.blog_researcher import researcher_chain
from agents.blog_writer import writer_chain

app = FastAPI(title="YouTube to Blog API", description="Convert YouTube videos to blog posts")

# Add CORS middleware to allow Streamlit to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class VideoRequest(BaseModel):
    video_url: str

class BlogResponse(BaseModel):
    blog_content: str
    video_url: str
    processing_time: float

@app.get("/")
async def read_root():
    return {
        "message": "YouTube to Blog API", 
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_blog": "/generate-blog",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "The server is running smoothly.",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/generate-blog", response_model=BlogResponse)
async def generate_blog(request: VideoRequest):
    """
    Generate a blog post from a YouTube video URL
    """
    start_time = datetime.datetime.now()
    
    try:
        # Step 1: Extract transcript
        print(f"[INFO] Extracting transcript from: {request.video_url}")
        transcript = get_transcript(request.video_url)
        
        if not transcript:
            raise HTTPException(status_code=400, detail="Could not extract transcript from the video")
        
        # Step 2: Generate outline
        print("[INFO] Generating blog outline...")
        outline = researcher_chain.invoke({"transcript": transcript})
        
        # Step 3: Generate full blog post
        print("[INFO] Generating full blog post...")
        blog_content = writer_chain.invoke({"outline": outline, "transcript": transcript})
        
        # Calculate processing time
        end_time = datetime.datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        print(f"[INFO] Blog generation completed in {processing_time:.2f} seconds")
        
        return BlogResponse(
            blog_content=blog_content,
            video_url=request.video_url,
            processing_time=processing_time
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid YouTube URL: {str(ve)}")
    except RuntimeError as re:
        raise HTTPException(status_code=400, detail=f"Transcript error: {str(re)}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/test-transcript/{video_id}")
async def test_transcript(video_id: str):
    """
    Test endpoint to check if transcript is available for a video
    """
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        transcript = get_transcript(video_url)
        return {
            "video_id": video_id,
            "transcript_available": True,
            "transcript_length": len(transcript),
            "preview": transcript[:200] + "..." if len(transcript) > 200 else transcript
        }
    except Exception as e:
        return {
            "video_id": video_id,
            "transcript_available": False,
            "error": str(e)
        }