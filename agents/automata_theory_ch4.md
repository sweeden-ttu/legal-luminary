4
1
3
1
4
4

and b =
0
1
2
3
4
2
1
3
4
4

.
By deﬁnition let ¯λ =
0
1
2
3
4
0
1
2
3
4

. Let
γ = ¯ab
=
 0
1
2
3
4
1
3
4
4
4

δ = ¯a ¯a
=
0
1
2
3
4
3
4
3
4
4

ε = ¯b¯b
=
0
1
2
3
4
3
1
4
4
4

ζ = b¯a
=
0
1
2
3
4
1
4
1
4
4

η = ¯a ¯ab =
0
1
2
3
4
3
4
4
4
4

θ = b¯ab
=
0
1
2
3
4
1
4
4
4
4

ϑ = ¯ab¯a =
0
1
2
3
4
3
4
3
4
4

ι = ¯a¯b¯b
=
0
1
2
3
4
4
3
4
4
4

κ = ¯b¯b¯b =
0
1
2
3
4
4
1
4
4
4

μ = abab =
0
1
2
3
4
3
4
4
4
4

.


3.3 MDAs and syntactic monoids
81
The table for the transformation monoid TM is seen to be
λ
¯a
b
γ
δ
ε
ζ
η
θ
ϑ
ι
κ
μ
λ
λ
¯a
b
γ
δ
ε
ζ
η
θ
ϑ
ι
κ
μ
¯a
¯a
δ
γ
η
η
ι
ϑ
η
μ
η
η
ι
η
b
b
ζ
ε
θ
η
κ
ζ
η
θ
η
η
κ
η
γ
γ
μ
ι
μ
η
ι
δ
η
μ
η
η
ι
η
δ
δ
η
η
η
η
η
η
η
η
η
η
η
η
ε
ε
ζ
κ
θ
η
κ
ζ
η
θ
η
η
κ
η
ζ
ζ
θ
θ
η
η
η
κ
η
η
η
η
η
η
η
η
η
η
η
η
η
η
η
η
η
η
η
η
θ
θ
η
η
η
η
η
η
η
η
η
η
η
η
ϑ
ϑ
η
μ
η
η
η
η
η
η
η
η
η
η
ι
ι
ϑ
ι
μ
η
ι
ϑ
η
μ
η
η
ι
η
κ
κ
ζ
κ
κ
η
κ
ζ
η
θ
η
η
κ
η
μ
μ
η
η
η
η
η
η
η
η
η
η
η
η
Theorem 3.6
Let M(, Q, s0, ϒ, F) be a minimal deterministic automaton
and TM be the transformation monoid for M, then TM is ﬁnite.
Proof
Each element of TM is a function from Q to Q. If Q contains n elements,
then there are nn possible functions from Q to Q. Therefore the order of M is
less than or equal to nn.
□
Theorem 3.7
The syntactic monoid of a regular language L is isomorphic
to the transformation monoid of the minimal deterministic automaton M that
accepts L.
Proof
Since, by the discussion following Deﬁnition 3.6, the syntactic monoid
can be considered to be the transformation monoid of the intrinsic minimal
deterministicautomaton,andallminimaldeterministicautomataareisomorphic
to the intrinstic minimal deterministic automaton, the transformation monoid
is isomorphic to the syntactic monoid.
□
We now examine some of the properties of the syntactic monoid of a lan-
guage. Unlike the transformation monoid, as mentioned above, the syntactic
monoid of a language also exists for languages that are not regular.
Deﬁnition 3.7
Let φ be a homomorphism from ∗to a monoid . A set
L ⊆∗is recognized by  if φ−1φ(L) = L.
Theorem 3.8
Let L ⊆∗. The following conditions are equivalent.
(i) L is a regular language.
(ii) The syntactic monoid Syn(L) is ﬁnite.
(iii) L is recognized by a ﬁnite monoid .


82
Automata
Proof
(i)⇒(ii) If L is a regular language, then its syntactic monoid is isomor-
phic to the transformational monoid of the minimal automaton generating L
and hence is ﬁnite.
(ii)⇒(iii) Assume φ is a homomorphism from ∗to Syn(L). If w ∈L and
φ(w) = φ(w′), then uwv ∈L if and only if uw′v ∈L for all u, v ∈∗. In
particular λwλ ∈L if and only if λw′λ ∈L. So w ∈L, if and only if w′ ∈L.
Therefore φ−1φ(L) = L. Since Syn(L) is ﬁnite, L is recognized by a ﬁnite
monoid.
(iii)⇒(i) Assume L is recognized by a ﬁnite monoid  and let φ : ∗→.
To show L is a regular language, we construct an automaton M(, Q, s0, ϒ, F)
that accepts L. Let Q = . Deﬁne ϒ :  ×  → by ϒ(a, m) = mφ(a), for
all m ∈ and a ∈. Let s0 = 1, the identity element of  and F = φ(). Then
w ∈L(M) if and only if ϒ(w, 1) ∈φ() if and only if w ∈φ−1(φ()) = L.
□
Exercises
(1) Find the minimal automaton which accepts the same language as the
automaton
s1
s0
s2
a,b
b
b
a
a
a
s3
b
(2) Find the minimal automaton which accepts the same language as the
automaton
s0
b
s3
a
s2
a
a
a
b
b
b
s1


3.3 MDAs and syntactic monoids
83
(3) Find the minimal automaton which accepts the same language as the
automaton
s1
a
s0
s2
a
b
b
a
b
s3
s4
b
a
b
a
(4) Find the minimal automaton which accepts the same language as the
automaton
s0
s1
a
s2
a
a
b
b
b
a,b
s3
(5) Find the minimal automaton which accepts the language described by
aa∗(b ∨c).
(6) Find the minimal automaton which accepts the language described by
a(b ∨c)∗bb∗.
(7) Find the minimal automaton which accepts the language described by
(abc)∗(b ∨c).
(8) Find the minimal automaton which accepts the language described by
(a ∨bc)c(ab)∗.
(9) Find the syntactic monoid of the language accepted by the automaton
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


84
Automata
(10) Find the syntactic monoid of the language accepted by the automaton
a
a
a
b
b
b
s0
s1
s2
(11) Find the syntactic monoid of the language accepted by the automaton
s1
a
s0
s2
a
b
b
a
b
(12) Find the syntactic monoid of the language accepted by the automaton
s2
s1
s0
a
a
b
b
(13) Find the syntactic monoid of the language accepted by the automaton
s1
a
s0
s3
a
b
b
a
b
s2
s4
b
3.4
Pumping Lemma for regular languages
We now show that certain languages are not regular languages. To do so we
ﬁrst prove a lemma known as the Pumping Lemma.
Lemma 3.5 (Pumping Lemma)
Let L be an inﬁnite regular language. There
exists a constant n such that if z ∈L and |z| > n, then there exists u, v, w ∈∗,
v ̸= λ such that z = uvw and uvkw ∈L for all k ≥0. The length of the string
uw is less than or equal to n. Further if M is an automaton accepting the
language L and M has q states, then n < q. It is possible to have the stronger
statement that z = uvw where the length of uv is less than or equal to q.
Proof
Let L be accepted by the automaton M = (, Q, s0, ϒ, F). Let
ϒ(si, ai) = si+1 for i = r to t; denote this by
(s1, ara2a3 . . . at) ⊢∗(st+1, λ).


3.4 Pumping Lemma for regular languages
85
Since L contains a word of length m, where m > q, say w = a1a2a3 . . . am.
Note that if (s1, a1a2a3 . . . am) ⊢∗(sm, λ), then sm is an acceptance state. Since
m > q, in reading w, M must pass through the same state twice. Therefore
(s1, a1a2a3 . . . a j−1) ⊢∗(sk, λ) and (s1, a1a2a3 . . . ak−1) ⊢∗(sk, λ) = for some
j < k and both
(s j, a ja j+1 . . . am) ⊢∗(sm, λ)
and
(s j, akak+1 . . . am) ⊢∗(sm, λ).
Thus
(s1, a1a2a3 . . . am) ⊢∗(sm, λ) and (s1, a1a2 . . . a j−1akak+1 . . . am) ⊢∗(sm, λ).
Also (s j, a ja j+2 . . . ak−1) ⊢∗s j, so in reading a ja j+2 . . . ak−1, M returns to the
same state and
(s1, a1a2 . . . a j−1(a ja j+2 . . . ak−1)nakak+1 . . . am) ⊢∗(sm, λ).
Letting u = a1a2 . . . a j−1, v = a ja j+2 . . . ak−1, and w = akak+1 . . . am, we
have uvnw ∈L for n ≥0.
Since |uw| < |uvw| = m, if |uw| > q, we can repeat this process on uv
until eventually we have u′(v′)nw′ ∈L for n ≥0 where |u′w′| < q. Let v be
the ﬁrst cycle in z produced by the same state being passed through twice when
the automaton is reading z. Then the length of uv is less than or equal to q.
Note that it is no longer true that the length of uw is less than q.
□
Using this lemma, we have the following theorem:
Theorem 3.9
The language L = {anbn : n ≥1} is not regular.
Proof
Assume L = {anbn : n ≥1} is regular. Since L is inﬁnite, there exist
strings u, v, w ∈∗, v ̸= λ such that uv∗w ⊆L. There are three possibili-
ties. First u = am−k, v = ak, and w = bm for some m. But then am−ka2kbm =
am+kbm ∈L, which is a contradiction. Second, u = am, v = bk, and w = bm−k.
Byasimilarargument,wereachacontradiction.Thirdu = am−k, v = akbr,and
w = bm−r. But then am−kakbrakbrbm−r ∈L, which is a contradiction. Hence
L is not regular.
□
Exercises
For each of the following sets, determine if the set is regular. If it is, describe the
set with a regular expression. If it is not a regular set, use the Pumping lemma
to show that it is not.
(1) {a2nbn : n ≥1}.


86
Automata
(2) {anb2nan : n ≥1}.
(3) {(ab)n : n ≥1}.
(4) {anbnan : n ≥1}.
(5) {anbm : m, n ≥1}.
(6) {ww : w ∈∗and || = 2}.
(7) {a2n : n ≥1}.
(8) {w ∈{a, b}∗: w contains an equal number of as and bs}.
(9) {w ∈{a, b}∗: w contains exactly four bs}.
(10) {wwR : w ∈{a, b}∗and the length of w is less that or equal to three}.
(11) {wwR : w ∈{a, b}∗.
(12) {wcwR : w ∈{a, b, c}∗.
(13) {w ¯w : w ∈(0, 1)∗and ¯w is the 1s complement of w}.
(14) {w ∈{a, b, c}∗: the length of w = n2 : n ≥1}.
(15) {w ∈{a, b, c}∗: the length of w ≥n for some n ≥1}.
(16) {w ∈{a, b}∗: w contains more as than bs}.
3.5
Decidability
In this section we answer the questions
(1) Is there an algorithm for determining whether the language accepted by a
ﬁnite automaton is empty?
(2) Is there an algorithm for determining whether two ﬁnite automata accept
the same language?
(3) Is there an algorithm for determining whether two regular languages are
the same?
(4) Is there an algorithm for determining whether a language accepted by an
automaton is inﬁnite?
The key to all of these questions is that they require the algorithm to be able
to provide a yes or no answer. We are not concerned with the efﬁciency of the
algorithm but only if within some ﬁnite length of time the algorithm can answer
the question. Note that if an algorithm can determine that a statement is true (or
false) within some bounded length of time, then the algorithm can determine
whether the statement is true.
We begin with a proof of the ﬁrst question although we can see that if we
can answer the second question, then we can answer the ﬁrst question. Given a
language L, as an expression, we simply determine the automaton that accepts
L and see if the language accepted is empty.


3.5 Decidability
87
Theorem 3.10
There is an algorithm for determining whether the language
M(L) accepted by a ﬁnite automaton is empty.
Proof
Let M(L) have n states. Then M(L) is empty if and only if s0 is not an
acceptance state and no string of length less than n is accepted since the shortest
string accepted by M(L) cannot enter a state twice. Since there are only a ﬁnite
number of these strings, they can be checked.
□
Theorem 3.11
There is an algorithm for determining whether two ﬁnite
automata accept the same language.
Proof
We already know that given automata M1 and M2 accepting languages
M1(L) and M2(L), respectively, we can construct automata for accepting
languages M1(L) ∩M2(L), and M1(L) ∪M2(L). Combining these construc-
tions, we can ﬁnd an automaton which accepts (M1(L) ∩M2(L)′) ∪(M2(L) ∩
M1(L)′), the symmetric difference of M1(L) and M2(L). But this set is empty if
and only if M1(L) = M2(L). Hence we use the previous theorem to determine
whether (M1(L) ∩M2(L)′) ∪(M2(L) ∩M1(L)′) is empty.
□
Theorem 3.12
There is an algorithm for determining whether two regular
languages are the same.
Proof
Given expressions for L1 and L2 , ﬁnd the automata M1 and M2 so that
L1 = M1(L) and L2 = M2(L). Now use the previous theorem to see if the two
automata accept the same language.
□
Before proving the next theorem, we need the following lemma.
Lemma 3.6
Assume that an automaton M has n states. The language L
accepted by M is inﬁnite if and only if there is a word in L whose length
is greater than n and less than 2n.
Proof
First assume L is inﬁnite. By the Pumping Lemma there exists uvmw ∈
L for all m ≥0. Further if M is an automaton accepting the language L and
M has n states, then |uw|, the length of the string uw, is less than or equal to
n. Assume that after u is read, the machine is in state s. If while reading v,
the machine returns to s, let v′ be the string that is read when the machine ﬁrst
returns to s and v′x = v. Thus if we have
(s0, uvw) ⊢∗(s, vw) ⊢∗(s, w) ⊢∗(s2, λ),
replace it with
(s0, uv′w) ⊢∗(s, v′w) ⊢∗(s, w) ⊢∗(s2, λ).


88
Automata
Thus M reads the string s0, u(v′)nw for any nonnegative integer n. If while
reading v′, a state t is repeated, remove all of the states including one of the
ts as well as the letters in v′ that were read in this cycle. Thus we are simply
removing all cycles in v′. Call this string v′′. Since reading v′′ uses no repeated
states except s, the length of v′′ is less than or equal to n. Thus the length of
uv′′w is less than or equal to 2n. If the length of uv′′w is less than or equal
to n, there exists a least integer m so that the length of u(v′′)nw is greater
than n. Since the length of v′′ is less than n, the length of u(v′′)mw is less
than 2n.
Conversely in the proof of the Pumping Lemma, we showed that if there is
a word in the language with length m greater than n, then for every positive
integer r, the word uvrw ∈L, where v is nonempty. Hence L is inﬁnite.
Theorem 3.13
There is an algorithm for determining whether a language
accepted by an automaton is inﬁnite.
Proof
Let M have n states. Then M(L) is inﬁnite if and only if M accepts a
string s with n ≤|s| ≤2n. Since there are only a ﬁnite number of such words,
check each of them to see if they are accepted by the automata.
Theorem 3.14
There is an algorithm for determining whether a language is
ﬁnite.
Proof
Using the proof of the previous theorem, if there is no string s accepted
by M, with n ≤|s| ≤2n, then M(L) is ﬁnite (where we include the empty set
and the set containing only the empty word as ﬁnite sets).
□
Theorem 3.15
There is an algorithm determining whether a language L1 ⊆
L2.
Proof
We already know that there is an automaton that accepts L1 ∩L′
2, which
is empty if and only if L1 ⊆L2.
□
Exercises
(1) Prove there is an algorithm for determining if regular language M(L) =
∗.
(2) Prove there is an algorithm for determining if a regular language M(L)
contains a word that contains a given letter of the alphabet.
(3) Prove there is an algorithm for determining if every letter in the alphabet is
contained in some word in a regular language L.


3.6 Pushdown automata
89
(4) Prove that for a positive integer n, there is an algorithm for determining if
a regular language contains a word with length less than n that contains a
given letter of the alphabet.
(5) Prove that for a positive integer n, there is an algorithm for determining if
every letter in the alphabet is contained in some word with length less than
n in a regular language L.
(6) Prove there is an algorithm for determining if a regular language contains
a word that begins with a given letter of the alphabet.
(7) Prove there is an algorithm for determining if there is a word in a regular
language L of even length.
(8) Prove that for any integer k there is an algorithm for determining if there is
a word in a regular language L of length mk for some m.
(9) Prove that for a regular language L, it is possible to determine if ∗−L is
ﬁnite.
3.6
Pushdown automata
In the previous section we mentioned that the set {anbn : n is a positive integer}
is not a regular language. Therefore it cannot be accepted by an automaton.
Intuitively, the problem is that after the automaton has read the as in a word,
it cannot remember how many it has read, so it does not know how many
bs it should read. The automaton basically needs a memory so that it can
remember the letters it has read. A pushdown automaton or PDA is essentially
an automaton together with a very simple memory. The memory is called a
pushdown stack. Associated with the stack is a set of symbols called the stack
symbols. A stack symbol may be placed on the stack. This process is called
pushing the symbol onto the stack. If x is a stack symbol, then push x simply
means x is placed on the stack. The top symbol may also be removed from the
stack. This is the last symbol placed on the stack. Since the last symbol placed
in the stack is the ﬁrst out, the stack is said to have the LIFO (last in–ﬁrst out)
property. Thus the symbols are removed from the stack in reverse order from
the order they were put in the stack. The process of removing the top symbol
from the stack is called popping the stack. If x is a stack symbol then pop x
simply means that when the stack is popped, the symbol x is removed if it is
on top of the stack. The purpose of the stack is to allow the PDA to remember
the letters in the word that it has read so that it can duplicate them or replace
them with other letters.
Assume that the word to be read is placed on a tape. The tape is divided
into little squares with the letters of the word in the ﬁrst squares. The rest of


90
Automata
the tape is considered to be blank. Since the words may be arbitrarily long, it
is best to use an inﬁnite tape. These may have to be custom made. One of the
advantages of mathematics is that mathematical structures do not usually have
to be actually constructed.
The PDA, beginning at the left, reads a letter at a time in the same manner as
a standard automaton. The PDA may read a letter from the tape or pop (remove
from the top) and read a symbol from the stack or both. Depending on its current
state and the symbol(s) read, the PDA may change state, push a symbol in the
stack, or both.
b
a
b
a
c
C
A
b
a
Processor
Δ
Tape
Stack
We now deﬁne a PDA more formally.
Let λ =  ∪{λ} and I λ = I ∪{λ}.
Deﬁnition 3.8
A pushdown automaton is a sextuple
M = (, Q, s, I, ϒ, F)
where  is a ﬁnite alphabet, Q is a ﬁnite set of states, s is the initial or starting
state, I is a ﬁnite of stack symbols, ϒ is the transition relation and F is the set
of acceptance states. The relation ϒ is a subset of
((λ × Q × I λ) × (Q × I λ)).
Thus the relation reads a letter from λ, determines the state, and reads a
letter from I λ. It then changes state or remains in the same state and gives a
letter of I λ as output. Similar to the automata, the letter of a word is removed
when it is read. The top letter on the stack is also removed when it is read. As
discussed above, we say it is popped from the top of the stack. The letter of I
produced by the relation is placed on top of the stack or pushed on the stack as
discussed above. A word is accepted by the PDA if and only if after beginning
in the start state, with an empty stack, the word is read, if possible, the machine
is in an acceptance state, and the stack is empty. If all of the above do not occur,
then the word is rejected. The language consisting of all words accepted by the
pushdown automaton M is denoted by M(L).


3.6 Pushdown automata
91
Elements of ϒ have the following rules:
((a, s, E), (t, D))
In state s, a is read and E is popped, go to state tand
push D.
((a, s, λ), (t, D))
In state s, a is read, go to state t and push D.
((λ, s, λ), (s, D))
In state s, push D.
((a, s, E), (t, λ))
In state s, and a is read, pop E and go to state t.
((λ, s, E), (s, λ))
In state s, pop E.
((a, s, λ), (t, λ))
In state s, read a and go to state t.
((a, s, λ), (s, λ))
In state s, read a.
((λ, s, λ), (t, λ))
Move from state s to state t.
Deﬁnition 3.9
M is a deterministic PDA if ϒ ⊆((λ × Q × I λ) × (Q ×
I λ)) has the property that if ((s, a, c), (s′, c′)) and ((s, a, c), (s′′, c′′)) ∈F then
s′ = s′′ and c′ = c′′.
Note that this deﬁnition differs between texts.
Since the requirement that M is a deterministic PDA restricts the languages
that it accepts, we will not consider the deterministic PDA.
Although it seems a severe restriction, any language accepted by a PDA can
be accepted by a PDA with only two states, which we will call s and t. The
automaton leaves the ﬁrst state before it reads the ﬁrst letter and while the stack
is still empty. The second state is then the terminal state. Often it is simpler or
more convenient to use more states. An example of this will be shown in the
examples.
As with the regular automaton, we will show the PDA graphically. The PDA
will be shown as a ﬂow chart using only the instructions start, read, push, pop,
and accept. It will be obvious that the ﬂow charts below describe PDAs. We
shall not try to prove that every PDA has a ﬂow chart. Each edge of a ﬂow chart
has a state associated with it. For example in the following ﬁgure, (t) on the
edge indicates that at that point on the chart, we are in state t. We could put
the state with each edge, but we only do so when the state is changed. Thus the
state is determined by the location on the ﬂow chart. When only two states are
used, including the start command which takes the PDA to the state t, the state
will not be indicated. The symbol
Start
(t)


92
Automata
indicates start and switch to state t. The symbol
Start
Push
(t) S
indicates start, push S, and switch to state t. The symbol
read
a
indicates read a. The symbol
pop
a
indicates pop a. The symbol
Push
a
indicates push a. Finally, the symbol
accept
indicates accept if the word has been read, the machine is in an acceptance state,
and the stack is empty. Thus the diagram
read
Start
push
accept
b
a
a
pop
a
a
(t)


3.6 Pushdown automata
93
allows the PDA to read a and then push it or read b and pop a if it is on the stack.
Thus every time a b is read, it removes an a which has been read and placed in
the stack. In this example the alphabet and the stack symbols will both consist
of a, and b. If, at any time, there were more bs read than as in the stack, there
would be no a in the stack to remove and the PDA could not continue. If the
number of as is equal to the number of bs when the word is read, then the stack
will be empty. A word is accepted if, after popping a, the word has been read
and the stack is empty. Therefore this PDA accepts words which have the same
number of as and bs provided that, for every b in the word, the string preceding
it contains more as than bs. For example consider the word aababb. We can
trace its path with the following table:
instruction
stack
tape
start
λ
aababb
read
λ
ababb
push a
a
ababb
read
a
babb
push a
aa
babb
read
aa
abb
pop
a
abb
read
a
bb
push a
aa
bb
read
aa
b
pop
a
b
read
a
λ
pop
λ
λ
accept
λ
λ
Example 3.26
The PDA
read
Start
push
Accept
a
pop
a
a
(t)
push
b
b
pop
b
b
a
b
a


94
Automata
accepts words containing the same number of as and bs. Consider the word
abba. We can trace its path with the following table:
instruction
stack
tape
start
λ
abba
read
λ
bba
push a
a
bba
read
a
ba
pop
λ
ba
read
λ
a
push b
b
a
read
b
λ
pop
λ
λ
accept
λ
λ
In the following example, three states are used. A move to a new state is
indicated in the diagram by an arrow for which there is no loop or are no return
arrows.
Example 3.27
The PDA
read
Start
push
a
pop
a
a
(s)
push
b
b
b
b
a
b
accept
pop
pop
read
(t)
b
a
b
a
(t)
b
accepts words wwRwhere wR is the word w reversed. We read the ﬁrst half of
the word and then switch states to read the second half of the word. Consider
the word abba. We can trace its path with the following table:
state
instruction
stack
tape
s
start
λ
abba
s
read
λ
bba
s
push a
a
bba
s
read
a
ba
s
push b
ba
ba
t
read
ba
a
t
pop
a
a
t
read
a
λ
t
pop
λ
λ
t
accept
λ
λ


3.6 Pushdown automata
95
Exercises
(1) Which of the following words are accepted by the following pushdown
automaton M1?
pop
Start
b
push
b
Accept
b
read
read
a
a
a
read
read
a
b
(a) abbb
(b) aabbb
(c) aabbbbb
(d) aaabbb
(e) aabab
(f) aaabbbb.
(2) Use a table to trace each of the above words through the pushdown automa-
ton M1.
(3) What is the language accepted by the pushdown automaton M1?
(4) Which of the following words are accepted by the following pushdown
automaton M2?
push
accept
b
a
b
a
a
(t)
read
read
pop
pop
Start
b
a


96
Automata
(a) abb
(b) aabbaaa
(c) aabbbaa
(d) aaabaaa
(e) aabba
(f) aabb.
(5) Use a table to trace each of the above words through the pushdown automa-
ton M2.
(6) What is the language accepted by the pushdown automaton M2?
(7) Which of the following words are accepted by the following pushdown
automaton M3?
Start
read
read
pop
read
Accept
a
a
a
b
a
a
a
push
(a) abb
(b) aabbaaa
(c) aabbbaa
(d) aaabaaa
(e) aabba
(f) aabb.
(8) Use a table to trace each of the above words through the pushdown automa-
ton M3.
(9) What is the language accepted by the pushdown automaton M3?
(10) Which of the following words are accepted by the following pushdown
automaton M4?


3.6 Pushdown automata
97
read
Start
push
a
a
a
(t)
push
b
b
pop
b
b
a
b
accept
push
read
read
read
a
a
b
b
a
accept
a
b
(a) abb
(b) bb
(c) aabbbaaa
(d) abbbaa
(e) aabba
(f) aabb.
(11) Use a table to trace each of the above words through the pushdown automa-
ton M4.
(12) What is the language accepted by the pushdown automaton M4?
(13) Given a pushdown automaton M = (, Q, s0, I, ϒ, F) where  = I =
{a, b}, Q = {s0, s1, s2}, F = {s2}, and ϒ has the following relations:
((a, s0, λ), (s1, a))
In state s0, a is read, go to state s1 and push a
((b, s0, λ), (s1, b))
((a, s1, λ), (s1, a))
((b, s1, λ), (s1, b))
((a, s1, λ), (s2, λ))
((a, s2, a), (s2, λ))
((b, s2, b), (s j, λ))
(a) Complete the statements in the table.
(b) Construct the ﬂow chart for the PDA.
(14) Given a pushdown automaton M = (, S, s0, I, ϒ, F) where  = I =
{a, b}, Q = {s0, s1, s2}, F = {s2}, and ϒ has the following relations:
((a, s0, λ), (s1, a))
In state s0, a is read, go to state s1 and push a
((b, s0, λ), (s1, b))
((a, s1, a), (s1, b))
((a, s1, b), (s1, b))
((a, s1, a), (s2, a))
((b, s1, a), (s j, λ))
((a, s2, a), (s2, a))
((b, s2, a), (s j, λ))


98
Automata
(a) Complete the statements in the table.
(b) Construct the ﬂow chart for the PDA.
(15) Let  = {a, b, c}. Construct a pushdown automaton that reads the lan-
guage L = {wcwr : w ∈{a, b}∗}.
(16) Let  = {a, b, c}. Construct a pushdown automaton that reads the lan-
guage L = {ancbn : n is a nonnegative integer}.
(17) Let  = {a, b, c}. Construct a pushdown automaton that reads the lan-
guage L = {wwr : w ∈{a, b}∗}.
(18) Let  = {a, b, c}. Construct a pushdown automaton that reads the lan-
guage L = {wcwr : w ∈{a, b}∗}.
(19) Let  = {a, b, c}. Construct a pushdown automaton that reads the lan-
guage L = {w : The number of as in w is equal to the sum of the number
of bs and cs}.
(20) Let  = {a, b}. Construct a pushdown automaton that reads the language
L = {w : The number of as in w is equal to twice the number of bs or the
number of bs in w is equal to three times the number of as}.
(21) Given two pushdown automata
 = (N, ϒ, S, P)
and
′ = (N ′, ϒ′, S′, P′)
over the same alphabet  and accepting languages L and L′ respectively,
(a) Describe how to construct a pushdown automaton 1 that accepts the
language L ∪L′.
(b) Construct a pushdown automaton 1 that accepts the language L ∪L′
where L is the language accepted by the automaton in Example 3.26
and L′ is the language accepted by the automaton in Example 3.27.
(22) Given two pushdown automata
 = (N, ϒ, S, P)
and
′ = (N ′, ϒ′, S′, P′)
over the same alphabet  and accepting languages L and L′ respectively,
(a) Describe how to construct a pushdown automaton 2 that accepts the
language LL′.
(b) Construct a pushdown automaton 2 that accepts the language LL′
where L is the language accepted by the automaton in Example 3.26
and L′ is the language accepted by the automaton in Example 3.27.


3.7 Mealy and Moore machines
99
(23) Given a pushdown automaton  = (N, ϒ, S, P) over the alphabet  and
accepting language L,
(a) Describe how to construct a pushdown automaton 3 which accepts
the language L∗.
(b) Construct a pushdown automaton 3 that accepts the language L ∪L′
where L is the language accepted by the automaton in Example 3.26
and L′ is the language accepted by the automaton in Example 3.27.
(24) Given two pushdown automata
 = (N, ϒ, S, P)
and
′ = (N ′, ϒ′, S′, P′)
over the same alphabet  and accepting languages L and L′ respectively,
Construct a pushdown automaton 4 that accepts the language L ∪L′
where L is the language accepted by the automaton in Example 3.26 and
L′ is the language accepted by the automaton in Example 3.27.
3.7
Mealy and Moore machines
Previously, we deﬁned a deterministic automaton, a device which only accepts
or recognizes words of a language of ∗. We now produce two machines which
are similar to deterministic automata, but produce output.
The ﬁrst machine we introduce is called a Moore machine, created by E. F.
Moore[30] and is denoted by (, A, S, s0, ϒ, φ). It also has a ﬁnite set of states
S including a starting state s0. It contains two alphabets  and A. The ﬁrst is
the alphabet of input characters to be read by the machine. The second is the
alphabet of output characters produced by the machine. The Moore machine
retains the transition function ϒ : S ×  →S of the ﬁnite state automaton.
It also contains an output function φ : S →A. In the operation of a Moore
machine, the output is ﬁrst produced using the output function φ before the
transition function F is used to read the input and change states. Imitating the
deterministic automaton, the Moore machine reads each element of a string w of
characters of  until it has read the entire string. During this process, it produces
output consisting of a string of characters of A. Since the Moore machine
produces output φ(s0) before the ﬁrst input character is read and produces
output from the last state reached before the transition function tries and fails to
read input, the output string contains one more character than the input string.
Also since φ(s0) is always executed ﬁrst, each output string must begin with


100
Automata
φ(s0). As with the deterministic automata, we say a Moore machine reads a
symbol a of the alphabet  to indicate that the letter a is used as input for the
function ϒ. Similarly, in state si, if the output is φ(si), we shall say that the
machine prints the value φ(si), although the output may be used for an entirely
different purpose. Thus one may envision a Moore machine reading a string in
 from a tape and printing a string in A∗on the tape or on another tape.
As with the ﬁnite state automaton, we shall illustrate the Moore machine
using a ﬁnite state diagram. As in the deterministic automaton, if ϒ(si, a) = s j,
this is represented by
si
sj
a
If φ(si) = z, this is represented by
si/z
so that both si and φ(si) are represented inside the vertices of the diagram.
In the diagram
s0
b
a
b
a
b
a
 1
s1 0
s2 0
 = {a, b}, A = {0, 1}, S = {s0, s1, s2}, ϒ is given by the table
F
s0
s1
s2
a
s0
s0
s2
b
s1
s1
s2
and φ is given by the table
s
φ(s)
s0
1
s1
0
s2
0


3.7 Mealy and Moore machines
101
Given the input string aba, the machine ﬁrst prints the value φ(s0) = 1. It
then reads a and remains in state ϒ(a, s0) = s0. It then prints φ(s0) = 1. Next
it reads b and travels to state ϒ(b, s0) = s1. It then prints φ(s1) = 0. Next it
reads a and travels to state ϒ(a, s1) = s0. It then prints φ(s0) = 1. Since there
is no more input, operations cease. The result is the output string 1101. The
input string aabab produces the output string 111010. The input string baab
produces the output string 10110.
Note that the Moore machine we have produced is actually the ﬁnite
automaton
s0
b
a
b
a
b
a
 1
s1 0
s2 0
except that we have added φ with the property that φ(si) = 0 if si is not an
acceptance state and φ(si) = 1 if si is an acceptance state. When we do this,
the last character printed will be 1 if and only if the input is accepted by the
ﬁnite automaton. Thus since the outputs for aba and ababa are 1101 and
110101 respectively, aba and ababa are accepted by the automaton. Using
this procedure we can “duplicate” any ﬁnite automaton with a Moore machine
where a word is accepted only if the last character output is 1. It may also be
observed that whenever a 1 appears in the output, the initial string of input which
has been read at that point is accepted by the ﬁnite automaton since the state
at that point is an acceptance state. For example, in the above example input
aabaabbab produces output 0001001001, so aab, aabaab, and aabaabbab
are all accepted by the automaton. Since φ(s0) = 1 the empty word is also
accepted. In general, the number of 1s in the output of a Moore machine which
“duplicates” a ﬁnite automaton is the number of initial strings of the input which
are accepted by the ﬁnite automaton.
Example 3.28
The automaton
a
b
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


102
Automata
has corresponding Moore machine
a
a,b
b
a
b
a
b
s3/0
s2/1
s1/0
s0/0
Input babbab produces output 0010010 so substrings ba and babba
are
accepted by the automaton. Since the input ababbbaa produces output
000100000, the only substring accepted by the automaton is aba since only
one 1 occurs.
Example 3.29
A unit delay machine delays the appearance of a bit in a string
by one bit. Hence the appearance of a character in the output is preceded by
one character in the input. The following machine is a unit delay machine.
0
1
0
1
s0/0
s2/1
s1/0
So far, we have primarily shown that a Moore machine may be used to
“duplicate” a ﬁnite automaton. This is only one of the uses of a Moore machine.
However, any task performed by a Moore machine can be performed by another
machine called a Mealy machine and conversely. In most cases the task is more
easily shown using a Mealy machine.
The Mealy machine also contains an output function, however, the input is
an edge rather that a state. Since the edge depends on the state and the input,
the output function δ “reads” a letter of a ∈ and the current state and prints
out a character of the output alphabet. Hence δ is a function from S ×  to A.
More formally a Mealy machine is a sextuple Me = (, A, S, s0, ϒ, δ) where
, A, S, s0, and ϒ are the same as in the Moore machine and δ : S × A →.
The Mealy machine is also best illustrated using a ﬁnite state diagram. Since
δ depends on both the state and the letter read, we shall denote the output by
placing it on the edge so that
si
sj
a/z


3.7 Mealy and Moore machines
103
corresponds to ϒ(si, a) = s j and δ(si, a) = z. Note that, unlike in the Moore
machine, the output occurs after the input is read. Hence for every letter of
input, there is a character of output.
Consider the Mealy machine
s1
s2
b/0
a/1
b/0
b/0
a/1
s0
a/0
The functions ϒ and δ are given by tables
ϒ
s0
s1
s2
a
s1
s2
s2
b
s2
s0
s1
and
δ
s0
s1
s2
a
1
1
0
b
0
0
0
Given the input string aaabb, a is read, 1 is printed, and the machine moves to
state s1. The second a is read, 1 is printed, and the machine moves to state s2.
The third a is read, 0 is printed, and the machine remains at state s2. The letter
b is read, 0 is printed, and the machine moves to state s1. Finally, b is read, 0
is printed, and the machine reaches state s0. Thus input aaabb produces output
11000.
Example 3.30
The Mealy machine
a/x
s0
b/y
c/z
simply converts every a in the string to x, every b to y, and every c to z. Thus
aabbcca is converted to xxyyzzx.


104
Automata
Example 3.31
The 1s complement of a binary string converts each 1 in the
string to a 0 and each 0 to a 1. It is given by the state diagram
s0
0/1
1/0
Example 3.32
If 1 is added to the 1s complement of a binary string of length
n, we obtain the 2s complement used to express the negative of an integer
if we discard any number carried over beyond n digits. Thus 1111 + 1 =
0000.
The following Mealy machine adds 1 to a binary string in this fashion. The
input string must be read in backwards and the output is printed out backwards
so the unit digit is read ﬁrst. The stage diagram
0/0
s0
s1
1/1
0/1
1/0
describes the Mealy machine. In this diagram, s1 is the state reached if there is
no 1 to carry when adding the digits. The state s2 is reached if there is a 1 to
carry when adding the digits. Let 1101 be the number in reverse. (Hence the
actual number is 1011.) First input 1 is read. The output is 0 and the machine
is in state s2. (This corresponds to 1 + 1 = 10 so 0 is output and 1 is carried.)
Now input 1 is read. The output is 0 and the machine remains in state s2.
(This corresponds to 1 + 1 = 10 so 0 is output and 1 is carried.) Next 0 is
input. The output is 1 and the machine moves to state s1. (This corresponds to
1 + 0 = 1 so 1 is output and nothing is carried.) Finally 1 is input. The output
is 1 and the machine remains in state s1. (This corresponds to 1 + 0 = 1 so
1 is output and nothing is carried.) Thus the output is 0011 and the number
is 1100.
Example 3.33
The Mealy machine M+ adds two signed integers. The signed
integer m is subtracted from the signed integer n by adding n to the 2s com-
plement of m. Thus M+ can also be used for subtraction by ﬁrst using the
machine in the previous example to ﬁnd the 2s complement of the number to
be subtracted. Assume an, an−1, . . . , a2, a1 and bn, bn−1, . . . , b2, b1 are the two
strings to be added. We again assume that the two strings to be added are read


3.7 Mealy and Moore machines
105
in reverse so the ﬁrst two digits to be input are a1 and b1, followed by a2 and
b2, . . . , followed by an and bn. We shall consider the pair of digits to be input
as ordered pairs, so that (a1, b1) is the ﬁrst element of input. The machine M+
is
(0,0)/0
(0,0)/1
(1,0)/1
(0,1)/0
(1,0)/0
(1,1)/1
(1,1)/0
(0,1)/1
s0
s1
The machine is in state s0 when no 1 has been carried in adding the previous
input and is in state s1 when a 1 has been carried in the addition. Assume that
0101 and 1101 are added. First (1, 1) is read, so the machine moves to s1 and
prints 0. Next (0, 0) is read, so the machine moves to s0 and prints 1. Then (1, 1)
is read, so the machine returns to s1 and prints 0. Finally (1, 0) is read, so the
machine remains at s1 and prints 0. Note that the 1, if it exists, which is carried
from adding the last two digits is discarded. Thus the sum of 0101 and 1101 is
0010.
Earlier in this section, we implied that Moore machines and Mealy machines
were equivalent in the sense that every Moore machine could be duplicated by
a Mealy machine and conversely. More speciﬁcally, given a Moore machine,
there is a Mealy machine which will produce output equivalent to the Moore
machine when given the same input. Conversely given a Mealy machine, there
is a Moore machine which will produce the output equivalent to the Mealy
machine when given the same input.
We ﬁrst need to specify what we mean by equivalent output since a Mealy
machine always has one less symbol of output than the Moore machine. A
string of output of a Mealy machine is equivalent to a string of output of a
Moore machine if it is equal to the substring of the Moore machine excluding
the ﬁrst symbol φ(s0). Thus if the Moore machine produced output 010010101,
the equivalent output from the Mealy machine would be 10010101.
The transformation from the Moore machine to an equivalent Mealy machine
is the simplest. With the transition
s0/a0
s1/a1
c


106
Automata
in a Moore machine, given input c, the character a0 will be printed, the machine
will move to state s1, and a1 will next be printed. In the transition
s0
s1
c/a1
of a Mealy machine, the machine will move to state s1 with input c and a1 will
be printed. Since we disregard a0 in the string produced by the Moore machine
in our deﬁnition of equivalent output, we have begun with the same output.
Assume that we have the transition
si/ai
sj/aj
b
in a Moore machine and ai has already been printed. Input b moves the machine
to state s j, and the next output will be a j. The corresponding transition in the
Mealy machine is
si
sj
b/aj
which produces the same transition and output.
Example 3.34
The Mealy machine corresponding to the Moore machine
s0/1
a
s1/0
s2/0
a
b
b
a
b
is
s0
a/0
s1
s2
b/1
b/0
a/0
b/0
a/1


3.7 Mealy and Moore machines
107
In transforming a Mealy machine to a Moore machine, we have to consider
the problem where arrows into a given state produce different output. Consider
the following example:
a/x
b/y
c/z
s
In a Moore machine, the state s produces unique output so it cannot produce
both x and y as output. We solve this by making two copies of s
c/z
c/z
a
b
sy/y
sx/x
One will produce x as output and the other y as output as follows. Obviously
both machines produce output x with input a and output y with input b. For
simplicity, we shall simplify sx/x to s/x and sy/y to s/y noting that they are
different states.
In general, for each state s, except the starting state, in a Mealy machine and
for each output symbol z, we shall produce a copy s/z of the state s. This may
result in some overkill since in the above example, if the output symbols were x,
y, and z, we would not have needed state s/z since there was no arrow entering
s with output z. We begin with initial state s0 and give it an arbitrary output
variable x0 from the set of output variables since it is not used in producing
output equivalent to the Mealy machine. If we have
a/x
c/z
b/y
s0
si
…
in the Mealy machine, we replace it with
s0/x0
si/x
si/y
si/z
a
b
c
…


108
Automata
in the Moore machine. For other states, we replace
si
sj
a/x
b/y
with
si/x
sj/y
a
b
We produce the same output at each step for both machines.
Thus the machine equivalent to
s1
a/0
s2
b/1
s3
s0
b/0
b/0
b/0
a/1
a/1
a/1
is strcj.eps
s3/1
s1/1
s3/0
a
a
b
b
s1/0
s2/0
s2/1
s0/0
b
b
b
b
b
a
a
a
a
a
Exercises
(1) Let the Moore machine Mo = (, A, S, s0, ϒ, φ) be given by the
diagram
a
a,b
b
a
b
a
b
s3/0
s2/1
s1/0
s0/0
Describe A, , and S. Find tables for F and φ.


3.7 Mealy and Moore machines
109
(2) Let the Moore machine Mo = (, A, S, s0, ϒ, φ) be given by the
diagram
a
b
c
c
a
a
a
b
b
c
b
c
s0/0
s1/1
s2/1
s3/0
Describe A, , and S. Find tables for ϒ and φ.
(3) Let the Moore machine Mo = (, A, S, s0, ϒ, φ) be given by the
diagram
s1/0
s0/1
s2/1
s3/1
a
a
a
a
b
b
b
b
(a) Find the output with input bbabab.
(b) Find the output with input aaabbaba.
(c) Find the output with input bbbaaa.
(d) Find the output with input λ, the empty word.
(4) Let the Moore machine Mo = (, A, S, s0, ϒ, φ) be given by the
diagram
a
b
c
c
a
a
a
b
b
c
b
c
s0/0
s1/1
s2/1
s3/0
(a) Find the output with input abcabca.
(b) Find the output with input bbbaaacc.
(c) Find the output with input aabbccaa.
(d) Find the output with input λ, the empty word.


110
Automata
(5) Find the Moore machine that duplicates the ﬁnite automaton
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
(6) Find the Moore machine that duplicates the ﬁnite automaton
s1
s0
s3
a
b
b
a
b
a
(7) Find the Moore machine that duplicates the ﬁnite automaton
s2
b
b
s0
s3
a
a
a
b
s1
a
b
(8) Find the Moore machine that duplicates the ﬁnite automaton
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


3.7 Mealy and Moore machines
111
(9) Let the Mealy machine Me = (, A, S, s0, ϒ, δ) be given by the
diagram
s0
a/1
b/0
b/1
s1
s3
s2
a/1
a/1
a/1
b/1
b/0
Describe A, , and S. Find tables for ϒ and δ.
(10) Let the Mealy machine Me = (, A, S, s0, ϒ, δ) be given by the
diagram
s1
a/0
s3
b/1
a/0
b/0
b/1
a/1
a/1
s0
s2
c/1
c/1
c/1
b/0
c/0
Describe A, , and S. Find tables for ϒ and δ.
(11) Let the Mealy machine Me = (, A, S, s0, ϒ, δ) be given by the
diagram
s0
b/0
b/0
a/0
s1
c/1
b/0
a/0
b/0
a/1
s2
s3
c/1
c/1
c/1
a/0
(a) Find the output with input abaabbab.
(b) Find the output with input bbaaba.
(c) Find the output with input aabbaaa.
(d) Find the output with input λ, the empty word.


112
Automata
(12) Let the Mealy machine Me = (, A, S, s0, ϒ, δ) be given by the diagram
s1
a/0
s3
b/1
a/0
b/0
b/1
a/1
a/1
s0
s2
c/1
c/1
c/1
b/0
c/0
(a) Find the output with input abcccbab.
(b) Find the output with input bbaabc.
(c) Find the output with input aaccbba.
(13) Given the Moore machine Mo = (, A, S, s0, ϒ, φ)
a
a,b
b
a
b
a
b
s3/0
s2/1
s1/0
s0/0
ﬁnd the equivalent Mealy machine.
(14) Given the Moore machine Mo = (, A, S, s0, ϒ, φ)
a
b
c
c
a
a
a
b
b
c
b
c
s0/0
s1/1
s2/1
s3/0
ﬁnd the equivalent Mealy machine.
(15) Given the Mealy machine Me = (, A, S, s0, ϒ, δ)
s1
s2
b/0
a/1
b/0
b/0
a/1
s0
a/0


3.7 Mealy and Moore machines
113
ﬁnd the equivalent Moore machine.
(16) Given the Mealy machine Me = (, A, S, s0, ϒ, δ)
s1
s2
b/0
a/1
a/0
b/0
a/1
s0
b/1
ﬁnd the equivalent Moore machine.
(17) Construct a Mealy machine which directly subtracts a signed binary num-
ber from another signed binary number.
(18) Let Z5 = {¯0, ¯1, ¯2, ¯3, ¯4} be the set of integers modulo 5, where the “sum” of
two integers is found by adding the numbers and ﬁnding the remainder of
thissumwhendividedby5.Therefore ¯3 + ¯4 = ¯2and ¯2 + ¯3 = ¯0.Construct
the Moore machine that gives a sum of initial strings of elements of Z5.
Thus the input ¯2¯1¯4¯0¯3¯2¯1 produces output ¯0¯2¯3¯2¯2¯0¯2¯3.


