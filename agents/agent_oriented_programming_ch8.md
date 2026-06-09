Chapter 8
Meta-Interpretation
I can play with the chessmen according to certain rules. But I can
invent a game in which I play with the rules themselves. The pieces
in my game are now the rules of chess, and the rules of the game
are, say, the laws of logic. In that case I have yet another game and
not a metagame.
Ludwig Wittgenstein, Philosophical Remarks
Quis custodiet ipsos custodes? Anyone familiar with the distinction between theory
and metatheory will answer instantly that of course the metaguards guard the guards.
“Meta-X is X about X” and from the time of Russell’s paradox dividing X up into
levels of X, meta-X, meta-meta-X and so on has been a useful aid to thought. If you
have experienced an argument change (as they often do!) from arguing about
something to arguing about the argument, you will have experienced a meta-
argument. If you have ever wondered who trains the people who teach in teacher-
training school, you will have started considering the possibility of an infinite number
of levels in the tower of meta-X. If the answer to this question is that the teachers in
teacher training school teach teaching in general and thus are perfectly capable of
teaching how to teach teaching you will have encountered the idea of metacircular-X.
You will, as well, experience the sort of convoluted sentence to which prolonged
thought on metalevels leads to.
Barklund and Hamfelt [1994], quoting Hart [1961], note that a correspondence can be
drawn between the different layers of reasoning in a system involving metalogic with
the different layers of law in a legal system. Some laws regulate behavior, while
others regulate the practice of law itself; these latter could be termed “metalaws”. The
constitution of a state or organization may be regarded as a formalization of the
concept of metalaws. A person may be judged guilty or innocent under the laws of
the land, but a constitution which contains a Bill of Rights in effect may judge a law
to be guilty or innocent according to this Bill of Rights and rule out laws which
conflict with it. Since there is, in general, no higher level constitution against which a
constitution may be judged, a constitution may be deemed metacircular. A
constitution defines in itself how it operates, but one could separate those clauses of a
constitution which deal with how it operates or may be amended as a
“metaconstitution” or “meta-metalaw”.
The British constitution is, unusually, “unwritten”. This does not mean, as some
suppose, that there is no such thing as a British constitution. Rather, that no formal
distinction is made between constitutional law and any other law: a law affecting or
amending the way the constitution works may be made in the same way as any other
law may be made, there is no special qualified voting or referendum. Ultimately,
British law rests on the absolute authority of the Sovereign (a legal concept that may
have originally meant literally the sovereign as a living human being, but at a later
date was taken to mean the sovereign acting through Parliament). A comparison may
M.M. Huntbach, G.A. Ringwood: Agent-Oriented Programming, LNAI 1630, pp. 247–278, 1999.
© Springer-Verlag Berlin Heidelberg 1999

248 Chapter 8
be drawn between the British legal system and programming languages that do not
have a metalanguage or mix in arbitrarily metaprogramming concepts with the
language itself: the ultimate authority is the hardware. Arguments for and against the
unwritten constitution sound rather like arguments for and against a programming
language without a strong and distinct metaprogramming layer: it is defended for its
efficiency and power and attacked for its inherent lack of safety. Bagehot [1861] in
comparing the UK and USA constitutions, attacks the latter for unnecessary layers of
complexity and defends the former as acceptable since relying on the “reasonableness
of the British middle classes”.
8.1 Metalanguage as Language Definition and Metacircular Interpreters
The concept of a metalanguage as a “language about language” is a vague one and
has led to it being used with several different meanings. The comment that
“metalogical has often been used where extralogical would be more appropriate” has
been made [Weyrauch, 1980]. This point will be returned to later in this chapter.
With programming languages, the term was used early on to describe languages that
could formally describe the meaning or behavior of the first high-level languages,
inspired in particular by Algol [Naur, 1960], one of the first attempts to define a
language formally first and practically second. It was also inspired by concern (see,
for instance, [Feldman, 1966]) that others of the then newly developed high-level
languages could only be genuinely considered “high-level” and could be safely
ported between machines if they could be described in terms other than the assembly
languages into which they compiled. If they could not and the assembly languages in
turn could only be described in terms of the physical electronics of the machines, the
languages were really only defined by the hardware. An important early conference
on metalanguage for programming language description held in Vienna in 1964
[Steel, 1966] was considered then as “among the most valuable and productive
scientific meetings ever held on a subject pertaining to information processing”. Note
that the vagueness of the term metalanguage was already apparent at this stage. Some
of the papers described metalanguages, which built on BNF (Backus Naur Form) and
some explicitly noted the distinction between syntax and semantics. Our interest here
will only be on the semantics side.
As mentioned in Chapter 2, Landin noted a correspondence between Algol and
Church’s lambda calculus [Landin, 1965] and expounded further on it at this Vienna
conference. At the same conference, McCarthy [1965] chose the different approach
of describing Algol in terms of a mini-language he called “Micro-Algol”. Programs
in this language consist only of assignments and conditional gotos of the form if p
then goto a. McCarthy later developed this into a full metacircular interpreter; the
idea was that since the interpreter was written in Micro-Algol and could interpret
Micro-Algol, Micro-Algol was a language, which defined itself. Algol and any other
high-level language that could be translated to Micro-Algol were thus fully defined.
The definition did not have to resort to a lowest-level description in terms of machine
hardware (just as the self-interpreting USA constitution means that the USA legal

Meta-Interpretation 249
system does not ultimately rely on the whims of a monarch or the reasonableness of
the middle classes).
The following is McCarthy’s [1965] Micro-Algol metacircular interpreter:
micro: n:=c(s,x );
if beyond(p ,m) then goto done;
s:=statement(n,p );
x :=if assignment(s) then a(sn,n+1,a(left(s),value(right(s),x ),x ))
else if value(proposition(s),x ) then a(sn,numb(destination(s),p ),x )
else a(sn,n+1,x );
goto micro;
done:
This requires some explanation. x is the state vector of the program p being
interpreted. The state gives the value of all the variables and all other information that
together with the program itself determines the future course of the computation.
Today this would be called a continuation. The pseudo-variable sn, whose value is
included in x , gives the number of the statement, which is currently being executed.
a(var,value,x ) gives the new state resulting from assigning value to variable var;
left(s) gives the variable on the left hand side of an assignment s, right(s) gives the
expression on the right-hand side; value(e,x ) evaluates expression e when the
current state is x ; proposition(s) gives p when s is if p then goto a while
destination(s) gives a; numb(L,p ) gives the statement number corresponding to
label L in program p .
Landin’s compilation into lambda calculus was the more immediately practical. Since
lambda calculus could be considered the machine code of the abstract SECD machine
which Landin had also developed [Landin, 1963], this could in turn be implemented
on a real machine, thus the approach could be the basis of a practical compiler. The
important thing was the introduction of clarity into what was then something of a
“black-art” of compiler writing through this division into layers. The division was
somewhat spoilt by the necessity to add further facilities to the SECD machine to
cope with those aspects of Algol that could not easily be represented in lambda
calculus. The development of programming languages that were purely sugared
lambda calculus came later [Turner, 1979].
McCarthy’s approach was not designed to lead to a practical compiler, or even to an
impractical one that could nevertheless be put forward as a working model to define
the semantics of a language operationally; it was more an operation in defining
semantics abstractly. An important distinction is that McCarthy’s interpreter makes
the machine state of the language an explicit object in the metalanguage, whereas in
Landin’s approach the implicit machine state of the language is translated to an
implicit machine state in the metalanguage. In the discussions following the
presentations of the papers Landin [1963] links McCarthy’s approach with a paper
presented by Strachey at the same conference, which in retrospect may be seen as
introducing ideas that led to the concept of denotational semantics [Scott and
Strachey, 1971]. (Helpfully for computer science historians, fairly full accounts of
these discussions are included in the proceedings.)

250 Chapter 8
8.2 Introspection
The idea of a programming language being able to handle an explicit representation
of its own state was of interest to workers in Artificial Intelligence. It was argued that
a crucial component of an intelligent system is the ability to reason about itself, or to
introspect. Maes [1986] gives a simple introduction to the subject. Introspection is
first clearly defined in the language 3-Lisp [Smith, 1984], although features that may
be regarded as introspective are provided in a more ad hoc manner in earlier
languages. The idea is that facilities exist in the language to take objects that may be
assumed to exist at the interpreter or metalanguage level and make them first-class
entities in the language level. In McCarthy’s micro-Algol meta-interpreter, for
example, the pseudo-variable sn might be considered such an object, as indeed might
any part of the state x . Object level decisions may be made on the basis of their value
and new values for them constructed and put back into the meta-interpreter. The term
reification came to be used to refer to taking metalevel objects from the program and
making them data, while reflection referred to the reverse process of putting data
objects into the program [Friedman and Wand, 1984].
Introspection was promoted not only as a way for allowing programs to reflect on
themselves, but also as a way for programmers to tailor the programming language
for their own needs, changing the evaluation order, adding traces for debugging and
so on. It was particularly influential in object-oriented programming [Maes, 1987]. In
Smalltalk [Goldberg and Robson, 1989], the idea that “everything is an object”,
including the classes that describe objects and hence the concept of a metaclass as the
class which describes classes, means that introspection is a natural part of the
language. In Prolog, the system predicate clause is a reification predicate, making
an aspect of the program into data, while assert is a reflection predicate. Prolog’s
retract may be regarded as a combination of reification and reflection. Even the cut
(and more so many proposed variants of it) may be regarded as a stereotyped
combination of reification and reflection, giving the program access to the abstract
search space of the interpreter and modifying it, though with severe restrictions on the
modifications possible. This is the connection between extralogical and metalogical
promised earlier.
The key to introspection in programming languages is that it relies on an abstract
interpreter, which is in fact a virtual interpreter. There is no requirement that the
meta-interpreter, which it assumes exists, actually does exist. Indeed it cannot always,
since reflection is often recursive: it is possible for the metalayer to introspect on a
meta-metalayer and so on infinitely, producing what is described as the “tower of
interpreters”. The real interpreter or compiler, which actually implements the
language, is something different and remains unreachable by the programmer. The
concepts in the meta-interpreters are produced lazily as required. If introspection
were introduced into McCarthy’s Micro-Algol, for instance, it would be possible to
access and change sn, the statement position indicator. But there is a clear distinction
between this, an abstract concept and the program counter of the underlying assembly
language. However deep you got into the tower of meta-interpreters, you would never
hit the real program counter.

Meta-Interpretation 251
The problem with introspection in programming languages is that it gives both the
power and the danger of self-modifying code. In 3-Lisp it is possible to access and
change variable bindings and function definitions using introspection. Thus the
barrier between language and metalanguage is broken down, it becomes a notational
convenience, but not one that can be relied on. If we can change the environment at
whim, we have lost the valuable declarative properties of functional programming.
As Hofstadter [1979] puts it: “below every tangled hierarchy lies an inviolate level.”
The only real metalanguage when we have unlimited reflection (perhaps we could
call it the hyper-language) is the inviolate machine code which implements the
system. In our constitutional analogy, we are back to the position where the only
absolute power lies with the whim of the sovereign; there are no hard constitutional
safeguards. The reasonableness of the programmer in not misusing reflection can be
compared to the reasonableness of the British middle classes in Bagehot’s defense of
the unwritten constitution.
8.3 Amalgamating Language and Metalanguage in Logic Programming
As mentioned above, the introduction of a meta-interpretation layer enables us to
reason explicitly about programs and their execution. In logic programming terms, it
enables one to reason explicitly about theories (collections of clauses) and about the
inference mechanism used to make derivations from these theories. We expressed
concern, however, about the lack of control when we had an implicit meta-interpreter
and an undisciplined approach to manipulating it. This can be overcome by making
an interpreter explicit, but explicit in a limited way. Only those elements of the
interpreter that we want to reason about are made explicit, while other elements
remain implicit. For example, if we want a program that adds or deletes clauses from
the set of clauses but does not make any changes to the inference mechanism, we can
write an interpreter with an explicit representation of the clauses, but the inference
mechanism remaining implicit and inviolate. In doing so, we limit the amount of
damage caused by work at the metalevel. As mentioned above, the metalevel and
object-level are in fact almagamated by giving the programmer control of both. But if
the communication between the two is limited as much as possible in the program it
is good software engineering principle, akin to other ways of dividing up programs
into modules and limiting and making explicit the communication between the
modules.
Bowen and Kowalski [1982] formalized discussion of metaprogramming in logic by
introducing two rules that describe the interactions between the object-level and
metalevel:
Pr |- demo(A´,B´) A |- B
M L
A |- B Pr |- demo(A´,B´)
L M
These are referred to as reflection rules, the terminology coming from Feferman
[1962] via Weyhrauch [1981]; it is related but not identical to the use of the term

252 Chapter 8
reflection in introspective systems. Here |- represents proof at the metalevel, while
M
|- represents proof at the object language level. So the first rule states that if it is
L
possible to prove that demo(A´,B´) follows from the program Pr at the metalevel,
then it can be inferred that B can be proved from A at the object level, while the
second rule states the reverse. A´ is the representation of the object-level theory A at
the metalevel and similarly B´ is the representation of the object-level expression B at
the metalevel. This relationship is specified formally by a naming relationship [van
Harmelen, 1992]. The naming relationship is a formalization of McCarthy’s
packaging of program state into the “state vector” x in his meta-interpreter.
The classic “vanilla” meta-interpreter of Prolog is simpler than Bowen and
Kowalski’s demo:
solve(true).
solve((A,B)) :- solve(A), solve(B).
solve(Goal) :- clause(Goal,Body), solve(Body).
because it makes no distinction between object-level and metalevel clauses. Here the
object level and the metalevel language are identical, except that object-level
predicate names are represented by metalevel function names. The blurring of object
and metalevel in clause confuses even this. A particularly important point is that
object-level variables are represented by metalevel variables.
We can remove the problem caused by Prolog’s clause by having the object-level
program represented as an explicit value in the metalevel program, then we can
define a demo which works as indicated by Bowen and Kowalski’s rules:
demo(Pr,[]).
demo(Pr,[A|B]) :- body(Pr,A,Body), demo(Pr,Body), demo(Pr,B).
The exact metalevel representation of object-level clauses will be further defined by
body, which it can be assumed selects a clause from the object-level program Pr,
whose head matches with A and returns in Body the body of that clause, importantly
with variables re-named as necessary. The interpreter does require that an object-level
clause body is represented by a metalevel list of metalevel representations of goals or
by the empty list if it is true at the object-level.
What is crucial is that object-level control is represented implicitly by metalevel
control. There is nothing in the interpreter that indicates that it is Prolog’s depth-first
left-to-right with backtracking control. We could build a tower of such meta-
interpreters and the control would remain in the underlying Prolog system (the
inviolate hyper-interpreter, introduced earlier). Indeed, if it were running on top of
GDC or some other non-Prolog logic language, it would inherit that language’s
control mechanism. We can note therefore that contrary to McCarthy’s intentions
with his Mini-Algol meta-interpreter, this metacircular interpreter does not fully
define the logic language, indeed in amalgamating language with metalanguage it
leaves it undefined.
The use of such a meta-interpreter comes when we do not wish to interfere with the
control, but wish to add some extra processing alongside inheriting the control
mechanism of the underlying language. The following meta-interpreter adds to the

Meta-Interpretation 253
“vanilla” interpreter a mechanism for counting the number of object-level goal
reductions:
demo(Pr,[],N) :- N=0.
demo(Pr,[A|B],N) :-
body(Pr,A,Body), demo(Pr,Body,N1), demo(Pr,B,N2),
N is N1+N2.
Another use might be an interpreter that simply prints each goal as it is reduced. This
could thus be used as a simple tracer. A useful aspect of this interpreter is that in
making the object-level program explicit we can handle program-altering primitives
like assert and retract in a way which viewed from the metalevel does not violate
the logical basis of the program:
demo(Pr,[]).
demo(Pr,[assert(C)|Rest]) :- !,
insert(C,Pr,Pr1), demo(Pr1,Rest).
demo(Pr,[retract(C)|Rest]) :- !,
delete(C,Pr,Pr1), demo(Pr1,Rest).
demo(Pr,[A|B]) :- body(Pr,A,Body), demo(Pr,Body), demo(Pr,B).
Some measure of the extent to which a primitive is merely extra-logical as opposed to
metalogical may be gained by the ease with which it can be incorporated into a
metacircular interpreter. Prolog’s cut performs badly on this front, since it is certainly
not possible to represent an object-level cut by a metalevel cut; to implement it
correctly would require a large amount of the underlying control to be made explicit
in the meta-interpreter so that it can be manipulated. On the other hand, negation by
failure is trivial to implement in the meta-interpreter; it requires just the addition of
the following clause to the vanilla demo:
demo(Pr,[not(G)|Rest]) :- not(demo(Pr,[G])), demo(Pr,Rest).
The version of demo suggested by Bowen and Kowalski enables greater control to
be exercised at the metalevel over the object level:
demo(Prog, Goals) :- empty(Goals).
demo(Prog, Goals) :-
select(Goals, Goal, Rest),
member(Clause, Prog),
rename(Clause, Goals, VariantClause),
parts(VariantClause, Head, Body),
match(Head, Goal, Substitution),
join(Body, Rest, NewGoals1),
apply(Substitution, NewGoals1, NewGoals),
demo(Prog, NewGoals).
Here the selection of the particular object-level goal to reduce is determined by the
metalevel procedure select and match determines the sort of matching of goal
against clause head. It would be possible for select and join which adds the new
goals to the existing waiting goals to be written so that the control regime provided at
object-level is not Prolog’s depth-first left-to-right, but something else. For example,
if join joined the new goals to the rear of the rest of the goals and select chose the
first goal from the front, the result would be breadth-first expansion of the search tree.

254 Chapter 8
Although match could be written as GDC style input matching rather than full
unification, this interpreter still inherits Prolog’s underlying assumption of sequential
execution. Note for example, it is assumed that a complete set of goals to be executed
is passed sequentially from each goal reduction, with Prolog’s global substitution on
unification assumed.
8.4 Control Metalanguages
In the interpreters discussed above, control is fixed, whether inherited implicitly from
the underlying hyper-interpreter, or provided explicitly through procedures such as
select. However, another strand of work in metalevel reasoning concerns the
definition of separate languages for programming control. Confusingly, these
languages are also referred to as “metalanguages”. In the Bowen and Kowalski
[1982], brief mention is made of a four argument demo predicate, whose first two
arguments are the theorem and expression to be proved as above, but whose third
argument is an input control value and whose fourth argument is an unspecified
output. The idea of a proof argument to demo is expanded in a further paper by
Bowen and Weinberg [1985]. With the four-argument demo, we can extend the
reflection rules:
Pr |- demo(A´,B´,C´,D´) A |- B,D
M L,C
A |- B,D Pr |- demo(A´,B´,C´,D´)
L,C M
Clearly, the proof argument C here could have a very simple structure, consisting
perhaps of just a single word indicating that search should be depth-first or breadth-
first. The existence of infinite trees means that something may be provable when
proof is specified as breadth-first but not when depth-first. Gallaire and Lassere
[1982] and Dincbas and Le Pape [1984] have proposed considerably more complex
metalanguages for control in logic programming. Trinder et al [1998] introduce a
meta-programming strategy argument to parallelize lazy functional programming.
Although control metalanguages are expressed here in terms of a second input along
with the object-level program to an explicit meta-interpreter, the more common
situation is that the meta-interpreter they control is implicit and as with introspection
may be considered a virtual concept. Just as with introspection, what the language
designer chooses to make reifiable and what remains inviolate is not fixed. It depends
on the way in which the language is intended to be viewed. What a control
metalanguage may actually control depends on what the language designer who
makes the control metalanguage available chooses to reveal as controllable. For
example, whereas the control metalanguages for logic programming mentioned above
view logic programming in terms of an abstract resolution model, another proposed
control metalanguage for Prolog [Devanbu et al., 1986] views Prolog in procedural
terms. Thus it gives the programmer the ability to alter the control pattern of Prolog
as expressed by the Byrd four port model [Byrd, 1980].

Meta-Interpretation 255
As noted in Section 1.8, the idea of explicit metalevel control systems which may
themselves be programmed first arose in the context of production rule systems,
where it was possible that in a given situation more than one rule could fire. In this
case, the potential set of rules that can fire is termed the conflict resolution set and the
mechanism for picking one rule to fire from these is termed conflict resolution. Early
production systems had simple built-in implicit strategies, just as Prolog had a built-
in control order. OPS [Forgy and McDermott, 1977], for example, gives a preference
to the rule which matches with the most recent additions to working memory and then
to the rule with the greatest number of conditional elements. One of the first systems
to give an explicit control over selection of rules in conflict resolution was
TEIRESIAS [Davis and Buchanan, 1977; Davis, 1980], which gave the ability to
specify which rule to select by a set of metarules. As these metarules took the same
format as the object-level rules, the possibility of meta-metalevel rules to govern
them and so on existed, though Davis did not find any need for levels of rules above
the metalevel.
The idea of structuring knowledge into multiple layers, with separate layers of
metaknowledge for reasoning about control is now commonplace. The KADS
methodology for developing expert systems [Schreiber et al., 1993], for example,
specifies four distinct layers [van Harmelen and Balder, 1992]:
• Domain layer – knowledge about the specific domain of the expert system.
• Inference Layer – how to use the knowledge from the domain layer.
• Task layer – specifies control over the execution of the inference steps.
• Strategy layer – concerned with task selection: how to choose between various
tasks that achieve the same goal.
In intelligent agent systems, multiple layers of control are also a common form of
structuring [Malec, 1994]. For example, a system developed in Sweden to give
intelligent assistance to drivers [Morin et al., 1992] has three layers:
• A process layer, which receives input from the environment and translates
continuous data to discrete values.
• An intermediate discrete response layer, which computes a response to events
forwarded from the process layer.
• An analysis layer, which deals with planning and reasoning.
We consider the idea of layering in agents in more detail in Chapter 10
Metalevel control systems can be divided into those that make use of domain
information and those that are purely concerned with the metalevel. In TEIRESIAS,
for example, a typical metarule will suggest that rules containing one specified
object-level property should be preferred over rules containing another: this is
domain level information. A medical expert system might, for example, have a
metarule that states that rules indicating the presence of an infectious disease should
always be tried before other rules. This sort of control rule may be considered
essentially as a structuring of the domain knowledge. An example of a metarule that

256 Chapter 8
does not involve domain knowledge would be one that stated that the rule with the
largest number of conditions to match should always be tried first. Metarules like
this, which simply specify a search order without reference to the domain or solely in
terms of the representation at the metalevel, may be considered essentially as a way
of structuring the interpreter. In a concurrent language, an important application of
this layering of interpreters is to have an interpreter which provides an abstract layer
of virtual parallelism [Burton and Huntbach, 1984]. The applications program
interpreted itself by a meta-interpreter maps the virtual parallelism onto a real parallel
architecture [Taylor et al., 1987]. Annotations such as those we have described for
priority and codemapping may be considered as a simple metalanguage that breaks
through to the mapping meta-interpreter. Prolog’s cut may be considered a similar
sort of notation which breaks through the control-free model of clause resolution in
logic to a separate control mechanism, thus accounting for the difficulty of modeling
it in a meta-interpreter.
Clancey argues the case for keeping domain knowledge out of metalevel control rules
[Clancey, 1983], saying that doing so keeps systems easier to debug and modify,
ensures that they are reusable in a variety of domains and also enables systems to
easily generate explanations for their actions. He demonstrated this by extracting the
domain-independent control strategy that was implicit in the MYCIN medical expert
system [Shortliffe, 1976] and making it separate and explicit in a new expert system
called NEOMYCIN [Clancey and Letsinger, 1981].
8.5 A Classification of Metalevel Systems
Drawing on the discussion above, we can now attempt a classification of metalevel
systems. The classification is based on that suggested by van Harmelen [1991]. The
first class of metalevel systems may be termed definitional and uses a metalanguage
in order to define another language. This may be purely in order to give a semantics,
which is operational if the metalanguage is executable, but it may also be part of a
practical implementation. Symbolic processing languages are particularly suited to
implementing other languages. In artificial intelligence, building a higher-level
knowledge-representation language on top of a lower-level declarative language is a
common practice, recommended in textbooks on artificial intelligence programming
in both Lisp [Charniak et al., 1987] and Prolog [Bratko, 1986].
A second class may be termed enhanced metacircular interpreters. In this class the
metalanguage is the same as the object language and the purpose of the interpreter is
to provide an additional output alongside the interpretation. Among the additional
outputs that can be provided are certainty factors for use in expert systems
applications [Shapiro, 1983] and computation trees for use in debugging [Huntbach,
1987]. The chapter on meta-interpreters in Sterling and Shapiro’s Prolog textbook
[Sterling and Shapiro, 1986] is largely confined to this sort of meta-interpreter and
provides numerous examples. Use of this sort of meta-interpreter occurs mainly
among logic programmers because they are easy to write in logic languages: complex
issues like control and variable handling are simply passed implicitly from object
level to metalevel to the underlying system.

Meta-Interpretation 257
The most varied class of metalevel systems, however, is that class of systems where
the aim is to separate control issues from declarative issues, but to provide the ability
to program both. This follows from Kowalski’s [1979] dictum “Algorithm = Logic +
Control.” Multiple layers of meta-interpreters means that it is possible to break down
control into metalogic and metacontrol and so on.
It might be possible to alter the flow of control in some procedural languages, but in
general these languages are such that logic and control are so intertwined as to be
inseparable. Declarative languages, however, are built around the idea that control is
left to the underlying system and the program is simply a declaration of the possible
set of solutions. This opens the question as to why the programmer should have any
control over control, since it is just an implementation detail. There is, however, a
group of languages that are neither procedural nor declarative. As suggested above,
production rule systems fall into this group and are the paradigm in which the issue of
metalevel control first received practical attention.
The reason why control arises as an issue in declarative languages is the question of
efficiency. In functional languages the only control issue is reduction order. The
Church–Rosser theorem [Barendregt, 1984] tells us that if it terminates, whatever
way we reduce a functional expression we will get the same result. It is possible for
one reduction order to return a result quicker than another is, or for one reduction
order to return a result while another does not terminate. Additional questions of
efficiency arise when implementing a functional language on a multi-processor
system when a decision has to be made as to whether the overhead of moving a
subexpression to another processor to be evaluated in parallel is outweighed by the
benefits of parallel execution. These considerations have led to suggestions for simple
control annotations controlling reduction order and parallel processing in functional
languages [Burton, 1987].
In logic languages, there is greater scope for order of reduction to affect efficiency.
Whereas in a functional language control is generally considered something for the
system to sort out, in logic languages there have been many proposals for methods to
give the user control over control. Smith and Genesereth [1985] analyze in detail the
effect that the ordering of conjunctive queries can have. The practical Prolog
programmer always has to be aware of Prolog’s left-to-right reduction order, writing
programs such that the optimal ordering of queries matches this built-in order.
However, the optimal order may only be determinable at run-time and often depends
on the mode in which a predicate is called. The lack of ability to change query order
dynamically is one of the reasons why Prolog’s multi-mode facility is rarely useful in
any but trivial programs. Metalevel annotations to give the programmer control over
query order were among the earliest suggestions to improve Prolog [Clark et al.,
1982; Colmerauer et al., 1982]. Cohen [1985] gives a metacircular interpreter to
implement Prolog II’s freeze. This is a metalevel procedure where freeze(X,G)
with X a variable and G a goal causes G to be removed from the list of goals waiting
for execution if X is unbound, but to be placed at the head of it as soon as X becomes
bound. Owen [1988] gives a metacircular interpreter that was used to allow flexible
goal ordering, which was used in the domain of protein topology. As we have seen, in
GDC there is a built-in suspension mechanism which works in a similar way to

258 Chapter 8
freeze and otherwise obviates the need for further goal ordering mechanisms until
we consider the speculative computation issues in Chapter 6.
Van Harmelen classifies metalevel systems on the basis on combinatorial soundness
and completeness. A metalevel inference system is combinatorially complete if it
derives all results derivable from the object level theory and combinatorially sound if
it derives only results derivable from the object level theory. Goal re-ordering will not
affect the soundness or completeness of a logic program (except that it may make
solutions obtainable that would be unobtainable due to being beyond infinite
branches). Metarules that prune the search tree by cutting out some clauses from
being considered will make a metalevel system incomplete, which is not a problem in
GDC, as it does not attempt to be complete. The unknown test in a guard is an
example of a metalevel feature that prunes the results possible. Prolog’s assert is an
example of a metalevel feature that introduces unsoundness. The distinction
commonly made in Prolog between “red cuts” and “green cuts” distinguishes those
usages of cut which affect the completeness of a Prolog program and those usages
where the cut is used purely to cut out search, which the programmer knows will not
lead to solutions and thus will not affect the completeness. The red/green distinction
could usefully be extended to other extra-logical notations: usages that affect the
soundness or completeness being termed red, those which do not being termed green.
A green assert in Prolog, for example, would be one which simply asserts a lemma
for efficiency reasons that could be proved form the existing clauses for the predicate.
A useful general rule in considering proposed metalevel control annotations would be
to accept only those that are capable of just green use.
Van Harmelen’s main classification of metalevel systems, however, concerns the
locus of action: the place in which the system is active at any one point in time. A
metalevel system with object-level inference is one where the main activity is in the
object-level interpreter. This covers those systems where the metalevel interpreter is
implicit and programmer control over it is limited to annotations, such as the various
examples above of Prolog control languages. A metalevel system with metalevel
inference is one where the computation takes place mainly in the metalevel
interpreter. This covers those systems where a full interpreter is available for
inspection and modification, and the attention is on this interpreter manipulating the
object-level program. An intermediate class covers those systems where the locus of
action shifts between the object-level and the metalevel. An example of the
intermediate class is those production systems where control jumps to the metalevel
for conflict resolution. In parallel logic programming, Pandora [Bahgat and Gregory,
1989] is an example of a mixed-level inference system. It behaves in a similar way to
the concurrent logic languages, but if it hits a deadlock, control jumps to a metalevel
deadlock handler [Bahgat, 1992] which resolves the situation by making a non-
deterministic choice.
The final distinction that van Harmelen makes is to distinguish between monolingual
and bilingual metalevel systems. A monolingual system is one where the language at
the metalevel is the same as at the object-level, in particular object-level variables are
mapped into metalevel variables. A bilingual system is one where the object-level
and metalevel languages are distinct, in particular object-level variables are

Meta-Interpretation 259
represented by ground terms at the metalevel. Van Harmelen argues strongly in favor
of bilingual systems on the grounds of clarity. The argument is both informal,
considering the practical and conceptual difficulties of mixing the two levels, and
formal, after Hill and Lloyd’s analysis [1988] which suggested that semantics for
metalevel programs could not be derived while there was a confusion between
metalevel and object-level variables. Hill and Lloyd followed this by introducing a
logic language, Gödel [Hill and Lloyd, 1994], in which there are built-in object-level
and metalevel variables, with predicates at the metalevel operating on object-level
variables which replace the extra-logical predicates of Prolog. The counter-argument
is the simplicity of monolingual interpreters due to not having to make explicit that
which they do not change from the underlying system. Martens and de Schreye
[1995] argue that it is possible to come up with a formal semantics for monolingual
systems.
8.6 Some GDC Monolingual Interpreters
Having discussed the background behind the idea of meta-interpreters and given a
classification, we can now consider the subject on a practical level by considering a
few examples. The following is the vanilla meta-interpreter for GDC:
reduce(X=Y) :- X=Y.
reduce(Actor) :- otherwise
| behavior(Actor, Body), reducelist(Body).
reducelist([]).
reducelist([H|T]) :- reduce(H), reducelist(T).
Since GDC does not have built-in operations for manipulating the behaviors that form
a program, the object level behaviors must be represented in a form that explicitly
marks them out as object-level behaviors. The following would be the representation
for quicksort:
behavior(qsort([],Sorted),Body)
:- Body=[Sorted=[]].
behavior(qsort([Pivot|List],Sorted), Body)
:- Body=[part(List,Pivot,Lesser,Greater),
qsort(Lesser,Lsorted),qsort(Greater,Gsorted),
concatenate(Lsorted,[Pivot|Gsorted],Sorted)].
behavior(part([],Pivot,Lesser,Greater),Body)
:- Body=[ Lesser=[],Greater=[]].
behavior(part([Item|List],Pivot,Lesser,Greater),Body)
:- Pivot=<Item
| Body=[ Greater=[Item|Upper],part(List,Pivot,Lesser,Upper)].
behavior(part([Item|List],Pivot,Lesser,Greater),Body)
:- Item=<Pivot
| Body=[Lesser=[Item|Lower],part(List,Pivot,Lower,Greater)].
behavior(concatenate([],List,Total), Body)
:- Body=[Total=List].
behavior(concatenate([Item|List1],List2,Total), Body)

260 Chapter 8
:- Body=[Total=[Item|List],concatenate(List1,List2,List)].
Note that in this interpreter the concurrency of the object level maps implicitly onto
the concurrency of the metalevel, the concurrency of the second behavior for
reducelist giving the concurrency of the object level. Behavior commitments at the
object level map implicitly onto the commitment of the actor in the second behavior
of reduce. Object level guards represent metalevel guards. The unification primitive
at the object-level maps onto the unification primitive of the first behavior for
reduce. Further primitive operations could be covered in a similar way to unification
by adding behaviors to reduce.
A number of simple interpreters may be derived from the above meta-interpreter
[Safra and Shapiro, 1986]. The following, for example, uses the “short-circuit”
technique to report when execution of an actor has completed:
reduce(X=Y,Left,Right)
:- (X,Right)=(Y,Left).
reduce(Actor,Left,Right) :- otherwise
| behavior(Actor,Body),
reducelist(Body,Left,Right).
reducelist([],Left,Right)
:- Right=Left.
reducelist([H|T],Left,Right)
:- reduce(H,Left,Middle),
reducelist(T,Middle,Right).
The initial call to the interpreter will take the form :- reduce(Actor,done,Flag). The
message done is sent on the channel Flag only when execution of all actors spawned
by the actor execution has completed. Note the assumption in the first behavior for
reduce is that the component parts of the unification can be assumed to be done
simultaneously (atomic unification). If this is not the case, we need to ensure that the
short-circuit is closed only when the unification of the two object level messages has
been completed. In this case we will need to use a system primitive which performs
unification on its first two arguments and binds a flag channel given as its third
argument, the message being sent only when the unification is complete. Assuming
the message done is sent on the flag channel following unification, this will give us
the following:
reduce(X=Y,Left,Right)
:- unify(X,Y,Flag), close(Flag,Left,Right).
close(done,Left,Right) :- Left=Right.
Similar flag-message sending versions of any other system primitives will be
required.
The short-circuit technique can be used to give sequential execution. If we want a
pair of actors to execute sequentially, we will not start execution of the second until
execution of the first has completely finished. The following meta-interpreter
enforces sequential execution:
reduce(X=Y,Flag)

Meta-Interpretation 261
:- (X,Flag)=(Y,done).
reduce(Actor,Flag)
:- otherwise
| behavior(Actor, Body),
reducelist(Body,Flag).
sequential_reducelist(List,done,Flag)
:- reducelist(List,Flag).
reducelist([],Flag)
:- Flag=done.
reducelist([H|T],Flag)
:- reduce(H,Flag1),
sequential_reducelist(T,Flag1,Flag).
The initial call is :- reduce(Actor,Flag) where Flag is an unbound channel.
In the GDC meta-interpreter above, the selection of a behavior to execute an actor
was mapped implicitly onto GDC’s own behavior selection mechanism. If, however,
we wish to override the built-in behavior-selection mechanism we must explicitly
program in a replacement behavior-selection mechanism. As an example, consider a
meta-interpreter where GDC’s indeterminism is resolved by offering a choice
between the behaviors, which may reduce an actor. Interpreters like this may be used
for debugging purposes letting the human user who is investigating different ways of
resolving the indeterminacy make the choice. Alternatively, we could have another
layer of meta-interpreter that selects between behaviors, essentially the same idea as
the conflict-resolution mechanism in production systems.
The following gives the top level:
reduce(X=Y)
:- X=Y.
reduce(Actor)
:- otherwise
| behaviors(Actor, Behaviors),
possbodies(Actor, Behaviors, Possibilities),
select(Actor, Possibilities, Body),
reducelist(Body).
reducelist([]).
reducelist([H|T])
:- reduce(H),
reducelist(T).
Here behaviors(Actor,Behaviors) is intended to give all behaviors for a possible
actor. The actor possbodies(Actor,Behaviors,Possibilities) will return in
Possibilities the bodies of all behaviors in Behaviors to which Actor may commit.
The actor select(Actor,Possibilities,Body) will select one of these possibilities.
In this conflict-resolution interpreter, it will be assumed, for convenience, that each
behavior in the list of behaviors given by behaviors contains distinct channels and
only behaviors with empty guards will be handled. Behaviors are represented by

262 Chapter 8
(Head, Body) pairs. Thus the program for non-deterministic merge would be
represented by:
behaviors(merge(X0,Y0,Z0), Behaviors)
:- Behaviors=[
(merge(X1,[],Z1),[Z1=X1]),(merge([],Y2,Z2),[Z2=Y2]),
(merge([H3|T3],Y3,Z3),[merge(T3,Y3,Z13), Z3=[H3|Z13]]),
(merge(X4,[H4|T4],Z4),[merge(X4,T4,Z14), Z4=[H4|Z14]])].
In order to gain a list of possible behavior bodies in possbodies, the OR-
parallelism of the object-level needs to be simulated by AND-parallelism at the
metalevel as described in Chapter 6. The behavior selection mechanism is made
explicit, involving an explicit call to a match actor which performs the matching
which is done implicitly in GDC execution. In this case, match as well as receiving
messages in the behavior head also sends on a flag channel the message true if the
match succeeds and false otherwise:
possbodies(Actor, [(Head,Body)|Rest], Poss)
:- match(Actor, Head, Flag),
possbodies(Actor, Rest, RPoss),
addposs(Flag, Body, RPoss, Poss).
possbodies(Actor, [], Poss) :- Poss=[].
The actor addposs simply adds a behavior body (with channels appropriately
bound) to the list of possibilities if matching succeeds:
addposs(false,_,RPoss,Poss)
:- Poss=RPoss.
addposs(true,Body,RPoss,Poss)
:- Poss=[Body|Poss].
Although it would be possible to provide a version of match as a system primitive, it
may be programmed directly:
match(X, Y, V) :- unknown(Y) | Y=X,V=true.
match(X, Y, V) :- X=Y | V=true.
match(X, Y, V) :- X=/=Y | V=false.
match(X, Y, V) :- list(X), list(Y) | matchlist(X, Y, V).
match(X, Y, V) :- tuple(X), tuple(Y)
| X=..LX, Y=..LY, matchlist(LX, LY, V).
matchlist([], [], V) :- V=true.
matchlist([H1|T1], [H2|T2],V)
:- match(H1, H2, VH), matchlist(T1, T2, VT) and(VH, VT, V).
matchlist(X, Y, V) :- unknown(Y) | Y=X, V=true.
and(true, true, V) :- V=true.
and(false, _, V) :- V=false.
and(_, false, V) :- V=false.
While this meta-interpreter is more complex than previous ones, a large amount of
the object-level GDC still maps implicitly onto metalevel GDC. In particular there is
no direct reference to the scheduling of actors or the suspension mechanism. The

Meta-Interpretation 263
scheduling of the object-level GDC is whatever is provided by the metalevel GDC. A
suspension in the object-level GDC will map into a suspension of the metalevel GDC
in the match actor of the meta-interpreter, when X is unbound but Y is bound so the
guards X==Y and X=/=Y are both suspended until X becomes sufficiently bound for
them to resolve. It is assumed that select will only present a menu of possible bodies
to resolve an actor when there are no suspensions for that actor. Note that it is a
context free selection as the set of actors awaiting execution remains implicit, so it is
not an explicit object that can be viewed when making a behavior selection. The
order in which the selection menus are presented will in effect be the scheduling
order, which is not under user control.
A further development would be to introduce an explicit scheduling list. This could
be used to give a meta-interpreter that implements the actor priorities of Chapter 6.
The following meta-interpreter does this. The idea is that the top-level actor network
is:
:- reduce(Actor/Priority,S), scheduler(S)
where S is a stream of messages of the form req(Priority,Go). These messages are
generated by the reduce actor and consumed by the scheduler actor. As generated
Go is unbound in the messages. The scheduler binds these channels in the order
determined by Priority. It is assumed that a behavior body consists of a list of
actor/priority pairs. A priority could be a constant or a channel which is bound during
execution.
The scheduler actor will keep an explicit list of priority requests, which will in effect
form the explicit scheduling list. The wait actor will ensure that behavior selection is
suspended until allowed by the scheduler since it cannot proceed until the request
channel is bound. Streams of requests are merged using conventional stream merging:
reduce(X=Y, S) :- X=Y, S=[].
reduce(Actor/Priority, S)
:- S=[req(Priority,Go)|S1],
behaviors(Actor,Behaviors),
wait(Go,Actor,Behaviors,Body),
reducelist(Body,S1).
reducelist([],S) :- S=[].
reducelist([H|T],S)
:- reduce(H,S1), reducelist(T,S2), merge(S1,S2,S).
wait(go,Actor,Behaviors,Body)
:- possbodies(Actor,Behaviors,Possibilities),
select(Actor,Possibilities,Body).
This interpreter is deficient because there are no limits on the scheduler. The
scheduler could just authorize every actor to proceed to behavior selection as soon as
it receives the actor’s request. This defeats the purpose of the interpreter, since given
a limited number of processors scheduling would default to whichever order is
decided by the underlying system. In order to give user-defined scheduling we need
to authorize only enough actors to keep the processors busy. To do this, the scheduler

264 Chapter 8
would need to know how many of the current set of actors are suspended on all their
possible messages and thus not consuming any processor resources. This could be
done with a version of match, but would require an explicit handling of suspensions
rather than the implicit mapping of objectlevel suspensions to metalevel suspensions.
Rather than suspend, match would terminate and return a list of channels and
messages to which they must be bound for the actor to be woken.
An interpreter that explicitly handled suspensions could either use busy-waiting,
continually testing whether a channel whose value is required has become bound, or
non-busy-waiting, in which a list of suspended actors is associated with each unbound
channel and the actors woken when the channel becomes bound. Such a meta-
interpreter would be considerably more complex than the simple meta-interpreters
with which we started, but it still relies on implicit mapping from metalevel to object
level of store allocation and garbage collection.
Another variant of the meta-interpreter that explicitly gives a selection between
behaviors to resolve an actor is one that illustrates the effect of choosing each
possible behavior. This is referred to as an all-solutions interpreter since it will give
all possible bindings of some channel in an actor. For a more detailed discussion of
this problem see [Ueda, 1987]. The way the all-solutions interpreter below works is
to maintain a list of actors and a list of partial solutions. When an actor may be
resolved in one of several ways a duplicate of these lists, or continuation, is made to
represent the position in the computation that would be obtained by choosing each
alternative. The continuation will rename each channel (so that, for example, the list
[X,X,Y] would become [X1,X1,Y1]), we will assume we have a primitive copy
which creates such a copy with renamed channels. The list of possible solutions is
obtained by appending together the list of solutions obtained from each continuation.
allsols(Actor,TermSols) :- reduce([Actor],[Term],Sols).
reduce([],Terms,Sols) :- Sols=Terms.
reduce([X=Y|Actors],Terms,Sols)
:- X=Y, reduce(Actors,Terms,Sols).
reduce([Actor|Actors],Terms,Sols)
:- otherwise
| behaviors(Actor,Behaviors),
reducewith(Actor,Actors,Behaviors,Terms,Sols).
reducewith(Actor,Actors,[(Head,Body)|Rest],Terms,Sols)
:- match(Actor,Head,Flag),
reduceon(Flag,Actors,Body,Rest,Terms,Sols1),
reducewith(Actor,Actors,Rest,Terms,Sols2),
append(Sols1,Sols2,Sols).
reducewith(Actor,Actors,[],Terms,Sols) :- Sols=[].

Meta-Interpretation 265
reduceon(true,Actors,Body,Rest,Terms,Sols)
:- append(Body,Actors,Actors1),
copy([Terms,Actors1],[Terms2,Actors2]),
reduce(Actors2,Terms2,Sols).
reduceon(false,Actors,Body,Rest,Terms,Sols) :- Sols=[].
The effect of a call allsols(Actor,Term,Sols) is to bind Sols to a list of the different
instances of Term given by all possible evaluations of Actor. For example, a call
allsols(merge([a,b],[c],X),X,Sols) will cause Sols to become bound to
[[a,b,c],[a,c,b],[c,a,b]], assuming we have the representation of non-deterministic
merge given previously.
In the interpreter reducewith matches an actor against the heads of each of the
behaviors for that actor. If matching succeeds, reduceon sets up a reduce actor to
construct all solutions which involve this particular matching. Note that the code
interpreted by this interpreter is limited to examples which do not require any
suspensions since reduceon which initiates solution of the remaining actors remains
suspended until matching has completed and sent the message true or false on the
channel Flag. Since matching does not bind channels in the actor, it is safe to leave
the construction of a continuation until after matching has completed successfully,
thus avoiding unnecessary copying for cases where matching fails.
8.7 GDC Bilingual Interpreters
The problems with monolingual interpreters became more apparent in Section 8.6.
The mapping of object-level variables to metalevel variables resulted in the need to
introduce a variety of extra-logical primitives, culminating in copy in the all-
solutions interpreter for general logic programs. The problem is that a single GDC
variable with its single-assignment property cannot be used to model a variable in a
logic language with non-deterministic backtracking as such a variable can be
reassigned its value on backtracking. What is needed is a separate representation of
object-level variables by ground terms at the metalevel, that is a bilingual interpreter.
In fact we have already seen a range of bilingual interpreters in Chapter 6. Search
programs specifically for the 8-puzzle were generalized generic search programs that
could be used for any system where a state is rewritten non-deterministically by a set
of rewrite rules. We could therefore consider the rules by which the successors to a
state are generated in the successors actor in Chapter 6 to be the object level
program and the various search programs to be metalevel programs.
While the object-level rules in Chapter 6 could be simple rules for showing the
possible changes of state in something like the 8-puzzle, they could equally well be a
complete set of rewrite rules specifying how a set of sentences in logic could be
changed using resolution. This would then make these rules themselves a
metaprogram, with the logic sentences being the object-level programs and the search
programs meta-metaprograms. If the search program used involved priorities and
these were implemented using a meta-interpreter as suggested above, this interpreter
would be a meta-meta-metalevel interpreter for the logic sentences. Note that this

266 Chapter 8
four-leveled layering of interpreters corresponds to the proposed four layers in the
KADS methodology for knowledge-based systems development noted previously.
Below is a simple implementation of Chapter 6’s successors for the case where the
state stored in a node in the search tree is a list of Goals in a Prolog-like language,
together with an environment giving the values of variables in the Goals. It is
assumed that variables in the Goals are represented by ground terms in GDC:
successors(state([Goal|Goals],Env), Succs)
:- Goal=..[Functor|Args],
clauses(Functor,Clauses),
expandGoal(Args,Goals,Env,Clauses,Succs).
expandGoal(Args,Goals,Env,[],Succs) :- Succs=[].
expandGoal(Args,Goals,Env,[clause(Head,Body,Vars)|Clauses],Succs)
:- append(Vars,Env,Env2),
unify(Args,Head,Env2,Env1,Flag),
expandGoal1(Flag,Args,Goals,Body,Env,Env2,Clauses,Succs).
expandGoal1(false,Args,Goals,Body,Env,Env1,Clauses,Succs)
:- expandGoal(Args,Goals,Env,Clauses,Succs).
expandGoal1(true,Args,Goals,Body,Env,Env1,Clauses,Succs)
:- append(Body,Goals,Goals1),
expandGoal(Args,Goals,Env,Clauses,Succs1),
Succs=[state(Goals1,Env1)|Succs1].
Here, the actor clauses returns a representation of the clauses associated with the
input goal name in the form of a list of triples. Each of these contains the head
arguments in list form, the body of the clause and a separate environment for the
variables in the clause (assuming a mechanism to make these fresh variables) each
linked with the value unbound. Clearly the issol required in the search programs in
Chapter 6 returns a solution found when the list of outstanding goals becomes empty:
issol(state([],Env),Flag) :- Flag=true.
issol(state([Goal|Goals],Env),Flag) :- Flag=false.
It can be seen that this version of successors always takes the first goal from the
list of outstanding goals and appends the body of any clause which it matches to the
front of the remaining goals. Therefore the goal ordering of Prolog is built-in. The
clause ordering is not, however, built-in since it will depend on the order in which the
search tree is searched. The search order also is not built-in and is determined at the
level of the search program.
The GDC code for unify sends true in its fifth argument if its first and second
arguments unify with the variable bindings of the environment of its the third
argument, giving the updated variable bindings as output in the fourth argument. If
unification is not possible, false is returned in the fifth argument, otherwise true is
returned here. This flag value is passed into expandGoal1, which adds a successor
state to the list of successor states if a successful unification was achieved.

Meta-Interpretation 267
If a variable at the object level is represented by the ground term var(<name>)
where <name> is some constant unique for each separate variable and environment
is a list of <name>/<value> pairs, the following code will implement unify:
unify([H1|T1],[H2|T2],IEnv,OEnv,Flag)
:- unify(H1,H2,IEnv,MEnv,Flag1),
unify1(Flag1,T1,T2,MEnv,OEnv,Flag).
unify(X1,X2,IEnv,OEnv,Flag) :- X1==X2 | OVars=IVars, Flag=true.
unify(var(A),var(B),IEnv,OEnv,Flag)
:- lookup(A,IEnv,AVal), lookup(B,IEnv,BVal),
unifyvars(A,B,IEnv,AVal,BVal,OVars,Flag).
unify(var(A),X2,IEnv,OEnv,Flag) :- X2=/=var(B)
| lookup(A,IEnv,AVal), setvar(A,AVal,X2,IVars,OVars,Flag).
unify(X1,var(A),IEnv,OEnv,Flag) :- X1=/=var(B)
| lookup(A,IVars,AVal), setvar(A,AV,X1,IEnv,OEnv,Flag).
unify(X1,X2,IEnv,OEnv,Flag) :- X1=/=var(A), X2=/=var(B), X1=/=X2
| Flag:=false, OEnv=IEnv.
unify1(false,X1,X2,IEnv,OEnv,Flag) :- Flag=false.
unify1(true,X1,X2,IEnv,OEnv,Flag)
:- unify(X1,X2,IEnv,OEnv,Flag).
unifyvars(A,B,IEnv,unbound,BVal,OEnv,Flag) :- BVal=/=unbound
| bind(A,BVal,IEnv,OEnv), Flag=true.
unifyvars(A,B,IEnv,AVal,unbound,OEnv,Flag) :- AVal=/=unbound
| bind(B,AVal,IEnv,OEnv), Flag=true.
unifyvars(A,B,IEnv,unbound,unbound,OEnv,Flag) :- A<B
| bind(B,var(A),IEnv,OEnv), Flag=true.
unifyvars(A,B,IVars,unbound,unbound,OEnv,Flag) :- A>B
| bind(A,var(B),IEnv,OEnv), Flag=true.
unifyvars(A,B,IEnv,AVal,BVal,OEnv,Flag)
:- AVal=/=unbound, BVal=/=unbound
| unify(AVal,BVal,IEnv,OEnv,Flag).
lookup(A,[B/Val|Env],AVal) :- A==B | AVal=Val.
=/=
lookup(A,[B/Val|Env],AVal) :- A B | lookup(A,Env,AVal).
setvar(A,unbound,X,IEnv,OEnv,Flag)
:- Flag=true, bind(A,X,IEnv,OEnv).
setvar(A,var(B),X,IEnv,OEnv,Flag)
:- lookup(B,IVars,BVal), setvar(B,BVal,X,IEnv,OEnv,Flag).
setvar(A,V,X,IEnv,OEnv,Flag) :- V==X
| Flag=true, OEnv=IEnv.
setvar(A,[HV|TV],[HX|TX],IEnv,OEnv,Flag)
:- unify(HV,HX,IEnv,MEnv,Flag1),
unify1(Flag1,TV,TX,MEnv,OEnv,Flag).

268 Chapter 8
setvar(A,[H|T],X,IEnv,OEnv,Flag) :- X=/=[HX|TX]
| Flag=false, OEnv=IEnv.
setvar(A,V,[HX|TX],IEnv,OEnv,Flag) :- V=/=[HV|TV], V=/=var(B)
| Flag=false, OEnv=IEnv.
setvar(A,V,X,IEnv,OEnv,Flag) :- X=/=[HX|TX], X=/=V, V=/=var(B)
| Flag=false, OEnv=IEnv.
bind(A,AVal,[B/BVal|Env],Env1) :- A==B
| Env1=[A/AVal|Env].
=/=
bind(A,AVal,[B/BVal|Env],Env1) :- A B
| bind(A,AVal,Env,Env2), Env1=[B/BVal|Env2].
The cost of the bilingual interpreter in having to implement unification completely
rather than inheriting any unification from the underlying system is apparent.
However, the division into layers means that once we have constructed this layer
implementing the resolution and unification, it may be incorporated with any of the
search programs in Chapter 6 which will add more control and also give the precise
nature of the output. For example, it could be used to give a single solution or all
solutions. One point to note is that the bilingual nature of the interpreter means that it
avoids use of extra-logical primitives, such as the copy that was needed in our all-
solutions interpreter above and is also needed in the OR-parallel Prolog interpreter
proposed by Shapiro [1987]. The importance of this will become more apparent when
partial evaluation of meta-interpreters is considered in Chapter 9.
In order to duplicate exactly Prolog’s search order though, a search program is
required that searches in depth-first order on demand, which was not given in Chapter
6. The following version of search will do this:
search(State,[],OutSlots) :- OutSlots=[].
search(State,[Slot|InSlots],OutSlots)
:- issol(State,Flag),
expand(Flag,State,[Slot|InSlots],OutSlots).
expand(true,State,[Slot|InSlots],OutSlots)
:- solution(State,Slot), OutSlots=InSlots.
expand(false,State,InSlots,OutSlots)
:- successors(State,States),
branch(States,InSlots,OutSlots).
branch([],InSlots,OutSlots) :- OutSlots=InSlots.
branch([H|T],InSlots,OutSlots)
:- search(H,InSlots,MidSlots),
branch(T,MidSlots,OutSlots).
Here the second input to search is a list of unbound channels or slots. Prolog-like
sequential clause will occur because no expansion of the right branch of the search
tree will take place until search of the left branch has completed and failed to fill the
slots available by binding them. An OR-parallel effect can be gained if this condition
is relaxed and search of the right-branch is allowed when it is not known whether a
solution will be found in the left branch. Adding the following clause:

Meta-Interpretation 269
search(State,InSlots,OutSlots)
:- unknown(InSlots)
| issol(State,Flag), expand(Flag,State,InSlots,OutSlots).
will achieve this, since it means that a node in the search tree will be expanded when
the binding status of the slots passed to it is unknown.
8.8 An Interpreter for Linda Extensions to GDC
As a final example of a meta-interpreter for a guarded definite clause language, an
interpreter is described which adds Linda extensions [Gelernter, 1985] to GDC.
According to Gelerntner, the Linda notation is a set of simple primitives, which may
be added to any programming language to introduce concurrency into it. The basis of
these notations is that a dynamic database of tuples exists. Actors communicate by
asserting, reading and retracting tuples from this database, it may therefore be
considered a blackboard system [Engelmore and Morgen, 1988]. The Linda
extensions are eval(P), which sets up P as an actor, out(T) which adds the tuple T to
the database, in(T) which removes the tuple T from the database and rd(T) which
reads the tuple T from the database. In the case of in and rd, the tuple argument may
contain unbound variables and there will be a search for a matching tuple in the
database; when a match is found the variables in the argument will be bound to the
matching values. If no match is found for in or rd the actor which made the call is
suspended until another actor adds a matching tuple using out, the suspended in or rd
call is then evaluated and the actor which made the in or rd call restarted.
The reason for paying particular attention to implementing Linda extensions to GDC
is that Linda has been proposed as a competitor [Carriero and Gelernter, 1989] to
GDC. It has achieved popularity in use as a concurrent programming paradigm,
though this may be because it can be grafted onto existing languages and thus there is
less of a barrier to using it than changing to a novel concurrent language.
Nevertheless, the simplicity of the conceptual model of Linda has led to it being put
forward as another way of introducing concurrency into logic programming [Brogi
and Cincanini, 1991]. The use of interpreters moves away from “language wars” to
the idea of multi-paradigm programming in which different parts of a program may
be expressed in whichever paradigm is most suitable for them. Correspondingly,
GDC equipped with a range of interpreters is a multi-paradigm language. The next
section shows how functional programming may be embedded in GDC using an
interpreter while in Chapter 9 an interpreter for an imperative language is given.
Linda extensions may be added to GDC by using an interpreter that passes on a
stream of the database handling commands to a database-handling actor. Each actor
that is interpreted will produce a stream of requests to the database. Non-primitive
actors will merge the streams from the subactors into which they reduce. The Linda
primitives will produce a stream consisting of a single database request. Other
primitives will produce an empty stream. Since in GDC all actors are concurrent,
there is no need for an explicit eval primitive. The following is the interpreter:

270 Chapter 8
reduce(X=Y,S) :- X=Y, S=[].
reduce(in(M),S) :- S=[in(M)].
reduce(rd(M),S) :- S=[rd(M)].
reduce(out(M),S) :- S=[out(M)].
reduce(Actor,S)
:- otherwise
| behavior(Actor,Body), reducelist(Body,S).
reducelist([], S) :- S=[].
reducelist([H|T],S)
:- reduce(H, S1), reducelist(T,S2), merge(S1,S2,S).
The top level actor network would be
:- reduce(Actor,Stream), database(Stream).
The database handler needs to keep two lists of tuples. One will be tuples currently in
the database. The other will be a list of in and rd requests that are suspended waiting
for a tuple to be added. When a tuple is added it is matched against all the suspended
in and rd requests. If it matches a suspended in request, it is not taken any further
since this in request will cause it to be removed from the database. The matching used
is similar to the matching we used in the meta-interpreters previously, except that we
need to overcome the problem that matching could fail after binding some channels.
The interpreter is monolingual, so if the binding took place it could not be undone if
matching failed later. We reduce the problem by using a version of match which
rather than bind any channels returns a list of channels which would be bound and
values to which they would be bound if the matching succeeds. If matching does
succeed, these bindings take place. This gives the following as the complete database
handler:
// Handle an out message by checking against all waiting in and rd
// messages. If it has not been matched with a waiting in message,
// the tuple is added to the database of tuples.
database([out(M)|S],Waits,Tuples)
:- checkwaits(M, Waits,OutWaits,Found),
addtuple(Found,S,M,OutWaits,Tuples).
// Handle an in message by checking against the database of
// tuples. If there are no matches, the in message is added to the
// list of waiting in and rd requests.
database([in(M)|S],Waits,Tuples)
:- checktuples(M,Tuples,OutTuples,Found),
addwait(Found,S,M,Waits,OutTuples).
// Handle a rd message similarly to an in message.
database([rd(M)|S],Waits,Tuples)
:- check(M,Tuples,Found), addrd(Found, S, M, Waits, Tuples).
addtuple(no,S,M,Waits,Tuples)
:- database(S,Waits,[M|Tuples]).
addtuple(yes,S,M,Waits,Tuples)
:- database(S,Waits,Tuples).

Meta-Interpretation 271
addwait(no,S,M,Waits,Tuples)
:- database(S,[in(M)|Waits],Tuples).
addwait(yes,S,M Waits,Tuples)
:- database(S,Waits,Tuples).
addrd(no,S,M,Waits,Tuples)
:- database(S,[rd(M)|Waits],Tuples).
addrd(yes,S,M,Waits,Tuples)
:- database(S,Waits,Tuples).
// Check a tuple against waiting in and rd requests. If it is
// matched successfully against an in request Found is bound to
// “yes”, the in request is removed from the list of waiting
// requests and no further checking is done. If it is successfully
// matched against a waiting rd request, the request is removed
// but checking against further requests continues. If all
// requests are checked and no successful matching with an in
// request occurs, Found is bound to “no”.
checkwaits(M,[in(N)|Waits],OutWaits,Found)
:- match(M,N,Flag,Matches),
isinmatch(Flag,Matches,M,N,Waits,OutWaits,Found).
checkwaits(M,[rd(N)|Waits],OutWaits,Found)
:- match(M,N,Flag,Matches),
isrdmatch(Flag,Matches,M,N,Waits,OutWaits,Found).
checkwaits(M,[],OutWaits,Found)
:- Found=no, OutWaits=[].
isinmatch(true,Matches,M,N,Waits,OutWaits,Found)
:- Found=yes, domatches(Matches), OutWaits=Waits.
isinmatch(false,Matches,M,N,Waits,OutWaits,Found)
:- checkwaits(M,Waits,OutWaits1,Found),
OutWaits=[in(N)|OutWaits1].
isrdmatch(true,Matches,M,N,Waits,OutWaits,Found)
:- domatches(Matches), checkwaits(M,Waits,OutWaits,Found).
isrdmatch(false,Matches,M,N,Waits,OutWaits,Found)
:- checkwaits(M,Waits,OutWaits1,Found),
OutWaits=[rd(N)|Outwaits1].
// Check an in request against the database of tuples.
// If a match is found the matching tuple is taken from the
// database of tuples and Found is bound to “yes”. Otherwise
// Found is bound to “no”.
checktuples(M,[N|Tuples],OutTuples,Found)
:- match(N,M,Flag,Matches),
ismatch(Flag,Matches,M,N,Tuples,OutTuples,Found).

272 Chapter 8
checktuples(M,[],OutTuples,Found)
:- Found=no, OutTuples=[].
// Perform the channel binding if matching succeeds.
ismatch(true,Matches,M,N,Tuples,OutTuples,Found)
:- domatches(Matches), OutTuples=Tuples, Found=yes.
ismatch(false,Matches,M,N,Tuples,OutTuples,Found)
:- checktuples(M,Tuples,OutTuples1,Found),
OutTuples=[N|OutTuples1].
domatches([Y/X|Matches]) :- Y=X, domatches(Matches).
domatches([]).
// Check a rd request against the database of tuples, bind Found
// to “yes” if a match is found, to “no” otherwise.
check(M,[N|Tuples],Found)
:- match(N,M,Flag,Matches),
isfound(Flag,Matches,M,Tuples,Found).
check(M,[],Found) :- Found=no.
isfound(true,Matches,M,Tuples,Found)
:- Found=yes, domatches(Matches).
isfound(false,Matches,M,Tuples,Found) :- check(M,Tuples,Found).
// A version of match which binds V to “true” if matching
// succeeds, “false”otherwise and which returns a list of
// channel bindings to be performed only if the complete match
// succeeds.
match(X,Y,V,Matches) :- unknown(Y) | Matches=[Y/X], V=true.
match(X,Y,V,Matches) :- X==Y | V=true, Matches=[].
match(X,Y,V,Matches) :- X=/=Y | V=false, Matches=[].
match(X,Y,V,Matches) :- list(X), list(Y)
| matchlist(X,Y,V,Matches).
match(X,Y,V,Matches) :- tuple(X), tuple(Y)
| X=..LX, Y=..LY, matchlist(LX,LY,V,Matches).
matchlist([],[],V,Matches) :- V=true, Matches=[].
matchlist([H1|T1],[H2|T2],V,Matches)
:- match(H1,H2,VH,Matches1), matchlist(T1,T2,VT,Matches2),
andp(VH,VT,V), merge(Matches1,Matches2,Matches).
matchlist(X,Y,V,Matches) :- unknown(Y)
| Matches=[Y/X], V=true.
andp(true,true,V) :-V=true.
andp(false,_,V) :- V=false.
andp(_,false,V) :- V=false.

Meta-Interpretation 273
The behavior representation below will reduce the Dining Philosophers problem
(Section 4.12) in a way similar to that described in [Carriero and Gelernter, 1989].
The idea is that a chopstick available for use is represented by a tuple in the database.
When a philosopher actor wishes to use a chopstick, an in command for the chopstick
is issued. If the chopstick is already in use by another philosopher the philosopher
actor will suspend until that other philosopher has finished with the chopstick and
issued an out command on it, putting it into the tuple database and awakening the in
command. To avoid deadlock, only four philosophers are allowed in the dining room
at any time. Initially, this is represented by having four meal tickets in the database.
A philosopher must issue an in command on a meal ticket and receive it before
entering the dining room, the ticket is put out again when the philosopher finishes
eating. Philosophers are represented by the indices of the chopsticks they use to eat.
behavior(hungryphil(hungry,F1,F2),Body)
:- Body=[in(ticket(T)),enteringphil(T,F1,F2)].
behavior(enteringphil(ticket,F1,F2),Body)
:-Body=[in(chopstick(F1,T1)),in(chopstick(F2,T2)),
eatingphil(T1,T2,F1,F2)].
behavior(eatingphil(chopstick,chopstick,F1,F2), Body)
:- Body=[eat(E), exitingphil(E,F1,F2)].
behavior(exitingphil(full,F1,F2), Body)
:- Body=[out(chopstick(F1,chopstick)),
out(chopstick(F2,chopstick)),
out(ticket(ticket)), thinkingphil(F1,F2)].
behavior(thinkingphil(F1,F2), Body)
:- Body=[think(H),hungryphil(H,F1,F2)].
behavior(init, Body)
:- Body=[out(chopstick(1,chopstick)),
out(chopstick(2,chopstick)),out(chopstick(3,chopstick)),
out(chopstick(4,chopstick)),out(chopstick(5,chopstick)),
out(ticket(ticket)),out(ticket(ticket)),
out(ticket(ticket)),out(ticket(ticket)),
thinkingphil(1,2),thinkingphil(2,3),thinkingphil(3,4),
thinkingphil(4,5),thinkingphil(5,1)].
Note that here it has been necessary to include explicit sequencing in the interpreted
program. For example a meal ticket is represented by the 1-tuple ticket(ticket) rather
than the 0-tuple ticket. A message in(ticket(T)) will bind T to ticket when a tuple
ticket(ticket) is in the database. The actor enteringphil(T,F1,F2) will suspend until
T is bound. Without this sequencing the calls in(ticket) and enteringphil(F1,F2)
would proceed in parallel. That is, a philosopher would not wait for the meal ticket to
become available. Similarly, the n-th chopstick is represented by the tuple
chopstick(n,chopstick) rather than just chopstick(n). It is assumed that think(H)
will bind H to hungry after a suitable interval of time and eat(E) will similarly bind
E to full.
A more complex form of the interpreter would make the sequencing implicit, using a
similar technique to that we used to introduce sequentiality previously. In this case, it

274 Chapter 8
is necessary to introduce the explicit primitive eval for the cases where we want a
concurrent actor to be spawned:
reduce(X=Y,S,Flag) :- unify(X,Y,Flag), S=[].
reduce(in(M),S,Flag) :- S=[in(M,Flag)].
reduce(rd(M),S,Flag) :- S=[rd(M,Flag)].
reduce(out(M),S,Flag) :- S=[out(M,Flag)].
reduce(eval(T),S,Flag) :- reduce(T,S,_), Flag=done.
reduce(Actor,S,Flag) :- otherwise
| behavior(Actor,Body), reducelist(done,Body,S,F).
reducelist(Flag1,[],S,Flag2) :- S=[], Flag2=Flag1.
reducelist(done,[H|T],S,Flag)
:- reduce(H,S1,Flag1),
reducelist(Flag1,T,S2,Flag),
merge(S1,S2,S).
Note that the Flag channel is added to the in, rd and out messages passed to the
database handler. It is assumed that the database handler will bind Flag to done
when the operation is completed. In the case of in and rd messages if there is no
matching tuple in the database, the requests will be queued as before, each with its
associated flag and the flag eventually will be bound when a matching tuple is added
by an out message.
Using this interpreter the program for the dining philosophers is:
behavior(hungryphil(F1,F2),Body)
:- Body=[in(ticket),enteringphil(F1,F2)].
behavior(enteringphil(F1,F2),Body)
:- Body=[in(chopstick(F1)),in(chopstick(F2)),eatingphil(F1,F2)].
behavior(eatingphil(F1,F2),Body)
:- Body=[eat,exitingphil(F1,F2)].
behavior(exitingphil(F1,F2),Body)
:- Body=[out(chopstick(F1)),out(chopstick(F2)),out(ticket),
thinkingphil(F1,F2)].
behavior(thinkingphil(F1,F2),Body)
:- Body=[think,hungryphil(F1,F2)].
behavior(init,Body)
:- Body=[out(chopstick(1)), out(chopstick(2)),
out(chopstick(3)), out(chopstick(4)),
out(chopstick(5)), out(ticket), out(ticket), out(ticket),
out(ticket), eval(thinkingphil(1,2)),
eval(thinkingphil(2,3)), eval(thinkingphil(3,4)),
eval(thinkingphil(4,5)), eval(thinkingphil(5,1))].
8.9 Parallelization via Concurrent Meta-interpretation
As the Linda extension interpreter indicates, the underlying parallelism in GDC may
be used through interpreters to provide parallelism in a form which is not directly

Meta-Interpretation 275
provided in GDC itself. Huntbach, [1991] gives an interpreter which models in GDC
the explicit message-passing parallelism of Occam, the transputer language based on
Dijkstra’s CSP [Dijkstra, 1975]. But the implicit parallelism in GDC may be used to
realize parallelism which exists implicitly in another language, through the use of a
GDC interpreter for that language.
Landin’s usage of lambda calculus as a metalanguage for describing the semantics of
Algol and the more direct basis of the functional languages on lambda calculus was
noted in Section 8.1. Landin proposed the abstract SECD machine to evaluate lambda
calculus expressions. The SECD machine reifies much of the control aspects of
lambda calculus evaluation by using explicit stacks, which can be seen as a sacrifice
of generality for the sake of efficiency. Because the control of the SECD machine is
explicit, it does not parallelize without modification. McCarthy’s Eval/Apply
interpreter [McCarthy, 1960] is more general. As a Lisp-like interpreter for Lisp, it
can be seen as another part of his interest in meta-interpreters discussed with respect
to Algol, in this case mapping the recursion of the functional language implicitly onto
the recursion of the interpreter. A GDC version of the Eval/Apply interpreter will
automatically parallelize lambda calculus evaluation, since the control is minimally
specified. Incorporation of such an interpreter for those problems where the power of
functional programming, particularly higher order functions, is useful, may be seen as
an alternative to developing a new language which explicitly combines logic and
functional programming [Belia and Levy, 1986].
The lambda calculus interpreter given below is based on one given by Field and
Harrison [1988]. Variables are stored in an explicit environment, similar to the
environments used to build an interpreter for a backtracking logic language in Section
8.7. The beta-reduction mechanism is implemented by adding the bindings for the
bound variable to the environment rather than actual textual substitution. Correct
binding of variables is achieved by the standard method of constructing a closure in
which an abstraction is linked with an environment giving values for any free
variables within it.
The interpreter works for expressions in lambda calculus, with l x.E, where E is any
expression, represented by lambda(x,E), the expression E1 E2, that is E1 applied to
E2 represented by apply(E1,E2) and the variable x represented by vbl(x). Arithmetic
and other built-in operators are represented in their curried form by op(p) where p is
the operator, or op1(p,E) where E is an expression for the partially applied form:
eval(apply(E1,E2),Env,R)
:- eval(E1,Env,R1), eval(E2,Env,R2), apply(R1,R2,R).
eval(lambda(X,Exp),Env,R) :- R=closure(X,Exp,Env).
eval(vbl(X),Env,R) :- lookup(X,Env,R).
eval(Exp,Env,R) :- otherwise | R=Exp.
apply(closure(X,Exp1,Env),Exp2,R)
:- eval(Exp1,[X/Exp2|Env],R).
apply(op(P),Exp,R) :- R=op1(P,Exp).
apply(op1(P,Exp1),Exp2,R) :- dobuiltin(P,Exp1,Exp2,R).

276 Chapter 8
dobuiltin(plus,Exp1,Exp2,R) :- R:=Exp1+Exp2.
// plus code for other built-in operations
If actors were executed sequentially, this interpreter would give us eager evaluation,
since both function and argument expressions in an application are evaluated before
applying the function. However, as we have unrestricted parallelism, initiation of the
evaluation of the function, evaluation of its argument and the function application
itself is concurrent. The effect is that if the function evaluates to a closure, the
function application may take place even though computation of its argument is still
in progress. With an actor network
:- eval(Exp2,Env,R2), apply(closure(X,Exp,Env1),R2,R).
applying the closure gives:
:- eval(Exp2,Env,R2), eval(Exp,[X/R2|Env2],R).
Although the value of R2 is still being computed we may proceed with the evaluation
of Exp. The channel R2 plays a role similar to MultiLisp’s “future” construct
[Halstead, 1985]: a place-holder which may be manipulated as a first-class object
while its final value is being computed. Application of strict operators however will
be suspended until their arguments are evaluated, for example, an arithmetic
operation will reduce to a call to GDC’s built-in arithmetic and suspend until its
arguments are ground.
If a curried operator implements conditional expressions, we will end up by
computing both branches of the conditional even though only one is needed since
computation of both branches will commence in parallel. To inhibit this, as in Field
and Harrison’s eager interpreter, we can treat conditionals as a special case by
including an additional constructor in the definition of expressions to accommodate
them. So “if E1 then E2 else E3” is parsed to cond(E1,E2,E3) rather than
apply(apply(apply(op(cond),E1),E2),E3). We then need to add additional
behaviors:
eval(cond(E1,E2,E3),Env,R)
:- eval(E1,Env,TruthVal), branch(TruthVal,E2,E3,Env,R).
branch(true,E2,E3,Env,R) :- eval(E2,Env,R).
branch(false,E2,E3,Env,R) :- eval(E3,Env,R).
The dependency in branch means that evaluation of the branches of the conditional
will not take place until the condition has been fully evaluated to a Boolean constant.
Full lazy evaluation, as used in modern functional languages, may be obtained by
passing the argument in an application in the form of a suspension containing the
unevaluated expression and its environment to ensure that if it is eventually evaluated
its channels are correctly bound. This gives us the following rule to replace the rule
for evaluating applications:
eval(apply(E1,E2),Env,R)
:- eval(E1,EnvR1), apply(E1,susp(E2,Env),R).
We also need a rule to evaluate suspensions when necessary:

Meta-Interpretation 277
eval(susp(E,Env1),Env2,R) :- eval(E,Env1,R).
Since the environment may contain suspensions, when we look up an identifier we
may need to evaluate it further, so we alter the rule for variable lookup to:
:- eval(vbl(X),Env,R) :- lookup(X,Env,V), eval(V,Env,R).
Since some primitives such as the arithmetic functions require their arguments to be
fully evaluated before the operation can be completed (that is, the primitives are
strict), we must add this to the code for executing the primitive, for example:
dobuiltin(plus,Exp1,Exp2,R)
:- eval(Exp1,[],R1), eval(Exp2,[],R2), R:=R1+R2.
Parallelism is limited in the lazy interpreter but not completely excised. We no longer
evaluate the function application and the argument simultaneously since evaluation of
the argument is suspended. However evaluation of the arguments to strict primitives,
such as plus above, does take place in parallel. The effect is to give conservative
parallelism: we only do those computations in parallel whose results we know are
definitely needed. A more sophisticated combination of lazy functional programming
could be obtained by using operators such as those proposed by Trinder et al [1998].
The interpreters given here for lambda calculus are not the most efficient that could
be achieved and are given mainly for illustration of the technique of using interpreters
to embed one language in another. One major issue we have not dealt with in lazy
evaluation is that in practice call-by-need is essential to ensure that suspensions are
evaluated once with the evaluation shared by all references to them, rather than re-
evaluated every time they are referenced. An efficient way of dealing with recursion,
used by Field and Harrison [1988], is to build circular environments rather than rely
on the fact that the fixpoint operator can be represented directly in lambda calculus
[Barendregt, 1984]. (These issues can be dealt with in GDC, but there is not space for
further detail here.) Circular environments can be represented directly if we take up
Colmerauer’s proposal [Colmeraurer, 1982] to recognize the lack of the occur check
as a language feature which can be interpreted as the logic of circular or infinite
structures. A more efficient way however would be to dispense with environments
altogether and use a combinator [Turner, 1979] or super-combinator [Hughes, 1982]
based evaluator.
8.10 Conclusion
The use of meta-interpreters may be seen as both a way of structuring programs and a
way of avoiding cluttering a programming language with a variety of features. It has
been recognized that programs are clearer if the logic of the program is separated
from the control. This was one of the guiding principles in the development of logic
programming languages. For efficiency reasons a detailed user-defined control
mechanism may be necessary, but this should not be mixed in with the specification
of the logic of the program. A meta-interpreter may be regarded as the third element
of a program that combines the logic and the control. It may be an implicit part of the
language or the programmers may themselves provide it. It is often the case that
program clarity is aided by writing the program in a simple problem-oriented

278 Chapter 8
language and implementing that language in a language closer to the underlying
machine. Recursively, the implementation language may itself be similarly
implemented. This is a technique already familiar under the name structured
programming [Dahl et al., 1972]. But metaprogramming provides a clear division
between the levels of structure and the potential separation of logic and control at
each layer means that the top-level layer is not constrained to inherit directly the
control of the machine level, or to be cluttered with explicit control structures to
subvert it.
On language features, meta-interpretation provides a facility to add features or change
aspects of that language as required through the use of an interpreter specifically
designed to add or change a particular feature. This compares with complex single-
level languages where every feature a programmer may at any time have to use must
be added as part of the language definition. This creates an unwieldy language that is
difficult to learn, use safely and debug. It should be recalled that every new feature
added to a language must not only be considered in its own terms but also in terms of
its impact on other features.
One important use of interpreters (not considered in detail) here is their use to assist
in the problem of mapping the abstract parallelism of a language like GDC onto a real
parallel architecture. Such an interpreter would deal with problems like load-
balancing and deciding when the increased communication costs involved in moving
some computation to another processor are balanced by an increased utilization of
parallelism.
The biggest barrier against the use of meta-interpreters as a program or language-
definition structuring device is the overhead. A program, which must work through
several layers of interpreter before getting to the machine level, will not be as
efficient as one that directly controls the machine level. To some extent this can be
overcome, as we have shown, through the use of interpreters in which much of the
lower level is inherited implicitly by the upper level rather than explicitly
reimplemented. However, even the “vanilla meta-interpreter” of logic programming
which inherits almost everything from the underlying level has been shown in
practice to increase execution time by an order of magnitude. A solution to the
problem is to use partial evaluation to flatten out the layers of interpretation into a
single-level program. This technique will be explored in detail in the next chapter.

