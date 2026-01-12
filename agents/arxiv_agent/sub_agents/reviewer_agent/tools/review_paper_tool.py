from . import settings

import base64
import requests
from google.adk.tools import FunctionTool, ToolContext
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage, SystemMessage
# from google.adk.agents import LlmAgent, ParallelAgent
# from google.adk.sessions import InMemorySessionService
# from google.adk.runners import Runner


def review_paper(pdf_urls: str, source_urls: str, tool_context: ToolContext):
    """Fetch string of urls divided by comma e.g: url1, url2, url3

    Args:
        pdf_urls (str): list of string of PDF URLs
        source_urls (str): list of string of source URLs
        tool_context (ToolContext): built-in ToolContext from ADK
    """
        
    try:
        pdf_urls = [i.strip() for i in pdf_urls.split(",")]
        source_urls = [i.strip() for i in source_urls.split(",")]
        session_id = tool_context.session.id
        user_id = tool_context.session.user_id
        print(f"[DEBUG] SESSION_ID / USER_ID: {session_id} / {user_id}")
    except:
        return "Unable to process the urls"
    
    llm = ChatGoogleGenerativeAI(
        model=settings.MODEL_ID,
        project=settings.GOOGLE_CLOUD_PROJECT
    )
    
    papers: list[str] = []
    for i, url in enumerate(pdf_urls):
        response = requests.get(url)
        status_code = response.status_code
        
        if status_code != 200:
            papers.append(f"PDF Unavailable | Take a look at {source_urls[i]}")
            continue
        
        try:
            pdf_b64 = base64.b64encode(response.content).decode("utf-8")
                        
            PROMPT = f"Summarize this documents and provide me list of the most important and exciting findings"
            
            system_prompt = SystemMessage(           
            """ 
            You are a seasoned researcher with more than 70 years of experience. 
            Your task is to create a comprehensive, specialized report analyzing the provided academic papers. 
            Your goal is to synthesize complex data into clear, actionable insights
            """
            )
            
            message = HumanMessage([
                {
                    "type": "text",
                    "text": PROMPT
                },
                {
                    "type": "file",
                    "base64": pdf_b64,
                    "mime_type": "application/pdf",
                }
            ])
            
            content = llm.invoke([system_prompt, message])
            
            papers.append(content.text)
                                    
                                    
        except Exception as e:
            print(f"[ERROR]: {e}")
            papers.append(f"Unable to process the PDF | take a look at {source_urls[i]}")
            
    return papers
 

review_paper_tool = FunctionTool(review_paper)