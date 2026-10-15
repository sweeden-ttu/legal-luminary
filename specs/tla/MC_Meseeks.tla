---------------------------- MODULE MC_Meseeks ----------------------------
(* TLC model for Meseeks.tla: a 3-message batch (question -> firm answer     *)
(* ordering, plus a hard-rejected message), 7 sub-agents (one with a budget *)
(* above MaxCall), 2 rounds, human in the loop, in a drill (window = 90% of *)
(* the capped budgets). Unparseable confidences (99) are covered by the     *)
(* Prolog universe in specs/prolog/meseeks.pl; here the oracle says 0 or 10.*)
EXTENDS Meseeks, TLC

\* Processing order mirrors the inbox order: a citizen's question, a firm's
\* reply to it, and a spam message that also claims to be an answer.
MC_Order == <<
  [id |-> "q1", dom |-> "gmail.com",      hard |-> FALSE, src |-> FALSE, scope |-> TRUE,  reply |-> "none", rcat |-> "question", rconf |-> 10],
  [id |-> "a1", dom |-> "examplelaw.com", hard |-> FALSE, src |-> FALSE, scope |-> FALSE, reply |-> "q1",   rcat |-> "answer",   rconf |-> 10],
  [id |-> "s1", dom |-> "seo-blast.biz",  hard |-> TRUE,  src |-> TRUE,  scope |-> FALSE, reply |-> "q1",   rcat |-> "notice",   rconf |-> 10]
>>
MC_OracleConf == {0, 10}
\* The oracle alphabet is cut to the categories these three messages can be argued
\* into (plus silence, null and an unknown label); the full alphabet at 3 messages ran
\* out of memory at 14.7M states with no violation. The full alphabet is covered by the
\* Prolog universe, where Decide is checked separately from the clock.
MC_OracleCat  == {"question", "answer", "notice", None, "junk", Silent}
MC_Firms      == {"examplelaw.com"}
MC_Questions0 == {}
MC_Agents     == <<"local", "claude", "codex", "agy", "agent", "opencode", "api">>
MC_Budget     == [a \in {"local", "claude", "codex", "agy", "agent", "opencode", "api"} |->
                   IF a = "local" THEN 2 ELSE IF a = "opencode" THEN 9 ELSE 1]
MC_MaxCall    == 2      \* opencode's 9 is capped to 2
MC_SlackPct   == 130    \* window = ceiling(1.3 * (2+1+1+1+1+2+1)) = 12 outside a drill
MC_SlackDrill == 90     \* window = ceiling(0.9 * 9) = 9 during a drill
MC_Drill      == TRUE
MC_Idle       == 3
MC_MaxRounds  == 2
MC_MinConf    == 5
=============================================================================
