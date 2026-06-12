import os
from langchain_core.messages import HumanMessage, SystemMessage

# LLM Backend selection pattern from texas_data_crawler.py
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:latest")
USE_OLLAMA = os.environ.get("USE_OLLAMA", "true").lower() == "true"

class VerifierAgent:
    """
    Quality Assurance Agent grounded in 'Agents in Trustworthy' (Section 8.4)
    and 'Agent-Oriented Programming' (Distributed Constraint Solving).
    Compares the refined article against the source for accuracy.
    """

    def __init__(self, model=None):
        if USE_OLLAMA:
            from langchain_ollama import ChatOllama
            self.llm = ChatOllama(model=model or OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(model=model or "gpt-4o-mini", temperature=0)

    def verify(self, refined_content, raw_source, source_url):
        """
        Verifies the refined content against the source.
        """
        system_prompt = """
        You are a fact-checker and quality auditor. Compare the REFINED Markdown article against the RAW source content.
        
        Your goals:
        1. Ensure no factual information from the main story was lost or altered.
        2. Ensure no hallucinations (content not in the source) were added.
        3. Confirm that the source link is present and correct.
        
        Output your results in JSON format:
        {
          "status": "APPROVED" | "REJECTED",
          "discrepancies": ["list of issues found"],
          "explanation": "Detailed reasoning for the score",
          "has_source_link": boolean
        }
        """
        
        human_message = f"RAW SOURCE (truncated):\n{raw_source[:8000]}\n\nREFINED CONTENT:\n{refined_content}\n\nSOURCE URL: {source_url}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message)
        ]
        
        response = self.llm.invoke(messages)
        return response.content

if __name__ == "__main__":
    verifier = VerifierAgent()
    print(verifier.verify("Refined Story", "Raw Source", "https://example.com"))
