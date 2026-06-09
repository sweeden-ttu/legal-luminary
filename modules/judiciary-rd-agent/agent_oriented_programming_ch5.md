Chapter 5
Actors and Agents
Even while it changes, it stands still
Heraclitus
Hewitt and Agha [1988], in a Fifth Generation conference, asked if Guarded Definite
Clause languages were logical. That they are sound but not complete should be clear
from previous chapters. Hewitt made a similar previous reappraisal of Planner. The
similarity of Planner with Smalltalk [Hewitt 1973, 1974] led Kornfield and Hewitt to
develop a pattern-directed invocation language, Actors, to build multi-agent systems.
Programming in the Actor formalism requires first deciding the messages each actor
can receive and then what each actor should do when it receives such a message. The
idea that single assignment variables can be considered as message channels was
raised in the previous chapter. The correspondence of GDC and Actors is explored in
this chapter. The superficial difference between Actors and GDC is one of ontology.
Actors names behaviors, message queues and local variables while GDC names only
behaviors and channels. The essential difference between the two languages is that
messages are defined inductively in GDC and message queues are implicit in Actors.
Like GDC, the process structure of Actors is small and therefore scalable. In
concurrent object-oriented programming, the uniformity of communication and
encapsulation, enable combination and co-operation of various levels and grains of
agents. This helps in constructing multi-grain intelligent architectures such as an
architecture for brain simulation [Weitzenfeld and Arbib, 1991]. In a similar way,
GDC programs can model fine entities such as neurons [Kozato and Ringwood,
1992]. This is illustrated in this chapter. The elegance with which process based
languages can be used to build neural networks indicates both the advantages of
implementing neural nets in a concurrent programming language and the innate
potential for massive parallelism with such languages. This Chapter also explores
new directions for both connectionism and symbolic AI research with a view to
fusion. For those readers who have managed to avoid connectionist propaganda until
now, the chapter introduces neural networks. In Section 5.8, an example indicates
how a self-replicating network of generic neurons can be produced. The neuron type
is specialized in Section 5.9 where its response behavior is programmed. Section 5.10
describes how such a neural network can be taught a simple recognition task, parity
determination. Parity recognition is an example celebre that presents a hard learning
exercise for most neural networks [Minsky and Papert, 1969].
Conway’s Life game provides a rich source of insight into how simple rules lead to
complex "social" behavior. Until the development of GDC languages, Logic
programmers were somewhat disadvantaged in this game. The chapter illustrates
how, with such Logic Languages, Logic programmers can readily join in. In
particular, the chapter reports a new asynchronous implementation of the Life game
on distributed workstations. This chapter is envisaged as the first step in the
M.M. Huntbach, G.A. Ringwood: Agent-Oriented Programming, LNAI 1630, pp. 139–173, 1999.
© Springer-Verlag Berlin Heidelberg 1999

140 Chapter 5
investigation of the use of GDC languages for building self-replicating multi-agent
systems.
5.1 The Actor Model
Newell [1962] pointed out that with conventional AI, a single agent appears to be
wandering over a goal net much as an explorer wanders over the globe. The agent has
a single context that it takes with it wherever it goes. This single agent view focuses
attention on the internal process of search with a single locus of control and attention.
This leads to preoccupation with control structures such as goal stacks and queues for
making decisions and changing contexts. Rather than a sequence of choices made by
a decision maker on a web of choice points, Hewitt [1977] envisages control as a
pattern of messages among a collection of computational agents he called Actors.
According to Hewitt [1985], incomplete knowledge is typical of AI and as such
requires an approach that allows continuous acquisition, refinement and toleration of
inconsistency. Hewitt claims open systems uncover important limitations in current
approaches to AI. Such systems require an approach more like organizational
behavior embodied in general systems theory [Skyttner, 1996]. Minsky [1986] has
claimed that intelligence in humans is a result of the interaction of a very large and
complex assembly of loosely connected subunits operating much like a society but
within a single individual. More generally, Hewitt argues that the agents in an
organization are open in the sense that they are embedded in an environment with
which they interact asynchronously. Open systems are not totally in control of their
fate. They consist of agents, conceptually parallel threads, which communicate with
each other and co-operatively or competitively respond to events that occur
indeterministicly in real-time.
Refinement of these ideas produced the Actor language [Agha, 1986] that attempted
to address the needs of distributed AI. The example of a stack is used to introduce
Actors in [Agha, 1986] using the Simple Actor Syntax:
def node(Item, Link)
[case operation of
push: (NewItem)
pop: (Customer)
end case ]
if operation = push then
let L = new node(Item, Link)
become node(NewItem, L)
fi
if operation = pop then
send Item to Customer
become forward(Link)
fi
end def

Actors and Agents 141
The case statement clearly corresponds to GDC guards. Besides the conditional,
actors are defined inductively with four primitive actions: send; become; create
and forward. The arrival order of messages is nondeterministic but the underlying
message passing system is assumed to guarantee eventual delivery. To send a
message, the identity (mail address) of the recipient needs to be specified. The
become directive specifies the subsequent behavior of the actor. The send action
causes a message to be put in the recipient’s mailbox (message queue). The create
primitive (let and new) is to Actors what procedural abstraction is to sequential
programming. Newly created actors are autonomous and have unique mail addresses
specified in the create command.
The forward primitive actor passes on received messages to the mailbox named in
its argument. It is left to a garbage collector to detect and finesse forwarders. Both
channels, such as Item and message queues, such as Link, are named in the language.
The forwarder can be understood in GDC as shorting two streams as in merge. To
better understand the Actor language, a GDC program for the stack example
corresponding closely to the Actor program is given:
//node(Item, Task ,Link)
node(Item, push(NewItem, Task),Link) :- true
| node(Item, L, Link), node(NewItem, Task,L)
node(Item,pop(Customer,Task),Link) :- true
| send(Task, Link) send(Item, Customer)
where send(Message, Channel) is used as a synonym for Channel=Message.
The first clause can be represented pictorially as in Figure 5.1.1 and the second clause
as in Figure 5.1.2. The essential difference between this and the previous program is
that Actors names message queues and channels, while GDC names only channels. In
Actors, variables are local variables and only message queues are shared. The
behavioral identity of an actor is ephemeral, as are GDC goals and lasts only one
reduction. Actor destruction is thus implicit.
push
Link
NewItem NewTask Item
node L node
node
Fig. 5.1.1 First node clause

142 Chapter 5
Item pop
Link
Customer
NewTask
send send
node
Fig. 5.1.2 Second node clause
A scenario illustrating how the stack grows and collapses is the following.
:- node(empty, Task, nil), send(push(m1,Task1),Task),
send(push(m2,Task2),Task1), send(pop(Top,Task3),Task2).
:- node(empty,push(m1,Task1),nil), send(push(m2,Task2),Task1),
send(pop(Top,Task3),Task2).
:- node(empty,push(m1,push(m2,Task2)),nil),
send(pop(Top,Task3),Task2).
:- node(empty, push(m1,push(m2,pop(Top,Task3))),nil).
:- node(m1,push(m2,pop(Top, pop(Top,Task3))),L1),
node(nil,L1,nil).
:- node(m2,pop(Top,Task3),L2), node(m1,L2,L1),
node(empty,L1,nil).
:- node(m1,L2,L1), node(empty,L1,nil), send(m2,Top),
send(Task3,L2).
:- node(m1,Task3,L1), node(empty,L1,nil), send(m2,Top).
.
.
.
Before the pop operation the initial node(empty,Task,nil) has evolved into three
nodes as in Figure 5.1.3.
empty
m2 m1 nil
node
Fig. 5.1.3 Node evolution

Actors and Agents 143
Here the identity of the stack is inherited from the initial node(empty,Task,nil).
That is, agent identity is emergent, in the sense of general systems theory and not
exhibited by a single node.
In the conditional semantics of GDC (described in Chapter 4):
a1, a2,...an ‹ R ‹ B ‹ I
lends itself to this idea of agent identity. If an actor ai in the initial network reduces to
a set of actors:
‹ b1, b2,... bm
the parent relation conveys a connotation of identity.
In the Actor interpretation of GDC, actors are defined inductively using a single
primitive agent send. The action is one of substitution of an actor by a network of
actors specified in the body of a clause. As actors in GDC are ephemeral, there is no
need for fowarders. This is summarized in the following table:
Table 5.1.4 Actor interpretation
behavior named set of condition action pairs (guarded clauses)
condition (guard) node(Item, Task, Link)
if receive(push(NewItem,NextTask),Task)
action – substitution become node(NewItem, NextTask, L)
by network of agents | node(Item,L,Link)
Yet again, the syntax of GDC has been changed to illustrate the actor interpretation.
The notation | for the concurrent composition of actors is borrowed from CCS
[Milner, 1980].
One problem with Actors is the combinatorial explosion in their number of actors.
Constructing message queues using data structures gives more flexibility and avoids
some of the explosion:
//node(Task, Stack)
node(Task, Stack)
if receive(push(NewItem, Task),Task)
become send(stack(NewItem, Stack),St1) | node(Task,St1).
node(Task, stack(Item, Stack))
if receive(pop(Customer, Task), Task),Item)
become send(Item, Customer) | node(Task, Stack)
In this revised implementation, a stack is formed by a message queue and node
becomes a server of the message queue. In the first behavior for node, the node
sends itself a message. This can be finessed:
node(Task,Stack) if receive(push(NewItem, Task),Item)
become node(Task, stack(Item, Stack)).
node(pop(Customer, Task),stack(Top, Stack))
if receive(pop(Customer, Task), Task),Item)
become send(Item, Customer) | node(Task, Top)

144 Chapter 5
Figure 5.1.5 illustrates the revised first behavior.
push
Task
NewItem
stack
node
Stack
node
Fig. 5.1.5 Revised node behavior
The diagram for the second behavior is similar. This solution is not possible in Actors
because, essentially, it requires two message queues.
5.2 Haggling Protocols
Interaction is a basic concept in multi-agent systems. Several agents can combine
their efforts by means of interaction. In an interaction, one agent takes an action or
decision that is influenced by the presence or knowledge of other agents. Each
interaction can cause revisions in an agent’s model of other agents. The example
below (illustrated in Figure 5.2.1) is a GDC program for the Winograd and Flores
haggling protocol [Winograd and Flores, 1986]:
B:accep
t
B:reject
B:counter
S:counter
S:accep
t
S:reject
Fig. 5.2.1 Winograd Flores labeled digraph
The buyer and seller start concurrently with a message for the buyer, the seller’s
asking price, already waiting:
become seller(100,Haggle,50) | buyer(30,counter(100,Haggle),60).
If the buyer receives an offer less than its upper limit, a message agreeing to the price
is sent:

Actors and Agents 145
//buyer(CurrentOffer, NewOffer, UpperLimit)
buyer(Offer, NewOffer, UpperLimit)
if receive(counter(Ask, Haggle),NewOffer) & Ask<UpperLimit
become send(accept(Ask),Haggle).
If the buyer receives an offer greater and the difference between its previous offer and
the new asking price is less than its upper limit, it proposes a counter offer:
buyer(Offer, NewOffer, UpperLimit)
if receive(counter(Ask, Haggle),NewOffer) & Ask>UpperLimit
& NewOffer:=(Ask+Offer)/2 & NewOffer<UpperLimit
become send(counter(NewOffer, NewHaggle),Haggle)
| buyer(NewOffer, NewHaggle, UpperLimit).
If splitting the difference is greater than the buyer is prepared to pay it rejects the
offer:
buyer(Offer, NewOffer, UpperLimit)
if receive(counter(Ask, Haggle),NewOffer) & Ask>UpperLimit
& NewOffer:=(Ask+Offer)/2 & NewOffer>UpperLimit
become send(reject(Ask),Haggle).
The code for the seller is similar:
//seller(CurrentAskingPrice, Offers, LowerLimit)
seller(Ask,Offers, LowerLimit)
if receive(counter(Offer, Haggle),Offers) & Offer>LowerLimit
become send(agreed(Offer),Haggle).
seller(Ask, Offers, LowerLimit)
if receive(counter(Offer, Haggle),Offers) & Offer<LowerLimit
& NewAsk:=(Ask+Offer)/2 & NewAsk>LowerLimit
become send(counter(NewAsk, NewHaggle),Haggle)
| seller(NewAsk, NewHaggle, LowerLimit).
seller(Ask, Offers, LowerLimit)
if receive(counter(Offer, Haggle),Offers)
& Offer<LowerLimit & NewAsk:=(Ask+Offer)/2
& NewAsk<LowerLimit
become send(reject(Offer),Haggle).
The comparison of the Winograd Flores network and finite-state-machine diagram is
readily apparent. A comparison of GDC and the specification of finite state machines,
decision tables was made in Chapter 4.
The given initial object network results in the following scenario:
become seller(100,Haggle,75) | buyer(40,counter(100,Haggle),80).
become seller(100,Haggle,50) | send(counter(0,Haggle1),Haggle)
| buyer(70,Haggle1,80).
become seller(100,counter(70,Haggle1),75) | buyer(70,Haggle1,80).
become seller(85,Haggle2,75) | send(counter(85,Haggle2),Haggle1)
| buyer(70,Haggle1,80).
become seller(85,Haggle2,75) | buyer(70,counter(85,Haggle2),80).

146 Chapter 5
become seller(85,Haggle2,75) | send(counter(77.5,Haggle3),Haggle2)
| buyer(77.5,Haggle3,80).
become seller(85,counter(77.5,Haggle3),75)
| buyer(77.5,Haggle3,80).
become send(agreed(77.5),Haggle3) | buyer(77.5,Haggle3,80).
become buyer(77.5,agreed(77.5),80).
5.3 Consensus Protocols
There are three equivalent agreement problems that illustrate the potential for fault
tolerance of distributed systems: the Byzantine agreement, the consensus problem
and the interactive consistency problem [Singhal and Shivaratri, 1994]. They are
equivalent in the sense that a solution to any one can be used to solve the others. The
Byzantine Generals problem [Dolev, 1982] is so called because it resembles a team of
army generals trying to agree an attack plan. The generals are located on different
hilltops around the battlefield and communicate by sending messages (by
semaphore). Some of the generals are traitors (faulty processors) who by sending
conflicting messages, deliberately try to prevent the loyal generals agreeing.
Lamport et al.’s [1982] Oral Message algorithm is one solution to the problem. The
following illustrates the situation of four generals, one of which is a traitor:
become source(1,[A,B,C]) | general(A) | traitor(B) | general(C).
An arbitrarily chosen source general broadcasts its plan to all other generals:
//source(Value, List_of_Messages)
source(N,[G1,G2,G3]) if true
become send(plan(N,[{G12,G21},{G13,G31}]),G1)
| send(plan(N,[{G21,G12},{G23,G32}]),G2)
| send(plan(N,[{G31,G13},{G32,G13}]),G3).
In doing so, the source sets up the mutual channels.
In the Lamport–Shostak–Pease [1982] solution, the generals send the plan they
received from the source to the other generals and choose the majority plan:
//general(Plans)
general(Plans) if receive(plan(N,[{TA,FA},{TB,FB}]),Plans)
become send(N,TA) | send(N,TB)
| majorityGeneral([N,FA,FB]).
//traitor(Plans)
traitor(Plans) if receive(plan(N,[{TA,FA},{TB,FB}]),Plans)
become send(N,TA) | send(0,TB) | majorityTraitor([N,FA,FB])
In this scenario, the faithful generals agree on the Plan 1:
become source(1,[A,B,C]) | general(A) | traitor(B) | general(C)

Actors and Agents 147
become send(plan(1,[{AB,BA},{AC,CA}]),A)
| send(plan(1,[{BA,AB},{BC,CB}]),B)
| send(plan(1,[{CA,AC},{CB,BC}]),C)
| general(A) | traitor(B) | general(C).
become general(plan(1,[{AB,BA},{AC,CA}]))
| traitor(plan(1,[{BA,AB},{BC,CB}]))
| general(plan(1,[{CA,AC},{CB,BC}]),C)).
source
1 1
1
g g
1
1
0
1
1
tra
Fig. 5.3.1 Four Byzantine generals
The three sends have been done simultaneously. Continuing:
become general(plan(1,[{AB,BA},{AC,CA}]))
| traitor(plan(1,[{BA,AB},{BC,CB}]))
| general(plan(1,[{CA,AC},{CB,BC}]),C)).
become send(1,AB) | send(1,AC) | majorityGeneral([1,BA,CA])
| traitor(plan(1,[{BA,AB}|{BC,CB}]))
| general(plan(1,[{CA,AC}|{CB,BC}]),C)).
become majorityGeneral([1,BA,CA])
| traitor(plan(1,[{BA,1},{BC,CB}]))
| general(plan(1,[{CA,1},{CB,BC}]),C)).
become majorityGeneral([1,BA,CA])
| traitor(plan(1,[{BA,1},{BC,CB}]))
| general(plan(1,[{CA,1},{CB,BC}]),C)).
send(1,CA) | send(1,CB) | majorityGeneral([1,1,BC]).
become majorityGeneral([1,BA,1])
| traitor(plan(1,[{BA,1},{BC,1}]))
| majorityGeneral([1,1,BC]).
become majorityGeneral(1|BA|1)
| send(1,BA) | send(0,BC) | majorityTraitor([N,FA,FB])
| majorityGeneral([1,1,BC]).
become majorityGeneral([1,1,1])
| majorityTraitor([1,1,0]),
| majorityGeneral([1,1,0]).

148 Chapter 5
5.4 Market Forces
In the much vaunted Contract Net Protocol [Smith, 1980], a customer requests
Contractors to tender for a specified job.
//contractNet(SpecifiedJob, SetOfContractors, Chosen)
contractNet(Job, Contractors, Chosen) if true
become tender(Job, Contractors,[],Time,Tenders)
| time(5,Time) | select(Tenders, Chosen).
The actor time/2 is a primitive that immediately it is spawned initializes a real-time
clock. After the designated five periods has elapsed, it sends a message timeUp on
the channel Time. (Man [1992] describes concurrent analysis techniques that, he
claims, make GDC programming suitable for hard realtime systems.) The actor
select/2, which is not specified, choses the contractor on the basis of the tenders
received (usually the lowest cost.)
After the timeout has expired, tender/4 sends the received bids on Tenders to the
selector actor. In the meantime it distributes the Job description to the set of
Contractors with a unique reply channel (as in the client actor in Chapter 4):
//tender(SpecifJob, Contractors, ReplyAcc, Time, TenderReplies)
tender(Job, Contractors, Accum, Time, Tenders)
if receive(timeUp,Time)
become send(Accum, Tenders).
tender(Job, Contractors, Accum, Time, Tenders)
if receive([Contractor|Cs],Contractors)
become send(offer(Job, Reply),Contractor)
| tender(Job, Cs, [Reply|Accum], Time, Tenders).
5.5 Poker Faced
A poker game can be seen as a combination of a contract net and the haggling
protocol. The auctioneer raises the stakes until there is only one punter left in the
game:
//auction(CurrentOffer, SetOfPunters)
auction(CurrentOffer, Punters) if Offer:=CurrentOffer+1
become request(Offer, Punters, Accum, Replies)
| time(5,Time) | wait(Time, Offer, Replies)
Punters are connected to the auction via fair merges. The punter is simplified to
remain bidding while Offer is less than some punter chosen limit:
//punter(Requests, UpperLimit)
punter(Requests, UpLimit)
if receive([bid(Offer, Reply)|Round],Requests)
& Offer=<UpLimit
become send(in(More),Reply) | punter(More, UpLimit).

Actors and Agents 149
punter(Requests, UpLimit)
if receive([bid(Offer, Reply)|Round],Requests)
& Offer>UpLimit
become send(out,Reply).
//request(Offer, SetPunters, Accumulator, SetBidReplyPairs)
request(offer, SetPunters, Accum, Replies)
if receive([in(Punter)|Ps],SetPunters)
become send(bid(offer,Reply),Punter)
| request(offer, Ps,[Reply|Accum],Replies).
request(offer, SetPunters, Accum,Replies)
if receive([out|Ps],SetPunters)
become request(offer,Ps,[Reply|Accum],Replies).
request(Job, SetPunters, Accum,Replies)
if receive([],SetPunters)
become send(AccumReplies).
request(offer, SetPunters, Accum, Replies)
if receive([X|Ps],SetPunters) & unknown(X)
become request(offer, Ps,[Reply|Accum],Replies).
wait(timeUp, offer, Replies) if true
become auction(Bid, NewPunters).
5.6 Virtual Neural Networks
Weitzenfeld and Arbib [1991] propose building a brain from a host of actors in much
the same way a biological brain is made up of neurons. That organic brains and
computers have approximately the same number of processing elements, 1011, might
initially suggest that the perceptive power advantage of organic brains over
computers must be due to the speed of its electrochemical processing elements,
neurons. This is not so. Neurons are significantly slower at firing than logic gates are
at changing state. Neurons fire in milliseconds whereas off-the-shelf solid-state
technology can switch state in nanoseconds. If raw processing power is calculated as
the product of the number of processing elements and the response rate, the computer
has an apparent power advantage of ten thousand. Nevertheless, this advantage is not
realized because only small fractions of logic gates change state simultaneously. It is
one thing to have the capacity for parallel processing, it is another to be able to
exploit it efficiently. It would seem to be the way in which potential parallelism is
exploited in organic brains that gives them greater power than conventional
computers.
Conscious thought, examined on time-scales of seconds or minutes has sequential
characteristics. Current psychological thinking on perception is that humans relate
fragmentary stimuli to knowledge familiar from various experiences and
unconsciously test and reiterate perceptions at different levels of abstraction. In other
words, what beings believe they perceive, is, in fact, only a mental reconstruction of

150 Chapter 5
fragments of sensory data. This is reminiscent of the philosophy of Husserl and
Heidegger. This suggests that symbolic AI is not made redundant by artificial neural
machines but is only part of the solution to Artificial Intelligence. Symbolic AI
corresponds to the higher conscious levels of human thought processes.
Linguists have speculated that higher levels of thought processes are only possible
with the aid of phonograms and ideograms. The superiority of ideograms over
phonograms has proved itself in mathematics and science. Uncritical surrender to
neural fever (or mad cow disease as it is known in the UK) threatens the transparency
and maintainability that software engineering is striving to achieve. An alternative to
surrender is compromise; the two approaches to AI should form different layers in the
pursuit of Artificial Intelligence. If thought processes are organized in hierarchical
layers of abstraction then the interface between symbolic AI and artificial neural
networks is a legitimate area of study. The combination of artificial neural networks
and computer symbolic processing holds the promise of being better than the sum of
the parts.
5.7 Biological and Artificial Neural Networks
Neurons are the primitive constituents of organic brains. A neuron is a nerve cell that
consists of a nucleus, dendrites, axon and synapses, as depicted in Figure 5.7.1. The
synapses form the connection between the axon of one cell and the dendrite of
another. Functionally, the dendrites are receptors and the axon an emitter of bursts of
electrochemical pulses generated by the cells. A neuron produces pulses along its
axon in response to pulses received from other neurons at its synapses. Whether a
neuron decides to ‘fire’, produce a pulse, depends on the combination of the present
state of the neuron and the pulses received from its immediate neighbors. The
similarity with Petri nets is clearly apparent. (For a better informed description of the
physiology of nerve cells the reader is referred to [Crick and Asanuma, 1986].)
Neurons in organic brains are autonomous computational units and each may be
directly connected with up to several thousand other neurons forming a network. The
computational mechanism of each neuron is local and simple. It can only be the
autonomy of neurons, as processing elements and the complexity of interconnections
wherein lies the ability to explore simultaneously many competing hypotheses. The
way neurons interconnect and fire allows the possibility of chain reactions in much
the same way as chain reactions occur in an atomic explosion. This analogy reveals
the way in which explosive parallelism can be achieved by neural systems.
Artificial neural networks are characterized by network topology, node characteristics
and training or learning rules. Though in what follows the three components are
explained separately for pedagogy, they are not independent. Neuron connectivity can
be represented as a directed graph with neurons as the vertices and directed edges
synaptic connections. In general, there can be cycles, closed loops, so that feedback is
possible as depicted in Figure 5.7.2. An artificial neural network adopting this type of
topology [Hopfield, 1982], was partly responsible for the renewed enthusiasm in
connectionist systems.

Actors and Agents 151
Fig. 5.7.1 A simplified organic neuron
If there is no feedback the network forms a DAG (directed acyclic graph) and is
stratified, as illustrated in Figure 5.7.3. This form of topology is exemplified by,
Nettalk [Sejnowski and Rosenberg, 1985]. Nettalk’s ability to read text aloud
contributed to the revival of interest in connectionist systems. External stimuli feed
into a bottom layer of neurons and the output is taken from the top layer; there can be
many layers of hidden neurons in-between. There may be different numbers of nodes
in each layer and such networks can be used to classify input patterns, the number of
output nodes reflecting the number of classes.
Fig. 5.7.2 The ’feed-all’ network
It is in the DAG topology that the potential for explosive parallelism can best be seen
when the hidden layers have increasing numbers of neurons. The way neurons
interconnect and fire in this topology allows the possibility of chain reactions in much
the same way as chain reactions occur in an atomic explosion.

152 Chapter 5
Fig. 5.7.3 The feed-forward network
5.8 Self-Replicating Neural Networks
For the sake of definiteness, the network topology chosen for implementation is a
binary tree, but other arrangements can be accommodated as easily. As will be
illustrated, such a neural network can be taught to recognize the parity of input bit
vectors. A binary tree of protoneurons with three layers can be brought into existence
by the GDC process invocation:
become tree(3, O, Is).
where the tree relation is defined by:
//tree(NumberOfLayers, OutputStream, ListOfInputStreams)
tree(NumberOfLayers,A,Ss) if receive(1,NumberOfLayers)
become send([S1|S2],Ss) | protoNeuron(A,S1,S2)
tree(N,A,Ss) if N>1 & N1:=N-1
become protoNeuron(A,A1,A2) | tree(N1,A1,S1s)
| tree(N1,A2,S2s) | concatenate(S1s,S2s,Ss).
A graphical trace of a parallel reduction of the initial agent [á la Ringwood, 1989a] is
given in Figures 5.8.1a and 5.8.1b; active (reducible) agents at each stage are shaded.
The tree process evolves into a tree of generic neurons (the type of neuron will be
specified in the next section).
5.9 Neuron Specialization
There are essentially two types of artificial neurons: analogue neurons [Pitts and
McCulloch, 1947], which are weighted sum threshold activation models, and the
earlier discrete logic gates [McCulloch and Pitts, 1943], which are motivated by
digital hardware (Figure 5.9.1).

Actors and Agents 153
A
3 tree
Ss
A
protoNeuron
2 tree 2 tree
conc
Ss
A
protoNeuron
protoNeuron protoNeuron
1 tree 1 tree 1 tree 1 tree
conc conc
conc
Ss
Fig. 5.8.1a Evolution of the net

154 Chapter 5
A
protoNeuron
protoNeuron protoNeuron
protoNeuron protoNeuronprotoNeuron protoNeuron
S1.S2.[] S3.S4.[] S5.S6.[] S7.S8.[]
conc conc
conc
Ss
A
protoNeuron
protoNeuron protoNeuron
protoNeuron
protoNeuron protoNeuron protoNeuron
[S1,S2,S3,S4] [S5,S6,S7,S8]
conc
Ss
A
protoNeuron
protoNeuron protoNeuron
protoNeuron protoNeuron protoNeuron protoNeuron
[S1,S2,S3,S4,S5,S6,S7,S8]
Ss
Fig. 5.8.1b Collection of inputs to the net.

Actors and Agents 155
Fig. 5.9.1 a) 1947 Pitts–McCulloch artificial neuron where H, is the Heaviside’s step function
and the weights w i and threshold Q are arbitrary real numbers; b) and c) 1943 McCulloch–Pitts
threshold logic gate neurons where the possible weights are +1 or -1 and the thresholds Q
integer.
Discrete logical neurons are, of course, ideally suited to implementation in
conventional hardware. One mutable form of a logic gate, Probabilistic Logic Neuron
[Aleksander, 1988] (PLN), was chosen for the present chapter for the sake of
definiteness. There is a sense in which the PLN is biologically more realistic than the
analogue McCulloch–Pitts [1947] neuron. In biological neurons it is widely believed
that, before adaptation, a neuron fires or does not with roughly equal probability. The
probability edges towards certainty as the learning process progresses [Sejnowski,
1981; Aleksander, 1988]. Any other form of artificial neuron or network can be
implemented by the same techniques used below.
The PLN is essentially a programmable, probabilistic, logic gate.
//protoNeuron(Axon,Synapse1,Synapse2)
protoNeuron(A,S1,S2) if true
become
pLN(table(Seed,unknown,unknown,unknown,unknown),S1,S2,A).
Initially, the gate type is unspecified (Figure 5.9.2). The constant unknown in the
table is used to indicate that the neuron will produce an indeterministic response (0 or
1) to a binary input pattern. The first parameter of table is used as the seed of a
pseudo random number generator to produce this effect. In this situation, the PLN
produces a 1 or 0 output with equal probability. This stochastic nature endows the
PLN with indeterministic properties that biological neurons are speculated to possess
[Sejnowski, 1981]. (By modifying the tree clause it can be arranged that the different
neurons do not have the same initial seed.)
Fig. 5.9.2 Initial State of the PLN

156 Chapter 5
As the neural network undergoes training, undetermined truth table entries become
learnt responses to controlled input (Figure 5.9.3).
Fig. 5.9.3 Some partially learnt state
The response behavior is captured by the actor pLN:
//pLN(State,InputStream1,InputStream2,OutputStream)
pLN(State,InputStream1,InputStream2,Output)
if receive([o(S1)|S1s],InputStream1)
& receive([o(S2)|S2s],InputStream2)
become send([o(A)|S3s],Output)
| gate({S1,S2},State, NewState,A)
| pLN(NewState,S1s,S2s,S3s).
The response consists of truth table lookup. If the table value has been learnt, this
value is returned:
//gate(InputPairState, LookUpTable, OuputState, Output)
gate(InputPairState, table(Seed, learnt(T),U,V,W),NewState,A)
if receive({0,0},InputPairState)
become send(T,A) | send(table(Seed,learnt(T),U,V,W),NewState).
gate(InputPairState, table(Seed,unknown,U,V,W),NewState,A)
if receive({0,0},InputPairState)
& NSeed:= if Seed<0 then shiftleft(Seed)XOR3
else shiftleft(Seed) & B:=NSeedmod2
become send(B,A) | send(table(NSeed,unknown,U,V,W),NewState).
gate({0,1},table(Seed, T, learnt(U),V,W),NewState,A) if true
become send(U,A) | send(table(Seed,T,learnt(U),V,W),NewState)
gate({0,1},table(Seed,T,unknown,V,W), NewState,A)
if NSeed:= if Seed<0 then shiftleft(Seed)XOR3
else shiftleft(Seed) & B:=NSeedmod2
become send(B,A) | send(table(NSeed,T,unknown,V,W),NewState)
gate({1,0},table(Seed,T,U,learnt(V),W),NewState,A) if true
become send(V,A) | send(table(Seed,T,U,learnt(V),W),NewState)
gate({1,0},table(Seed,T,U,unknown,W),NewState,A)
if NSeed := if Seed<0 then shiftleft(Seed)XOR3)
else shiftleft(Seed) & B := NSeedmod 2
become send(B,A) | send(table(NSeed,T,U,unknown,W),NewState)

Actors and Agents 157
gate({1,1},table(Seed,T,U,V,learnt(W)),NewState,A) if true
become send(W,A) | send(table(Seed,T,U,V,learnt(W)),NewState)
gate({1,1},table(Seed,T,U,V,unknown),NewState,A)
if NSeed := if Seed<0 then shiftleft(Seed)XOR3
else shiftleft(Seed) & B := NSeed mod 2
become send(B,A) | send(table(NSeed,T,U,V,unknown),NewState).
The algorithm for calculating random bits is taken from Knuth [1969].
A trace of how inputs propagate in parallel through a PLN tree network is shown in
Figure 5.9.4. (The word propagate does not really convey the sense of urgency
associated with combinatorially explosive parallelism.)
5.10 The Teacher Teaches and the Pupil Learns
In artificial neural networks, there is no conventional stored database, no carefully
worked out application specific rules. The only principle that guides the system is that
it incorporates some notion of a right and wrong. It is constructed to strive to respond
correctly. In this way, the network can be self-taught: each input produces an output.
Correct outputs are reinforcing, incorrect outputs cause internal adjustments. By
modifying its internal state, the network strives to achieve favorable responses. At
first, the response is by trial and error; later, as the learning process continues, it
becomes a mixture of trial, error and experience. Eventually the machine behaves as
if it "knew" exactly what it was the instructor was trying to tell it. When the neural
machine has learned something, the instructor does not know at the conceptual level
what is going on inside the machine – it is generally far too complex for that.
Training for a PLN neuron can be effected by a second clause for pLN: the functors t
on the input are used to indicate that the training mode is operating:
pLN(Table,[t(S1,R1)|S1s],[t(S2,R2)|S2s],Output) if true
become send(t(A,R)|S3s,Output) | gate({S1,S2},Table,A)
| training({A,R},Table,{{S1,R1},{S2,R2}},NewTable)
| pLN(NewTable,S1s,S2s,S3s).
Here, the recursive pLN clause simulates a perpetual actor that changes state
according to the training relation. Output response pairs {S1, R1}, {S2, R2} and
{A, R} are used to direct the responses to the proffered inputs back to the nodes
responsible for them. Back-communication naturally lends itself to back-propagation
[Rumelhart et al., 1986], a learning technique for networks with hidden layers of
neurons that was partially responsible for the neural network renaissance. The
training process records the output and amends the lookup table as dictated by the
response for the recursively-reincarnated neuron.

158 Chapter 5
A
pLN
pLN pLN
pLN pLN pLN pLN
[o(1),S7s] [o(1)S8s]
[o(1),S3s] [o(1),S4s]
[o(1),S1s] [o(1),S2s] [o(1),S5s] [o(1),S6s]
A
pLN
pLN pLN
[o(S12),A1s.[][o34),A2s] [o(S56),A3s] [o78),A4s]
pLN pLN pLN pLN
S1s S2s S3s S4s S5s S6s S7s S8s
A
pLN
[o(S1234),A5s] [o(S5678),A6s]
pLN
pLN
pLN pLN pLN pLN
S1s S2s S3s S4s S5s S6s S7s S8s
[o(S12345678),A7s]
pLN
pLN
pLN
pLN pLN pLN pLN
S1s S2s S3s S4s S5s S6s S7s S8s
Fig. 5.9.4 Trace of virtual neurons firing in response to input
It then remains to specify the training algorithm. The method chosen for the present
work, is one of several possibilities [Myers and Aleksander, 1988]:

Actors and Agents 159
• Step 1: Choose an input pattern from some training set and apply it to the input
nodes.
• Step 2: Allow values to propagate through all neurons in the network. (Each PLN
responds according to the state of its truth table.)
• Step 3: If the values on the output connections are the ones expected, the output of
each neuron becomes established (learnt).
• Step 4: Otherwise, return to Step 2 and try again (because the output of each
neuron is stochastic the output will generally be different) until a correct output is
generated or
• Step 5: A ’sufficient’ number of errors has been made suggesting the possibility of
succeeding is effectively zero. In this situation, all nodes are returned to their
initial indeterministic state.
• Step 6: Repeat steps 1 to 5 until ’consistent’ success indicates that all patterns have
been learned:
//training(OutputPair, OldTbl, InputPairs, NewTbl)
training({A,confirmed},table(Seed,T,U,V,W),{{0,R1},{0,R2}},Tbl1)
if true
become send(Tbl1,table(Seed,learnt(A),U,V,W))
| send(R1,confirmed) | send(R2,confirmed)
training({A,incorrect},table(Seed,T,U,V,W),{{0,R1},{0,R2}},T1)
if true
become send(T1,table(Seed,unknown,U,V,W))
| send(R1,incorrect) | send(R2,incorrect)
training({A,confirmed},table(Seed,T,U,V,W),{{0,R1},{1,R2}},T1)
if true
become send(T1,table(Seed,T,learnt(A),V,W))
| send(R1,confirmed) | send(R2,confirmed)
training({A,incorrect},table(Seed,T,U,V,W),{{0,R1},{1,R2}},T1)
if true
become send(Tbl1,table(Seed,T,unknown,V,W))
| send(R1,incorrect) | send(R2,incorrect)
training({A,confirmed},table(Seed,T,U,V,W),{{1,R1},{0,R2}},T1)
if true
become send(T1,table(Seed,T,U,learnt(A),W))
| send(R1,confirmed) | send(R2,confirmed)
training({A,incorrect},table(Seed,T,U,V,W),{{1,R1},{0,R2}},T1)
if true
become send(T1,table(Seed,T,U,unknown,W))
| send(R1,incorrect) | send(R2,incorrect)
training({A,confirmed},table(Seed,T,U,V,W),{{1,R1},{1,R2}},T1)
if true
become send(T1=table(Seed,T,U,V,learnt(A))
| send(R1,confirmed) | send(R2,confirmed)

160 Chapter 5
training({A,incorrect},table(Seed,T,U,V,W),{{1,R1},{0,R2}},T1)
if true
become send(T1,table(Seed,T,U,V,unknown))
| send(R1,incorrect) | send(R2,incorrect)
5.11 Neural Simulation
The implementation of a neural net described in the previous section has been
successfully taught to recognize the parity of input bit vectors [Kozato, 1988].
Clearly, this means that each PLN has learnt to behave as an Exclusive-Or gate. The
implementation was slow, not the least because of the overhead of process switching.
The speed of process switching is of the order of the response rate of biological
neurons, that is microseconds. Organic neural nets illustrate how fast processing can
be achieved even by such slow processing elements. This is due to the way in which
parallelism is organized into small, equal sized portions without any synchronization
problems. The feed-forward network topology is amenable to explosive
computational parallelism of which organic brains are capable. With this topology of
actors, there is only one producer and ideally many consumers so there is no binding
conflict problem.
As the number of processors is increased, there will be less demand for process
switching. In this regime, the implementation of neurons by software processes could
be a viable proposition. However, to expand this model to a real application on
multiple processors the further factor of processor communication cost must be
considered. Since the communication is only an activation signal, this cannot be too
expensive. Judicious partitioning of neurons across processes minimizes the cost and
this will be particularly beneficial when there are highly interconnected clusters with
few connections between clusters. These virtual neurons can even be allowed to
migrate between processors.
The choice of illustration, a tree network of PLN neurons, was purely for the sake of
explanation and definiteness; the techniques presented here are capable of
implementing any topology, any type of artificial neuron and any training rules. It can
be seen that the computational model of GDC corresponds largely with a
connectionist one. Actors fire or not depending on their internal state and on data
received from other actors. While shared variables do give potential synchronization
problems in GDC when there are multiple producers, a style of programming can be
adopted, such as the feed-forward network, where there are only single producers for
shared variables.
Some features of a neural network implementation in GDC are unusual. It is
generally believed that neural nets should ultimately be built in hardware. Yet
experience has revealed many difficulties with this philosophy. For example, training
a network is a very slow and painful business. For the network described above,
learning proceeds by a process of trial and error. For each input-output pair, trials are
made a predetermined number of times. This is the accepted regime because the
intended implementation medium is hardware. When the implementation medium is
software, as herein, the number of trials can be adjusted to reflect the number of

Actors and Agents 161
unknown entries in the lookup tables. This is achieved by making the propagation
signals carry information on the internal states of the neurons. This modification for
the above implementation is simple but would be impractical if not impossible to
achieve in a hardware implementation. Thus, for software implementations the
learning phase can be dramatically shortened [Kozato, 1988].
There is some belief that sophisticated cognitive systems can only be built from a
suitable combination of neural networks and symbolic AI techniques [Hendler, 1989].
From this point of view, the advantages of implementing neural nets in a
programming language that is suitable for symbolic manipulation are clear.
Furthermore, for hardware implementations, reconfiguring neural nets and adding
new nodes to accommodate more concepts seems impossible without having great
redundancy. In software, for languages like GDC, this presents no difficulty. GDC
allows dynamic process creation and this allows dynamic neuron creation. The above
section illustrating the dynamic construction of a neural net exemplifies this. Thus, in
a learning situation, new neurons can be created as necessary. This increases the
potential of the system to learn new concepts. Because the language GDC, by
inheritance from Prolog lends itself to partial evaluation, the training sessions could
be viewed in this light. After a training session, a virtual neural net will have acquired
some knowledge. Viewed as partial evaluation, this new goal has been specialized for
the training data. Once a particular neural net has acquired some knowledge, the
resolvent can be saved as a partially evaluated goal. Goals can be composed to give
more complex nets that accumulate knowledge.
The implementation of neural nets in GDC is not just a simulation. It offers an
executable language for describing neural networks and opens the possibility of
dynamically evolving neural systems. This research suggests a new direction for both
neural network research and conventional symbolic AI with a view to their fusion.
In general, neural networks tend to be regarded with disdain by the symbolic AI
community: they are seen as a rival technology. This attitude overestimates the
capability of both connectionist and symbolic systems and as an alternative, the two
technologies might be more usefully viewed as complementary. Hybrid systems
could provide a fruitful line of research for constructing more sophisticated, artificial
cognitive systems. There are of course many possible variations for hybrid systems,
e.g. on the symbolic side rule-based systems or semantic networks, discrete or analog
neurons implemented in software or hardware on the connectionist side. Some
tentative hybrid neural networks have already been proposed, e.g. [Ballard, 1986;
Derthick, 1988; Touretzky and Hinton, 1988; Shastri, 1988 and Shastri, 1989], but
the software-hardware implementation issue of neural networks has not received any
attention. This is because it has naturally been assumed that software implementation
is a temporary expedient and connectionist systems eventually, when the technology
catches up, will be totally implemented in VLSI.
The neural simulation represents an initial step investigating a language-based
approach to hybrid symbolic connectionist systems. By implementing a neural
network in the language GDC, the correspondence between the computational models
of neural networks and Actors are brought to light. Some of the advantages of a
software implementation of connectionist systems are discovered and the simplicity

162 Chapter 5
with which the construction can be achieved indicates the potential capacity for
parallel processing which GDC languages possess.
5.12 Simulated Life
Conway’s Life game is not as its name might suggest, competitive, nor a game of
chance. Rather it is a deterministic simulation of the evolution of a population of
interdependent individuals. The only randomness is in the choice of the initial state.
Evolution proceeds according to a small number of simple, fixed rules. Life is played
out on a square board in the fashion of chess. Each square or cell may be occupied or
unoccupied. The board is assumed infinite but initially (and subsequently) only
finitely many cells are occupied. The rules describe the evolution of an individual in
terms of the occupancy of neighboring cells.
A cell has four nearest neighbors and a further four next nearest diagonal neighbors.
Each cell passes through a sequence of generations. The occupant of a cell with two
or three occupied neighbors survives to the next generation. A cell with less than two
occupied neighbors dies of loneliness. A cell with four or more contemporaries dies
from overcrowding. Exactly three neighboring cells of an unoccupied cell give birth
(triolism) to a new occupant.
The board is taken to be infinite to avoid introducing special rules for boundary
conditions. Given that there are only going to be a finite number of occupied cells in
any one generation, simulation on an infinite board is approximated by taking a finite
array with cyclic (or twisted) boundary conditions. This means that the simulated Life
Game is played out on a torus or Klein bottle. Such a board on a closed surface can
be thought of as an infinite flat board on which the pattern of the finite colony is
repeated as with a wallpaper pattern. The boundary effects are then explicable in
terms of the state of the neighboring colonies.
The rules that determine the life and death cycle of cells are local. Nevertheless,
given the generational life of a cell the dynamics can be extrapolated to determine the
state of the whole board in successive generations. Such a lock-step simulation can
easily be programmed in an imperative language such as C using arrays to represent
the board. What tends to exclude Prolog programmers from this form of the game is
that the problem domain is naturally expressed in terms of an array of cells. The tree-
like data structures in logic programs do not prevent the representation of arrays but it
is not particularly sympathetic to it. The single assignment of logic variables can
make updating a single element an expensive business [e.g., Eriksson and Rayner,
1984].
GDC having a rather different computational model from Prolog allows computation
via concurrent processes organized by local communication. An actor that accepts
messages to lookup and update its elements can model a mutable array:

Actors and Agents 163
arrayn((trans(lookup(1,Element),Rmgs),E1,E2,...,En) if true
become send(E1,Element) | arrayn(Rmgs,E1,E2,...,En);
...
arrayn(trans(update(1,Element),Rmgs),E1,E2,...,En) if true
become arrayn(Rmgs,Element,E2,...En)
...
This is implemented using tail-recursion so that the recursive actor takes over the
process descriptor of the parent, thus saving the copying of most of the arguments.
Another possibility is to simulate each element of the array by an actor. This will be
demonstrated with the Game of Life below.
Fig. 5.12.1: Representation of a 3x4 torus and Klein board
5.13 Life Yet in GDC
Each cell need never know where it is in the array. For simplicity, only four nearest
neighbors: North; South; East and West will be represented. Each cell of the array

164 Chapter 5
has a small amount of transitory state, occupation, which it communicates to its
neighbors. The rule concerning a cell dying by overcrowding is simulated by the
definite clause:
//cell(State, North, South, East, West, OutputStream)
cell(State,[occpd|RNs],[occpd|RSs],[occpd|REs],[occpd|RWs],Os)
if true
become send([unoccpd|ROs],Os)
| cell(unoccpd, RNs, RSs, REs, RWs, ROs)
The first argument of cell is its current state. This actor blocks waiting for its middle
four arguments to be instantiated to streams such that the head of each list is the
constant occpd. When this constraint is satisfied, the cell actor can metamorphose
into a similar actor and output its new state on the stream Os.
The other conditions that govern the life of a cell can be represented in a similar way.
As there are a large number of combinations, a more succinct representation is
obtained by denoting the state of the cells by integers: 0 for unoccupied and 1 for
occupied:
cell(State,[Nn|Ns],[Sn|Ss],[En|Es],[Wn|Ws],Os)
if Nn+Sn+En+Wn<2
become send([0|ROs],Os)
| cell(0,Ns,Ss,Es,Ws,ROs)
cell(State,[Nn|Ns],[Sn|Ss],[En|Es],[Wn|Ws],Os)
if Nn+Sn+En+Wn=:=2
become send([State|ROs],Os)
| cell(State,Ns,Ss,Es,Ws,ROs)
cell(State,[Nn|Ns],[Sn|Ss],[En|Es],[Wn|Ws],Os)
if Nn+Sn+En+Wn=:=3
become send([1|ROs],Os)
| cell(1,Ns,Ss,Es,Ws,ROs)
cell(State,[Nn|Ns],[Sn|Ss],[En|Es],[Wn|Ws],Os)
if Nn+Sn+En+Wn>=4
become send([0|ROs],Os)
| cell(0,Ns,Ss,Es,Ws,ROs).
In this situation the guards of the clauses are disjoint and so deterministic.
5.14 Cheek by Jowl
In operation the simplified four nearest neighbor game, a cell is connected to its
neighbors by shared logic variables:
become ...| cell(N,NNs,Os,NEs,NWs,Ns) | ...
| cell(E,ENs,ESs,EEs,Os,Es) | ...
| cell(M,Ns,Ss,Es,Ws,Os) | ...
| cell(W,WNs,WSs,Os,WWs,Ws) | ...
| cell(S,Os,SSs,SEs,SWs,Ss) |...

Actors and Agents 165
A recursively-defined actor may easily generate a (one-dimensional) chain of N cells
connected with two nearest neighbors:
chain(1,Es,Ws,Os) if true
become cell(State, Es, Ws, Os);
chain(N, Es, Ws, Os) if N>1 & N1:=N-1
become cell(State, Es, Ws, Os) | chain(N1,Os,W1s,Ws).
amended to get the connectivity required for a one-dimensional Life game of N cells
on a circle:
cycle(N) if N>1
become cycle1(N, Es, Ws, Os, Es)
cycle1(1,Es,Ws,Os,Ts)
become send(Ws, Ts) | cell(Es, Ws, Os)
cycle1(N, Es, Ws, Os, Ts) if N>1 & N1:=N-1
become cell(Es, Ws, Os) | cycle1(N1,Os,W1s,Ws,Ts).
A two-dimensional generalization of this idea can be used to produce an M by N
array of cells with four nearest neighbors connected as a torus:
torus(M,N) if N>1
become torus(M, N, Es, Ws, Os, Es)
torus(M,1,Es,Ws,Os,Ts)
become send(Ws, Ts) | col(M, s, Ws, Os)
torus(M, N, (M, Es, Ws, Os) | torus(M,N1,Ns,Ss,Os,W1s,Ws,Ts)
This forms a cycle of columns. The columns are then unfolded into a torus:
col(1,Es,Ws,Os)
become cell(Es,Ws,Os)
col(M,Ess,Wss,Oss) if M>1
become send([Os|ROss],Oss) | col1(M,Ns,Ss,Ess,Wss,Os,ROss,Ns)
col1(1,Ns,Ss,[Es|Ess],[Ws|Wss],Os,Oss,Rs) if true
become send(Ss,Rs) | cell(Ns,Ss,Es,Ws,Os)
col1(M,Ns,Ss,[Es|Ess],[Ws|Wss],Os,Oss,Rs) if M>1 & M1:=N-1
become send([Ss|ROss],Oss) | cell(Ns,Ss,Es,Ws,Os)
| col1(M1,Os,S1s,Ess,Wss,Ss,ROss,Rs)
While the suffix s denotes a stream the suffix ss denotes a stream of streams.
5.15 Distributed Implementation
The GDC program for Life described in the previous section has been has been
implemented [Linney and Ringwood, 1992] on a distributed system of workstations.
The game is started with an actor life/3 that has three channels. These are the size of
the board; the maximum number of iterations a cell may go through and a list of the
coordinates of the cells that are initially occupied. To initialize and observe the game
a controller actor is required. Besides the code given above, each cell shares a
command stream with the controller. To initialize particular cells each cell must carry
its identity (x-y coordinate pair) as part of its state. Commands can then be broadcast

166 Chapter 5
to the cells; only those cells with the same identity will change state according to the
commands. To observe the output of the game, a display thread must also share
stream of each cell. The Life program is inherently concurrent, and so is suited to
execution on multiprocessor systems.
At the 1948 Hixon Symposium, von Neumann [1951] reflected on McCulloch and
Pitts’ work on the design of digital computers. Turing's result of a universal
computing-machine suggested to him that there might be a universal construction
machine. A machine which when provided with a description of an automaton and a
component rich environment could construct a copy of itself.
In a manuscript published after his death [1966] von Neumann demonstrated a
Turing-like machine that could reproduce itself. To do this von Neumann imagined
an infinite "chess board" in which each cell is either empty, or contains a single
component. Each component can be in one of several states. A group of occupied
cells in the plane is interpreted as an organism. Such systems have become known as
cellular automata [e.g., Toffli and Margolis, 1987].
The present chapter describes the use of GDC Languages for simulating a particular
cellular automaton, Conway's Life, on a distributed collection of workstations. The
simulation has a similar structure to the simulation of artificial neurons in GDC
Languages as described by Kozato and Ringwood [1990]. The traditional
implementation of the Life game is played in a lock-step fashion. Typically, the grid
of cells being stored as a two-dimensional array with the algorithm updating all the
cells at each generation. This version is very different in that each cell is a process
and cells asynchronously communicate their states to each other. This inherently
concurrent behavior allows cells to be updated in parallel.
Newman [1990] describes an implementation in Parlog of the Life Game, which
came to the attention of the authors after the present simulation was designed.
Newman's implementation lies somewhere in between the conventional
implementation and the one described here in that while the cells are modeled as
processes, they are updated lock-step generation by generation. Newman generates
the cells in two phases. First the cells are generated; then the streams are connected to
nearest neighbors. In this chapter, generation and connection is performed in one
step.
The present asynchronous implementation makes the program much simpler. Despite
the asynchronous communication, a cell cannot advance more than one generation in
front of a neighbor because the next state is determined by the cumulative state of its
neighbors. Generations by generation then, the expected patterns associated with the
sequential implementations of the Game are exhibited.
The original idea that self-replicating automata should be cellular arose from its
origins in the Turing machine and the need to supply a component rich environment
from which to build replicas. With concurrent languages such an environment is not
necessary, as can be seen from the array program that generates the matrix of cells
(from thin air), so that restriction to an array is unnecessary. Systolic algorithms
[Kung, 1982] can be seen as a generalization to other tessellations of the plane. They
were developed to exploit pipeline parallelism, inherent in many algorithms, by the

Actors and Agents 167
use of special purpose hardware. Shapiro [1984] saw the advantages of the use of
GDC for the implementation of such algorithms.
Given that systolic automata can be built in software, there is no necessity for them to
be simple. For example, reactive problem solving agents can be constructed
dynamically. In a real-world situation, things do not usually proceed as planned. The
traditional assumptions made by planning systems, for example STRIPS [Fikes et al.,
1971], are that the environment is totally predictable. The world model is totally
complete and correct, and primitive actions are instantaneous and can never fail. Such
an environment is termed static. In the real world, this is rarely the case, it is a
dynamic, on-going, real-time and unpredictable environment. An agent interacting
with it must be able to behave appropriately - this suggests that the agent should
possess a degree of reactivity and should be created dynamically when demand
arises. The Life simulation should be viewed as an initial investigation into the
possibility of using GDC for building self-replicating agents.
5.16 Agent Micro-Architectures
The notion of a rational agent is that of an agent that has explicit representation of its
own goals and beliefs about its environment. Two lines of approach to multi-agent
systems can be distinguished: macro and micro. The macro-micro distinction is
common to disciplines such as economics and sociology that are metaphors for multi-
agent systems. Microsystems focus on the architecture of an individual.
Macrosystems are concerned with interagent dynamics. The examples so far have
been about macrosystems.
Shoham [1990] proposes an architecture as a specialization of Actors. Following
Dennett [1987] and McCarthy [1979] Shoham endows agents with a state consisting
of mentalistic components: beliefs, capabilities, choices, commitments etc. Following
Searle [1969], Cohen and Perrault [1979], agents communicate with other agents by
Speech-acts. Speech-act theory categorizes communication as informing, requesting,
offering and so on. In GDC, a Shoham agent would be similar to the client actor
described in the previous chapter:
//agent0(MessageStream, Beliefs, Commitments)
agent0([inform(Fact)|Stream], Beliefs, Commitments) if true
become
inform(Fact,Beliefs,NewBeliefs,Commitments,NewCommitments)
| agent0(Stream,NewBeliefs,NewCommitments)
agent0([request(Action)|Stream],Beliefs,Commitments) if true
become request(Action,Beliefs,NewBeliefs,Commitments,
NewCommitments)
| agent0(Stream,NewBeliefs,NewCommitments)

168 Chapter 5
agent0([offer(Action)|Stream],Beliefs,Commitments) if true
become
offer(Action,Beliefs,NewBeliefs,Commitments,NewCommitments)
| agent0(Stream,NewBeliefs,NewCommitments)
etc
The actors inform, request and offer etc execute commitments. Shoham uses a
real-time clock to time the actions, but in GDC time is measured by events and events
are the sending (or receipt) of messages. A real-time clock is a concept, like
inheritance, that does not fit well in distributed systems. Rather than regarding history
as the passage of time, time is considered as the passage of history. If no events have
taken place, no time has passed. This is the philosophy of discrete event simulation.
A local clock is just a monotonic counter:
become clock(A)|send(s(B),A)|send(s(C),B)|send(s(D),C) ...
become clock(s(B)) | send(s(C),B) | send(s(D),C) ...
become clock(s(s(C))) | send(s(D),C) ...
become clock(s(s(s(D)))) | ...
5.17 Metalevel Agent Architectures
An agent’s belief typically includes beliefs about actions the agent can perform and
beliefs about the other agents. Reflexive or meta-level architectures where an agent
reasons about itself and other agents [Maes, 1988] is another micro-architecture.
Being symbolic, GDC shares with Prolog and Lisp an affinity for meta-interpretation.
In Prolog, a simple propositional Prolog meta-interpreter would take the form:
//demo(Program, Goals)
demo(G) if true
become clause(G:-G1) | demo(G1).
demo(G1|G2) if true
become demo(G1) | demo(G2).
demo(true) if true become true.
Here, the demo predicate expresses that the goal G can be demonstrated from the
program P. A clause is represented as a conjoined list terminated by true:
clause(g:-[g1,g2,...,gn|true])
While this is propositional, it can be generalized to the first order case:
demo(G1) if true
become demo(forall(X,G)) | substitute(X,G,Y,G1).
The predicates hold when G1 results from substituting the term Y for the variable X
in G. The Prolog meta-interpreter is nondeterministic, because it is not determined
which clause might demonstrate the goal G. The inbuilt depth-first engine performs
the search.
Because there is no backtracking in GDC, the search has to be programmed. This is
achieved by organizing the alternative search branches as a stream. As a simple

Actors and Agents 169
illustration, a resource bounded meta-interpreter for propositional Prolog in GDC
follows. It is adapted from [Kowalski, 1995]:
//demo(KB,InGoals,Result)
demo(KB,fail,Result) if true
become send(fail,Result).
demo(KB,[]+AltGoals,Result) if true
become send(true,Result).
demo(KB,fail+AltGoals,Result) if true
become demo(KB,AltGoals,Result).
demo(KB,[G|Rest]+AltGoals,Result) if true
become ask(KB,G,D) | dnf([D|Rest],AltGoals, DNF)
| demo(KB,DNF,Result)
Here, the demo agent reduces a stream of InGoals with respect to the definite
clauses in a knowledgebase, KB. Alternative branches of the search space are
represented by disjuncts. That is, the clauses having conclusion G, are represented by
a single list of alternative body goals terminated by fail, e.g.
‹
G D where D=Alt1+Alt2+...+fail and Alti=[Gi1,Gi2,...,Gin]
Thus, every disjunct is terminated by fail and if a goal G is the conclusion of no
clause in the knowledgebase, ask returns the value fail in its third channel. The actor
dnf computes the disjunctive normal form of its first argument. As the disjunctive
normal form is not unique, this actor behaves as a selection rule.
In the above program, the agent persists until it reduces the goal to true or fails in the
attempt. In practice, agents will have a limited time to reach a conclusion; they will
be resource-bounded. A resource-bounded agent can easily be formed by a slight
modification of the previous program:
//demo(KB,InGoals,OutGoals,Resource)
demo(KB,fail,OutGoals,R) if true
become send(fail,OutGoals).
demo(KB,[]+AltGoals,OutGoals,R) if true
become send(true,OutGoals).
demo(KB,InGoals,OutGoals,0) if true
become send(InGoals,OutGoals).
demo(KB,[G|Rest]+AltGoals,OutGoals,R)
if R>0 & R1:=R-1
become ask(KB,G,D)
| dnf([D|Rest],AltGoals, DNF)
| demo(KB,DNF,OutGoals,R1)
demo(KB,InGoals,OutGoals,R) if otherwise
become send(InGoals,OutGoals)
Here, the demo agent reduces a stream of InGoals to a stream of OutGoals with
respect to the definite clauses in the knowledgebase, KB. This is done within
Resource backward chaining steps, so this agent is bounded. The work that dnf
does is not included in the resource count but probably should be.

170 Chapter 5
The demo agent can be modified to include abducibles:
//demo(KB,Abducibles,InGls,OutGls,Resource)
demo(KB,Abs,{fail,Beliefs},OutGls,R) if true
become send({fail,Beliefs},OutGls).
demo(KB,Ab,{[],Beliefs}+AltGls,OutGls,R) if true
become send({true,Beliefs},OutGls)
demo(KB,Ab,InGls,OutGls,0) if true
become send(InGls,OutGls).
demo(KB,Ab,{[G|Rest],Beliefs}+AltGls,OutGls,R)
if R>0 & R1:=R-1
become ask(KB,Ab,{[G|Rest],Beliefs},D)
| dnf([[D|Rest]+AltGLs, DNF)
| demo(KB,Ab,DNF,OutGls,R1)
demo(KB,Ab,InGls,OutGls,R) if otherwise
become send(InGls,OutGls)
The knowledge base is extended with a set of abducibles, Ab. The ask agent returns
true if the goal is a belief or an abducible. If not already a belief, the abducible is
added to the set of beliefs. The actor dnf also has to be modified to handle beliefs
appropriately.
5.18 Actor Reconstruction of GDC
Hewitt [1985] argues that systems of interconnected and interdependent computers
are qualitatively different from the self-contained computers of the past. The
argument goes as follows: if, to avoid the von Neumann bottleneck, decision making
is decentralized, no system part can directly control the resources of any other system
part (otherwise it would itself become a bottleneck). The various autonomous parts
must necessarily communicate with one another if anything is to be co-operatively
achieved. Response from a remote service typically has latency. Consequently,
communication should be asynchronous so that the local computation can continue
and do something useful rather than waiting for a response. This contrasts with CSP
where communication is synchronous.
Kahn and Miller [1988] argue that most current programming languages are
inadequate for large-scale open systems. They say there are two notable exceptions
Actors and GDC. In distributed systems the remote procedure call (RPC) is favored
because it to some extent it imitates the procedure call of third generation languages.
However, the synchronous call/return of RPC can cause an inefficient use of
resources. A response from a remote server typically has a long latency. While
asynchronous message passing is possible, it is difficult to integrate with third
generation languages.
RPC differs from procedure call in that it is call by value. Call by reference cannot be
achieved because remote nodes do not share the same address space. A local
procedure call cannot usually be replaced by an RPC. It cannot easily transmit
mutable values.

Actors and Agents 171
One approach to the problem is at the operating system level. Mach [Rashid, 1988],
for example, distinguishes between threads and tasks. While threads are loci of
control sharing the same address space, tasks are not. Processes (threads or tasks)
send messages to named ports (message queues). Port names can be passed in
messages but the message queue is mutable.
However, an operating system is not a programming language. In an operating
system, the criterion of locality is address space while for procedure calls it is local
variables. A programming language allows a decoupling of concurrency and the
allocation of processes to processors. This transparency between local and remote
affords scalability.
Both Actors and GDC can be rationalized from the starting point of asynchronous
message passing agents. According to Russell and Norvig [1995], an agent can be
viewed as anything perceiving its environment through sensors and acting upon that
environment through effectors. The actions are not generally random: there is some
correlation between percept and action. For software agents, perceptions are received
messages. The characteristics of a software agent are:
• asynchronous message passing;
• local decision making.
Point-to-point asynchronous communication allows locality to be expressed and
optimized. The local decision making decides which actions, if any to perform. A
primitive action is to send a message. In its primitive form, the reactive agent, the
behavior can be specified by a set of stimulus response pairs, such as the decision
tables of Chapter 3. Alternative behaviors are discriminated by the message received.
Subsequent behaviors can be defined inductively by a network of agents that replace
the agent. In Actors, the replace is specified by become and create. In GDC it is
only specified by create. The action become is distinguished from create in Actors
by the inheritor of the message queue. The speculation is that rational agents can be
built up from herds of reactive agents by programming. A rational agent is one that
behaves logically or maximizes its own utility.
Kornfield and Hewitt [1981] extend the principles of Actor theory, to provide what
they call a scientific community metaphor. They claim that scientific communities
behave as parallel systems, with scientists working on similar problems concurrently
with other scientists. This is reminiscent of the blackboard metaphor described in
Chapter 1. Hewitt [1985] explains the idea of open systems in distributed AI; an open
system is a large collection of computational services that use each other without
central co-ordination, trust or complete knowledge of each other. This is reminiscent
of open systems theory [von Bertalanffy, 1968]. It contrasts with, closed systems and
conjures up completeness and the Closed-World assumption of databases as invoked
by Absys, Planner and Prolog to explain negation as failure.
Agent identity is recognised as an essential problem of multi-agent systems [Gasser
and Briot, 1992]. Fixed boundaries for objects are considered to be too inflexible and
do not reflect theoretical positions in which agents are dynamically defined by
reference to their changing position in the community. Computational units may
participate in different agents. It is thus necessary to distinguish between agents and

172 Chapter 5
actors. There is nothing to maintain a stable identity when an agent is composed of
ever changing definitions and patterns of interaction.
When the number of agents becomes large, individual referencing becomes difficult
so it becomes necessary to organize them into larger entities. Most conceptions of
group employ a representative agent that serves as a surrogate for the group. This
surrogate becomes a bottleneck and conflicts with the initial intentions.
With Actors, the notion of identity is somewhat confused because identity is
manifested in different ways. To send a message an agent must be able to take for
granted some predictable stable quality of the recipient, such as the name of the
mailbox. An agent can also be identified by its behavior: the messages it is prepared
to accept and its subsequent behavior. In Actors, a name is associated with an
inductively defined behavior. A name is also associated with a mailbox (a message
queue). The two are associated by the create action. The become action relates the
mailbox name to subsequent behavior. While the inductively defined behavior is
shortlived, a message queue is long lived. The forward actor that serves no useful
purpose (no decisions to make) exemplifies the problem and it is left to the garbage
collector to remove. There is no explicit destruction of actors in the Actor language.
The message queue has a long-lived identity whereas process behavior has a short-
lived identity. Tomlinson and Singh [1989] suggest reifying the message queue in
Actors to gain some control over the acceptance of messages. That is, the queue may
be accessed other than by its head. Other authors suggest multiple message queues.
This was noted in the previous chapter where it was shown how in GDC languages a
message queue can be built up from a nesting of channels.
The essential difference between Actors and GDC is that Actors names local
variables and message queues while GDC only names channels. Message queues or
mailboxes allow many to one communication. In GDC, this must be done with an
explicit merge. Channels have the same lifetime as behaviors; they can only receive
one message.
There have been a number of attempts to simulate Actors in GDC languages:
Vulcan [Kahn et al., 1986]; Mandala [Ohki et al., 1987] and POLKA [Davison,
1992]. As can be understood from above, this simulation essentially consists of
implementing a message queue as a list of channels and hiding from view. As can
also be seen from this section and as Kahn [1989] admits, this is not necessarily an
advantage.
5.19 Inheritance Versus Delegation
A common feature of object-oriented languages is encapsulation (locality).
Inheritance is an additional feature of sequential object-oriented languages such as
Smalltalk and C++. Object-oriented languages such as Actors and ABCL [Yonezawa,
1990] emphasize concurrency as a characteristic. ABCL [Yonezawa, 1990] provides
two message queues with each object, a normal one and an express one. These
languages are sometimes referred to as object-oriented concurrent languages,
OOCLs. Numerous authors [America, 1987; Briot and Yonezawa, 1987; Chaffer and

Actors and Agents 173
Lee 1989; Papathomas, 1989; Tomlinson and Singh, 1989] have pointed out the
conflicts between inheritance and concurrency that break encapsulation. Matsuoka
and Yonezawa [1993] call the phenomenon inheritance anomaly.
In most OOCLs, the programmer explicitly programs the synchronization, the guard
in GDC, to restrict the set of acceptable messages. The inheritance anomaly is that the
synchronization code cannot be effectively inherited. This is illustrated with the
bounded buffer example of Matsuoka and Yonezawa:
b_buf([put(Item)|Tasks],List\EndList) if true
become send([Item|NewEndList],EndList)
| buffConsumer(Tasks,List\NewEndList)
b_buf([get(Contents)|Task],[Item|List]\EndList) if true
become send(Item,Contents)
| buffConsumer(Tasks,List\NewEndList).
A put message stores an item in the buffer, a get message removes it. Upon creation,
the buffer is in the empty state.
become b_buf(Tasks,EndList\EndList) | ....
Now consider the a subclass gb_buf which accepts an additional message gget().
The behavior of gget() is almost identical to that of get(), with the exception that it
cannot be immediately accepted after a put() message. This can only be handled by
adding a state variable, afterPut. That is b_buf must be redefined to account for the
newly added method. The problem is that gget() is history sensitive. This is similar to
the Brock–Ackerman anomaly [1981] described in Chapter 4.

