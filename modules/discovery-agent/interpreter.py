import os
from langchain_core.messages import HumanMessage, SystemMessage

# LLM Backend selection pattern from texas_data_crawler.py
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:latest")
USE_OLLAMA = os.environ.get("USE_OLLAMA", "true").lower() == "true"

class InterpreterAgent:
    """
    Interpretation Agent grounded in 'Agents in Trustworthy' (Section 2.1.2)
    and 'Prompt Engineering for Developers' (CoT, ReAct).
    Extracts the core story from raw text/HTML, removing ads and noise.
    """

    def __init__(self, model=None):
        if USE_OLLAMA:
            from langchain_ollama import ChatOllama
            self.llm = ChatOllama(model=model or OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(model=model or "gpt-4o-mini", temperature=0)

    def extract_story(self, raw_content, source_url):
        """
        Uses Chain-of-Thought prompting to isolate the news story.
        """
        system_prompt = """
        You are an expert news editor. Your task is to extract the core journalistic story from the provided raw content.
        
        Rules:
        1. Remove all advertisements, navigation links, social media widgets, and site boilerplates.
        2. Retain the headline, byline (if available), date, and the full body of the article.
        3. BE CAREFUL WITH AUTHOR NAMES. Do not guess or hallucinate. Only include the author if explicitly stated in a byline or author metadata.
        4. Do not summarize; extract the actual content.
        5. Format the output in clean Markdown.
        6. Always ensure the source URL is mentioned at the bottom as 'Source: [URL](URL)'.
        
        Process (Chain-of-Thought):
        - Identify the main headline.
        - Locate the byline or author attribution. Check <meta> tags or JSON-LD if body byline is missing.
        - Scan for the primary text blocks of the story. Ignore <script>, <style>, and <iframe> content.
        - Identify and discard non-story elements (ads, recommended articles, etc.).
        - Verify that no promotional links are included in the story body.
        """
        
        # Truncate raw content to avoid context limits
        human_message = f"Raw Content (truncated):\n{raw_content[:15000]}\n\nSource URL: {source_url}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message)
        ]
        
        response = self.llm.invoke(messages)
        return response.content

if __name__ == "__main__":
    # Quick test
    interpreter = InterpreterAgent()
    sample_text = "ADVERTISEMENT: Buy gold now! Killeen Daily Herald. City Council meets tonight to discuss budget. Click here for more ads."
    print(interpreter.extract_story(sample_text, "https://kdhnews.com/example"))
