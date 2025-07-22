# blog_writer.py
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from config.llm_config import llm

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional blog writer."),
    ("user", """
        Using the outline below and referencing the transcript, 
        write a well-structured blog post with:
        - 1 introduction paragraph
        - 8 content paragraphs
        - 1 conclusion paragraph
        - Add engaging headings for each section.

        Outline:
        {outline}

        Transcript:
        {transcript}
    """)
])

writer_chain = writer_prompt | llm | StrOutputParser()
