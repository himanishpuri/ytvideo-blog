# main.py
from agents.yt_tool import get_transcript
from agents.blog_researcher import researcher_chain
from agents.blog_writer import writer_chain

def main():
    video_url = input("Enter YouTube video URL: ")

    print("\n[Step 1] Extracting transcript...")
    transcript = get_transcript(video_url)
    print("\nGenerated Transcript:\n", transcript)
    
    print("\n[Step 2] Generating blog outline...")
    outline = researcher_chain.invoke({"transcript": transcript})
    print("\nGenerated Outline:\n", outline)

    print("\n[Step 3] Generating full blog...")
    blog_post = writer_chain.invoke({"outline": outline, "transcript": transcript})

    with open("blog_post.txt", "w", encoding="utf-8") as f:
        f.write(blog_post)

    print("\nBlog saved to blog_post.txt")

if __name__ == "__main__":
    main()
