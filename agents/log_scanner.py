class LogScanner:
    def __init__(self):
        # V: Variables (Non-Terminals)
        self.V = {'S', 'A_RESEARCH', 'A_VERIFY', 'A_SPAWN', 'A_LOG'}

        # Sigma: Terminals (Spawned Tasks/Actions)
        self.Sigma = {
            'init_directive',
            'acquire_knowledge',
            'verify_truth',
            'spawn_agent',
            'log_output'
        }

        # R: Production Rules
        # S -> init_directive A_RESEARCH
        # A_RESEARCH -> acquire_knowledge A_VERIFY
        # A_VERIFY -> verify_truth A_SPAWN | verify_truth A_LOG
        # A_SPAWN -> spawn_agent S
        # A_LOG -> log_output

        self.R = {
            'S': [['init_directive', 'A_RESEARCH']],
            'A_RESEARCH': [['acquire_knowledge', 'A_VERIFY']],
            'A_VERIFY': [['verify_truth', 'A_SPAWN'], ['verify_truth', 'A_LOG']],
            'A_SPAWN': [['spawn_agent', 'S']],
            'A_LOG': [['log_output']]
        }

        # S: Start Symbol
        self.start_symbol = 'S'

    def parse_log(self, token_sequence):
        """
        Validates if a sequence of logs (terminals) belongs to the language L(G).
        Implements a simple top-down parser.
        Returns True if valid, False if Anomaly detected.
        """
        def match(current_symbol, tokens):
            if not tokens:
                # If we're out of tokens but not done expanding, or we just perfectly matched
                # Let's say empty string isn't in our language unless explicitly handled.
                return []

            if current_symbol in self.Sigma:
                if current_symbol == tokens[0]:
                    return [tokens[1:]] # matched, return remaining tokens
                else:
                    return [] # mismatch
            elif current_symbol in self.V:
                all_possible_remainders = []
                for rule in self.R.get(current_symbol, []):
                    # Try to match the sequence of symbols in the rule
                    current_tokens = [tokens]
                    for symbol in rule:
                        next_tokens = []
                        for ct in current_tokens:
                            res = match(symbol, ct)
                            next_tokens.extend(res)
                        current_tokens = next_tokens
                        if not current_tokens:
                            break # This rule failed
                    all_possible_remainders.extend(current_tokens)
                return all_possible_remainders
            return []

        results = match(self.start_symbol, token_sequence)
        # It's valid if there's at least one parse that consumed ALL tokens (remainder is empty list)
        for r in results:
            if len(r) == 0:
                return True

        return False

    def scan(self, token_sequence):
        if not self.parse_log(token_sequence):
            raise Exception("Anomaly: System truth alignment failed. Log sequence not in L(G).")
        return "Log Sequence Validated"
