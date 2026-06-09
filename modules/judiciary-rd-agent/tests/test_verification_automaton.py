import pytest
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from verification_automaton import LogScannerAutomaton

def test_valid_agent_log_sequence():
    log_content = """
    ollama launch llama3 --prompt 'Target URL'
    Navigating to https://example.com
    Screenshot saved successfully.
    Headshot detected at coordinates [0, 0, 100, 100].
    Verification complete for data.
    Agent task complete.
    """
    scanner = LogScannerAutomaton()
    scanner.scan_log(log_content)
    
    assert scanner.state == 'S6', "Failed to reach final S6 state"
    assert scanner.valid_path == True, "Automaton registered an invalid path"

def test_invalid_agent_log_sequence():
    log_content = """
    ollama launch llama3 --prompt 'Target URL'
    Screenshot saved successfully.
    Navigating to https://example.com
    """
    scanner = LogScannerAutomaton()
    scanner.scan_log(log_content)
    
    assert scanner.state != 'S6', "Should not reach final state"
    assert scanner.valid_path == False, "Automaton failed to detect out-of-order execution"

def test_incomplete_log():
    log_content = """
    ollama launch llama3
    Navigating to https://example.com
    """
    scanner = LogScannerAutomaton()
    scanner.scan_log(log_content)
    
    assert scanner.state == 'S2', "Should be stuck in S2 state"
    assert scanner.valid_path == True, "Path is valid, just incomplete"
