------------------------------- MODULE Meseeks -------------------------------
(***************************************************************************)
(* Meseeks: a model-dependency-free, clocked orchestration of sub-autonomous *)
(* agents over a public legal inbox.                                         *)
(*                                                                          *)
(* Implementation: agents/meseeks/agent.yaml (LoopAgent orchestrator),       *)
(* round.yaml (one sub-agent round), backends.py (clock window + chain),     *)
(* adk_agent.py (callbacks), guardrails.py (Enforce).                        *)
(* First-order twin of this module, checked over the whole finite universe:  *)
(* specs/prolog/meseeks.pl.                                                 *)
(*                                                                          *)
(* The model provider is an ORACLE: at each round it may return any value    *)
(* at all (any category, an unknown category, an unusable confidence, or    *)
(* nothing), or fail to answer in time. Nothing in this module depends on   *)
(* which provider it is - local Ollama, a headless coder, or an API.        *)
(*                                                                          *)
(* The language of publishable outcomes is nevertheless DETERMINED: for     *)
(* every oracle behaviour and every timing, the published set lies inside   *)
(* Admissible, a set computed from the batch alone (decidable, no model),   *)
(* every message is either published or held, and the run ends. That is    *)
(* ModelDependencyFreeRecursivelyEnumeratedLanguageWhichHasDetermined.      *)
(*                                                                          *)
(* Clocks. `now` is the orchestrator's clock, in cycles.                    *)
(*  - Each sub-agent has a budget of cycles for one unattended call, never  *)
(*    above MaxCall (60 s in production).                                   *)
(*  - A round is one chain of calls, first answer wins, inside a window     *)
(*    that is SlackPct% of the summed budgets (130%): room for overhead,    *)
(*    not enough for a stalling model to hold the orchestration. Each call  *)
(*    is also capped by what is left of the window.                         *)
(*  - After a round the orchestrator stops, or issues one more question +   *)
(*    reason + instruction for the ids still unanswered. It also stops      *)
(*    after Idle cycles (60 s) without a new proposal, after MaxRounds, or  *)
(*    when no sub-agent answered at all.                                    *)
(*                                                                          *)
(* Human in the loop. Once the loop stops and Decide has run, every held    *)
(* message that was not hard-rejected waits for a human, who may confirm   *)
(* it into a category (the confirmation passes the same gate, at full      *)
(* confidence) or acknowledge it as held; the run completes after the last *)
(* acknowledgement. In a drill (Drill = TRUE) the human is standing by, so  *)
(* the sub-agents' window shrinks to SlackDrill% (90%) of their budgets.    *)
(*                                                                          *)
(* Witnesses. Only a witness may act as the human: an actor is a record of  *)
(* address, origin network, platform and authentication, and it is a       *)
(* witness exactly when the address is a known person at an allowed       *)
(* domain, the origin is the local or wide-area network, the platform is   *)
(* one the witness agents run on, and the identity was proven by a         *)
(* verified OpenID Connect ID token from the configured issuer. Any other  *)
(* actor's confirm or ack is refused (no state change).                     *)
(***************************************************************************)
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Order,       \* sequence of message records: the batch, in processing order
  Firms,       \* participating firm domains (allowlist for "answer")
  Questions0,  \* ids of questions already posted on the page
  Agents,      \* sequence of sub-agent names, tried in order within a round
  Budget,      \* [Agents -> Nat]: cycles each sub-agent may take for one call
  MaxCall,     \* cap on any single call's budget (60 s)
  SlackPct,    \* window = ceiling(SlackPct% of the summed budgets), e.g. 130
  SlackDrill,  \* the same during a human-in-the-loop drill, e.g. 90
  Drill,       \* TRUE when a human is in the loop for this run
  Idle,        \* cycles without a new proposal after which the loop stops (60 s)
  MaxRounds,   \* question + reason + instruction rounds allowed
  MinConf,     \* confidence floor on a 0..10 scale (0.5 in production)
  Actors,      \* set of [addr, dom, net, os, auth] records that may try to act as the human
  WitnessAddrs, WitnessDoms, WitnessNets, WitnessOS  \* _data/meseeks_witnesses.yml

Cats     == {"opportunity", "notice", "standing_order", "question", "answer"}
None     == "none"
Silent   == "absent"   \* the oracle said nothing about this message
Ids      == {Order[i].id : i \in 1..Len(Order)}
Msg(id)  == Order[CHOOSE i \in 1..Len(Order) : Order[i].id = id]
NAgents  == Len(Agents)

\* A message carries only what the guardrails look at. `rcat`/`rconf` is the
\* deterministic keyword-rule classification (rule_classify).
MsgType == [id    : Ids,
            dom   : STRING,
            hard  : BOOLEAN,         \* hard_reject: spam, abuse, bad attachment, too short
            src   : BOOLEAN,         \* has a source link or PDF
            scope : BOOLEAN,         \* originates in the Killeen / Bell County / Texas statutory context
            reply : Ids \cup {None}, \* [Q-id] this message replies to
            rcat  : Cats \cup {None},
            rconf : 0..10]

\* What an oracle may say about one message. "junk" is any string outside Cats;
\* 99 stands for any confidence that does not parse. The oracle may also stay silent.
OracleConf == {0, 10, 99}
OracleCat  == Cats \cup {None, "junk", Silent}
Proposal   == [cat : OracleCat, conf : OracleConf]
RoundOutput == [Ids -> Proposal]
Absent     == [cat |-> Silent, conf |-> 0]
IsAbsent(p) == p.cat = Silent
NoOutput   == [id \in Ids |-> Absent]

Min(a, b) == IF a < b THEN a ELSE b
Max(a, b) == IF a > b THEN a ELSE b

\* witness.is_witness: address, origin network, platform and a verified ID token all have to pass.
IsWitness(a) == a.addr \in WitnessAddrs /\ a.dom \in WitnessDoms
                /\ a.net \in WitnessNets /\ a.os \in WitnessOS /\ a.auth
Witnesses == {a \in Actors : IsWitness(a)}
Nobody    == [addr |-> None, dom |-> None, net |-> None, os |-> None, auth |-> FALSE]

(***************************************************************************)
(* Budgets and the derived window (backends.call_budget / Window).          *)
(***************************************************************************)
CallBudget(a) == Min(Budget[a], MaxCall)

RECURSIVE SumFrom(_)
SumFrom(i) == IF i > NAgents THEN 0 ELSE CallBudget(Agents[i]) + SumFrom(i + 1)
SumBudgets == SumFrom(1)

\* ceiling(Slack * SumBudgets / 100), with the drill slack when a human is in the loop
Slack  == IF Drill THEN SlackDrill ELSE SlackPct
Window == (Slack * SumBudgets + 99) \div 100

(***************************************************************************)
(* The deterministic layer (adk_agent._advisory + guardrails.enforce).       *)
(***************************************************************************)

\* Model output is advisory: validated, clamped, capped when it disagrees with
\* the rules, and never allowed to strip a question of its anonymity.
Advisory(m, p) ==
  IF IsAbsent(p)                             THEN [cat |-> m.rcat, conf |-> m.rconf]
  ELSE IF p.cat = None                       THEN [cat |-> None,   conf |-> 0]
  ELSE IF p.cat \notin Cats                  THEN [cat |-> m.rcat, conf |-> m.rconf]
  ELSE IF p.conf \notin 0..10                THEN [cat |-> m.rcat, conf |-> m.rconf]
  ELSE IF m.rcat = "question" /\ p.cat /= "question"
                                             THEN [cat |-> "question", conf |-> Max(m.rconf, p.conf)]
  ELSE IF m.rcat \in Cats /\ m.rcat /= p.cat THEN [cat |-> p.cat, conf |-> Min(p.conf, 6)]
  ELSE                                            [cat |-> p.cat, conf |-> p.conf]

\* The final gate. `qs` is the set of question ids posted so far (grows during a batch).
\* Scope: a post must sit in the thread this inbox serves (Killeen, Bell County, Texas
\* statutory, political and judicial matters); an answer inherits the scope of the
\* posted question it replies to.
Enforce(m, cat, conf, qs) ==
  /\ ~m.hard
  /\ cat \in Cats
  /\ conf >= MinConf
  /\ cat = "answer" => (m.dom \in Firms /\ m.reply \in qs)
  /\ cat = "standing_order" => m.src
  /\ cat /= "answer" => m.scope

\* Everything the guardrails could ever let through, computed from the batch
\* alone. This is the decidable language the oracle can only select within.
QuestionsEver == Questions0 \cup Ids
Admissible ==
  {p \in [id : Ids, cat : Cats] :
     \E conf \in MinConf..10 : Enforce(Msg(p.id), p.cat, conf, QuestionsEver)}

\* Process the batch in order with a given merged proposal map.
RECURSIVE DecideFrom(_, _, _, _, _)
DecideFrom(i, props, qs, pub, hld) ==
  IF i > Len(Order) THEN [pub |-> pub, held |-> hld]
  ELSE LET m   == Order[i]
           adv == Advisory(m, props[m.id])
       IN IF Enforce(m, adv.cat, adv.conf, qs)
          THEN DecideFrom(i + 1, props,
                          IF adv.cat = "question" THEN qs \cup {m.id} ELSE qs,
                          pub \cup {[id |-> m.id, cat |-> adv.cat]}, hld)
          ELSE DecideFrom(i + 1, props, qs, pub, hld \cup {m.id})

Decide(props) == DecideFrom(1, props, Questions0, {}, {})
RulesOnly     == Decide(NoOutput)

(***************************************************************************)
(* The orchestration.                                                       *)
(***************************************************************************)

VARIABLES
  phase,        \* "idle" | "loaded" | "calling" | "merging" | "review" | "done"
  now,          \* orchestrator clock, in cycles
  roundStart,   \* when the current round's window opened
  lastProgress, \* when a proposal last arrived (the idle clock)
  round,        \* completed rounds
  agentIdx,     \* which sub-agent is on the current call (1..NAgents)
  callStart,    \* when the current call began
  deadline,     \* when the current call must have answered
  roundOut,     \* this round's oracle output (NoOutput when it failed)
  roundFailed,  \* no sub-agent answered this round
  answeredBy,   \* sub-agent that answered this round, or None
  merged,       \* proposals accepted so far
  published,    \* set of [id, cat]
  held,         \* set of ids
  review,       \* held ids waiting for the human
  stop,         \* why the loop stopped, or None
  decidedBy     \* [Ids -> Actors \cup {Nobody}]: who confirmed or acknowledged each id

vars == <<phase, now, roundStart, lastProgress, round, agentIdx, callStart, deadline,
          roundOut, roundFailed, answeredBy, merged, published, held, review, stop, decidedBy>>

Horizon == MaxRounds * Window + 1

TypeOK ==
  /\ phase \in {"idle", "loaded", "calling", "merging", "review", "done"}
  /\ now \in 0..Horizon
  /\ roundStart \in 0..Horizon
  /\ lastProgress \in 0..Horizon
  /\ round \in 0..MaxRounds
  /\ agentIdx \in 1..Max(NAgents, 1)
  /\ callStart \in 0..Horizon
  /\ deadline \in 0..Horizon
  /\ roundOut \in RoundOutput
  /\ roundFailed \in BOOLEAN
  /\ answeredBy \in {Agents[i] : i \in 1..NAgents} \cup {None}
  /\ merged \in RoundOutput
  /\ published \subseteq [id : Ids, cat : Cats]
  /\ held \subseteq Ids
  /\ review \subseteq held
  /\ stop \in {None, "complete", "no sub-agent answered", "idle", "max rounds"}
  /\ decidedBy \in [Ids -> Actors \cup {Nobody}]

Missing == {id \in Ids : IsAbsent(merged[id])}

Init ==
  /\ phase = "idle" /\ now = 0 /\ roundStart = 0 /\ lastProgress = 0 /\ round = 0
  /\ agentIdx = 1 /\ callStart = 0 /\ deadline = 0
  /\ roundOut = NoOutput /\ roundFailed = FALSE /\ answeredBy = None
  /\ merged = NoOutput /\ published = {} /\ held = {} /\ review = {} /\ stop = None
  /\ decidedBy = [id \in Ids |-> Nobody]

\* load_inbox: start the loop clock, build the redacted batch.
Load ==
  /\ phase = "idle"
  /\ phase' = "loaded" /\ lastProgress' = now
  /\ UNCHANGED <<now, roundStart, round, agentIdx, callStart, deadline, roundOut, roundFailed,
                 answeredBy, merged, published, held, review, stop, decidedBy>>

\* Open a round's window and start the first sub-agent on its own deadline.
StartRound ==
  /\ phase = "loaded"
  /\ roundStart' = now
  /\ answeredBy' = None
  /\ IF NAgents = 0
       THEN /\ phase' = "merging" /\ roundFailed' = TRUE /\ roundOut' = NoOutput
            /\ UNCHANGED <<agentIdx, callStart, deadline>>
       ELSE /\ phase' = "calling" /\ agentIdx' = 1 /\ callStart' = now
            /\ deadline' = now + Min(CallBudget(Agents[1]), Window)
            /\ roundFailed' = FALSE /\ roundOut' = NoOutput
  /\ UNCHANGED <<now, lastProgress, round, merged, published, held, review, stop, decidedBy>>

\* The sub-agent answers, early or at its deadline, with ANY output at all for the
\* ids the round asked about (a follow-up round asks only for the missing ones;
\* anything said about an already-merged id is ignored by Merge anyway).
Answer ==
  /\ phase = "calling"
  /\ \E t \in {now, deadline}, out \in RoundOutput :
       /\ \A id \in Ids : ~IsAbsent(merged[id]) => IsAbsent(out[id])
       /\ now' = t
       /\ roundOut' = out
       /\ answeredBy' = Agents[agentIdx]
  /\ phase' = "merging"
  /\ UNCHANGED <<roundStart, lastProgress, round, agentIdx, callStart, deadline, roundFailed,
                 merged, published, held, review, stop, decidedBy>>

\* The sub-agent's budget runs out (hang, crash, missing binary, empty reply):
\* move to the next one with what is left of the window, or give up on this round.
Timeout ==
  /\ phase = "calling"
  /\ now' = deadline
  /\ LET left == Max(0, (roundStart + Window) - deadline)
     IN IF agentIdx < NAgents /\ left > 0
          THEN /\ agentIdx' = agentIdx + 1
               /\ callStart' = deadline
               /\ deadline' = deadline + Min(CallBudget(Agents[agentIdx + 1]), left)
               /\ UNCHANGED <<phase, roundOut, roundFailed, answeredBy>>
          ELSE /\ phase' = "merging" /\ roundFailed' = TRUE /\ roundOut' = NoOutput
               /\ UNCHANGED <<agentIdx, callStart, deadline, answeredBy>>
  /\ UNCHANGED <<roundStart, lastProgress, round, merged, published, held, review, stop, decidedBy>>

\* check_round: merge what arrived; stop, or ask again for what is missing.
Merge ==
  /\ phase = "merging"
  /\ LET newMerged == [id \in Ids |-> IF IsAbsent(merged[id]) THEN roundOut[id] ELSE merged[id]]
         newIds == {id \in Ids : IsAbsent(merged[id]) /\ ~IsAbsent(newMerged[id])}
         progressAt == IF newIds /= {} THEN now ELSE lastProgress
         stillMissing == {id \in Ids : IsAbsent(newMerged[id])}
         r == round + 1
         reason == IF stillMissing = {}           THEN "complete"
                   ELSE IF roundFailed            THEN "no sub-agent answered"
                   ELSE IF newIds = {} /\ now - progressAt >= Idle THEN "idle"
                   ELSE IF r >= MaxRounds         THEN "max rounds"
                   ELSE None
     IN /\ merged' = newMerged
        /\ lastProgress' = progressAt
        /\ round' = r
        /\ stop' = reason
        /\ phase' = IF reason = None THEN "loaded" ELSE "review"
        /\ IF reason = None THEN UNCHANGED <<published, held, review>>
           ELSE LET d == Decide(newMerged)
                IN /\ published' = d.pub /\ held' = d.held
                   /\ review' = {id \in d.held : ~Msg(id).hard}
  /\ UNCHANGED <<now, roundStart, agentIdx, callStart, deadline, roundOut, roundFailed, answeredBy, decidedBy>>

\* A witness confirms a held message into a category. The confirmation is a
\* proposal at full confidence: it goes through the same advisory layer (so a
\* citizen's question cannot be confirmed out of its anonymity) and the same gate,
\* against the questions posted so far. TLC found the version without Advisory.
PostedQuestions == Questions0 \cup {p.id : p \in {x \in published : x.cat = "question"}}
HumanConfirm ==
  /\ phase = "review"
  /\ \E w \in Witnesses, id \in review, cat \in Cats :
       LET adv == Advisory(Msg(id), [cat |-> cat, conf |-> 10])
       IN /\ Enforce(Msg(id), adv.cat, adv.conf, PostedQuestions)
          /\ published' = published \cup {[id |-> id, cat |-> adv.cat]}
          /\ held' = held \ {id}
          /\ review' = review \ {id}
          /\ decidedBy' = [decidedBy EXCEPT ![id] = w]
  /\ UNCHANGED <<phase, now, roundStart, lastProgress, round, agentIdx, callStart, deadline,
                 roundOut, roundFailed, answeredBy, merged, stop>>

\* A witness acknowledges a held message: it stays held.
HumanAck ==
  /\ phase = "review"
  /\ \E w \in Witnesses, id \in review :
       /\ review' = review \ {id}
       /\ decidedBy' = [decidedBy EXCEPT ![id] = w]
  /\ UNCHANGED <<phase, now, roundStart, lastProgress, round, agentIdx, callStart, deadline,
                 roundOut, roundFailed, answeredBy, merged, published, held, stop>>

\* Anyone who is not a witness may try; the inbox refuses and nothing changes.
StrangerTries ==
  /\ phase = "review"
  /\ \E a \in Actors \ Witnesses, id \in review : TRUE
  /\ UNCHANGED vars

\* Nothing left for the human: the run is complete.
Finish ==
  /\ phase = "review" /\ review = {}
  /\ phase' = "done"
  /\ UNCHANGED <<now, roundStart, lastProgress, round, agentIdx, callStart, deadline,
                 roundOut, roundFailed, answeredBy, merged, published, held, review, stop, decidedBy>>

Next == Load \/ StartRound \/ Answer \/ Timeout \/ Merge \/ HumanConfirm \/ HumanAck
        \/ StrangerTries \/ Finish

Spec == Init /\ [][Next]_vars /\ WF_vars(Next)

(***************************************************************************)
(* Properties.                                                              *)
(***************************************************************************)

\* --- guardrails hold whatever the oracle did ---
AnswersOnlyFromFirms ==
  \A p \in published : p.cat = "answer" => Msg(p.id).dom \in Firms
AnswersReplyToPostedQuestions ==
  \A p \in published : p.cat = "answer" =>
     Msg(p.id).reply \in Questions0 \cup {q.id : q \in {x \in published : x.cat = "question"}}
StandingOrdersHaveSources ==
  \A p \in published : p.cat = "standing_order" => Msg(p.id).src
NothingHardRejectedIsPublished ==
  \A p \in published : ~Msg(p.id).hard
QuestionsStayQuestions ==
  \A p \in published : Msg(p.id).rcat = "question" => p.cat = "question"
ThreadStaysInScope ==
  \A p \in published : Msg(p.id).scope \/ (p.cat = "answer" /\ Msg(Msg(p.id).reply).scope)
OnlyWitnessesDecide ==
  \A id \in Ids : decidedBy[id] /= Nobody => IsWitness(decidedBy[id])
OnePostPerMessage ==
  \A p, q \in published : p.id = q.id => p = q

Guardrails ==
  /\ AnswersOnlyFromFirms /\ AnswersReplyToPostedQuestions /\ StandingOrdersHaveSources
  /\ NothingHardRejectedIsPublished /\ QuestionsStayQuestions /\ OnePostPerMessage
  /\ ThreadStaysInScope /\ OnlyWitnessesDecide

\* --- the clocks ---
WindowIsSlackOverBudgets == Window = (Slack * SumBudgets + 99) \div 100
DrillShrinksTheWindow    == Drill => Window <= (SlackDrill * SumBudgets + 99) \div 100
NoCallBeyondMaxCall      == phase = "calling" => deadline - callStart <= MaxCall
EachCallWithinItsBudget  == phase = "calling" => deadline - callStart <= Budget[Agents[agentIdx]]
RoundNeverPastItsWindow  == phase \in {"calling", "merging"} => now <= roundStart + Window
                                                             /\ deadline <= roundStart + Window
RoundsBounded            == round <= MaxRounds
RunBounded               == now <= MaxRounds * Window
Clock == /\ WindowIsSlackOverBudgets /\ DrillShrinksTheWindow /\ NoCallBeyondMaxCall
         /\ EachCallWithinItsBudget /\ RoundNeverPastItsWindow /\ RoundsBounded /\ RunBounded

\* --- the determined language ---
\* Whatever any provider said, whenever it said it, and whatever the human then
\* confirmed: the published set is inside the batch-determined Admissible set,
\* every message is decided exactly once, nothing hard-rejected ever reaches the
\* human, and with no model at all the loop's outcome is exactly the rules' outcome.
ModelDependencyFreeRecursivelyEnumeratedLanguageWhichHasDetermined ==
  /\ phase \in {"review", "done"} =>
       /\ published \subseteq Admissible
       /\ {p.id : p \in published} \cup held = Ids
       /\ {p.id : p \in published} \cap held = {}
       /\ \A id \in review : ~Msg(id).hard
  /\ (phase = "review" /\ review = {id \in held : ~Msg(id).hard} /\ NAgents = 0)
       => published = RulesOnly.pub

Invariants == TypeOK /\ Guardrails /\ Clock
              /\ ModelDependencyFreeRecursivelyEnumeratedLanguageWhichHasDetermined

\* --- liveness: the orchestration always finishes ---
Terminates == <>(phase = "done")

=============================================================================
