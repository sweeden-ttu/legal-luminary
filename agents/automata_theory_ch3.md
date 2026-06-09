3
Automata
3.1
Deterministic and nondeterministic automata
An automaton is a device which recognizes or accepts certain elements of ∗,
where  is a ﬁnite alphabet. Since the elements accepted by the automaton are
a subset of ∗, they form a language. Therefore each automaton will recognize
or accept a language contained in ∗. The language of ∗consisting of the
words accepted by an automaton M is the language over ∗accepted by M
and denoted M(L). We will be interested in the types of language an automaton
accepts.
Deﬁnition 3.1
A deterministic automaton, denoted by (, Q, s0, ϒ, F), con-
sists of a ﬁnite alphabet , a ﬁnite set Q of states, and a function ϒ : Q ×  →
Q, called the transition function and a set F of acceptance states. The set Q
contains an element s0 and a subset F, the set of acceptance states.
The input of ϒ is a letter of  and a state belonging to Q. The output is a
state of Q (possibly the same one). If the automaton is in state s and “reads”
the letter a, then (s, a) is the input for ϒ and ϒ(s, a) is the next state. Given a
string in ∗the automaton “reads” the string or word as follows. Beginning at
the initial state s0, and beginning with the ﬁrst letter in the string (if the string is
nonempty), it reads the ﬁrst letter of the string. If the ﬁrst letter is the letter a of
, then it “moves” to state s = ϒ(s0, a). The automaton next “reads” the second
letter of the string, say b, and then moves to state s′ = ϒ(s, b). Therefore, as the
automaton continues to “read” a string of letters from the alphabet it “moves”
from one state to another. Eventually the automaton “reads” every letter in the
string and then stops. If the state the automaton is in after reading the last letter
belongs to the set of acceptance states, then the automaton accepts the string.
Let M be the automaton with alphabet  = {a, b}, set of states Q = {s0, s1, s2},
37


38
Automata
and ϒ deﬁned by the table
ϒ
s0
s1
s2
a
s1
s2
s2
b
s0
s0
s1
Suppose M “reads” the string aba. Since the automaton begins in state s0, and
the letter read is a, and ϒ(s0, a) = s1, the automaton is now in state s1. The
next letter read is b and ϒ(s1, b) = s0. Finally the last letter a is read and, since
ϒ(s0, a) = s1, the automaton remains in state s1. We may also state ϒ as a set
of rules as follows:
If in state s0 and a is read go to state s1.
If in state s1 and a is read go to state s2.
If in state s2 and a is read go to state s2.
If in state s0 and b is read go to state s0.
If in state s1 and b is read go to state s0.
If in state s2 and b is read go to state s1.
Let s0 and s2 be the acceptance states.
This deterministic automaton is best shown pictorially by a state diagram
which is a directed graph where the states are represented by the vertices and
each edge from s to s′ is labeled with a letter, say a, of the alphabet  if
ϒ(s, a) = s′. A directed arrow from s to s′ labeled with the letter a will be
called an a-arrow from s to s′. If s is a starting state, then its vertex is denoted
by the diagram
s
If s is an acceptance state, its vertex is denoted by the diagram
s
Therefore the deterministic automaton above may be represented pictorially
as seen in Fig. 3.1. More speciﬁcally, an automaton “reads” a word or string
a0a1a2 . . . an of ∗by ﬁrst reading a0, then reading a1 and continuing until it
has read an. If an automaton is in state s1 and reads the word w and is then
in s2, then w is a path from s1 to s2. A deterministic automaton accepts or
recognizes a0a1a2 . . . an if after beginning with a0 in state s0 and continuing
until reading an, the automaton stops in an acceptance state. Thus the automaton


3.1 Deterministic and nondeterministic automata
39
s1
s0
s2
a
b
b
a
b
a
Figure 3.1
above would not accept aba since s1 is not an acceptance state. It would however
accept bbaaa and bab, since s0 and s2 are acceptance states.
The automaton with the state diagram
s0
s1
s3
s4
s2
a
a
a
a
a
b
b
b
b
b
has initial state s0 and acceptance state s3. It accepts the word aba since after
reading a, it is in state s1. After reading b, it is still in state s1. After reading
the second a, it is in state s3, which is an acceptance state. One can see that
it also accepts abbba and bb, so they are in the language accepted by the
given automaton. However bbb, abab, and abb are not. Notice that any string
beginning with two as or two bs is accepted only if the string is not extended.
Also, if three as occur in the string, the string is not accepted. The state s4 is an
example of a sink state. Once the automaton is in the sink state, it can never
leave this state again, regardless of the letter read.
Since ϒ is a function, a deterministic automaton can always read the entire
string. We shall later deﬁne a nondeterministic automaton which may not always
be able to read the entire string. In such a case the word cannot be accepted.
Example 3.1
Consider the automaton with state diagram
s1
a
b
b
s0
s2
s3
b
a
a
a
b
having  = {a, b}, starting state s0, and acceptance states s0, s1, and s2. It
obviously accepts the word bb. In each state, there is a loop for a so that


40
Automata
if a is read then the state does not change. This enables us to read as many
as as desired without changing states, before reading another b. Thus the
automaton reads aababaaa, baabab, baaab, babaaa, aabaabaa, and in fact
we can read any word in the language described by the regular expression
(a∗ba∗ba∗) ∨(a∗ba∗) ∨a∗. This language can also be described as the set of all
words containing at most two bs. Notice that s3 is a sink state.
Example 3.2
Consider the automaton with state diagram
s0
s1
s2
s3
a
a
a
b
b
b
c
c
c
which we simplify as
s0
s2
s1
s3
a
a
a,b,c
a,b,c
b,c
b,c
to decrease the number of arrows. This automaton obviously accepts only
the words ab and ac. This language may be described by the regular expres-
sion a(b ∨c). Notice that the sink state s2 eliminates all other words from the
language.
Example 3.3
Consider the automaton with state diagram
b
c
a
b
a,b,c
a,b,c
a,c
c
a,b
s0
s1
s3
s4
s2
The only words accepted are b and abc. Therefore the expression for the lan-
guage accepted is b ∨abc.


3.1 Deterministic and nondeterministic automata
41
Example 3.4
Consider the automaton with state diagram
a
a
a
b
b
b
a,b
s0
s1
s2
s3
In this automaton, if three consecutive bs are read, then the automaton is in state
s3, which is a sink state and is not an acceptance state. This is the only way to
get to s3 and every other state is an acceptance state. Thus the language accepted
by this automaton consists of all words which do not have three consecutive bs.
An expression for this language is
(a ∨(ba) ∨(bba))∗(λ ∨b ∨(bb)).
As previously mentioned, the automata that we have been discussing are
called deterministic automata since in every state and for every value of the
alphabet that is read, there is one and only one state in which the automata can
be. In other words, ϒ : Q ×  →Q is a function. It is often convenient to relax
the rules so that ϒ is no longer a function, but a relation. If we again consider
ϒ as a set of rules, given a ∈ and s ∈Q, the rules may allow advancement
to each of several states or there may not be a rule which does not allow it to
go to any state after reading a in state s. In the latter case, the automaton is
“hung up” and can proceed no further. This cannot occur with a deterministic
automaton.
Although the deﬁnition of a nondeterministic automaton varies, we shall use
the following deﬁnition:
Deﬁnition 3.2
A nondeterministic automaton, denoted by
(, Q, s0, ϒ, F)
consists of a ﬁnite alphabet , a ﬁnite set Q of states, and a function
ϒ : Q ×  →P(Q)
called the transition function. The set Q contains an element s0 and a subset
F containing one or more acceptance states. (Note that P(Q) is the power set
of Q.)
Thus given a ∈ and s ∈Q, there may be a-arrows from s to several dif-
ferent states or to no state at all. By deﬁnition, a deterministic automaton is also


42
Automata
considered to be a nondeterministic automaton. A nondeterministic automaton
often simpliﬁes the state diagram and eliminates the need for a sink state. In
Example 3.2, the state diagram can be simpliﬁed to
s2
s1
s0
a
b,c
Note that in reading aa, after reading the ﬁrst a, the automaton is in state s3,
and when the second a is read the automaton “hangs up”, since there is no a
arrow out of state s3.
Example 3.5
The deterministic automaton represented by
s0
s1
s3
s4
s2
a
a
a
a
a
b
b
b
b
b
can be simpliﬁed using a nondeterministic automaton by simply eliminating
state s4 and all arrows into or out of this state.
Example 3.6
It is easily seen that the automaton with state diagram
s0
s1
s2
a
c
b
accepts the language with regular expression ab∗c.
Example 3.7
The automaton with state diagram
s1
s0
a,b
accepts the language with regular expression a ∨b.


3.1 Deterministic and nondeterministic automata
43
Example 3.8
The automaton with state diagram
s2
s1
s0
a
a
b
b
accepts the language with regular expression aa∗bb∗.
Example 3.9
The automaton with state diagram
s2
s1
s0
a,b
a,b
a,b
a
a
accepts the language consisting of strings with at least two as and so may be
written as (a ∨b)∗a(a ∨b)∗a(a ∨b)∗.
Obviously any language accepted by a deterministic automaton is accepted
by a nondeterministic automaton since the set of deterministic automata is a
subset of the set of nondeterministic automata. In the following theorem, how-
ever, we shall see that any language accepted by a nondeterministic automaton
is also accepted by a deterministic automaton.
Theorem 3.1
For each nondeterministic automaton, there is an equivalent
deterministic automaton that accepts the same language.
We demonstrate how to construct a deterministic automaton which accepts
the language accepted by a nondeterministic automaton. We shall later give a
formal proof that a language is accepted by a deterministic automaton if and
only if it is accepted by a nondeterministic automaton. If Q is the set of states
for the nondeterministic automaton, we shall use elements of P(Q), i.e. the
set of subsets of Q, as states for the deterministic automaton which we are
constructing. Some of these states may not be used since they do not occur
on any path which leads to acceptance state. Hence they could be removed
and greatly simplify the deterministic automaton created. However, for our
purpose, we are only interested in showing that a deterministic automaton can be
created.


44
Automata
In general we have the following procedure for constructing a deterministic
automaton
M = (, Q′, {s0}, ϒ′, F′)
from a nondeterministic automaton.
N = (, Q, s0, ϒ, F).
(1) Begin with the state {s0} where s0 is the start state of the nondeterministic
automaton.
(2) For each ai ∈, construct an ai arrow from {s0} to the set consisting of all
states such that there is an ai-arrow from s0 to that state.
(3) For each newly constructed set of states s j and for each ai ∈ construct
an ai arrow from s j to the set consisting of all states such that there is an ai
arrow from an element of s j to that state.
(4) Continue this process until no new states are created.
(5) Make each set of states s j, that contains an element of the acceptance set
of the nondeterministic automaton, into an acceptance state.
Example 3.10
Consider the nondeterministic automaton N
s2
s1
s0
b
b
a
a
Construct an a-arrow from {s0} to the set of all states so that there is an a-arrow
from s0 to that state. Since there is an a-arrow from s0 to s0 and an a-arrow from
s0 to s1, we construct an a-arrow from {s0} to {s0, s1}. There is no b-arrow from
s0 to any state. Hence the set of all states such that there is a b-arrow to one of
these states is empty and we construct a b-arrow from {s0} to the empty set ∅.
We now consider the state {s0, s1}. We construct an a-arrow from {s0, s1} to the
set of all states such that there is an a-arrow from either s0 or s1 to that state.
Thus we construct an a-arrow from {s0, s1} to itself. We construct a b-arrow
from {s0, s1} to the set of all states such that there is a b-arrow from either s0
or s1 to that state. Thus construct a b-arrow from {s0, s1} to {s2}. Since there
are no a-arrows or b-arrows from any state in the empty set to any other state,
we construct an a-arrow and a b-arrow from the empty set to itself. Consider
{s2}. Since there is no a-arrow from s2 to any other state, we construct an a-
arrow from {s2} to the empty set. Since the only b-arrow from s2 is to itself, we
construct a b-arrow from {s2} to itself. The acceptance states consist of all sets


3.1 Deterministic and nondeterministic automata
45
which contain an element of the terminal set of N. In this case {s2} is the only
acceptance state. We have now completed the state diagram
{s0 ,s1}
b
a
b
Ø
a
a
b
a
b
{s0}
{s2}
which is easily seen to be the state diagram of a deterministic automaton. This
automaton also reads the same language as N, namely the language described
by the expression aa∗bb∗.
Example 3.11
Given the nondeterministic automaton
s2
s1
s0
s3
b
b
a
a
a
a
using the same method as above we complete the deterministic automaton
{s0 ,s2}
a,b
a
b
b
b
b
a
a
a
{s0}
{s1}
{s3}
{s1 ,s3}
Ø
At this point we introduce a new notation. The ordered pair (si, w) indicates
that the automaton is in state si and still has input w left to read. For example,


46
Automata
(s2, abbb) indicates that the automaton is in state s2 and must still read abbb.
Assume that we have (si, aw) w ∈+. Thus the automaton is in state si and
must still read a followed by w. The notation (si, aw) ⊢(s j, w) means that the
automaton has read a and moved from state si to state s j. Therefore ϒ(si, a) =
s j. In the automaton
a
a
a
b
b
b
a,b
s0
s1
s2
s3
we have (s2, bab) ⊢(s3, ab). We also have
(s0, babba) ⊢(s1, abba) ⊢(s0, bba) ⊢(s1, ba) ⊢(s2, a) ⊢(s0, λ).
If we have (si, wi) ⊢(s j, w j) ⊢· · · ⊢(sm, wm), we denote this by (si, wi) ⊢∗
(sm, wm). We also let (s, w) ⊢∗(s, w). Thus a word w is accepted by an automa-
ton if and only if (s0, w) ⊢∗(s, λ) where s is an acceptance state. In our example
(s0, bababb) ⊢∗(s0, λ), so bababb is accepted by the automaton.
We shall now prove that a language is accepted by a deterministic automa-
ton if and only if it is accepted by a nondeterministic automaton. We begin
with two lemmas. The ﬁrst is obvious since every deterministic automaton is a
nondeterministic automaton.
Lemma 3.1
Every language accepted by a deterministic automaton is
accepted by a nondeterministic automaton.
Lemma 3.2
Let N = (, Q, s0, ϒ, F) be a nondeterministic automaton and
M = (, Q′, {s0}, ϒ′, F′)bethedeterministicautomatonderivedfrom N using
the above process. Then (s0, w) ⊢∗(s, λ) in N if and only if there exists X such
that ({s0}, w) ⊢∗(X, λ) in M where s ∈X.
Proof
We ﬁrst show that if (s0, w) ⊢∗(s, λ) in N, then ({s0}, w) ⊢∗(X, λ)
where s ∈X. The proof uses induction on the length n of w. If n = 0, we
have (s0, λ) ⊢∗(s0, λ) in N, ({s0}, λ) ⊢∗({s0}, λ) in M, and s0 ∈{s0}, so the
statement is true if n = 0. Assume w = va ∈+ has length k + 1, so v has
lengthn.Since(s0, va) ⊢∗(s, λ),then(s0, va) ⊢∗(t, a) ⊢(s, λ)forsomet ∈Q
and (s0, v) ⊢∗(t, λ). Therefore by induction, there exist Y so that t ∈Y and
({s0}, v) ⊢∗(Y, λ).Sincet ∈Y and(t, a) ⊢(s, λ)in N,(Y, a) ⊢(X, λ)forsome
X where s ∈X. Therefore ({s0}, va) ⊢∗(Y, a) ⊢(X, λ) or ({s0}, va) ⊢∗(X, λ)
where s ∈X.


3.1 Deterministic and nondeterministic automata
47
Conversely, we show that if ({s0}, w) ⊢∗(X, λ) in M, then (s0, w) ⊢∗(s, λ)
in N where s ∈X. We again use induction on n, the length of the word w.
Assume there exists X such that ({s0}, w) ⊢∗(X, λ) in M where s ∈X. If
n = 0, we have ({s0}, λ) ⊢∗({s0}, λ) in M, (s0, λ) ⊢∗(s0, λ) in N, and s0 ∈{s0},
so the statement is true if n = 0. Given ({s0}, va) with length k + 1, so v has
length n. Assume ({s0}, va) ⊢∗(Y, a) ⊢(X, λ). Therefore ({s0}, v) ⊢∗(Y, λ).
Byinduction,(s0, v) ⊢∗(t, λ)forallt inY andhence(s0, va) ⊢∗(t, a)forallt in
Y. By deﬁnition, since (Y, a) ⊢(X, λ) and (t, a) ⊢(s, λ),then (s0, w) ⊢∗(s, λ)
in N for s ∈X.
□
We are now able to prove the desired Theorem 3.1.
Theorem 3.2
A language is accepted by a deterministic automaton if and
only if it is accepted by a nondeterministic automaton.
Proof
To show this we need only show that a word is accepted by a non-
deterministic automaton if and only if it is accepted by the corresponding
deterministic automaton. If (s0, w) ⊢∗(s, λ) where s is an acceptance state
in the nondeterministic automaton, then ({s0}, w) ⊢∗(X, λ) where X contains
an acceptance state. Hence X is an acceptance state. Assume X is an accep-
tance state, then it contains an acceptance state r from the nondeterministic
automaton. But by the previous lemma, if ({s0}, w) ⊢∗(X, λ) and r ∈X then
(s0, w) ⊢∗(r, λ). Therefore r is an acceptance state.
□
At this point we shall deﬁne an extended nondeterministic automaton and
prove that a language is accepted by an extended nondeterministic automaton
if and only if it is accepted by a nondeterministic automaton (and hence a
deterministic automaton).
Using a nondeterministic automaton, we can extend the automaton so that
(+, Q, s0, ϒ, F) consists of +, a ﬁnite set Q of states, and a function
ϒ : + × Q →P(Q), called the transition function. Thus ϒ reads words
instead of letters. This can be changed back to reading letters by adding new
nonterminal states. If ϒ reads the word w = a1a2 · · · ak, and moves from state
s to state s′, add states σ2σ3 · · · σk, and let ϒ(s, a1) = σ2, ϒ(σ2, a2) = σ3,
ϒ(σ3, a3) = σ4, . . . , ϒ(σk−1, ak−1) = σk, and ϒ(σk, ak) = s′. This forms a
nondeterministic automata, but we can form a deterministic automata with
the same language as shown above.
If we allow the automaton to pass from one state si to another state s j without
reading a letter of the alphabet, this may be shown as the automaton having an
edge from si to s j with label λ. Thus paths may contain one or more λ′s. Such
an automaton is said to have λ-moves. We can then have an automaton with the
form (∗, Q, s0, ϒ, F).


48
Automata
Formally a ﬁnite automaton M = (, Q, s0, ϒ, F) with λ-moves has the
property that ϒ maps Q ∪{λ} to Q. We wish to create a deterministic automata
M′ = (, Q′, s′
0, ϒ′, F′) containing no λ-moves with the same language. Thus
M(L) = M′(L). Given a letter q in , deﬁne E(q) to be all the states that
are reachable from q without reading a letter in the alphabet. Thus E(q) =
{p : (q, w) ⊢(p, w). In our construction, the set of states of M′ is a subset of
P(Q). The state s′
0 = E(s0), and F′ is a set containing an element of F. For
each element a of , deﬁne ϒ′ by ϒ′(P, a) = 
p∈P E(ϒ(p, a)).
We ﬁrst show that M′ is deterministic. It is certainly single valued. Further
ϒ′(P, a) will always have a value even if it is the empty set.
We must now show that M(L) = M′(L). To do this we show that for any
states p and q in Q, and any word w in ∗
(p, w) ⊢∗(q, λ) in M if and only if (E(p), w) ⊢∗(P, λ) in M′
for some P containing q. From this it will follow that
(s0, w) ⊢∗( f, λ) in M if and only if (E(s0), w) ⊢∗(P, λ) in M′
for some P containing f , where f ∈F.
We prove this using induction of the length of w. If |w| = 0, then w = λ,
and it must be shown that
(p, λ) ⊢∗(q, λ) in M if and only if (E(p), λ) ⊢∗(P, λ) in M′
for some P containing q. Now (p, λ) ⊢∗(q, λ) if and only if q ∈E(p);
but since M′ is deterministic and no letter is read, then P = E(p) and
p ∈E(p). Therefore the statement is true if |w| = 0.
Assume the statement is true for all strings having nonnegative length k. We
now have to prove the statement is true for any string w with length k + 1.
⇒: Assume w = va for some letter a and w and (p, w) ⊢∗(q, λ) so that
(p, va) ⊢∗(q1, a) ⊢(q2, λ) ⊢∗(q, λ)
where at the end, possibly no letters of the alphabet are read. Since (p, va) ⊢∗
(q1, a) then (p, v) ⊢∗(q1, λ) and, by induction, (E(p), v) ⊢∗(R, λ) for some R
containing q1. But since (q1, a) ⊢(q2, λ), by construction, E(q2) ⊆ϒ′(R, a),
and since (q2, λ) ⊢∗(q, λ), q ∈E(q2) by deﬁnition of E, and hence q ∈
ϒ′(R, a). Therefore (R, a) ⊢((P, λ) for some P containing q by deﬁnition
of ϒ′ and (E(p), va) ⊢∗(R, a) ⊢((P, λ) for some P containing q.
In M′, assume (E(p, va)) ⊢∗(R, a) ⊢(P, λ) where q ∈P and ϒ′(R, a) =
P. By deﬁnition ϒ′(R, a) = 
r∈R E(ϒ(r, a)). There exists some state r ∈R
such that ϒ(r, a) = s and q ∈E(s). Therefore (s, λ) ⊢∗(q, λ) by deﬁnition


3.1 Deterministic and nondeterministic automata
49
of E(s). By the induction hypotheses (p, v) ⊢∗(r, λ). Therefore (p, va) ⊢∗
(r, a) ⊢(s, λ) ⊢∗(q, λ).
Example 3.12
Given the automaton (M = (, Q, s0, ϒ, F)
s1
s0
b
a
c
b
c
s3
a
l
l
l
s2
which has λ-moves, we construct M′ = (, Q′, s′
0, ϒ′, F′) containing no
λ-moves: E(s0) = {s0, s1, s2}, E(s1) = {s1, s2}, E(s2) = {s2}, and E(s3) =
{s0, s1, s2, s3}. Denote these sets by s′
0, s′
1, s′
2, and s′
3 respectively. Then ϒ′
is given by the following table
a
b
c
s′
0
s′
3
s′
1
s′
2
s′
1
∅
s′
1
s′
2
s′
2
∅
∅
s′
2
s′
