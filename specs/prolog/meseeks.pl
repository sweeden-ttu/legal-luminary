/*  Meseeks universe: first-order twin of specs/tla/Meseeks.tla, checked over the
    whole finite universe with SWI-Prolog.

        swipl -g run_all -t halt specs/prolog/meseeks.pl

    The universe is a timeline of tests. Each test is a game: a batch of messages
    (the dilemma), a set of players (the sub-autonomous agents: local model, claude,
    codex, agy, agent, opencode, api) each holding a Bayesian belief network over
    atomic evidence axioms, and the orchestrator whose laws every proposal must pass.

    Part 1  Laws: the guardrails (physical laws of this universe, ratified by a
            majority of the players), the advisory layer, Decide, Admissible.
    Part 2  Universe check: for every test, every oracle output of every round and
            every timing of every sub-agent call, the invariants of Meseeks.tla hold:
            Guardrails, Clock, and
            ModelDependencyFreeRecursivelyEnumeratedLanguageWhichHasDetermined.
            Decide does not read the clock and the clock does not read the output, so
            the two quantifiers are checked separately and the product follows.
    Part 3  Games: each player forms beliefs from evidence (naive-Bayes decomposition
            of P(category | atoms)), chooses a strategy, and is paid by ownership of
            the proposals the laws accept. Every strategy profile is enumerated; the
            all-honest profile is a Nash equilibrium, maximises welfare (mutually
            beneficial) and pays every player at least its outside option
            (individually acceptable).
*/
:- module(meseeks, [run_all/0]).
:- use_module(library(lists)).
:- use_module(library(apply)).
:- use_module(library(aggregate)).
:- use_module(library(pairs)).

:- dynamic law_vote/2.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Part 1. Laws
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

category(opportunity). category(notice). category(standing_order).
category(question).    category(answer).

min_conf(5).            % 0.5 in production, on a 0..10 scale
max_call(2).            % no single unattended call beyond this many cycles (60 s)
slack_pct(130).         % window = ceiling(130% of the summed budgets)
idle_limit(3).          % stop after this many cycles without a new proposal (60 s)
max_rounds(2).

% Sub-autonomous agents, in chain order, with the budget each asks for.
agent(local,    2).
agent(claude,   1).
agent(codex,    1).
agent(agy,      1).
agent(agent,    1).
agent(opencode, 9).     % capped to max_call by the orchestrator
agent(api,      1).

agents(As) :- findall(A, agent(A, _), As).
call_budget(A, B) :- agent(A, Want), max_call(Max), B is min(Want, Max).
sum_budgets(S) :- aggregate_all(sum(B), (agent(A, _), call_budget(A, B)), S).
window(W) :- sum_budgets(S), slack_pct(P), W is (P * S + 99) // 100.

% Laws in force are those a majority of the players voted for. Each guardrail is a
% law; the seven agents vote (the votes are part of the universe's setup).
law(no_hard_reject).      law(min_confidence).
law(answers_from_firms).  law(answers_cite_questions).
law(orders_have_sources). law(questions_stay_anonymous).
law(thread_in_scope).     % Killeen / Bell County / Texas statutory, political, judicial matters
law(witnessed_review).    % only a witness may confirm or acknowledge a held message

% Witness agents (_data/meseeks_witnesses.yml): an actor actor(Local, Domain, Net, OS) is a
% witness when every component passes. The universe of actors below is exhaustive over the
% small alphabets, so is_witness is checked for every combination in Part 2c.
witness_person(scott_weeden,   [scotdwg, sweeden, 'scott.weeden', 'weeden.scott', scottweeden]).
witness_person(johnathan_king, [jcking1278, 'johnathan.king', 'king.johnathan', johnathanking]).
witness_domain('ttu.edu'). witness_domain('cloudfrontsgroup.org'). witness_domain('cloudfronts.group').
witness_domain('legalluminary.com'). witness_domain('luminarylegal.com').
witness_net(lan). witness_net(wan).
witness_os(macos). witness_os(rocky). witness_os(kodachi).

actor_local(L)  :- witness_person(_, Ls), member(L, Ls).
actor_local(someone). actor_local(meseeks). actor_local('sweeden.ttu').
actor_domain(D) :- witness_domain(D).
actor_domain('gmail.com'). actor_domain('seo-blast.biz').
actor_net(N)    :- witness_net(N).
actor_net(internet).
actor_os(O)     :- witness_os(O).
actor_os(windows). actor_os(unknown).

is_witness(actor(L, D, N, O), P) :-
    witness_person(P, Ls), memberchk(L, Ls), witness_domain(D), witness_net(N), witness_os(O).

% A human decision: a witness's confirmation is a proposal at full confidence through the same
% advisory layer and gate; anyone else is refused and nothing changes.
human_confirm(Actor, M, Cat, Firms, Qs, published(Cat1)) :-
    ( in_force(witnessed_review) -> is_witness(Actor, _) ; true ),
    advisory(M, p(Cat, 10), a(Cat1, Conf)),
    enforce(M, Cat1, Conf, Firms, Qs), !.
human_confirm(_, _, _, _, _, refused).
law_vote(L, A) :- law(L), agent(A, _), A \== opencode.   % opencode abstains on everything
in_force(L) :-
    law(L), agents(As), length(As, N),
    aggregate_all(count, law_vote(L, _), V),
    V * 2 > N.

% The timeline of tests. test(Id, Title, Firms, Questions0, Messages) with
% message m(Id, Domain, HardReject, HasSource, ReplyTo, RuleCat, RuleConf).
% out_of_scope(Id): the message does not originate in the inbox's context; every other
% message does. An answer inherits the scope of the question it replies to.
out_of_scope(a1).   % the firm's reply carries no place or statute words of its own
out_of_scope(s1).
out_of_scope(a2).
out_of_scope(x1).
in_scope(m(Id, _, _, _, Reply, _, _), Cat) :-
    (   \+ out_of_scope(Id) -> true
    ;   Cat == answer, Reply \== none -> true
    ;   fail ).
test(1, 'citizen question, firm answer, spam that claims to be an answer',
     ['examplelaw.com'], [],
     [ m(q1, 'gmail.com',      false, false, none, question, 10),
       m(a1, 'examplelaw.com', false, false, q1,   answer,   10),
       m(s1, 'seo-blast.biz',  true,  true,  q1,   notice,   10) ]).
test(2, 'standing order without a source, order with one, answer from a stranger',
     ['examplelaw.com'], [q0],
     [ m(o1, 'bellcounty.texas.gov', false, false, none, standing_order, 10),
       m(o2, 'bellcounty.texas.gov', false, true,  none, standing_order, 10),
       m(a2, 'yahoo.com',            false, false, q0,   answer,         10) ]).
test(3, 'notice, opportunity, a question the rules cannot place, and a notice from Seattle',
     [], [],
     [ m(n1, 'killeentexas.gov',       false, true,  none, notice,      10),
       m(j1, 'centexlegalaid.org',     false, false, none, opportunity, 10),
       m(u1, 'gmail.com',              false, false, none, none,        0),
       m(x1, 'cityofseattle.example',  false, true,  none, notice,      10) ]).

msg_id(m(Id, _, _, _, _, _, _), Id).

% ---- the advisory layer (adk_agent._advisory): model output is advisory ---------
% proposal: absent | p(Cat, Conf) with Cat a category, none or junk; Conf 0..10 or 99.
advisory(m(_, _, _, _, _, RC, RF), absent,     a(RC, RF)) :- !.
advisory(_,                        p(none, _), a(none, 0)) :- !.
advisory(m(_, _, _, _, _, RC, RF), p(C, _),    a(RC, RF)) :- \+ category(C), !.
advisory(m(_, _, _, _, _, RC, RF), p(_, F),    a(RC, RF)) :- \+ between(0, 10, F), !.
advisory(m(_, _, _, _, _, question, RF), p(C, F), a(question, Conf)) :-
    C \== question, !, Conf is max(RF, F).
advisory(m(_, _, _, _, _, RC, _), p(C, F), a(C, Conf)) :-
    category(RC), RC \== C, !, Conf is min(F, 6).
advisory(_, p(C, F), a(C, F)).

% ---- the final gate (guardrails.enforce), under the laws in force ---------------
enforce(M, Cat, Conf, Firms, Qs) :-
    M = m(_, Dom, Hard, Src, Reply, _, _),
    ( in_force(no_hard_reject) -> Hard == false ; true ),
    category(Cat),
    ( in_force(min_confidence) -> min_conf(Min), Conf >= Min ; true ),
    ( Cat == answer, in_force(answers_from_firms) -> memberchk(Dom, Firms) ; true ),
    ( Cat == answer, in_force(answers_cite_questions) -> memberchk(Reply, Qs) ; true ),
    ( Cat == standing_order, in_force(orders_have_sources) -> Src == true ; true ),
    ( in_force(thread_in_scope) -> in_scope(M, Cat) ; true ).

% ---- Decide: process the batch in order with a merged proposal map --------------
decide([], _, _, _, [], []).
decide([M|Ms], Props, Firms, Qs, Pub, Held) :-
    msg_id(M, Id),
    ( memberchk(Id-P, Props) -> true ; P = absent ),
    advisory(M, P, a(Cat, Conf)),
    ( enforce(M, Cat, Conf, Firms, Qs)
    -> ( Cat == question -> Qs1 = [Id|Qs] ; Qs1 = Qs ),
       Pub = [Id-Cat|Pub1], decide(Ms, Props, Firms, Qs1, Pub1, Held)
    ;  Held = [Id|Held1], decide(Ms, Props, Firms, Qs, Pub, Held1) ).

rules_only(Msgs, Firms, Qs0, Pub, Held) :- decide(Msgs, [], Firms, Qs0, Pub, Held).

% ---- Admissible: everything the laws could ever let through, from the batch alone
admissible(Msgs, Firms, Qs0, Id-Cat) :-
    member(M, Msgs), msg_id(M, Id), category(Cat),
    maplist(msg_id, Msgs, Ids), append(Qs0, Ids, QsEver),
    min_conf(Min), between(Min, 10, Conf),
    enforce(M, Cat, Conf, Firms, QsEver), !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Part 2. The universe check
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

oracle_cat(C) :- category(C).
oracle_cat(none). oracle_cat(junk).
oracle_conf(0). oracle_conf(10). oracle_conf(99).
oracle_proposal(absent).
oracle_proposal(p(C, F)) :- oracle_cat(C), oracle_conf(F).

% Every oracle output for a batch: one proposal per message id.
round_output([], []).
round_output([Id|Ids], [Id-P|Ps]) :- oracle_proposal(P), round_output(Ids, Ps).

% A merged map after any number of rounds is itself a round output (merge only
% fills absent slots), so quantifying over round outputs covers every reachable
% merged map.

% -- decision invariants, for one output
guardrails_ok(Msgs, Firms, Qs0, Pub) :-
    forall(member(Id-answer, Pub),
           ( member(m(Id, Dom, _, _, Reply, _, _), Msgs), memberchk(Dom, Firms),
             ( memberchk(Reply, Qs0) ; memberchk(Reply-question, Pub) ) )),
    forall(member(Id-standing_order, Pub), member(m(Id, _, _, true, _, _, _), Msgs)),
    forall(member(Id-_, Pub), member(m(Id, _, false, _, _, _, _), Msgs)),
    forall(( member(m(Id, _, _, _, _, question, _), Msgs), member(Id-C, Pub) ), C == question),
    forall(( member(Id-C1, Pub), member(Id-C2, Pub) ), C1 == C2),
    forall(member(Id-C, Pub), ( member(M, Msgs), msg_id(M, Id), in_scope(M, C) )).

determined_ok(Msgs, Firms, Qs0, Pub, Held) :-
    forall(member(P, Pub), admissible(Msgs, Firms, Qs0, P)),
    maplist(msg_id, Msgs, Ids),
    pairs_keys(Pub, PubIds), append(PubIds, Held, Decided),
    msort(Decided, DS), msort(Ids, IS), DS == IS,          % every id exactly once
    forall(member(Id, PubIds), \+ memberchk(Id, Held)).

% -- witnesses: every actor in the universe, every held message, every category
check_witnesses(Checked) :-
    aggregate_all(count,
        ( actor_local(L), actor_domain(D), actor_net(N), actor_os(O), Actor = actor(L, D, N, O),
          test(_, _, Firms, Qs0, Msgs), member(M, Msgs), category(Cat),
          human_confirm(Actor, M, Cat, Firms, Qs0, Out),
          ( Out = published(C1)
          -> is_witness(Actor, _),                           % only witnesses ever publish
             msg_id(M, Id), admissible(Msgs, Firms, Qs0, Id-C1),
             ( M = m(_, _, _, _, _, question, _) -> C1 == question ; true )
          ;  Out == refused ) ),
        Checked),
    aggregate_all(count, ( actor_local(_), actor_domain(_), actor_net(_), actor_os(_),
                           test(_, _, _, _, Msgs), member(_, Msgs), category(_) ), Total),
    Checked == Total.

check_decisions(TestId, Count) :-
    test(TestId, _, Firms, Qs0, Msgs),
    maplist(msg_id, Msgs, Ids),
    aggregate_all(count,
        ( round_output(Ids, Props),
          decide(Msgs, Props, Firms, Qs0, Pub, Held),
          ( guardrails_ok(Msgs, Firms, Qs0, Pub), determined_ok(Msgs, Firms, Qs0, Pub, Held)
          -> true
          ;  format("  VIOLATION test ~w output ~w -> ~w / ~w~n", [TestId, Props, Pub, Held]), fail ) ),
        Count),
    aggregate_all(count, round_output(Ids, _), Total),
    Count == Total.

% -- the clock, over every timing. State of one run of the orchestration loop:
%    s(Phase, Now, RoundStart, LastProgress, Round, AgentIdx, CallStart, Deadline, Answered, Missing)
%    Answered: whether this round's call answered; Missing: number of ids still unanswered.
%    The oracle's content is abstracted to "answered something new / nothing new";
%    Decide does not read the clock, so this is exact for the clock properties.
step(s(idle, Now, RS, _, R, I, CS, D, A, Miss), s(loaded, Now, RS, Now, R, I, CS, D, A, Miss)).
step(s(loaded, Now, _, LP, R, _, _, _, _, Miss), s(calling, Now, Now, LP, R, 1, Now, D, no, Miss)) :-
    agents([A1|_]), call_budget(A1, B), window(W), D is Now + min(B, W).
% answer at any cycle within the deadline
step(s(calling, Now, RS, LP, R, I, CS, D, _, Miss), s(merging, T, RS, LP, R, I, CS, D, yes(New), Miss)) :-
    between(Now, D, T), member(New, [0, 1, Miss]), New =< Miss.
% budget exhausted: next agent with what is left of the window, or give up
step(s(calling, _, RS, LP, R, I, _, D, _, Miss), Next) :-
    window(W), Left is max(0, RS + W - D), agents(As), length(As, N),
    ( I < N, Left > 0
    -> I1 is I + 1, nth1(I1, As, A), call_budget(A, B), D1 is D + min(B, Left),
       Next = s(calling, D, RS, LP, R, I1, D, D1, no, Miss)
    ;  Next = s(merging, D, RS, LP, R, I, D, D, no, Miss) ).
step(s(merging, Now, RS, LP, R, I, CS, D, Ans, Miss), s(Phase, Now, RS, LP1, R1, I, CS, D, Ans, Miss1)) :-
    ( Ans = yes(New) -> Miss1 is Miss - New ; Miss1 = Miss, New = 0 ),
    ( New > 0 -> LP1 = Now ; LP1 = LP ),
    R1 is R + 1, idle_limit(Idle), max_rounds(MR),
    (   Miss1 =:= 0            -> Phase = done
    ;   Ans == no              -> Phase = done
    ;   New =:= 0, Now - LP1 >= Idle -> Phase = done
    ;   R1 >= MR               -> Phase = done
    ;   Phase = loaded ).

clock_ok(s(Phase, Now, RS, _, R, I, CS, D, _, _)) :-
    window(W), max_rounds(MR), max_call(Max),
    R =< MR,
    Now =< MR * W + 1,
    ( Phase == calling -> D - CS =< Max, agents(As), nth1(I, As, A), agent(A, Want), D - CS =< Want ; true ),
    ( memberchk(Phase, [calling, merging]) -> Now =< RS + W, D =< RS + W ; true ).

% exhaustive reachability from the initial state, checking clock_ok on every state
% and that every maximal path ends in `done` (termination).
check_clock(NMsgs, Visited) :-
    Init = s(idle, 0, 0, 0, 0, 1, 0, 0, no, NMsgs),
    explore([Init], [], VisitedL),
    length(VisitedL, Visited),
    forall(member(S, VisitedL), clock_ok(S)),
    forall(( member(S, VisitedL), \+ step(S, _) ), S = s(done, _, _, _, _, _, _, _, _, _)).

explore([], Seen, Seen).
explore([S|Q], Seen, Out) :-
    ( memberchk(S, Seen) -> explore(Q, Seen, Out)
    ; findall(N, step(S, N), Ns), append(Q, Ns, Q1), explore(Q1, [S|Seen], Out) ).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Part 3. Games: beliefs, strategies, payoffs, Nash equilibrium
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Atomic evidence axioms a player can question about a message.
atom_of(m(_, Dom, _, _, _, _, _), firm(true),  Firms) :- memberchk(Dom, Firms), !.
atom_of(_,                        firm(false), _).
atom_of(m(_, _, Hard, _, _, _, _), hard(Hard), _).
atom_of(m(_, _, _, Src, _, _, _),  source(Src), _).
atom_of(m(_, _, _, _, Reply, _, _), replies(R), _) :- ( Reply == none -> R = false ; R = true ).
atom_of(m(_, _, _, _, _, RC, _),   hint(RC), _).
evidence(M, Firms, Es) :- findall(E, atom_of(M, E, Firms), Es).

% Naive-Bayes decomposition: P(C | atoms) ~ prior(C) * prod_i P(atom_i | C).
prior(none, 0.30). prior(question, 0.20). prior(notice, 0.20).
prior(opportunity, 0.15). prior(standing_order, 0.10). prior(answer, 0.05).

lik(hard(true),   none, 0.95). lik(hard(true),   _, 0.01).
lik(hard(false),  none, 0.05). lik(hard(false),  _, 0.99).
lik(firm(true),   answer, 0.90). lik(firm(true),  _, 0.05).
lik(firm(false),  answer, 0.10). lik(firm(false), _, 0.95).
lik(replies(true),  answer, 0.90). lik(replies(true),  _, 0.10).
lik(replies(false), answer, 0.10). lik(replies(false), _, 0.90).
lik(source(true),  standing_order, 0.90). lik(source(true),  notice, 0.60). lik(source(true),  _, 0.30).
lik(source(false), standing_order, 0.10). lik(source(false), notice, 0.40). lik(source(false), _, 0.70).
lik(hint(H), C, 0.80) :- H == C, !.
lik(hint(none), none, 0.60) :- !.
lik(hint(_), _, 0.04).

likelihood(E, C, P) :- lik(E, C, P), !.

% Each player's network has its own sharpness: a noisier local model, a crisp API.
sharpness(local, 0.6). sharpness(claude, 1.0). sharpness(codex, 0.9). sharpness(agy, 0.8).
sharpness(agent, 0.8). sharpness(opencode, 0.7). sharpness(api, 1.0).

posterior(Player, M, Firms, C, P) :-
    evidence(M, Firms, Es), sharpness(Player, K),
    findall(C1-U, ( prior(C1, Pr), foldl(mul_lik(C1, K), Es, Pr, U) ), Us),
    aggregate_all(sum(U), member(_-U, Us), Z),
    member(C-U0, Us), P is U0 / Z.
mul_lik(C, K, E, Acc, Out) :- likelihood(E, C, L), Out is Acc * L ** K.

belief(Player, M, Firms, Best, Conf) :-
    findall(P-C, posterior(Player, M, Firms, C, P), Ps),
    max_member(PBest-Best, Ps), Conf is round(10 * PBest).

% Strategies a player may adopt for a round.
strategy(honest).       % argmax belief, calibrated confidence
strategy(inflate).      % argmax belief, confidence 10
strategy(adversarial).  % claims "answer" for everything at confidence 10
strategy(stall).        % never answers inside its budget
strategy(silent).       % answers with nothing

act(honest,      Player, M, Firms, p(C, F)) :- belief(Player, M, Firms, C, F).
act(inflate,     Player, M, Firms, p(C, 10)) :- belief(Player, M, Firms, C, _).
act(adversarial, _, _, _, p(answer, 10)).
act(silent,      _, _, _, absent).

% One round of the chain: the first player that does not stall answers.
play_round(Profile, Msgs, Firms, Owner, Props) :-
    agents(As),
    member(Owner, As), memberchk(Owner-S, Profile), S \== stall, !,
    findall(Id-P, ( member(M, Msgs), msg_id(M, Id), act(S, Owner, M, Firms, P) ), Props).
play_round(_, _, _, none, []).

% Payoffs. The owner of the round is paid +1 for each proposal the laws accept as
% proposed (ownership of the task), -1 for each claim at or above the confidence
% floor that the laws override or hold (a misleading claim), and -1 per cycle it
% held the orchestration (stalling costs its budget). Everyone else gets 0.
payoff(Profile, TestId, Player, Pay) :-
    test(TestId, _, Firms, Qs0, Msgs),
    play_round(Profile, Msgs, Firms, Owner, Props),
    decide(Msgs, Props, Firms, Qs0, Pub, _),
    memberchk(Player-S, Profile),
    (   S == stall -> call_budget(Player, B), Pay is -B
    ;   Player \== Owner -> Pay = 0
    ;   aggregate_all(sum(V), proposal_value(Props, Pub, V), Pay) ).

proposal_value(Props, Pub, V) :-
    member(Id-p(C, F), Props), min_conf(Min), F >= Min, category(C),
    ( memberchk(Id-C, Pub) -> V = 1 ; V = -1 ).

welfare(Profile, TestId, W) :-
    agents(As), aggregate_all(sum(P), ( member(A, As), payoff(Profile, TestId, A, P) ), W).

profile(Profile) :- agents(As), maplist([A, A-S]>>strategy(S), As, Profile).

% Nash: no player can strictly improve by deviating alone, in any test on the timeline.
deviation(Profile, Player, S, Dev) :-
    strategy(S), memberchk(Player-S0, Profile), S \== S0,
    maplist([A-X, A-Y]>>( A == Player -> Y = S ; Y = X ), Profile, Dev).
nash(Profile) :-
    agents(As),
    forall(( member(P, As), deviation(Profile, P, _, Dev), test(T, _, _, _, _) ),
           ( payoff(Profile, T, P, V), payoff(Dev, T, P, V1), V1 =< V )).

honest_profile(Pr) :- agents(As), maplist([A, A-honest]>>true, As, Pr).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Runner
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

run_all :-
    format("Meseeks universe~n"),
    forall(law(L), ( in_force(L) -> format("  law in force : ~w~n", [L]) ; format("  law NOT in force: ~w~n", [L]) )),
    window(W), sum_budgets(S), format("  window = ~w cycles (130%% of ~w summed budgets)~n", [W, S]),
    forall(test(T, Title, _, _, _), format("  test ~w: ~w~n", [T, Title])),
    format("~nPart 2a. decisions: every oracle output of every test~n"),
    forall(test(T, _, _, _, _),
           ( check_decisions(T, N) -> format("  test ~w: ~w outputs, Guardrails + Determined hold~n", [T, N])
           ; format("  test ~w: FAILED~n", [T]), halt(1) )),
    format("Part 2b. clock: every timing of every sub-agent call, every round~n"),
    forall(member(N, [2, 3]),
           ( check_clock(N, V) -> format("  ~w messages: ~w reachable states, Clock holds, every path terminates~n", [N, V])
           ; format("  ~w messages: FAILED~n", [N]), halt(1) )),
    format("Part 2c. witnesses: every actor x every message x every category~n"),
    ( check_witnesses(NW) -> format("  ~w human decisions: only witnesses publish, always within Admissible~n", [NW])
    ; format("  witnesses: FAILED~n"), halt(1) ),
    format("Part 3. games: ~w strategy profiles over the timeline~n", [78125]),
    honest_profile(H),
    forall(test(T, _, _, _, _),
           ( welfare(H, T, WH), format("  test ~w: all-honest welfare ~w~n", [T, WH]) )),
    ( nash(H) -> format("  all-honest is a Nash equilibrium~n") ; format("  all-honest is NOT a Nash equilibrium~n"), halt(1) ),
    ( forall(( profile(P), test(T, _, _, _, _) ), ( welfare(P, T, WP), welfare(H, T, WH), WP =< WH ))
    -> format("  all-honest maximises welfare in every test (mutually beneficial)~n")
    ;  format("  a profile beats all-honest on welfare~n"), halt(1) ),
    ( forall(( agents(As), member(A, As), test(T, _, _, _, _) ),
             ( payoff(H, T, A, V), deviation(H, A, silent, Dev), payoff(Dev, T, A, V0), V >= V0 ))
    -> format("  every player prefers honest to its outside option, silent (individually acceptable)~n")
    ;  format("  a player prefers silence~n"), halt(1) ),
    aggregate_all(count, ( profile(P), forall(test(T, _, _, _, _), ( welfare(P, T, WP), welfare(H, T, WH), WP =:= WH )) ), Opt),
    format("  profiles that tie all-honest on welfare in every test: ~w~n", [Opt]),
    format("~nUniverse check passed.~n").
