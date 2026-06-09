import logging

class AlphaOrchestrator:
    """
    Orchestration & Layered Control (The Alpha Role)
    Based on Agent-Oriented Programming (Huntbach & Ringwood), Chapter 10 & 5.
    """
    def __init__(self):
        self.iteration = 0
        self.run_count = 0
        self.logger = logging.getLogger("AlphaOrchestrator")

    def spawn_sub_agent(self, agent_role, initial_state=0):
        """
        Manages recursive spawning based on Subsumption Architecture.
        Each spawned agent starts with its state set to the specific initial_state (usually 0).
        """
        self.logger.info(f"Spawning sub-agent for role: {agent_role} with state: {initial_state}")
        # In a real implementation, this would instantiate the agent, isolated process or container
        return {"role": agent_role, "state": initial_state, "status": "active"}

    def consensus_protocol(self, data_streams):
        """
        Implements Consensus Protocol (Section 5.3) for reaching a verified 'system truth'.
        Takes a list of data streams (findings from agents) and resolves conflicts.
        """
        if not data_streams:
            return None

        # Simplified consensus: returning the most frequent finding
        counts = {}
        for stream in data_streams:
            finding = str(stream.get("finding", ""))
            counts[finding] = counts.get(finding, 0) + 1

        system_truth = max(counts, key=counts.get)
        self.logger.info(f"Reached consensus. System Truth: {system_truth}")
        return system_truth

    def orchestrate(self, tasks):
        """
        Coordinates agents and processes streams.
        """
        self.run_count += 1
        return [self.spawn_sub_agent(task) for task in tasks]
