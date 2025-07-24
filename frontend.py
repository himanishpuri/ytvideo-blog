# frontend.py - Streamlit Frontend
import streamlit as st
import requests
import time

# Page config
st.set_page_config(
    page_title="YouTube to Blog Converter",
    page_icon="📝",
    layout="wide"
)

st.title("🎥 YouTube to Blog Converter")
st.markdown("Convert any YouTube video into a well-structured blog post using AI!")

# Backend URL
BACKEND_URL = "http://127.0.0.1:8001"

# Input section
st.header("📍 Step 1: Enter YouTube URL")
video_url = st.text_input(
    "YouTube Video URL:",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Paste the full YouTube video URL here"
)

# Processing section
if st.button("🚀 Generate Blog Post", type="primary"):
    if video_url:
        # Validate URL
        if "youtube.com/watch" not in video_url and "youtu.be/" not in video_url:
            st.error("❌ Please enter a valid YouTube URL")
        else:
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Start tracking time
                start_time = time.time()
                
                # Call backend API with progress tracking
                status_text.text("🔍 Extracting video transcript...")
                progress_bar.progress(25)
                
                # Create a placeholder for real-time timer
                timer_placeholder = st.empty()
                
                # Make the request in a way that allows us to track progress
                status_text.text("⚙️ Processing content with AI...")
                progress_bar.progress(50)
                
                # Start a timer that updates while request is processing
                import threading
                import queue
                
                # Queue to communicate between threads
                result_queue = queue.Queue()
                
                def make_request():
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/generate-blog",
                            json={"video_url": video_url},
                            timeout=1200  # 20 minute timeout
                        )
                        result_queue.put(("success", response))
                    except Exception as e:
                        result_queue.put(("error", e))
                
                # Start the request in a separate thread
                request_thread = threading.Thread(target=make_request)
                request_thread.start()
                
                # Update timer while request is processing
                response = None
                while request_thread.is_alive():
                    elapsed = time.time() - start_time
                    timer_placeholder.info(f"⏱️ Processing time: {elapsed:.1f} seconds")
                    
                    # Update status message with elapsed time
                    status_text.text(f"⚙️ Processing content with AI... ({elapsed:.1f}s elapsed)")
                    
                    # Update progress based on time (capped at 90%)
                    progress_percent = min(50 + (elapsed / 120) * 40, 90)  # 2 minutes to reach 90%
                    progress_bar.progress(int(progress_percent))
                    
                    time.sleep(0.5)  # Update every half second
                
                # Get the result
                try:
                    result_type, result = result_queue.get_nowait()
                    if result_type == "error":
                        raise result
                    response = result
                except queue.Empty:
                    raise RuntimeError("Request completed but no result received")
                
                # Calculate and display total time
                elapsed_time = time.time() - start_time
                timer_placeholder.success(f"✅ Total processing time: {elapsed_time:.2f} seconds")
                progress_bar.progress(100)
                
                if response.status_code == 200:
                    status_text.text("✅ Blog post generated successfully!")
                    
                    result = response.json()
                    
                    # Display results
                    st.header("📝 Generated Blog Post")
                    
                    # Show processing time from backend if available
                    if "processing_time" in result:
                        st.info(f"🔧 Backend processing time: {result['processing_time']:.2f} seconds")
                    
                    # Show video info if available
                    if "video_info" in result:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.subheader("📹 Video Information")
                            st.write(f"**URL:** {video_url}")
                        
                    # Display the blog content
                    st.subheader("📄 Blog Content")
                    st.markdown(result["blog_content"])
                    
                    # Download button
                    st.download_button(
                        label="📥 Download as Markdown",
                        data=result["blog_content"],
                        file_name="blog_post.md",
                        mime="text/markdown"
                    )
                    
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error occurred')}")
                    
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. The video might be too long or the server is busy.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to backend server. Make sure FastAPI is running on port 8001.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
            finally:
                # Clean up UI elements
                try:
                    progress_bar.empty()
                    status_text.empty()
                    if 'timer_placeholder' in locals():
                        timer_placeholder.empty()
                except Exception:
                    # Ignore cleanup errors
                    pass
    else:
        st.warning("⚠️ Please enter a YouTube URL first!")

# Sidebar with instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. **Paste YouTube URL** - Enter the full YouTube video URL
    2. **Click Generate** - Wait for the AI to process the video
    3. **Read & Download** - View your blog post and download as needed
    
    ### ⚡ Features
    - Automatic transcript extraction
    - AI-powered content generation
    - Structured blog format
    - Markdown export
    
    ### 🔧 Requirements
    - FastAPI backend running on port 8001
    - Ollama with llama3.2 model
    - Valid YouTube video with available transcript
    """)
    
    st.header("🚨 Troubleshooting")
    st.markdown("""
    **Common Issues:**
    - Ensure backend is running: `fastapi run stream.py --port 8001`
    - Check if Ollama is running: `ollama list`
    - Some videos may not have transcripts available
    """)
