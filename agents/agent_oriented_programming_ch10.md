Chapter 10
Agents and Robots
Civilization advances by extending the number of important
operations that we can perform without thinking about them.
AN Whitehead (1861–1947)
Stemming from several sources, the notion of a computational agent came to
prominence in the 1990s. The multiple parentage of the concept meant that there was
no clear definition as to what the terminology meant. The rapid growth of interest led
to many using the term as a buzzword in the hope of gaining a foothold on the
bandwagon. As this book has indicated, agents have been a common theme in the
sociology of artificial intelligence. At the 13th International Conference on
Distributed AI, Hewitt remarked that the question “what is an agent?” is as
embarrassing for the agent-based computing community as the question “what is
intelligence?” Underlying the development of the concept of agent is the move away
from computers as stand-alone systems that are used to model aspects of the world
towards being active participants in the world. One of the dictionary definitions of
agent is “a person or thing, which exerts power or has the power to act” and this sense
lies behind the use of the word in computing.
As Gelernter and Carriero [1992] and many others have noted, computing has
developed with the processing of data seen as paramount and the transmission of data
and results as secondary or superficial. AI systems used for problem solving or expert
systems illustrate this. They provide output when given input, the output reflecting
how a human would approach the same mental task. They do not attempt to interfere
with the world itself. This is left to humans. Such systems have a complete and closed
model of the world, working on the assumption that manipulating this model will
parallel manipulating the real world. This will work perfectly in real world situations
like game playing where strict rules are obeyed. It is not surprising that the playing of
games like chess has been one of the most successful applications of AI. However,
the capturing of uncertainty has been a major theme in moving beyond simple
microworlds like this. Systems are soon engulfed by the amount of information
needed and combinatorial explosion when every possible result of attempting an
action in the real world is considered.
10.1 Reactive Agents: Robots and Softbots
Concerns of this sort led Brooks [1991a] to challenge the Artificial Intelligence
community, claiming it had gone down a blind alley. Brooks was concerned with
building robots that could cope with ordinary physical environments [Brooks, 1986].
He wanted his robots to be robust, able to deal with inconsistency in sensor readings
and able to achieve a modicum of sensible behavior if the environment changed,
rather than fail and halt or engage in irrational behavior. His response to this
M.M. Huntbach, G.A. Ringwood: Agent-Oriented Programming, LNAI 1630, pp. 319–351, 1999.
© Springer-Verlag Berlin Heidelberg 1999

320 Chapter 10
challenge was to drop the good old-fashioned AI approach involving detailed
planning and knowledge representation and build robots that worked purely on
reaction to sensor input. He argued that this was how real animals worked (or, as he
put it, “Elephants don’t play chess” [Brooks, 1990]). This harks back to the
behavioral psychology, Section 1.6. Thus, an artificial intelligence should be
constructed by first building a base with animal-like behavior with simple reactive
rules and then adding to it layers of more intelligent control. Experiments with real
animals, for example [Arbib and Liaw, 1995], have been used to show that much
animal behavior can be accounted for by simple reactive mechanisms.
The lowest level of control of Brooks’ robots led them simply to avoid collision
(bearing in mind they had to exist in environments where other objects might be
moving) by sending appropriate messages to movement motors when the sensors
detected the approach of an object. The next level of control caused the robots to
move independently but aimlessly by sending messages to move and turn at random.
A level above this gave some direction to the movement, sending the robot towards
areas that its sensors detected had free space. Only at levels above this (which were
not included in Brooks’ original robots) would the robot store maps it had constructed
of its environment and plan movement around these maps. Each layer of control in
the robots worked independently of the higher layers. Higher levels could take control
from the lower levels by issuing instructions that the lower level messages be
ignored, but the lower levels would continue issuing the messages regardless. This
was called a subsumption architecture.
Agre and Chapman [1987] made a similar use of a purely reactive architecture in their
influential PENGI system. This system was designed to play an arcade computer
game involving moving an object in an environment where points may be gained by
reaching certain positions. Hostile moving objects have to be avoided and the player
may set other objects in motion. Unlike Brooks’ robots, the PENGI system was
working with an artificial and thus strictly limited world. The large numbers of
objects in this world, their unpredictable behavior and the time-dependent nature of
the game, meant that tackling the game in a way involving detailed modeling and
planning was unfeasible. Rather, the approach used was for the artificial player to
react immediately based on simple rules involving the immediate surroundings of the
manipulable object.
The most obvious aspect of the move of computing away from standalone systems is
the development of the Internet, making all connected machines one large distributed
system. The term agent has been associated with systems designed to work with the
Internet. Reading email or directly requesting the transfer of remote files, the Internet
is an infrastructure driven by human actions. Systems designed to explore the Internet
in order to discover information, or to filter email to reduce information overload
[Maes, 1994] are agents in a second dictionary sense of the word “ones entrusted with
the business of another”. Clearly such systems may be simple and we would resist
describing a mail filter that simply throws away all email not from a given list of
addresses as “intelligent”. Higher levels of intelligence might include making use of
some set of rules and an inference engine in order to make decisions, build user
models, learn and adapt in response to feedback and so on.

Agents and Robots 321
The connection of these software agents with agents in the Brooks’ sense is argued by
Etzioni [Etzioni, 1993]. He suggests that a system operating in a real software
environment shared by other users faces much the same problems as a robot working
in a physical environment. These are: lack of complete knowledge of what the
environment contains; the need to be able to handle whatever is encountered in the
environment without failing; the dynamic nature of the environment; the ability of the
agent to change the environment. To emphasize the similarity with physical robots,
Etzioni uses the term softbot. The pragmatic convenience of softbots over robots for
agent research is noted. It is cheaper and quicker to build and experiment with
software artifacts rather than physical artifacts, but such experimentation is not
simply games-playing as it has obvious commercial potential [Tenenbaum, 1997].
10.2 A Simple Robot Program
As shown in Chapter 5, an actor can be represented by a system where (mutually)
recursive calls represent a continuation of a state. Single assignment variables and
terms can be interpreted as recursively defined messages. Consider an input stream
connected to a sensor which converts messages to the single assignment form while
an output stream connected to an effector which converts values to commands to a
robot’s motors. A robot working in an environment may then be programmed. This
has been done with real robots by Nishiyama et al. [1998]. To demonstrate this,
consider a simple world consisting of a two-dimensional grid (similar to the tile world
[Pollack and Ringuette, 1990] that has been used as the basis for a number of agent
experiments). We have a robot situated in this world which can face one of the four
compass points. Squares in the grid are either clear or blocked and the robot may only
move to clear squares. The robot has one sensor that returns the message clear if the
square it is facing is clear, blocked otherwise. Its one effector may be sent the
messages move to move forward one square, clock to turn a quarter-turn clockwise
(without changing square) and anti to similarly turn anticlockwise.
The state of the robot will consist of the streams connected to the sensor and effector,
the direction it is facing and the x and y coordinate. Additionally, differences between
the square in which the robot is located and a goal square (positive if the robot is to
the south/west of the goal, negative if it is to the north/east) can be stored. The
program will simply cause the robot to move towards the goal square avoiding
blocked squares.
The algorithm may be represented by a finite state machine as in Table 10.2.1. Here
State 0 is the state the robot is in before making a move. Recalling that on a square
grid, two of the compass directions will be facing towards the goal location and two
away, States 2 and 4 represent the robot turning in the alternative direction to the goal
if its initial direction is blocked. If the second direction is also blocked, the double
turn after this to States 3 and 5 means the robot only returns the way it has entered a
square if all other adjoining squares are blocked. States 6 and 8 represent a robot,
which is not initially facing the goal turning to face it. States 7 and 9 represent it
turning back to the original direction if the new direction is blocked. If the original

322 Chapter 10
direction is also blocked, again it turns to the third facing, returning the way it came
only if that too is blocked.
Table 10.2.1 Finite state machine robot
State 0: If clear and facing goal: move forward, goto state 0.
If blocked and facing goal and a clockwise turn faces
goal: turn clockwise, goto state 2.
If blocked and facing goal and an anticlockwise turn
faces goal: turn anticlockwise, goto state 4.
If not facing goal and a clockwise turn faces goal: turn
clockwise, goto state 6.
If not facing goal and an anticlockwise turn faces goal:
turn anticlockwise, goto state 8.
State 1: If clear: move forward, goto state 0.
If blocked:goto state 0.
State 2: If clear: move forward, goto state 0.
If blocked:turn clockwise twice, goto state 3.
State 3: If clear: move forward, goto state 0.
If blocked: turn anticlockwise, goto state 1.
State 4: If clear: move forward, goto state 0.
If blocked: turn anticlockwise twice, goto state 5.
State 5: If clear: move forward, goto state 0.
If blocked: turn clockwise, goto state 1.
State 6: If clear: move forward, goto state 0.
If blocked: turn anticlockwise, goto state 7.
State 7: If clear: move forward, goto state 0.
If blocked: turn anticlockwise, goto state 3.
State 8: If clear: move forward, goto state 0.
If blocked: turn clockwise, goto state 9.
State 9: If clear: move forward, goto state 0.
If blocked: turn clockwise, goto state 5.
Note that in State 1, representing the robot returning the way it came, a check is made
to see whether the way is blocked and if so the robot returns to checking other
directions. This is because the robot program is intended to operate in a dynamic
environment, so the way may have become blocked since the robot moved from it
and other ways may become unblocked.
The code for this is tedious, but not complex:
robot0(north,Xd,Yd,[clear|S],E) :- Yd>=0
| E=[move|E1], Yd1:=Yd+1,
robot0(north,Xd,Yd1,S,E1).
robot0(south,Xd,Yd,[clear|S],E) :- Yd<0
| E=[move|E1], Yd1:=Yd-1,
robot0(south,Xd,Yd1,S,E1).

Agents and Robots 323
robot0(east,Xd,Yd,[clear|S],E) :- Xd>=0
| E=[move|E1], Xd1:=Xd-1,
robot0(east,Xd1,Yd,S,E1).
robot0(west,Xd,Yd,[clear|S],E) :- Xd<0
| E=[move|E1], Xd1:=Xd+1,
robot0(west,Xd1,Yd,S,E1).
robot0(north,Xd,Yd,[block|S],E) :- Yd>=0, Xd>=0
| E=[clock|E1], robot2(east,Xd,Yd,S,E1).
robot0(south,Xd,Yd,[block|S],E) :- Yd<0, Xd<0
| E=[clock|E1], robot2(west,Xd,Yd,S,E1).
robot0(east,Xd,Yd,[block|S],E) :- Xd>=0, Yd<0
| E=[clock|E1], robot2(south,Xd,Yd,S,E1).
robot0(west,Xd,Yd,[block|S],E) :- Xd<0, Yd>=0
| E=[clock|E1], robot2(north,Xd,Yd,S,E1).
robot0(north,Xd,Yd,[block|S],E) :- Yd>=0, Xd<0
| E=[anti|E1], robot4(west,Xd,Yd,S,E1).
robot0(south,Xd,Yd,[block|S],E) :- Yd<0, Xd>=0
| E=[anti|E1], robot4(east,Xd,Yd,S,E1).
robot0(east,Xd,Yd,[block|S],E) :- Xd>=0, Yd>=0
| E=[anti|E1], robot4(north,Xd,Yd,S,E1).
robot0(west,Xd,Yd,[block|S],E) :- Xd<0, Yd<0
| E=[anti|E1], robot4(south,Xd,Yd,S,E1).
robot0(north,Xd,Yd,[_|S],E) :- Yd<0, Xd>=0
| E=[clock|E1], robot6(east,Xd,Yd,S,E1).
robot0(south,Xd,Yd,[_|S],E) :- Yd>=0, Xd<0
| E=[clock|E1], robot6(west,Xd,Yd,S,E1).
robot0(east,Xd,Yd,[_|S],E) :- Xd<0, Yd<0
| E=[clock|E1], robot6(south,Xd,Yd,S,E1).
robot0(west,Xd,Yd,[_|S],E) :- Xd>=0, Yd>=0
| E=[clock|E1], robot6(north,Xd,Yd,S,E1).
robot0(north,Xd,Yd,[_|S],E) :- Yd<0, Xd<0
| E=[anti|E1], robot8(west,Xd,Yd,S,E1).
robot0(south,Xd,Yd,[_|S],E) :- Yd>=0, Xd>=0
| E=[anti|E1], robot8(east,Xd,Yd,S,E1).
robot0(east,Xd,Yd,[_|S],E) :- Xd<0, Yd>=0
| E=[anti|E1], robot8(north,Xd,Yd,S,E1).
robot0(west,Xd,Yd,[_|S],E) :- Xd>=0, Yd<0
| E=[anti|E1], robot8(south,Xd,Yd,S,E1).
robot1(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot1(Face,Xd,Yd,[block|S],E)
:- robot0(Face,Xd,Yd,[block|S],E).

324 Chapter 10
robot2(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot2(Face,Xd,Yd,[block|S],E)
:- E=[clock,clock|E1], reverse(Face,Face1),
consume(S,S1),
robot3(Face1,Xd,Yd,S1,E1).
robot3(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot3(Face,Xd,Yd,[blocked|S],E)
:- E=[anti|E1], anti(Face,Face1),
robot1(Face1,Xd,Yd,S,E).
robot4(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot4(Face,Xd,Yd,[block|S],E)
:- E=[anti,anti|E1], reverse(Face,Face1),
consume(S,S1), robot5(Face1,Xd,Yd,S1,E1).
robot5(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot5(Face,Xd,Yd,[blocked|S],E)
:- E=[clock|E1], clock(Face,Face1),
robot1(Face1,Xd,Yd,S,E).
robot6(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot6(Face,Xd,Yd,[block|S],E)
:- E=[anti|E1], anti(Face,Face1),
robot7(Face1,Xd,Yd,S,E1).
robot7(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot7(Face,Xd,Yd,[block|S],E)
:- E=[anti|E1], anti(Face,Face1), robot3(Face1,Xd,Yd,S,E1).
robot8(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot8(Face,Xd,Yd,[block|S],E)
:- E=[clock|E1], clock(Face,Face1), robot9(Face1,Xd,Yd,S,E1).

Agents and Robots 325
robot9(Face,Xd,Yd,[clear|S],E)
:- E=[move|E1], move(Face,Xd,Yd,Xd1,Yd1),
robot0(Face,Xd1,Yd1,S,E1).
robot9(Face,Xd,Yd,[block|S],E)
:- E=[clock|E1], clock(Face,Face1), robot5(Face1,Xd,Yd,S,E1).
consume([_|S],S1) :- S1=S.
move(north,Xd,Yd,Xd1,Yd1) :- Xd1=Xd, Yd1:=Yd-1.
move(south,Xd,Yd,Xd1,Yd1) :- Xd1=Xd, Yd1:=Yd+1.
move(east,Xd,Yd,Xd1,Yd1) :- Xd1:=Xd-1, Yd1=Yd.
move(west,Xd,Yd,Xd1,Yd1) :- Xd1:=Xd+1, Yd1=Yd.
clock(north,Face) :- Face=east.
clock(east,Face) :- Face=south.
clock(south,Face) :- Face=west.
clock(west,face) :- Face=north,
anti(north,Face) :- Face=west.
anti(west,Face) :- Face=south.
anti(south,Face) :- Face=east.
anti(east,Face) :- Face=north.
reverse(north,Face) :- Face=south.
reverse(south,Face) :- Face=north.
reverse(east,Face) :- Face=west.
reverse(west,Face) :- Face=east.
Stopping the robot from turning back the way it has come is necessary to prevent it
from reaching a situation where it is forced to move away from the goal because all
ways to it are blocked. But then, having moved one square away, it immediately
returns to the blocked square and repeats this until the blocks disappear. An initial
situation is shown in Figure 10.2.2 with the robot initially at <e,3> and facing west,
moving towards the goal at <b,1>. It will move to <d,3> and finding <c,3> blocked,
turn first south (entering State 4), then finding <d,2> blocked, turn north (State 5).
Finding <d,4> clear, it will move to <d,4> (returning to State 0). At this point, the
robot will turn again towards the goal (entering State 8) rather than proceed in the
clear direction in front of it. As it then faces blocked <c,4> it turns back north (State
9) and proceeds to <d,5>. It does this, rather than turn to face the goal in the way it
has come and returns to <d,3>. At <d,5> the process of turning west, finding the way
blocked and proceeding north is repeated, moving to <d,6>. At <d,6>, again it turns
west, this time the way is not blocked and it proceeds to <c,6>. At <c,6>, it is facing
towards the goal, so moves to <b,6>. Here the west direction is no longer facing
towards the goal, so it turns south (entering State 8) and finding the way clear
continues to move to the goal.

326 Chapter 10
The program as given, however, will not always avoid going into a loop (in this case
causing the robot actually traverse a loop of squares indefinitely). Consider the
arrangement in Figure 10.2.3. Here the robot will proceed as before until it reaches
<d,4>. At this point, in State 9 facing north, it finds the way ahead blocked, so turns
east (entering State 5) and finding the way clear moves to <e,4>. At <e,4> it turns
south to face the goal and moves to <e,3>. Finding the way ahead blocked, it turns to
the alternative direction for the goal (State 2) and finding the way ahead clear moves
forward. It is now in an identical position to a previous state and unless there are any
changes in the blocks will continue to move around the four squares <d,3>, <d,4>,
<e,4> and <e,3>.
6
n
5
n
4
n
3 <R
n n
2
1 G
a b c d e f
Fig. 10.2.2 Initial state of robot and environment
6
n n
5
n
4
n
3 <R
n n n
2
1 G
a b c d e f
Fig. 10.2.3 An arrangement which causes the robot to loop

Agents and Robots 327
10.3 Reaction and Intelligence
In the case of the above robot, a more sophisticated set of rules could be devised to
enable it to correctly manoeuver around an obstacle to reach its goal. However,
another tactic could be to use a technique similar to simulated annealing [Kirkpatrick
et al., 1993]. In this technique an agent occasionally (using a random choice
mechanism) makes a move which according to its heuristics is not the best one
available. This enables it to escape from situations that are local but not global best
positions. Treating the concept of hill-climbing literally, a robot whose goal is to
move to the highest point on a landscape would have the heuristic that it generally
moves in whichever direction takes it upwards, but at random can make the
occasional downward move. Without such downward moves, it would stay put at the
top of a small hill once it reached it and never explore larger hills. Similarly in any
situation where an agent inhabits a world which is too complex for its simple
heuristics to bring it inevitably to its goal, some random antiheuristic behavior may
help. Such behavior can avoid it getting stuck in situations where rigidly obeying its
rules causes it to continually repeat a sequence of behavior without real progression.
Another approach for the agent would be to physically alter the environment. Imagine
a robot with a supply of pebbles, the ability to drop a pebble in a square, and the
ability to detect the presence of a pebble in a square (and possibly pick it up).
Periodically the robot drops a pebble on the square it is in. A robot entering a square
containing a pebble might choose the second best exit route on the grounds that
choosing the best exit route has simply led it returning to the same location.
In both these approaches, no attempt is made to model the world in which the robot
moves as part of its internal state and use this to reason about routes through the
world. (It may be argued that dropping pebbles is using the environment as its own
model.) Brooks proposed originally that such modeling and planning behavior would
exist as a higher level layer in his robots, though he became the champion of the
purely reactive approach. In practice, a layered approach [Müller, 1996; Chaib-Draa
and Levesque, 1996] combining reaction and planning has become common in
building agents. The balance of planning and reaction employed will depend on the
characteristics of the environment. In an environment which is largely static, planning
may be used generally, with a resort to reactive techniques only when changes render
the planning inaccurate. This enables an agent to get over the brittleness of a planning
system that can take no account at all of changes to the environment. As an analogy,
consider the case where one is driving one’s car along a route planned in advance. It
would be foolish to plan in advance for every possible roadblock that might occur. It
would be dangerous to have no way of reacting should the planned route be blocked
at some point. The usual approach taken to divert from the planned route and feel
one’s way using a sense of direction until a position of the planned route is found
again and the plan is resumed, is a mixture of planning and reaction. The fact that
while driving a car it is not always possible to stop, consult a map and replan the
route indicates the real-time constraints that might favor a reactive approach. It is
better to make a quick decision on which direction to take, even though that may not
turn out to have been the best one, than halt to ponder the decision and cause a pile-
up!

328 Chapter 10
The argument as to whether reactive systems are intelligent falls at the heart of the
question “what is intelligence?” Traditional artificial intelligence has tried to model
behavior which in a human we would regard as signs of high intelligence. Thus,
ability to play a good game of chess, or to solve logical puzzles is often considered
the sign of an intelligent person, indeed IQ tests are based on problem solving. A
computer system, which can solve puzzles or play games, is deemed intelligent on a
subjective basis because it seems to behave as a human would. Intensive media
comment on “computers becoming human” was generated by the first computer to
beat the world chess champion and was not dimmed by explanations of the fairly
simple nature of computer chess-playing algorithms. Similarly, fairly simple reactive
systems can look alive on a subjective human view. For example, a few rules of
attraction and repulsion have been used to model a system which can be viewed as an
animal risking approaching a waterhole while avoiding predators [Kearny, 1992]. A
human viewer is led to believe two predator agents are acting in planned
coordination, though there is no real communication between them. The appearance
of planned cooperative behavior in a system with multiple reactive agents is taken
further in simulations of social insects like ants [Drogoul and Ferber, 1992], where
the behavior extends to different social roles being taken by the agents similar to that
in a real ants’ nest. Drogoul calls this Eco-Problem Solving.
It may be better to use the term Artificial Life [Langton, 1989] for those systems
whose approach to the goal of Artificial Intelligence is to model general life-like
behavior in an unpredictable environment and build upwards from this platform. The
name “Artificial Intelligence” could be reserved for the approach of building systems
that behave intelligently in a more restricted realm. The former could be seen as
building using horizontal layers, while the latter uses vertical layers. The emergence
of intelligent behavior from a collection of reactive agents is a further approach to
building intelligence. Drogoul [1993a] discusses this issue and demonstrates a chess
playing system whose behavior derives from the joint behavior of a collection of
agents, each representing an individual chess piece. This system plays chess to the
point where it can beat weak amateurs, but not a standard search-based computer
chess machine. Drogoul [1993b] has also shown that other classic planning problems,
such as the N-puzzle, can be tackled by collections of agents each of which has no
goal itself and works as a finite state automaton, making just tropistic movements.
Brooks’ robots are themselves collections of agents, since their behavior emerges
from the collective behavior of their layers. Taken further, with the reactive
components within an agent becoming simpler, we eventually reach the neural-
network architecture. Brooks [1991b] is however, careful to distinguish his work
from neural networks. He notes that neural networks consist of undifferentiated
components without a detailed design, whereas his robots are designed and built from
distinguishable components. However, the human brain can be considered as a
network of networks of neurons [Minsky, 1986] with different functions.
Brooks’ approach to building artificial intelligence without the use of representation
is criticized by Kirsh [1991]. Kirsh argues that the lack of internal representational
methods in reactive agents means they will always remain limited to animal-like
behavior. Without a representational language, agents are restricted to simply hard-

Agents and Robots 329
wired goals and thus cannot define their own goals. Reactive agent communication is
on a simple basis, either attractant-repellant behavior, or indirectly through
mechanisms like the robot pebble-dropping involve changing the environment (called
stigmergy [Holland, 1996]).
10.4 Objects, Actors and Agents
Reactive agents, as described above, are similar in some ways to objects in the
computational sense. A reactive agent reacts to messages received on its input sensors
by changing its state and sending messages on its output effectors. An object reacts
on receiving messages by changing its state and sending messages to other objects.
The internal appearance is the same – to the agent the environment it works in as it
interacts through its sensors and effectors might be just another agent. Where it
differs is that agents have autonomy and seek primarily to satisfy their own goals
rather than simply respond to orders in a fixed way. The robot described previously
had the goal of reducing the x and y differences in its state to 0, while avoiding
crashing into blocks and responded to its inputs with whatever outputs would assist in
satisfying this goal. A computational object, however, would not vary its output
depending on its own desires, it simply responds in a predictable manner
Additionally, an agent is embodied not only in the sense of its physical presence in
and interaction with its environment, but also in having its own processor dedicated
to its own use. That is why an object can easily create new objects, since they are just
software entities that can be created by copying and instantiation, whereas robots
don’t usually create complete new bodies for new robots. (This excludes industrial
robots.) An actor in a concurrent object-oriented system, however, could be
considered as being created with its own processor, using the principle of virtual
parallelism discussed in Chapter 6. That is, the assumption that there are always
enough spare processors for any computations declared as running concurrently (with
the practical resource allocation hidden from view). So another approach to multi-
agent systems is to consider agents as a development from concurrent object-oriented
systems, with the addition of further autonomy built into the objects. This should be
distinguished from the use of parallelism for speedup purely to improve response
time. Here the division of tasks between objects is done on a conceptual basis. In
general, the emphasis is on separate objects with separate tasks in the solving of
problems, whereas parallel AI tends to be concerned with large numbers of similar
objects dividing out the work pragmatically.
Object-oriented programming emerged as a silver bullet [Brooks, 1987], as the next
attempt after structured programming to tackle the complexity barrier [Winograd,
1973] whereby computer systems become increasingly risky as their size increases:
difficult to construct, difficult to maintain and difficult to guarantee error-free. A
large part of the complexity is due to the complex nature of possible interactions
(planned and accidental) between different components of a computer program.
Structured programming partitioned code into blocks, thus limiting the range of
control transfers possible, but it left the data unconnected with the control structure.

330 Chapter 10
The key idea of object-oriented programming was encapsulating the data with code,
so that data access too is limited. Concurrent object-oriented programming maps the
logical distribution of the object paradigm onto the physical distribution of parallel
processors. As we have seen, GDC programming can be seen in terms of concurrent
object-oriented programming.
Miller and Drexler [1988] compare the encapsulation of data with the human
ownership of property: both establish protected spheres in which entities can plan the
use of their resources free of interference from unpredictable external influences. This
enables entities to act despite having limited local knowledge, aiding the division of
labor. They take the concept of encapsulation further and propose it be extended to
physical computational resources such as memory blocks or processor time slices.
Clearly this is necessary for a truly autonomous agent, since such an agent needs to
have assurance that it will have the physical resources necessary for it to remain in
active existence responding to inputs in real time. A robot has by definition its own
physical resources but a softbot would need ownership of a share on the machine on
which it resides.
Currently, concurrent languages work on a “socialist” planned economy where
resources are shared out as needed by a central planner or on an “anarchist” basis
where there is a free-for-all (as with human anarchism its success depends on the
assumption that all agents are benevolent towards each other). Miller and Drexler
[1988] propose a “capitalist” ownership of property, in which absolute ownership
rights are protected even where, for example, a planner might see cases where a
reallocation of resources would improve efficiency in reaching the overall goal.
While an agent which is currently idle cannot be forced to give room on a processor it
owns to another which needs the processing capacity, it is suggested that agents may
trade their ownership rights amongst themselves. Ideally, each agent is programmed
to fulfil its own goals and trades resources it has but does not need for resources it
needs but does not have (for example, time slices on a processor could be traded for
memory). The result, it is claimed, will be a better allocation of resources overall
than could be obtained by a global allocation algorithm once the overall system
becomes so complex that it is not possible to operate a simple global resource
allocation algorithm. This is the classic free market economy argument, associated
with Adam Smith [1776] and later economists. The emergence of what from a global
perspective seems a planned algorithm from what on closer inspection seems
unplanned chaos is similar to that which has already been noted with eco-problem
solving, except here there is no suggestion that the components be restricted to simple
reactive agents.
As can be seen, once agents become truly autonomous, the ease with which
discussions on the organization of multi-agent systems slip into analogies with the
organization of human societies becomes irresistible. Fox [1991] suggests that such
analogies are not cute anthropomorphisms, but an inevitable response to the growing
complexity of computer systems and in particular to the problem of bounded
rationality [Simon, 1957], when the complexity of a problem exceeds the capacity of
a single agent to solve it. Organizational techniques to distribute problems amongst
human teams can be applied to distributed computer systems. For example, an

Agents and Robots 331
alternative to arranging multi-agent systems on a flat market-type basis is to construct
hierarchies similar to management hierarchies in large organizations. Quoting
Galbraith [1973], Fox claims that in both human and computer systems, whereas
complexity suggests the market approach, uncertainty, defined as the difference
between the information available and the information necessary to make the best
decision, suggests the hierarchical approach. In the hierarchical approach, managers
can switch tasks and resources between employees as new information becomes
available, whereas the market approach requires the striking of contracts that cannot
be so easily altered.
Another way in which multi-agent systems develop from concurrent object-oriented
systems by employing human metaphors concentrates on the design of individual
agents, ascribing to them mental components such as beliefs, capabilities, choices and
commitments, standing in rough correspondence to their common sense counterparts
in human life. Such an agent is termed an intentional system [Dennett, 1987]. The
idea is most clearly developed by Shoham [1993] who describes a framework called
agent-oriented programming which may be considered a specialization of object-
oriented programming. Agent-oriented programming is a form of object-oriented
programming where the state of objects is restricted to parameters which can be
labeled as mental states and the messages between objects consist of “speech acts”
[Searle, 1969], informing, requesting, offering, promising and so on. The exact
mental attributes that should be given to an agent are a matter of contention.
Following McDermott [1978], Shoham stresses that the decision should not be
arbitrary but should enable the development of a theory that may be used non-trivially
to analyze a system. Beliefs, desires and intentions, leading to the terminology BDI
architecture [Rao and Georgeff, 1991] are a popular set of mental attributes used, but
Shoham prefers beliefs, obligations and capabilities. The values of the mental
attributes within the states are built up using knowledge representation formalism,
often a form of temporal logic.
The beliefs of an agent refer to the model of its environment it has built up. This
model may be incomplete and/or incorrect. In a multi-agent system it may include
beliefs about other agents, indeed in some multi-agent systems the environment may
consist solely of other agents. Desires are the overall goals of an agent, while
intentions are the elements of plans it has made to reach its desires. Shoham’s system
enables a stronger relationship between agents in a multi-agent system to be modeled,
since an obligation is a relationship between one agent and another, with one
committed to the other to bring about some situation. An intention in this case is an
obligation of an agent to itself. The capabilities of an agent are its physical abilities in
the environment it shares with the other agents.
Agents in Shoham’s system are programmed in a language called AGENT-0, which
constrains them to follow certain behaviors. Mental states may not be changed
arbitrarily, but only as a fixed response to speech acts. For example, an agent may not
drop its commitment to another agent, but an agent A may release another agent B
from a commitment that B has to A. An agent will always update its own beliefs in
response to a message informing it of new facts from another agent. In effect, every
agent believes every other agent is telling it the truth. The internal knowledge

332 Chapter 10
representation language of Shoham’s agents is restricted so that checking consistency
when new knowledge is added is tractable. A strong assumption of AGENT-0 is that
all internal updating in response to messages and execution of any commitments for a
particular time can be made in a single real-time interval. The whole system depends
on this cycle being performed each time a real-time system clock emits a signal,
which it does at fixed intervals.
10.5 Objects in GDC
As demonstrated in this book, programming concurrent objects can easily be done in
GDC. The behaviors below define an object of type xyobj that has just two simple
elements to its state, which may be set using messages setx and sety to set each
individually, and setxy to set both to the same value. The values of the components
of the state of the object may be obtained by sending it the messages valx and valy
with an unbound variable argument as a “reply slot”. A new xyobj object with the
same state values as the original may be obtained by sending the message new to the
object, with a reply slot for the reference to the new object:
xyobj([setx(V)|S],X,Y) :- xyobj(S,V,Y).
xyobj([sety(V)|S],X,Y) :- xyobj(S,X,V).
xyobj([setxy(V)|S],X,Y) :- xyobj(S,V,V).
xyobj([valx(V)|S],X,Y) :- xyobj(S,X,Y), V=X.
xyobj([valy(V)|S],X,Y) :- xyobj(S,X,Y), V=Y.
xyobj([new(A)|S],X,Y) :- xyobj(S,X,Y), xyobj(A,X,Y).
To create a new object of type xyobj with initial state values a and b the object
xyobj(S,a,b) is required. S may refer to the object, except that we can only safely
have one writer to a channel. To have several we need to write to separate channels
and merge. If it is necessary to share references to xyobj, we set up objects p and q
:- p(…,S1,…), q(…,S2,…), merge(S1,S2,S), xyobj(S,a,b)
which both have the xyobj as an acquaintance. In concurrent object-oriented
languages, all first-class values in a state are themselves objects, but this is not so in
GDC. Here the two values in the state of the xyobj are just values. If they were to be
objects, the behaviors for xyobj would be more complex:
xyobj([setx(V)|S],X,Y) :- xyobj(S,V,Y), X=[].
xyobj([sety(V)|S],X,Y) :- xyobj(S,X,V), Y=[].
xyobj([setxy(V)|S],X,Y)
:- xyobj(S,V1,V2), X=[], Y=[], merge(V1,V2,V).
xyobj([valx(V)|S],X,Y)
:- xyobj(S,X1,Y), merge(V,X1,X).
xyobj([valy(V)|S],X,Y)
:- xyobj(S,X,Y1), merge(V,Y1,Y).
xyobj([new(A)|S],X,Y)
:- xyobj(S,X1,Y1), xyobj(A,X2,Y2), merge(X1,X2,X),
merge(Y1,Y2,Y).
xyobj([],X,Y) :- X=[], Y=[].

Agents and Robots 333
An object which is input is represented by a channel used as a stream to output
messages, an object which is output is represented by a channel used as a stream to
input messages. Using an object as an argument in a recursive behavior counts as
outputting it. References to an object are tied together by merging all the input
streams, representing each place the object is output into one stream that is sent to the
input occurrence of the object. If there are no output occurrences of an object which is
input, the variable used for its input is sent the empty list value, as in the first three
behaviors above where the input objects X and Y are no longer referred to, being
replaced by V. The final behavior which has been added above is similar to a
destructor operator in conventional object-oriented programming, detailing the
behavior of an object when it no longer has any references. In this case, xyobj
terminates itself and also terminates its references to its acquaintance objects. This
would give automated garbage collection of unreferenced objects were it not for the
problem of self-reference. As an object may have a reference to itself as an
acquaintance, or to an acquaintance which has itself as an acquaintance, or so on, so a
clique of objects with only internal references could remain in existence.
To give an example of a behavior in which messages are sent in response to messages
received, consider additional messages, copyx and copyy, similar to valx and valy.
However, the object returns a reference to new copies of the X and Y acquaintances
rather than references to the original object. If we assume X and Y are programmed to
respond to new messages similarly to an xyobj object, the following will give this
effect:
xyobj([copyx(A)|S],X,Y) :- X=[new(A)|X1], xyobj(S,X1,Y).
xyobj([copyx(A)|S],X,Y) :- Y=[new(A)|Y1], xyobj(S,X,Y1).
The flexible nature of GDC means that many techniques, which in dedicated object-
oriented languages require special language features, may be programmed without
introducing new primitives. For example, consider a version of our original xyobj
(with non-object X and Y values) in which we want two classes of access, one of
which may rewrite the values in the state of the object, but the other of which may
only read them. This can be done by having two output streams as references to an
xyobj object, one with privileged access (able to use the setting operations), the other
without:
xyobj(S,[setx(V)|P],X,Y) :- xyobj(S,P,V,Y).
xyobj(S,[sety(V)|P],X,Y) :- xyobj(S,P,X,V).
xyobj(S,[setxy(V)|P],X,Y) :- xyobj(S,P,V,V).
xyobj([valx(V)|S],P,X,Y) :- xyobj(S,P,X,Y), V=X.
xyobj([valy(V)|S],P,X,Y) :- xyobj(S,P,X,Y), V=Y.
xyobj(S,[valx(V)|P],X,Y) :- xyobj(S,P,X,Y), V=X.
xyobj(S,[valy(V)|P],X,Y) :- xyobj(S,P,X,Y), V=Y.
xyobj(S,[new(A)|P],X,Y) :- xyobj(S,P,X,Y), xyobj(B,A,X,Y), B=[].
xyobj([new(A)|S],P,X,Y) :- xyobj(S,P,X,Y), xyobj(A,B,X,Y), B=[].
xyobj([],[],X,Y).
The two behaviors for the new message show how either privileged or normal access
may be granted. A new message received on the privileged stream causes a new
xyobj object to be created and returns the privileged reference to that object. A new

334 Chapter 10
message on the standard stream returns a standard reference to the new xyobj object.
Clearly, in a complex system, any number of classes of access rights could be
programmed in.
In a similar way, express mode message passing, as employed in the concurrent
object-oriented language ABCL/1 [Yonezawa et al., 1986] may be programmed by
having a separate stream for express messages:
xyobj(S,[setx(V)|E],X,Y) :- xyobj(S,E,V,Y).
xyobj(S,[sety(V)|E],X,Y) :- xyobj(S,E,X,V).
xyobj(S,[setxy(V)|E],X,Y) :- xyobj(S,E,V,V).
xyobj(S,[valx(V)|E],X,Y) :- xyobj(S,E,X,Y), V=X.
xyobj(S,[valy(V)|E],X,Y) :- xyobj(S,E,X,Y), V=Y.
xyobj(S,[new(A,B)|E],X,Y) :- xyobj(S,E,X,Y), xyobj(A,B,X,Y).
xyobj([valx(V)|S],E,X,Y) :- unknown(E)
| xyobj(S,U,X,Y), V=X.
xyobj([valy(V)|S],E,X,Y) :- unknown(E)
| xyobj(S,E,X,Y), V=Y.
xyobj([setx(V)|S],E,X,Y) :- unknown(E)
| xyobj(S,E,V,Y).
xyobj([sety(V)|S],E,X,Y) :- unknown(E)
| xyobj(S,E,X,V).
xyobj([setxy(V)|S],E,X,Y) :- unknown(E)
| xyobj(S,E,V,V).
xyobj([new(A,B)|S],E,X,Y) :- unknown(E)
| xyobj(S,E,X,Y), xyobj(A,B,X,Y).
xyobj([],[],X,Y).
A message is taken from the non-express stream only when there are no messages
available on the express stream, so it is an unbound channel. Here, new xyobj
objects are returned with both their normal and express streams available. As an
alternative to the use of unknown, the alternatively construct of KL1 could be
used to separate behaviors dealing with handling messages from the express stream
(which would be placed before the alternatively) from behaviors dealing with
handling messages from the standard stream.
The creation of new xyobj objects by sending a new message to an existing xyobj
object indicates a form of prototyping [Borning, 1986], that is new objects being
created by cloning old ones. Prototyping is associated with delegation [Lieberman,
1986] where several objects may delegate responsibility to a single shared parent
object. In our cloning of objects, new objects shared the acquaintances of old ones,
through streams, which are merged to a single object. This would give delegation as
Lieberman explained it. For example, a royal elephant is an elephant identical to the
prototype elephant except that its color is white. If E is a reference to a prototype
elephant object, a reference to a royal elephant object could be obtained in R by the
object royal(R,E) where the behaviors for royal are:

Agents and Robots 335
royal([color(C)|R],E)
:- C=white, royal(R,E).
royal([new(A)|R],E)
:- royal(A,E1), royal(R,E2), merge(E1,E2,E).
royal([M|R],E) :- otherwise
| E=[M|E1], royal(R,E).
Any message other than a new message or a color message is passed on to the
prototype to deal with. However, a closer correspondence to inheritance, as
conventionally understood in the object-oriented programming paradigm, is obtained
by cloning the acquaintances of a new object when creating one by cloning, thus:
royal([color(C)|R],E)
:- C=white, royal(R,E).
royal([new(A)|R],E)
:- royal(A,E1), royal(R,E2), E=[new(E1)|E2].
royal([M|R],E) :- otherwise
| E=[M|E1], royal(R,E).
so each royal object has its own elephant object to send messages to other than
new and color messages. In this case, sharing of delegation is not wanted, since
otherwise a change in an attribute a royal elephant has by virtue of it being a form of
elephant would be propagated to every royal elephant. Note that, circular
acquaintance references give problems here as they did with garbage collection, since
if there was a rule that on cloning all acquaintances were cloned, a circular reference
would cause an infinite production of new messages as the circle was continuously
cycled.
The fact that stream merging is explicit in the GDC form of object-oriented
programming means programmers can alter the merge procedures as desired. For
example, a biased merge gives priority access to an object, so
:- p(…,S1,…), q(…,S2,…), bmerge(S1,S2,S), xyobj(S,a,b)
where bmerge passes on values from its second stream only when it has none on its
first stream causes the object p to have priority access to the xyobj object and
:- p(…,S1,…), q(…,S2,…), append(S1,S2,S), xyobj(S,a,b)
locks the xyobj object to the p object. Messages from the q object will only be
passed on to the xyobj object after all messages from the p object (assuming the
convention that objects close their references to acquaintances when they terminate
by sending the empty list, so S1 is a finite list).
Huntbach [1995] has considered proposals for a syntactic sugar or preprocessor so
that programs written in an object-oriented like notation may be translated to GDC in
the way described here. Although the approach considered in this preprocessor is a
compiler into GDC, rather than an interpreter written in GDC which interprets object-
oriented code, the results of the compilation could benefit from the program
transformation techniques outlined in Chapter 9. These would produce code that is
more efficient, but less obviously built on the object-oriented principle than code
directly output by the translator.

336 Chapter 10
Note that a difference between GDC and classic object-oriented programming as
found in Smalltalk and the concurrent object-oriented languages, is that GDC does
not work on the basis that all entities in the language are themselves objects. In GDC,
a client receiving a message knows which arguments are objects and which are
simple atomic values or tuples. Kahn and Miller [1988] point out this is an advantage
in avoiding Trojan horses. They consider a service that computes some mathematical
function according to a proprietary algorithm. If the numbers the client sends are
objects that report back the tests and operations performed on them, the secrecy of the
algorithm is compromised. There are no such problems if the numbers are known by
the receiver of the message to be just atomic numeric values.
10.6 Agents in GDC
Moving the concurrent object-oriented style of programming in GDC towards agent-
oriented programming in Shoham’s sense could be partly just a matter of scale. The
restriction that object states be seen in terms of attributes of mind and messages be
seen in terms of speech acts reacted to appropriately by objects, could simply be
adopted as a code of practice by programmers. Suppose one element of an object’s
state is defined to be its beliefs and another its obligations. Then, an insistence on a
common semantics could be made, such that for example when an object receives a
message inform(B) it adds belief B to its set of beliefs, while when it receives a
message request(C) it adds commitment C to its obligations. But there is nothing in
the semantics of GDC to stop it from idiosyncratically treating the messages the other
way round. Alternatively, a compilation approach could be used so that an agent
language like Shoham’s AGENT-0, with its semantics for these messages and for
object states, is translated into GDC. Note that there is no necessity for an agent to be
represented by a single GDC actor. As we indicated with the royal elephant example,
something, which is conceptually a single object, may be represented by more than
one GDC actor. So several actors could in fact represent an agent, with one managing
each component of the mental state. The beliefs of an agent could be represented
rather like the Linda tuple space we covered in Section 8.8. Hewitt and Inman [1991]
discuss a method by which collections of actors may be composed and viewed as a
single actor.
A successor to AGENT-0 is a language called PLACA [Thomas, 1994]. PLACA
works similarly to AGENT-0, with a propositional temporal logic language used to
construct the mental states of agents and a language for inter-agent communication of
beliefs and requests to take actions. It differs from AGENT-0 in allowing an agent to
request that another agent takes an action which requires planning to achieve,
whereas AGENT-0 allows requests only of primitive capabilities. The fact that
higher-level goals may be communicated in the place of a stream of actions planned
by one agent but requested of another agent to perform, cuts down on the
communication overhead. It is also assumed an agent will be able to do a better job of
planning for itself (including recovering from any unforeseen failures in the plan) on
the basis of an allocated high level goal than following a plan drawn up for it by
another agent.

Agents and Robots 337
An agent in PLACA has an input buffer for both messages from other agents and
information from its sensors. It has two output buffers: one for messages intended for
other agents and one for commands to its own effectors. It can be seen to combine the
robot concept, with its sensors and effectors reacting with the physical environment
and the actor concept, with its interactions with the virtual environment of other
actors. In GDC, a mapping mechanism would be needed to map the logical goals onto
the physical architecture. The fact that GDC has a separate output stream for
messages to each acquaintance is a minor matter of difference. What GDC lacks,
however, to fully implement PLACA is real-time facilities.
At its most basic level, a PLACA agent’s computation consists of the following:
1. Collect messages received from other agents
2. Update its mental state as specified in its program
3. If sufficient time remains before the next tick of the clock, refine its plans
4. Begin execution of the action to be performed next and return to step 1.
Step 3 relies on a global clock and can be compared to the behavior of layered agents
considered above. So long as there is time available, an agent plans by refining its
goals, but it reacts when forced to, in this case by the clock. There is also a facility to
ignore input messages, leaving them in the buffer while planning continues. The
handling of express messages in GDC using unknown or alternatively as
described previously, suggests a clock mechanism could be handled by converting
clock ticks to messages on an express stream. Note that, if the actors performing the
planning share a processor with the process suspended waiting for the planning to
finish or for a clock tick to be received, the waiting process needs to have priority
over the planning processes. As soon as the clock tick is received, it can take action to
shut off further planning.
The physical architecture of guarded definite clause languages is currently not well
developed, not merely by accident but as a matter of principle. The languages
developed on the basis that a declarative style of programming gave programmers the
opportunity to break away from the architecture of the machines on which their
programs ran and to think purely in abstract terms. Parallel architectures were merely
a convenience, which enabled declarative languages to be implemented efficiently.
Since they were not based around the single processor architecture of the von
Neumann machine and since the declarative style involves breaking programs down
into discrete components with well-defined limited methods of communication,
concurrent declarative languages could, it was thought, easily be mapped onto
parallel architectures. It was in the interest of programmers not to have to be
concerned with this mapping. Just as it was in the interest of programmers in high-
level imperative languages not to be concerned with mapping variables onto registers,
core memory and backup store, but instead to leave the operating system to work it
out, while maintaining the illusion of a single store with infinite capacity.
It would not be desirable to depart from this principle of abstract parallelism where it
is not necessary to do so. When an algorithm is AND-parallel it should be enough to
break down the problem into pieces and leave the underlying system to decide where

338 Chapter 10
and when to run each piece, as when one is run relative to another does not affect the
algorithm. The guarded definite clause languages have an AND-parallel basis, but as
we saw with search algorithms can be used to model OR-parallel algorithms. At this
point, the assumption that we need not bother with the physical mapping of process to
processor broke down. The introduction of the priority operator recognized that
computational resources are not infinite and that in some cases the programmer needs
to ensure that finite computational resources are used in an effective manner.
The connection of processes to processors matters in multi-agent systems when as
shown, those agents are connected to the environment through physical sensors and
effectors, needing to make decisions in real time, with a process running an agent.
Miller and Drexler’s ideas of encapsulated control of physical resources may offer a
clean way to incorporate architectural considerations in GDC in a more sophisticated
manner than the simple priority mechanism and thus to construct agents in the sense
where an agent is an actor plus its physical embodiment. A priority attached to a
GDC actor has a meaning only in the global context of an entire GDC computation,
giving privileged access of a process to a processor only if other processes competing
for the processor have not been given higher priorities. However, “ownership” of a
processor or a time-slice on a processor due to resource encapsulation guarantees
access to it. The need for such a guarantee becomes more important as we move away
from systems of benevolent agents where all agents can be assumed to be working
towards a common goal, to competitive systems where agents are pursuing their own,
possibly conflicting, goals.
Waldspurger et al. [1992] describe an experimental system, called Spawn, which
implements market-based access to computational resources based on Miller and
Drexler’s ideas. The system of prioritizing they use is based on one developed for
Actor languages, but which could easily be adapted to guarded definite clause
languages. In it, every transaction must be sponsored by a tick, the basic unit of
computational resource. A global sponsor provides a flow of ticks which is divided
amongst lower level sponsors responsible for individual threads of computation. A
sponsor may either grant a number of ticks to a computation or deny further funding,
in which case the thread is aborted, rather like academic research. Funds may be
allocated in any manner, but may neither be created nor destroyed (unlike GDC
priorities, which can be set at any level arbitrarily). The Spawn system refines this
notion of sponsorship by replacing the straight matching of ticks against resources by
an auction system in which agents bid for time slices on idle processors. The
allocation system used is a sealed-bid second-price auction. That is, bidding agents
cannot access information about other agents’ bids, the agent bidding highest wins the
time-slice but pays the amount offered by the second-highest bidder. If there is no
second bidder, the time slice is given free. The Spawn system was used to implement
a Monte Carlo algorithm running on a network of processors, with figures indicating
some success in establishing a computational market.

Agents and Robots 339
10.7 Top-Down and Bottom-Up Multi-Agent Systems
From the discussion so far, two approaches to multi-agent systems are emerging. One
approach, which could be called bottom-up, develops from work on robots and
softbots and focuses on the individual agent working in its environment. As we have
suggested, an intelligent agent might construct a partial model of its environment
noting the existence of other agents in the environment. The agent may have to exist
in an environment where other agents make changes to the detriment of its own
attempt to reach its goals. On the other hand, other agents may make changes, which
benefit it. We have discussed multi-agent behavior which simply emerges from
reaction rules, but more sophisticated agents may communicate with other agents in
their environment in order to minimize harmful interferences and maximize beneficial
interferences. A team at the Hebrew University in Jerusalem have given extensive
study to the topic of negotiation between agents which may not necessarily share
goals [Zlotkin and Rosenschein, 1991].
The second approach takes multi-agent systems as a development from object-
oriented systems, seeing the concept as a step in an evolutionary process of
programming methodologies forced by the growing complexity of problems tackled
by computer systems. In this case, the environment in which the agents work may be
a network of computers, the agent concept being used as a way to handle
computational resources efficiently without the need for a central planning
mechanism. The environment may also be the other agents, each agent
communicating directly with those it has as acquaintances, or as an alternative, it may
be some blackboard or tuple space so that the agents communicate only indirectly by
adding to and taking from the blackboard. This approach is top-down in that we are
concentrating on seeing a collection of agents working together to achieve a common
goal of the overall system.
In the top-down approach, agents may generally be assumed to be benevolent towards
each other. That is, since the agents in the system exist only to pursue some overall
system goal, an agent can assume that other agents it interacts with will not
deliberately set out to harm or mislead them and agents will willingly help each other
achieve their respective goals. For example, Shoham’s agents accept that when other
agents send them information that information will be true or at least believed by the
other agent to be true and accept requests from other agents without expecting a trade
in return. Such benevolence cannot be expected in systems where there is no overall
goal. We could imagine an automatic trading system in which agents are software
entities acting on behalf of human traders, each of whom has the separate goal of
maximizing his profit. Some trades may be beneficial to both parties: a trader who
has X and needs Y to complete some goal will trade with one who has Y and needs X.
Other trades will be seeking to make a profit at the expense of some other agent’s
loss. Consider two traders who both need X interacting with a third trader that has a
single X to exchange.
The top-down approach moves towards the bottom-up approach when we consider
dividing a problem into self-interested agents as a means of simplifying coordination.
At the cost of needing to resolve local conflict, we lose the need to consider complex

340 Chapter 10
global coordination. In a simple way, OR-parallel search in GDC works in this way.
We need a problem solved, but we are not sure which is the best way to solve it. So
we divide it amongst several agents each trying to solve it in a different way. These
agents compete for computational resources, the processors in a limited
multiprocessor system. Coordination is resolved purely at local level using the rule
that whichever of several agents competing for control of a processor can present the
most promising partial solution (given by its heuristic value) wins. “Competition of
the fittest” ensures that the best solution tends to win out. Jennings [1995] points out
that some degree of “social concern” amongst competing agents is beneficial. He
suggests that agents that ultimately have a common goal be under an obligation to
inform other agents if that goal has become obsolete, or conditions for reaching it
have changed, or it has itself changed in some way. Again, this can be seen as just a
more complex form, befitting a more complex problem, of the passing of bounds in
our distributed search programs which are used to inform search goals of limitations
on the search required of them.
The bottom-up approach moves towards the top-down approach as agents become
more sophisticated, using intelligent techniques to combine goals and develop plans
to work together to achieve them. It has already been noted that an agent may be
layered with a reactive component and a planning component. A third layer is used in
several systems (for example by Müller [1996]) to deal with the multi-agent
coordination work.
A third “middle-out” approach to multi-agent systems comes from distributed
systems. A distributed system is one that consists of several physically distributed
processors. Such processors may store separately maintained databases for example,
with the distributed system involving bringing together information from several
databases. Other forms of distributed systems link together processors containing
sensors and effectors distributed over a physical environment. Such systems move
into the field of distributed artificial intelligence (DAI) when artificial intelligence
techniques are incorporated either in the individual processors, or in their overall
coordination. DAI is sometimes used as a synonym for multi-agent systems (MAS),
but many researchers distinguish between the two [Stone and Velso, 1996]. MAS is
seen as a specialization of DAI which is only applicable when the components of a
DAI system achieve “agenthood” through a high degree of autonomy and possibly
through being constructed on an intentional basis and/or communicating with an
agent communication language.
Ygge and Akkermans [1997] give a critical discussion of the value of bringing agent
techniques into distributed systems. They discuss a classic distributed system
application, the control of air-conditioning in a building. They compare systems
constructed using standard control engineering methods, with systems constructed on
the basis of a collection of agents bidding in a market system for cooling power.
Surprisingly, their conclusion, based on empirical results, is that the multi-agent
approach is at least as effective as the more traditional approach.
Distributed systems may be constructed because of the need to bring together
physically distributed computational mechanisms dealing with a physical problem or
environment. More generally, it has been suggested [Tokoro, 1993] that there will be

Agents and Robots 341
an increasing tendency for computing systems to be constructed by making use of
remote services over networks. This can be seen as an extension of the object-
oriented idea of reusability. In object-oriented programming, programmers are
encouraged to make use of existing libraries of code rather than program from
scratch. In the network computer, programmers make use of existing services in a
more direct way, not by copying their code but by accessing their actual instances,
using an agent in the sense of code embodied by a processor, rather than an object in
the sense of just code. Gelernter and Carriero [1992] suggest that programmers will
move from being concerned mainly with the computational aspects of programming
to being concerned with the coordination aspects, with asynchronous ensembles of
computational entities being brought together by coordination languages becoming
the dominant model of computer systems in the future.
Programmers of such ensembles have the advantage of being able to use expensive
computational mechanisms and extensive databases without the expense of having to
maintain their personal copies. Rather they need only a network computer and access
rights for the limited time-share of the larger system they need. Miller and Drexler
[1988] describe the economic advantages of this “charge-per-use” as opposed to
“charge-per-copy” approach to the use of software. One major advantage is the
inhibition of software piracy. When Miller and Drexler wrote their paper, this could
be seen as an idealistic view of the future, but with the development of the Web it has
moved closer to reality. Currently, Web services tend to be offered free of charge (in
fact free access is exchanged for expected real-world publicity) or are available with
unrestricted access once a real-world agreement to exchange passwords has been
made. Most users of the Web offer little back in return. Miller and Drexler envisage a
world where a personal computer connected to a network may be offered to be used
by any large application, which needs computational resources. The active offering
and exchanging may be done by an agent rather than by the human computer owner.
A computer used intermittently by its owner for domestic tasks, such as playing
games or writing letters might be used (in exchange for real money, or some
computational access rights) by a computationally-bound service (say, a weather
forecasting system). The service searches (again through agents) for computational
power being offered, dividing its computations up as resources are located and bid
for.
10.8 GDC as a Coordination Language
As noted by Gelernter and Carriero [1989], the move towards multi-agent systems
emphasizes the need for coordination or composition [Nierstrasz and Meijler 1994]
languages, acting as the “glue” for joining diverse computational entities together. In
conventional languages, the only coordination activity built into the language is that
which binds the computation to the input/output devices attached to the computer on
which it runs and such I/O is often added grudgingly as an afterthought to a
computational model. Declarative languages can be even worse, since I/O is
dismissed as part of the dirty imperative stuff, which the languages are trying to
escape from. Recently [Wadler, 1997], the concept of monads has been popularized

342 Chapter 10
for obtaining imperative effects cleanly in functional languages. Logic languages
would seem to fall into this trap, since in their abstract form their only means of
communicating with the outside world is through the variables in the arguments to
logic goals. The inductively defined messages of guarded definite clause languages
rescues them from the solipsism of the classic declarative language. As shown in
Chapter 4, partially bound channels bring the ability for conversational information
exchange into guarded definite clause languages. All that is required is for a protocol
to be developed so that channels are connected to external devices, which obey the
“once-only” assignment rule (with the flexibility of partial binding) and guarded
definite clause languages become effective coordination languages. Such a
mechanism is already used in KLIC to provide I/O and links with the underlying
Unix system [Chikayama, 1995]. To print a value x for example from KLIC, it is
necessary to send a message of the fwrite(x) to a stream which has been linked to the
standard output via a primitive defined as making that link. There is no primitive
actors of the form write(x) which simply writes x.
This has some similarity to the monadic approach in functional programming where a
program evaluates to a stream of instructions to some external machine. However, in
the monadic approach there is just a single link between the “mind” of the program
and the “body” of the machine, the analogue of Descartes’ pineal gland as Wadler
[1997] puts it. The use of channels in GDC allows arbitrary numbers of linkages
between the program and the machine, each linkage representing a separate sense
organ or limb.
As noted in Chapter 8, the basis of the Linda mechanism proposed by Gelernter and
Carriero as a coordination language is that a few simple primitives may be added to
any language X to produce the parallel language Linda-X. One primitive, eval, sparks
a new parallel process and parallel processes communicate only through a global
shared database, with the primitive out putting data-objects called “tuples” into this
database, while rd and in read tuples from it (the former leaving it unchanged, the
latter consuming the tuple read). An in or rd statement may contain variables which
are matched against constants in the database, but if no matching tuple is found, the
process containing the statement suspends until another process introduces one with
an out. The system is multi-lingual since systems written in Linda-X may share a
database with systems written in some other language Linda-Y.
An obvious criticism of this approach is that the global database offers no security. A
tuple put out by one process intended for coordination with another may be removed
by a third process using an in inadvertently due to a programming mistake, or by
design if a hostile agent is attempting to “hack” into the system. Various ways of
tackling this problem, generally involving multiple tuple spaces [Gelernter, 1989;
Minsky and Leichter, 1994], have been proposed. Hewitt and Lieberman (1984) note,
however, that once one has got into the complexity of multiple blackboards, one has
lost the conceptual simplicity of the blackboard idea. The argument against using
straight message passing has been lost – a blackboard can be seen as just a
complicated form of message channel.
Primitives of similar simplicity to Linda’s could be added to existing languages, but
which, rather than use a global data base, communicate through shared single-

Agents and Robots 343
assignment variables. Such variables have one writer and may have several readers
and only the process initializing the concurrency (and any process to which access
has been granted recursively) grants access to them. Any reader who needs to access
the value of a variable will suspend until it has been assigned one by its writer, but
unbound variables may otherwise be passed as first-class values. The variables may
be termed single assignments but could also be termed futures, as used in parallel
functional [Halstead, 1985] and object-oriented [Lieberman, 1987] languages. We use
the term future in the discussion below to emphasize the fact that the computations
being coordinated do not themselves have to be written in a logic language. The use
of single-assignment variables as a way of coping with parallelism has also been
considered in imperative languages [Thornley, 1995].
Any language which is to be used to build a component of a system coordinated in
this approach needs a way in which a program in that language may be invoked with
input and output futures and a way of reading and writing futures. A future may be
bound to a constant or to a tuple with a fixed number of arguments each of which are
further futures, which may be bound then or at a later stage. Some sort of error
condition may be raised if there is an attempt to bind a future that has already been
bound. Similarly, when a future is read, it is read as a name and a fixed-length list of
further futures, which is empty if the future is bound to a constant and stores the
arguments to a tuple otherwise. No guarantee can be given as to when or in which
order these further futures may be bound to. For simplicity, assume there is no back-
communication; that is, a reader of a variable is always a reader of arguments of a
tuple to which it becomes bound; a writer is always a writer to the arguments of any
tuple to which it binds a variable. Back communication could be added at the expense
of needing a slightly more complex protocol. Coordination is provided by giving
primitives in languages which provide this reading and writing of tuples; we shall
leave it to others to fit such primitives into existing languages, but they should be no
more difficult to incorporate than Linda’s in, rd and out.
This leaves the need for the equivalent of Linda’s eval. A process named p, which is
a reader of m futures and a writer of n could be set up by
eval(p(x ,…,x )fi (y ,…,y )). Each x ,…x is either a new future or one to which
1 m 1 n 1 m
the originating process is a reader or writer, while each y ,…,y is either a future to
1 n
which the originating process is a writer or a new future. Any of x ,…x which is a
1 m
new future becomes an output future in the calling process, while all y ,…y whether
1 n
new or existing output futures become input futures.
We could also allow a form of eval which sets up multiple processes, possibly
communicating with each other through new futures. In this case, k concurrent
processes are set up by
eval(p (x ,…,x ) fi (y ,…,y ),…p(x ,…x ) fi (y ,…y )).
1 11 1m1 11 1n1 k1 kmk k1 knk
Here, any x
ij
must be either an existing future to which the originating process is a
reader or writer, or a new future and similarly any y
ij
must be either an existing future
to which the originating process is a writer or a new future. No future may occur
more than once in a y position, a new future occurring in a y position becomes an
ij ij

344 Chapter 10
input future in the originating process, any new future occurring in an x position but
ij
not a y position becomes an output future in the originating process. An error
ij
condition occurs if the originating process terminates without binding all its output
futures. This keeps the property that every future has exactly one writer and one or
more readers.
The eval construct allows GDC computations to be set up within foreign language
programs. These computations may use their variables as communication between
these programs and others similarly equipped with a GDC link. Note that for
simplicity of handling a mode is assigned either input or output, to channels used in
non-logic programs, with the fi symbol separating those variables used for input
from those used for output.
It has been described how an interface to a guarded definite clause program can be
defined in another language X with similar ease to the addition of a few primitives to
make Linda-X. The channel binding coordination method removes the insecure tuple-
space blackboard. It fits in with the object-oriented concept, with modularity
guaranteed by the limited means of communication between objects. There is in fact
no way in which a guarded definite clause actor, communicating through a shared
single assignment can know whether that single assignment is shared with another
actor, or is in fact joined to a non-logic process viewing it as a “future” through the
protocol described above.
Kahn and Miller [1988] suggest that guarded definite clause languages have many of
the features required in a language for programming “open systems”, defined as “a
large collection of computational services that use each other without central
coordination, trust or complete knowledge of each other”. Guarded definite clause
actors react to a simultaneous influx of information received asynchronously, because
they must be able to deal with channels being bound by other actors on an
unpredictable timescale. Because channels are both the means of communication and
first-class citizens in the language, guarded definite clause systems have the property
of evolvability, allowing the dynamic linking of names to object and the transfer of
access to a server. Complete encapsulation of data, allowing services to interact with
untrustworthy clients is guaranteed in the guarded definite clause languages since the
only means by which a client may interact with a server is by putting a message on an
channel, which it takes as input and handles itself. The merging of input streams
gives safe mutual reference to objects.
Kahn and Miller note some points where guarded definite clause languages do not
work in a way ideal for open systems. The main one is that they do not have any
mechanisms for dealing with failure, either hardware or software. It is not reasonable
for a service to break because it receives a malformed request, but an actor can only
deal with an input pattern that matches with one of its behaviors. When failure occurs
because no behavior matches, the complete system fails, there is no simple way to
isolate and recover from failure. The guarded definite clause languages assume that a
computation moved to another processor will eventually complete, they do not allow
backtracking and reassignment of a partially completed computation. As noted by
Waldo et al. [1996] partial failure is a central reality of distributed computing caused

Agents and Robots 345
when a machine crashes or a network link goes down. Given the lack of central
coordination, there may not be any agent able to determine that a component has
failed and inform other components of that failure. Clearly this is an area where more
work needs to be done on the guarded definite clause languages if they are to be used
on large-scale distributed networks.
10.9 Networks and Mobile Agents
As an example of the use of GDC for coordination, let us consider a simple setup that
simply coordinates two systems. Suppose we start with:
:- setup(AB,BA,ArgsA)@systemA,
setup(BA,AB,ArgsB)@systemB.
Here systemA and systemB could be considered separate processors or separate
networks of parallel processors. We assume the underlying setup is such that no actor
is moved from systemA to systemB as part of the built-in load balancing of GDC,
though if both are systems of parallel processors, actors may be moved about freely
between them without the programmer giving explicit instructions for it. The
arguments ArgsA and ArgsB could in fact be large numbers of arguments, including
links to sensors and effectors, single arguments are given here for the sake of
simplicity.
Let setup set up two processes, one to manage the system, the other to run a
program on the system:
setup(Out,In,Args)
:– split(Args,SysArgs,ProgArgs),
manager(Out,In,ForSelf,ForOther,SysArgs),
program(ForSelf,ForOther,ProgArgs).
The result of this is that two programs will be running, one on systemA, the other on
systemB and any communication between the two has to pass through a manager.
The stream ForSelf is intended to be used for messages to the system running the
program and ForOther for messages to the other system. Such messages could be
used to access services provided by the systems. The streams are separated and
merged as usual, so:
program(ForSelf,ForOther,Args)
:– split(Args,Args1,Args2),
merge(ForSelf1,ForSelf2,ForSelf),
merge(ForOther1,ForOther2,ForOther),
program1(ForSelf1,ForOther1,Args1),
program2(ForSelf2,ForOther2,Args2).
The manager may choose not to pass on messages intended for the other system, thus
we could have the behavior:
manager(Out,In,ForSelf,[Message|ForOther],Args)
:- acceptable(Message,Args,Flag),
manager1(Flag,Message,Out,In,ForSelf,ForOther,Args).

346 Chapter 10
where manager1 is defined as:
manager1(true,Message,Out,In,ForSelf,ForOther,Args)
:- Out=[Message|Out1],
manager(Out1,In,ForSelf,ForOther,Args).
manager1(false,Message,Out,In,ForSelf,ForOther,Args)
:- handle(Message,Args,Args1),
manager(Out,In,ForSelf,ForOther,Args1).
The second behavior for manager1 indicates the case where the manager decides to
handle the message itself rather than pass it on. Handling the message may cause its
own arguments to change and may also bind return channels in the message. The
presence of return channels in a message means that if it is accepted for sending to the
other system, a direct means of communication between two processes in the two
different systems, which does not go through the manager, is established. It is
assumed that the messages accepted by the manager are those that conform to a
protocol that limits the format of messages passed over.
The managers may need to negotiate about the extent to which they are willing to
accept messages from each other. Negotiations about shared work could be
formalized, for example in the way suggested by Zlotkin and Rosenschein [1989]. Let
us assume an agreement less complex than that, in which the systems simply agree to
charge each other one nominal unit for each transferred message handled, with the
proviso that one system may not go into a debt of 10 or more units to the other. The
manager actor will have an extra argument recording its credit level, so the initial
call to manager in setup is:
:- manager(0,Out,In,ForSelf,ForOther,SysArgs).
To maintain the credits, we have the following behaviors for manager to deal with
sending and receiving messages from the other system:
manager(Credit,Out,In,ForSelf,[Message|ForOther],Args)
:- acceptable(Credit,Message,Args,Flag),
manager1(Flag,Message,Credit,Out,In,ForSelf,ForOther,Args).
manager(Credit,Out,[Message|In],ForSelf,ForOther,Args)
:- Credit<10
| handle(Message,Args,Args1),
Credit1:=Credit+1,
manager(Credit1,Out,In,ForSelf,ForOther,Args1).
with manager1 defined by:
manager1(true,Credit,Message,Credit,Out,In,ForSelf,ForOther,Args)
:- Out=[Message|Out1],
Credit1:=Credit-1,
manager(Credit1,Out1,In,ForSelf,ForOther,Args).
manager1(false,Message,Credit,Out,In,ForSelf,ForOther,Args)
:- handle(Message,Args,Args1),
manager(Credit,Out,In,ForSelf,ForOther,Args1).
The second behavior for manager1 deals with the case where a message is not sent
but is instead handled locally. If the credit level reaches 10, messages from the other

Agents and Robots 347
system are not received but in effect left in a buffer. The system waits until it receives
messages to send and thus reduce its credit level, when they can be received in the
order sent. Note that the credit level is given as an argument to acceptable, as it
may be used as a factor in deciding whether to transfer a message. A behavior to
allow actors to check the credit level of their system may be useful as an actor’s own
decision on whether to send a message for the other system may depend on the credit
level:
manager(Credit,Out,In,[credit(C)|ForSelf],ForOther,Args)
:- C=Credit, manager1(Credit,Out,In,ForSelf,ForOther,Args1).
Clearly, the system management described here could be extended to more complex
arrangements than just two systems communicating with each other. A whole
network of systems can be envisaged, each with its own manager process managing
communication between processes on the system and processes on other systems.
An actor can move itself from one system to the other by converting itself into a
message and sending itself on the ForOther stream. The following behavior will do
this for the actor actor:
actor(ForSelf,ForOther,Args)
:- ForSelf=[], ForOther=[actor(Args)].
The actor has to trust it will be unpacked and turned back into an actor once it has
been sent to the other system. The following behavior will do this:
manager(Credit,Out,[actor(PArgs)|In],ForSelf1,ForOther1,Args)
:- Credit<10
| actor(ForSelf2,ForOther2,PArgs),
Credit1:=Credit+1,
manager(Credit1,Out,In,ForSelf,ForOther,Args),
merge(ForSelf1,ForSelf2,ForSelf),
merge(ForOther1,ForOther2,ForOther).
It is assumed here that the charge for running actor on the new system will be one
credit unit, though a more complex system of charging based on estimated resource
usage could be developed. Note that the arguments to actor will be the same ones as
on the old system including variables which may be used as channels for
communication without going through the manager. The ForSelf and ForOther
streams however refer to the new situation, so ForSelf sends messages intended for
the new system that actor has migrated to and ForOther sends messages to the old
one. Alternatively the ForSelf and ForOther arguments to the new actor could be
put the other way round so that references to systemA and systemB in the code for
actor remain linked to those systems independently of where the code is executing.
The above gives some ideas as to how mobile agents [Knabe, 1996] may be
implemented in GDC. In this case, the idea that agents are autonomous is maintained,
since the actor has to take the initiative to migrate, the first moves towards migration
are not made by the system calling a process over. The migrating process is
dependent on the system it migrates to willingly accepting it, if it were somehow to
trick the system into giving it space and processing time to run, it would be a virus. In
a system involving resource encapsulation the process would have to be assigned

348 Chapter 10
resources, possibly involving some degree of negotiation between systems. The
giving of a limited amount of resources would act as a protection against the
migrating process taking over the system to which it has migrated.
However, mobile agents are generally objects that contain their own code. The code
must be in a form such that it is executable on the system migrated to. We have so far
assumed that every processor in a distributed system has access to a copy of the same
GDC code. Clearly this is not an assumption that can be made if we are considering
open systems. We cannot assume the code for actor on systemA is identical to the
code for actor on systemB. A mechanism for attaching code to messages could be
introduced in GDC. Alternatively, a meta-interpreter approach could be used. If
systemA and systemB both have copies of the behaviors for some meta-interpreter,
a message exchanged between them could consist of data representing code that runs
on this meta-interpreter, plus an initial meta-interpreter goal.
The abstract nature of GDC means it has the platform independence that is essential
for a language for mobile agents. In addition, its declarative nature means there are no
problems with name conflicts, external references and the like. A goal and its
behaviors are a self-contained unit, with shared variables providing all necessary
communication. Knabe [1996] argues for a functional based language to be used for
mobile agents on similar grounds. We have suggested ways in which resource
awareness may be incorporated into GDC, as for example proposed in the Java-
extension Sumatra [Acharya et al., 1996]. Although Java [Gosling and McGilton,
1995] has attracted much attention as a language for Internet applications, it is limited
in its scope for programming truly mobile agents, classified as at best a weakly
mobile code language [Cugola et al., 1996]. Java lacks built-in communication
primitives and agents are unable to initiate migration themselves. The authors of the
Sumatra language claim that truly mobile agents need three properties:
1. awareness – the ability of a computational agent to monitor the availability and
quality of computational resources in its environment;
2. agility – the ability to react quickly to asynchronous events such as changes in
the computational environment
3. authority – the ability of agents to control the way in which resources are used on
their behalf by system support.
The distributed computational environment in a mobile agent system is like the
physical environment in a multiple robot system. The system manager in our example
above works like Sumatra’s resource monitor.
10.10 Conclusion
We have moved a long way from the origin of guarded definite clause programming
with the Japanese Fifth Generation Initiative. The aim initially was to produce a
“parallel Prolog”, on the grounds that this would be the most suitable way to
implement intelligence programs on parallel architectures. Prolog was based not on

Agents and Robots 349
the architecture of a computer, but on a knowledge representation system, predicate
logic, tried and tested by generations of philosophers. Computation in Prolog was
reasoning with logic and knowledge, plus reasoning was thought to equal
intelligence. In addition, the lack of a basis on computer architecture meant that
Prolog was not dependent on the single-processor von Neumann machine, unlike
standard high-level languages, which had been built up in an evolutionary manner
from machine code.
The Fifth Generation Initiative was buried by developments that were visible at its
start, but became much more prominent as it went on. The limitations of predicate
logic as a knowledge representation system became more obvious as logicians
struggled with problems (often involving Tweety the bird who may or may not be a
non-flying penguin) caused by the closed world assumption. Radical critiques of the
knowledge based approach to AI, such as the revived neural network community and
Brooks with his reactive robots, gathered forces. The cycle of hype and inevitable
disappointment at ambitious goals not being reached was seen, as it had been before
and undoubtedly will be again in AI. In the computer world, the standalone
mainframe was succeeded by the networked personal computer. While declarative
languages failed to find much of a market outside their academic developers, object-
oriented programming, in the shape of C++, boomed. The language C++ moved from
initial release to the language of choice for many new developments in a matter of
months, before a satisfactory description of it could be put together. Part of the reason
for its success was that it was a hybrid language, combining high-level object-
oriented principles with low-level control of physical computer architecture. Java
followed on its heels, claiming machine independence but not in the way dreamed of
by the declarative programmers. The first lesson to be learnt from this is the
importance of commercial backing in programming language adoption. The second
lesson was that ideas on programming languages originating in academic research
labs can eventually make it into commercial computing, but we should not
underestimate the timescale required for them to do so. C/C++/Java can be seen as
representing the ultimate triumph of Algol in the 1960s Algol v FORTRAN/Cobol
war.
The Fifth Generation Project concluded viewing the language it developed as its main
achievement [Shapiro and Takeuchi, 1993]. It was flexible [Huntbach and Ringwood,
1995], implementable [Rokusawa et al., 1996] and recognized by some [Kahn and
Miller, 1988] as having potential unmet by most other current languages. However, it
was not a “parallel Prolog”. Prolog turned out to be far more dependent on a single
processor and global structures than was thought when it was adopted as the base for
the Fifth Generation. In making compromises necessary to map the logic paradigm
onto parallel architecture, many considered the guarded definite clause languages had
lost those aspects of logic programming which made it attractive. The Holy Grail of a
language in which programs were logical statements continued to be pursued
elsewhere [Hill and Lloyd, 1994; Wetzel, 1997].
What had been achieved was an abstract concurrent language. The clarity of this
achievement was clouded by arguments over whether it was really logical and
differences over minor matters [Shapiro, 1989] which hid the fact that several teams,

350 Chapter 10
not only the Japanese one but elsewhere, had converged on essentially the same
language. The symbol-processing nature of this language inherited from its logic
background made it suitable for the symbol processing of representational AI. Its
simple operational semantics and declarative nature made it suitable for program
tools such as debuggers, code transformers and abstract interpreters. It enabled the
programmer to think in terms of abstract concurrency while ignoring the real
architectural details of parallel machines.
Almost accidentally, the guarded definite clause languages were found to correspond
closely to the concurrent object-oriented paradigm. This looks less accidental when
one considers that object-oriented programming owes its origins to thinking in
parallel. The ancestor of object-oriented programming, SIMULA [Birtwistle et al.,
1973], was devised as a language to program simulations of systems of several
components working in parallel. The power of object-oriented programming may be
seen as lying in the way it enables the programmer to relax from the restrictions of
having to think about the data of the program being manipulated as a single object in
a purely sequential way. Rather, it exists in discrete parts that can be guaranteed to
remain unchanged in parallel with other parts changing. In performing an action on A
and leaving B unchanged then performing an action on B and leaving A unchanged
we are saved from having to think in terms of performing two sequential actions on
AB. Having to think of an order at all is an unnecessary complexity forced on us by a
