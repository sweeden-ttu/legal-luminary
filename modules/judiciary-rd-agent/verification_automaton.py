import re
import sys

class LogScannerAutomaton:
    """
    Formal Automaton G = (V, Sigma, R, S) for Agent Log Verification.
    States:
    S0: Start / Idle
    S1: Agent Process Launched
    S2: Researching Target URL
    S3: Screenshot Captured
    S4: Headshot Detected
    S5: Data Verified
    S6: Completion / Success
    """
    def __init__(self):
        self.state = 'S0'
        self.transitions = {
            ('S0', 'LAUNCH'): 'S1',
            ('S1', 'CRAWL'): 'S2',
            ('S2', 'SCREENSHOT'): 'S3',
            ('S3', 'DETECT'): 'S4',
            ('S4', 'VERIFY'): 'S5',
            ('S5', 'DONE'): 'S6'
        }
        self.valid_path = True

    def transition(self, event):
        key = (self.state, event)
        if key in self.transitions:
            print(f"[Automaton] Transition: {self.state} --({event})--> {self.transitions[key]}")
            self.state = self.transitions[key]
        else:
            print(f"[Automaton] INVALID TRANSITION: State {self.state} cannot handle event {event}")
            self.valid_path = False

    def scan_log(self, log_content):
        # Mapping log keywords to events
        events = [
            ('LAUNCH', r'ollama launch'),
            ('CRAWL', r'Navigating to|Crawling'),
            ('SCREENSHOT', r'Screenshot saved'),
            ('DETECT', r'Headshot detected|Bounding box'),
            ('VERIFY', r'Verification complete|Source confirmed'),
            ('DONE', r'Agent task complete')
        ]
        
        for line in log_content.split('\n'):
            for event_name, pattern in events:
                if re.search(pattern, line, re.IGNORECASE):
                    self.transition(event_name)
        
        if self.state == 'S6' and self.valid_path:
            print("[Automaton] VERIFICATION SUCCESS: Log follows formal grammar.")
        else:
            print(f"[Automaton] VERIFICATION FAILED: Final State {self.state}, Valid: {self.valid_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            scanner = LogScannerAutomaton()
            scanner.scan_log(f.read())
