import streamlit as st
import requests
import time

st.set_page_config(
    page_title="YouTube to Blog Converter",
    page_icon="📝",
    layout="wide"
)

st.title("🎥 YouTube to Blog Converter")
st.markdown("Convert any YouTube video into a well-structured blog post using AI!")

BACKEND_URL = "http://127.0.0.1:8001"

st.header("📍 Step 1: Enter YouTube URL")
video_url = st.text_input(
    "YouTube Video URL:",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Paste the full YouTube video URL here"
)

if st.button("🚀 Generate Blog Post", type="primary"):
    if video_url:
        if "youtube.com/watch" not in video_url and "youtu.be/" not in video_url:
            st.error("❌ Please enter a valid YouTube URL")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                start_time = time.time()
                
                status_text.text("🔍 Extracting video transcript...")
                progress_bar.progress(25)
                
                timer_placeholder = st.empty()
                
                status_text.text("⚙️ Processing content with AI...")
                progress_bar.progress(50)
                
                import threading
                import queue
                
                result_queue = queue.Queue()
                
                def make_request():
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/generate-blog",
                            json={"video_url": video_url},
                            timeout=1200  # 20 minute
                        )
                        result_queue.put(("success", response))
                    except Exception as e:
                        result_queue.put(("error", e))
                
                request_thread = threading.Thread(target=make_request)
                request_thread.start()
                
                response = None
                while request_thread.is_alive():
                    elapsed = time.time() - start_time
                    timer_placeholder.info(f"⏱️ Processing time: {elapsed:.1f} seconds")
                    
                    status_text.text(f"⚙️ Processing content with AI... ({elapsed:.1f}s elapsed)")
                    
                    progress_percent = min(50 + (elapsed / 120) * 40, 90)  # 2 minutes to reach 90%
                    progress_bar.progress(int(progress_percent))
                    
                    time.sleep(0.5)
                
                try:
                    result_type, result = result_queue.get_nowait()
                    if result_type == "error":
                        raise result
                    response = result
                except queue.Empty:
                    raise RuntimeError("Request completed but no result received")
                
                elapsed_time = time.time() - start_time
                timer_placeholder.success(f"✅ Total processing time: {elapsed_time:.2f} seconds")
                progress_bar.progress(100)
                
                if response.status_code == 200:
                    status_text.text("✅ Blog post generated successfully!")
                    
                    result = response.json()
                    
                    st.header("📝 Generated Blog Post")
                    
                    if "processing_time" in result:
                        st.info(f"🔧 Backend processing time: {result['processing_time']:.2f} seconds")
                    
                    if "video_info" in result:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.subheader("📹 Video Information")
                            st.write(f"**URL:** {video_url}")
                        
                    st.subheader("📄 Blog Content")
                    st.markdown(result["blog_content"])
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
                try:
                    progress_bar.empty()
                    status_text.empty()
                    if 'timer_placeholder' in locals():
                        timer_placeholder.empty()
                except Exception:
                    pass
    else:
        st.warning("⚠️ Please enter a YouTube URL first!")

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
