import os
import requests
from bs4 import BeautifulSoup
import subprocess
import tempfile
import json
from datetime import datetime, timedelta
from langchain_core.messages import HumanMessage, SystemMessage

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:latest")
USE_OLLAMA = os.environ.get("USE_OLLAMA", "true").lower() == "true"

class KilleenCouncilAgent:
    """
    Dedicated agent to crawl, summarize, and publish Killeen City Council meeting minutes and agendas.
    Grounded in 'Agents in Trustworthy' (Task-Specific Specialist Agents).
    """

    def __init__(self, model=None):
        if USE_OLLAMA:
            from langchain_ollama import ChatOllama
            self.llm = ChatOllama(model=model or OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(model=model or "gpt-4o-mini", temperature=0)
            
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_page = os.path.abspath(os.path.join(script_dir, "../../_pages/killeen-city-counsel.md"))
        self.cutoff_date = datetime.now() - timedelta(days=60) # Last two months

    def crawl_documents(self):
        """Scrapes the Agenda Center for recent PDFs."""
        url = "https://www.killeentexas.gov/284/Agendas-Minutes"
        print(f"Scanning Killeen Agendas: {url}")
        results = []
        try:
            response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                text = link.text.lower()
                href = link['href']
                if 'agenda' in text or 'minutes' in text:
                    full_url = requests.compat.urljoin(url, href)
                    if full_url.endswith('.pdf'):
                        results.append({
                            "title": link.text.strip(),
                            "url": full_url
                        })
            return results
        except Exception as e:
            print(f"Error scanning Killeen: {e}")
            return []

    def extract_text_from_pdf(self, url):
        """Downloads a PDF and extracts text."""
        try:
            print(f"Downloading: {url}")
            resp = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp.write(resp.content)
                tmp_path = tmp.name
            
            result = subprocess.run(['pdftotext', tmp_path, '-'], capture_output=True, text=True)
            text = result.stdout
            os.remove(tmp_path)
            return text
        except Exception as e:
            print(f"Failed to process PDF {url}: {e}")
            return ""

    def process_document(self, text, url):
        """Uses LLM to determine date and summarize if within the last two months."""
        system_prompt = f"""
        You are a government data analyst. You will be given raw text extracted from a Killeen City Council meeting agenda or minutes document.
        
        Task:
        1. Identify the Date of the meeting.
        2. Determine if the meeting date is on or after {self.cutoff_date.strftime('%B %d, %Y')}.
        3. If it is NOT within the timeframe, return exactly this JSON: {{"relevant": false}}
        4. If it IS within the timeframe, summarize the key points, decisions, and discussions of the meeting.
        5. Output valid JSON in this format:
        {{
            "relevant": true,
            "date": "YYYY-MM-DD",
            "summary": "Detailed markdown summary of the meeting..."
        }}
        """
        
        human_message = f"Raw Document Text (truncated):\n{text[:15000]}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message)
        ]
        
        try:
            response = self.llm.invoke(messages)
            json_str = response.content.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            
            data = json.loads(json_str)
            return data
        except Exception as e:
            print(f"LLM processing error for {url}: {e}")
            return {"relevant": False}

    def update_page(self, summaries):
        """Updates the killeen-city-counsel.md page."""
        os.makedirs(os.path.dirname(self.output_page), exist_ok=True)
        
        content = f"""---
layout: default
title: "Killeen City Council Updates"
permalink: /killeen-city-counsel/
description: "Latest summaries from Killeen City Council meeting agendas and minutes."
last_updated: {datetime.now().strftime('%Y-%m-%d')}
---

# Killeen City Council Meetings

This page provides automated summaries of Killeen City Council meetings from the last two months.

"""
        if not summaries:
            content += "\n*No recent meeting summaries available at this time.*\n"
        else:
            # Sort by date descending
            summaries.sort(key=lambda x: x.get('date', ''), reverse=True)
            for s in summaries:
                content += f"## Meeting Date: {s.get('date', 'Unknown')}\n"
                content += f"**Source Document:** [{s.get('title')}]({s.get('url')})\n\n"
                content += s.get('summary', '') + "\n\n---\n\n"
                
        with open(self.output_page, 'w') as f:
            f.write(content)
        print(f"Updated {self.output_page}")

    def run(self):
        print("Starting Killeen Council Agent...")
        docs = self.crawl_documents()
        
        # Limit to first 5 documents for testing/speed to avoid timeouts
        docs = docs[:5]
        
        valid_summaries = []
        for doc in docs:
            text = self.extract_text_from_pdf(doc['url'])
            if text.strip():
                print(f"Analyzing document: {doc['title']}")
                result = self.process_document(text, doc['url'])
                if result.get("relevant"):
                    result['title'] = doc['title']
                    result['url'] = doc['url']
                    valid_summaries.append(result)
                    
        self.update_page(valid_summaries)
        print("Killeen Council Agent run complete.")

if __name__ == "__main__":
    agent = KilleenCouncilAgent()
    agent.run()
