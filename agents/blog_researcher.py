# blog_researcher.py
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from config.llm_config import llm

researcher_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a blog research assistant."),
    ("user", """
        Analyze the transcript below and create:
        - A blog title suggestion
        - A structured outline with 10 bullet points (each bullet = a future paragraph).
        
        Transcript:
        {transcript}
    """)
])

researcher_chain = researcher_prompt | llm | StrOutputParser()
