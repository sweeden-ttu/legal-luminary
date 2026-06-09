8 Explaining
To earn p eople’s trust, AI systems need to be able to explain their p erformance.
But what does explain mean, and what counts as a sufficient explanation?
Explanation is one of Marvin Minsky’s (2006) “suitcase” words, which are
words into which p eople pack multiple meanings. For example, a doctor’s
explanation of why you should take your medicine can involve medically
sophisticated causal chains, non- specialist- oriented causal chains, projec-
tions about what will happen if you don’t, population-l evel statistics about
the benefits of the drug, and so on.
Recent years have witnessed an avalanche of publications on trust and
explainability in AI, viewed from scientific, technological, philosophical,
ethical, and societal angles. But how can one explain data- driven systems
that are in princi ple not explainable? By changing the definition of expla-
nation. In data- driven AI, “explanations” do not attempt to convey how
the system works or why it produced the results it did; instead, they pro-
vide corroborating evidence for system results that is disjoint from how
those results w ere derived. So, earning p eople’s trust in such systems then
becomes a m atter of convincing them that non-e xplanatory corroboration
is a reliable measure of the system’s competence. While this rejigging might
satisfy some end users of some applications, it seems unlikely that it will sat-
isfy individuals who are responsible for outcomes in high- stakes domains.
We believe that for AI systems to be truly explainable, they must be
anchored in the kinds of knowledge we have been describing throughout
this book. To recap some key features of this knowledge:
• It must be both interpretable by people and optimized for machine
reasoning.
• It must include computational cognitive models of the world (ontol-
ogy), language, and the agent’s knowledge of self and others: its goals

228 Chapter 8
and plans, biases, preferences, reasoning methods, and more. Notably,
the knowledge should include typical causal chains of events since they
provide the best kind of explanation.
• It must include knowledge about how to derive correlational explana-
tions for cases when causal explanations are unavailable.
• It must support pro cessors that translate input data— language, visual
inputs, and so on—i nto knowledge structures that feed machine
reasoning.
Agents operating with such knowledge w ill emulate h uman be hav-
ior in the tradition of folk psyc hol ogy.1 For example, a h uman physi-
cian can decide to prescribe a par tic u lar medi cation based primarily on
causal information about how it works, but also taking into account
population- based statistics about its efficacy and side-e ffects. Explan-
atory AI systems must emulate this beh av ior. Just as a physician can
explain to a patient that population-b ased statistics do not predict how
he or she w ill respond to a medic ation, so, too, must a clinically oriented
AI system.
Explaining recommendations is impor tant and has been a focus of atten-
tion for data- driven AI. However, LEIAs need to explain much more than
recommendations since they are far more than recommendation systems:
they are collaborators that will function in many ways and learn over time
through their interactions with people. For such collaborations to be suc-
cessful, the p eople involved w ill need to understand many t hings about
their LEIA teammates— what they know, whether they have successfully
learned new information and skills, what they have perceived and done
when operating in de pen dently, what they plan to do now and why, and
so on. Explanation is the win dow into this inner world of LEIAs, and the
microtheory of explanation needs to model it all.
The explanatory potential of the LEIA ecosystem is enhanced by a suite
of visualization tools. All LEIA applications that address specialist domains
are grounded in models that are (a) available for evaluation by domain
experts; (b) open to par am e terization, to accommodate diff er ent expert
opinions; and (c) inspectable by a wide variety of stakeholders: system
users, domain experts, educators, funders, investors, and beyond. Both the
static and dynamic aspects of t hese models can be viewed thanks to visual-
ization strategies that will be presented later in this chapter.

Explaining 229
Explanation-O riented Opportunities in the LEIAs’ Ecosystem
LEIAs can explain
– what they perceive and how they interpret it;
– their reasoning and decision- making;
– their actions;
– their knowledge of language and the world; and
– what they have learned in a given learning session.
Visualization tools allow developers to demonstrate LEIAs’ knowledge and
pro cessing to a broad array of stakeholders.
8.1 LEIAs as Social Agents That Explain
LEIAs are social agents that can play vario us roles in their interactions with
people. Some such pairs of roles are shown in table 8.1. In these dif fer ent
roles, LEIAs need to explain dif fer ent things. For example:
• When a human and a LEIA are collaborating on a task in the same space,
they need to e ither follow predefined rules for their respective roles in
the team or negotiate their roles in real time. The latter can require the
LEIA to explain its understanding of the plan, every one’s role in it, which
step they are carry ing out at a given moment, and so on. The collabora-
tion might involve misunderstandings, as can occur between people.
If the agent does something unexpected, the h uman can troubleshoot
by asking questions like why the agent did something, what it thought
someone said, or what it thought it was asked to do.
Table 8.1
Some roles that humans and LEIAs can play in application systems.
Human Roles Corresponding LEIA Roles
Live collaborator Live collaborator
Remote collaborator Remote collaborator
Teacher Student
Student Tutor
Student Simulated social role (e.g., virtual patient)
Recommendation system user Recommendation system

230 Chapter 8
• When an agent is a remote collaborator—f or example, in the case of an
unmanned vehicle— the human must be able to check what the agent is
perceiving in its environment, what actions it is taking, the rationale for
those actions, and its current plan.
• When a human is teaching a LEIA, the quality and efficiency of that
learning depend on the human’s understanding of what the agent
already knows and whether it has correctly learned the new material.
• When a human is a student, the LEIA can play a part ic u lar social role
that the h uman must learn to interact with, such as a virtual patient.
Depending on the agent’s role, it can need to explain its experiences, its
actions, and/or its decision- making.
• When a human is a student, the LEIA can also serve as a tutor in a train-
ing environment. As a tutor, the agent needs to not only offer situation-
specific advice, flags, and explanations but also put that information
into a larger context that serves teaching goals.
• When a LEIA is used as an assistant to a human decision- maker, it pro-
vides recommendations, warning flags, and reminders. The agent must
be prepared to explain each such move at varying levels of detail.
LEIAs provide explanations under two conditions: when system users
ask for them and as a side effect of generating recommendations and warn-
ings. When users ask for explanations, this is a dialog interaction that plays
out in the normal way (cf. chapter 6): The agent recognizes the request for
explanation as an instance of a par tic ul ar ontological concept, it instantiates
that concept’s adjacency pair, and it follows the algorithm recorded in the
latter to formulate a response. For example, if I think that the agent misun-
derstood who I was talking about, I can ask, Who do you think I was referring
to? The LEIA w ill recognize this as an instance of the concept REQUEST- ID- OF-
REFERENT, whose adjacency pair is EXPLAIN- ID- OF- REFERENT. The latter contains
the algorithm that guides the agent in searching its memory for the iden-
tity of that individual and conveying it through language. When the LEIA
generates an explanation as a side-e ffect of issuing a recommendation or
warning, the default explanation is brief and intended to cover what most
users are likely to want to know. If users do not want such explanations,
they can turn them off. If they want deeper explanations, they can request
them through dialog.

Explaining 231
A LEIA’s status as a social agent is key to its ability to provide satisfactory
explanations. If its initial explanation does not provide exactly what the per-
son wanted to know in terms that w ere fully understandable, the person can
ask follow-up questions. This means that LEIAs w ill be able to provide useful
explanations long before they achieve humanlike sophistication.
There is nothing simple about fashioning an explanation, even after
the knowledge prerequisites for it have been met. Consider the example
of doctors explaining relevant aspects of clinical medicine to patients.
The task has two parts: deciding what to say and how to say it. Both of
these depend not only on medical and clinical knowledge but also on
the salient features of individual patients as hypothesized by the doctor,
such as their health literacy, their interest in medical details, and their
ability to p rocess information based on their physical, m ental, and emo-
tional states. Identifying these salient features involves mindreading, also
known as m ental model ascription.2 An explanation can be presented in
many dif fer ent ways:
• as a causal chain: You feel tired because of an iron deficiency;
• as a counterfactual argument: If you hadn’t s topped taking your medicine
you w ouldn’t be feeling so tired;
• as an analogy: Most people find it easier to remember to take their medicine
first thing in the morning. You should try that; or
• using a future- oriented mode of explanation: If you take your medicine
regularly, you should feel more energetic.
Moreover, explanations are not limited to speech— they can include images,
videos, body language, live demonstrations, and any combination of the
above. Optimizing the automatic generation of explanations tailored to
par tic u lar individuals in part ic u lar circumstances requires a large program
of work in itself. However, as with all other aspects of cognitive modeling,
simpler solutions can be useful as we make pro gress over time.
Modeling explanation, like all cognitive modeling, involves anticipat-
ing and preparing for eventualities. A convenient way to organize the
model is with reference to the agent’s cognitive architecture, anticipating
what humans might want explained about the agent’s perception, rea-
soning (specifically, the kind of reasoning carried out in the Deliberation

232 Chapter 8
module of the LEIA’s architecture), action, and knowledge resources. For
each anticipated explanation need, the agent is provided with an ontologi-
cal concept containing methods to detect what needs to be explained and a
paired concept that guides the agent in providing the explanation (cf. sec-
tion 6.2). These pairs of concepts, connected by the ADJACENCY- PAIR relation,
are recorded in the ontological subtrees headed by REQUEST- EXPLANATION and
PROVIDE- EXPLANATION, shown in t able 8.2.
It is the leaf concepts in each subtree that contain the agent’s reasoning
functions. A pair of expanded subtrees, with their leaf concepts in boldface,
is shown in table 8.3.3 The boldface concepts prepare the agent to detect
and respond to questions about what the agent heard, what it thought
somebody pointed to, and what it saw.
The agent detects what is being asked about—a concept in the left-
hand side of the t able— using its natur al language understanding system.
For example, for the agent to understand that Come again? is a request to
repeat what one just said (REQUEST- REPEAT- STRING), the lexicon needs to map
the English construction Come again? to the concept REQUEST- REPEAT- STRING.
And for the agent to be able to carry out this request, the ontology needs
to contain the procedural knowledge, recorded in REPEAT-S TRING, to guide its
reasoning and action.
Table 8.2
The paired ontological subtrees involving explanation, unexpanded.
– REQUEST- EXPLANATION – PROVIDE- EXPLANATION
+ REQUEST- INFO- AGENT- PERCEPTION + EXPLAIN- AGENT- PERCEPTION
+ REQUEST- INFO- AGENT- ACTION + EXPLAIN- AGENT- ACTION
+ REQUEST- INFO- AGENT- KNOWLEDGE + EXPLAIN- AGENT- KNOWLEDGE
+ REQUEST- AGENT- REASONING + EXPLAIN- AGENT- REASONING
Table 8.3
An example of a pair of expanded subtrees. The leaves are linked using the relation
ADJACENCY- PAIR, so when a request on the left is recognized, the concept on the right
is instantiated and guides the agent in responding.
– REQUEST- INFO- AGENT- PERCEPTION – EXPLAIN- AGENT- PERCEPTION
– REQUEST- INFO- PERCEPTION- RECOGNITION – EXPLAIN- PERCEPTION- RECOGNITION
– REQUEST- REPEAT- STRING – REPEAT- STRING
– REQUEST- POINTED- TO- OBJ – CONVEY- POINTED- TO- OBJ
– REQUEST- SEEN- OBJ – CONVEY- SEEN- OBJ

Explaining 233
8.2 Explaining Perception and Action
When humans and agents are collaborating in person, questions about per-
ception and action are useful for coordinating joint activities and for trouble-
shooting when something goes wrong. When agents are operating remotely,
questions are more likely to seek information about t hings the agent per-
ceives and does that are not directly accessible to the h uman. T able 8.4 pro-
vides some examples.
We will consider a couple of examples in more detail. Imagine that a
future robotic LEIA is assisting its h uman at a barbecue. Among the foods
on the grill are veggie bur gers. From afar, the human yells:
Human: Turn the veggie bur gers!
Robotic LEIA: [Generates a TMR that uses the concept ROTATE to analyze the
ambiguous word turn, which can mean ROTATE or FLIP- OVER.]
OK.
[It rotates the veggie burg ers.]
Human: [ Comes to the grill a c ouple of minutes later to find veggie bur-
gers that are burnt on the bottom and uncooked on the top.]
Why d idn’t you turn them?!
Robotic LEIA: I did.
Human: W hat do you think I meant by turn them?
Robotic LEIA: Rotate them.
This misunderstanding occurred because the agent selected the wrong sense
of the verb turn, which can mean either ROTATE or FLIP- OVER. (Note that Turn
the pizza would mean to rotate it.) This example illustrates a well-k nown
Table 8.4
Examples of requests for explanation concerning perception and action.
Perception Action
– What do you think I said? – What are you d oing?
– What do you think I meant? – Why are you doing that?
– Who/what do you think I pointed to? – Did you [do something]?
– Who/what do you think I was referring to? – Where are you going?
– What do you see? – What are you planning to do next?
– What do you hear?
– What just happened?

234 Chapter 8
source of miscommunication: p eople not realizing that what they are say-
ing is ambiguous or that the addressee d oesn’t have the world knowledge
to understand what is meant.
As another example, consider a situation in which a robotic LEIA is
assisting a h uman in a large room full of h uman and robotic workers. At
some point in a longer exchange, this happens:
Human: Go ask her to come help us.
Robotic LEIA: OK.
[The LEIA sets off in a par tic u lar direction.]
Human: [Watching the LEIA go in the wrong direction]
Wait, where are you g oing?
Robotic LEIA: To get Erica.
Human: We don’t need her, we need Judy.
This illustrates another poss i ble source of misunderstandings between
people: misidentifying the individual referred to by a pronoun.
Perception- and action- oriented explanations share two key similarities:
(1) they involve questions that can be answered using knowledge stored in
the situation model and (2) answering them is straightforward— the agent
need not engage in extensive decision- making about content se lection,
depth of description, or linguistic formulation. The import ant thing is for
the agent to understand what is being asked of it, which is enabled by the
lexicon, where linguistic constructions used to ask questions are mapped to
the associated ontological concepts. If the agent doesn’t understand what is
being asked of it, then it can ask for clarification in the usual way.
8.3 Explaining Knowledge
When humans are teaching or collaborating with a LEIA, they need to
understand what the agent already knows and w hether it has successfully
learned what it was taught. Queries can involve the lexicon, the ontology,
and episodic memory. For example:
• Lexicon: Do you know what upend means? Do you know what it means to
upend something? What meanings of the verb upend do you know?
• Ontology: Are BoTox injections painful? What is needed to diagnose achala-
sia? What are the most common colors of cars? [And, as a follow-up to any
of the above] How do you know?

Explaining 235
• Episodic Memory: Who performed your Heller Myotomy? When did you fin-
ish building this chair? What has Dr. Smith done so far in treating Mrs. Rob-
inson? [And, as a follow-up] How do you know?
As with explaining perception, explaining knowledge requires language
understanding to identify what is being asked and procedural ontological
knowledge to guide the agent in responding. Specific kinds of requests
are recognized as instances of concepts in the ontological subtree REQUEST-
INFO- AGENT- KNOWLEDGE, and the algorithms guiding the agent in respond-
ing are recorded in adjacency pairs in the subtree EXPLAIN- KNOWLEDGE (cf.
table 8.2).
When explaining their knowledge, LEIAs generate the kinds of explana-
tions we think people want when asking dif fer ent kinds of questions. For
example, the answer to yes-no questions is just yes or no or some paraphrase
of them, like I do or I don’t. If I ask an agent Do you know what a stethoscope
is? and it replies Yes, I w ill trust that it knows the right meaning and w ill
move on. I d on’t want the agent to habitually elaborate, saying something
like Yes. I think it means a medical instrument for listening to someone’s heart-
beat or breathing. Of course, it is pos sib le that the agent knows a dif fere nt
meaning than the one I had in mind, but this unlikely situation does not
justify creating agents that are annoyingly verbose. By contrast, if the agent
knows more than one meaning of the word, it responds variously based
on how many senses it knows. If it knows just two senses, it responds I
know two senses, which mean X and Y. If it knows three or more senses, it
says I know # senses of that word and waits to see if the h uman wants more
information. In short, the model of explanation includes normal expecta-
tions about how people behave and what they bring to the table when
collaborating with agents. If an agent’s initial, minimalistic response is not
enough, the h uman can ask a follow-up question as a matter of course.4
Answering questions about the content of the ontology depends on what,
exactly, is being asked about. There are dif fer ent algorithms for answering
questions about ontological property values, questions about scripts, and
broad questions whose answers could involve a variety of ontology ele-
ments. Starting with questions about property values, some eventualities
are as follows:
• The question can ask about a property that has only a value facet, such as
the DEFINITION, so the answer is straightforward. For example, the agent
will answer the question What is an EGD? by generating the filler of the

236 Chapter 8
concept’s DEFINITION field: A diagnostic procedure involving examination of
the lumen of the esophagus, stomach and duodenum using an endoscope.
• The question can ask about a property’s default value. If t here is one, the
agent reports it; if not, it reports the sem value. For example, Q: What are
the most common colors of cars? A: White, black, silver, and gray.
• The question can ask about a property that is defined for multiple fac-
ets, in which case the agent needs to incorporate the diff er ent values
into a fluent English sentence that indicates their status. For example, Q:
Who can perform surgery? A: Most commonly, a surgeon, but in some cases, a
doctor.
• The question can be a non sequitur based on the agent’s ontological
knowledge. For example, Q: How tall is a snowstorm? A: Height isn’t defined
for snowstorms.
As regards ontological scripts, questions can be generic or specific, and
fielding them can be simple or difficult based on what is asked and how
complex the script is. A generic question about a script that contains many
subevents with extensive optionality and variability— for example, Tell me
about GERD—is harder to answer than a specific question about what action
comes next in a script that contains only a half dozen strictly ordered
subevents— for example, What do you do a fter you grind the coffee?
The point of departure for LEIAs in answering open-e nded questions
about complex scripts is the script’s definition field. For example, the defini-
tion of GERD is GERD is a disease that occurs when acid from the stomach flows
back into the esophagus and irritates its lining. The next layer of explanation
leverages the fact that scripts are organized hierarchically, with the nested
subevents also having definitions. These can be strung together, with sur-
face smoothing by the language generation system, to explain how a script
works. Of course, it is also pos si ble to avoid using the definition fields at
all and, instead, construct explanations on the basis of the concept descrip-
tions themselves, using the LEIA’s language generation capabilities. This is
needed for scripts that the agent learns in dep en dently since they do not have
explanatory metadata. It is an empirical question in which other situations
this processing- heavy approach to explaining a script might be justified.
It is impor tant to underscore that LEIAs are not competing with large
language models (LLMs) in answering open-e nded questions about the

Explaining 237
world. When LEIAs field questions, they consult their internal knowledge
bases, which contain less information than the training datasets used by
LLMs. So, when asked how to make coffee, LEIAs build their response on
the basis of their ontological script for making coffee, not unvetted descrip-
tions of coffee- making extracted from uninterpreted texts.
A noteworthy complication of script-o riented questions is that they are
often elliptical— that is, they ask for information that is more specific than
is obvious from the surface form of the question. For example, the question
What do waiters do? is a paraphrase of Tell me the set of events in which wait-
ers typically participate and their role in each of them. Agents need to infer the
specific meanings of such questions during language understanding. For
this example, they need to recognize that the construction What do Xs do?
has a special meaning if Xs is generic and refers to a social role, and do is in
the pre sent tense, s imple aspect. This question is mapped to REQUEST- INFO-
SOCIAL- ROLE, whose adjacency pair, DESCRIBE- SOCIAL-R OLE holds the algorithm
for formulating the response.
To generalize, in keeping with expectation- oriented modeling, the kinds
of script- based questions an agent must be prepared to field include:
• Questions about who or what fills a part ic u lar case- role in an event.
For example, Q: Who gives you advice about wine in a restaurant? A: The
sommelier.
• Questions about the next event in the sequence. For example, Q: What
do you do a fter the waiter takes your order? A: You wait for your food to be
served.
• Questions about the role of someone or something in the script overall.
For example, Q: What do waiters do? A: They explain the menu, take custom-
ers’ orders, serve food, and so on.
• Questions that ask for a description of the script overall. For example, Q:
How do you make coffee? A: First you set the water to boil, then you grind the
coffee beans, and so on.
Apart from scripts, agents need to be able to field broad questions about
ontological knowledge such as Tell me about penguins. The basic algorithm
is as follows: Indicate the concept’s parent; report locally defined property
values, which differentiate the child from its parent; if the concept has any
subclasses, name them; and if the concept is a script— that is, if it has fillers

238 Chapter 8
of the SUBEVENTS slot— launch the EXPLAIN- SCRIPT function. For the penguin
example, this w ill result in: Penguins are a type of bird. They are black and
white, they weigh between 3 and 35 kilograms, they are between 30 and 120 cen-
timeters tall, and they don’t fly. Other clauses in the algorithm for explaining
ontological knowledge anticipate requests for further information, such as
What e lse do you know about penguins?, and requests that the agent explain
what it has learned during a teaching session, such as Tell me what you now
understand about penguins. In modeling the agent’s explanation capabilities,
the first priorities are clarity and accuracy, with the smoothness of the lan-
guage formulation being, at pres ent, less import ant. This is in contrast to
LLMs, which excel at smoothness while having no control over accuracy.
Everyt hing described so far orients around preparing agents to provide
specific kinds of answers to anticipated kinds of questions. None of this
requires the agent to mindread its interlocutor—t hat is, to try to figure
out why the person is asking the question, what background knowledge
he or she already has, and so on. Enabling such mindreading is pos si ble
and would give the agent more sophisticated explanatory power. However,
before undertaking such modeling with res pect to explaining knowledge—
which is all that we are talking about in this section—we must assess how
useful that would be and assign it an associated priority in the overall pro-
gram of LEIA development.
For narrowly focused questions, mindreading is hardly needed except
for choosing which words to use to convey certain information—f or exam-
ple, w hether to use or avoid technical terms. The real need for mindreading
involves open- ended questions, for which dif fer ent kinds of answers are
appropriate for c hildren, non- specialist adults, domain specialists, and so
on. For now, such par am et erization is not a high priority for the same rea-
sons described e arlier: the person can ask follow-up questions as needed, so
the initial explanation need not be perfect, and we expect p eople to behave
in reasonable ways and ask appropriate questions. It would not make sense
to ask a LEIA that has significant expertise in clinical medicine a question
like What do you know about health care? Even a human would balk at such
a question.
Turning, fin ally, to episodic knowledge, explanation requests and
responses are very similar to those involving the ontology. The most note-
worthy difference between explaining ontological and episodic knowledge

Explaining 239
involves the fact that episodic knowledge actually comprises two diff ere nt
things: information relating to the agent and its human collaborators, and
information about real- world entities outside of the agent’s world. By defini-
tion, the agent has full knowledge about its private experiences. By contrast,
when it comes to public information, it can lack episodic knowledge just
like it can lack ontological knowledge. However, recall what we are talking
about: explaining the agent’s knowledge. This is quite dif fer ent from casting
LEIAs as all-p urpose question- answering systems, which they are not.
People can ask LEIAs questions about ontology or episodic knowledge
either to refresh their memory or because they don’t know the answer. If
they are just refreshing their memory and the response sounds right, then
no explanation is needed. By contrast, if the answer does not sound right,
or if the information is new, then they might want to validate its verac-
ity. To do so, they might ask questions like How do you know? or What
exactly did you read/hear/find? In some cases, the agent will have recorded
the source of information as metadata, as when it engages in learning by
reading or is being instructed by a par tic u lar human. In cases when the
source of information is not known, the agent could be instructed to search
a corpus for corroborating information that includes a source; but this goes
beyond the basic functionality of enabling agents to explain their current
state of knowledge.
This section has described how a LEIA can explain the content of its lexi-
con, ontology, and episodic memory. This does not exhaust its knowledge.
Another aspect of its knowledge is that which underlies its reasoning, to
which we now turn.
8.4 Explaining Reasoning
According to the AGENT- FUNCTIONING- FLOW script that implements the LEIA’s
architecture (cf. section 3.2.4), agent action is triggered in four ways:
1. The action can be the output of a specific decision function. For exam-
ple, when the agent is serving as an advisor, if it detects a user error, it
issues a warning flag.
2. The action can be the ADJACENCY- PAIR of the previous event. For example,
when a person asks a question, the agent answers it.

240 Chapter 8
3. The action can be triggered by a daemon (a standing goal). For exam-
ple, a par ticu lar virtual patient might need to know if procedures are
painful before agreeing to them. If the doctor recommends a procedure
for which the patient lacks information about pain, it posts the goal of
tracking down that information.
4. The action can be the next step in the current plan on the agent’s agenda,
launched when the previous step is completed. For example, if a robotic
LEIA is building a chair, then after it attaches the first leg, it undertakes
to attach the second leg, and then the third, and the fourth.
In all cases, the agent knows why it chose a given action. Formally, this is
recorded as metadata with the remembered instance of the event. For cases
2–4, explaining the reasoning is relatively straightforward, apart from some
details of language generation. If the agent is asked Why did you say that? or
Why are you doing that? it answers:
2a. B ecause [a brief description of the first event in the adjacency pair]. For
example, Q: Why did you say that? A: Because Joe asked me where I was
going.
3a. Because [a brief description of the daemon]. For example, Q: Why did
you ask that question? A: B ecause I need to know if procedures are painful
before agreeing to them.
4a. It’s the next step in [plan name]. For example, Q: Why are you d oing
that? A: It’s the next step in building a chair.
By contrast, explaining decision functions, the first case above, is more
complicated since t hose decisions can involve not only agent actions but
also recommendations, advice, warnings, and so on. Examples of what a
person might want to know about decisions include, among many others:
• Why did you do that?
• Why did you recommend that?
• Why do you think that what I was planning to do is wrong?
• What did you base your recommendation on?
• Was your recommendation informed by machine learning?
• Would any additional information be useful in making this decision?
• How sure are you of this recommendation?
• Are you sure this is best?
• Why is [option X] better than [option Y]?

Explaining 241
The most impor tant point about preparing LEIAs to explain their decision-
making is that all of the information they need is either recorded as knowl-
edge associated with the decision function or is dynamically generated and
stored as metadata while the decision is being made. This means that agents
do not need to invent or reconstruct the reasoning behind their decisions if
they are asked about them; they need only look up what was already prepared
and then package it as a situationally appropriate utterance.
The static and dynamically generated information a LEIA relies on to
explain its decision-m aking is recorded as values of the following metalevel
properties:
• EXPL provides a short E nglish explanation of a decision function; it typi-
cally includes variable slots.
• CONFIDENCE holds the agent’s confidence in the decision, m easured on
the abstract scale {0,1}.
• RELEVANT-F EATURES holds the list of properties whose values, if known, con-
tribute to the decision.
• CONTRIBUTING- FEATURE- VALUES holds the list of actual property values con-
tributing to the decision in the given context.
• ABSENT-F EATURE- VALUES holds the list of properties for which the decision
function needs values that are unknown in the given context.
• ROLE- OF- ML conveys the role of data- driven methods in the decision, apart
from its role in perception proc essing, which is considered separately;
the role of ML affects the agent’s confidence in the decision.
• COMPARISON- OF- OPTIONS holds the result of comparing decision options
that are above a quality threshold.
• IDIOSYNCRATIC- DECISION-T RACE allows for any other aspects of the decision
function to be prepared in advance as an explanation; for example, a
numerical calculation that contributes to a decision can be described in
detail in plain English.
We will describe the use of these features on the example DETECT-J UMPING-
TO- CONCLUSIONS- DIAGNOSIS, which is used by agents that are serving as medi-
cal tutors or advisors. This algorithm detects w hether a diagnosis posited
by a system user is clinically appropriate. H ere we focus on how this algo-
rithm’s content supports explanation; how the algorithm is used in a medi-
cal application system is described in section 8.5.

242 Chapter 8
DETECT- JUMPING- TO- CONCLUSIONS- DIAGNOSIS
DEFINITION This procedure detects if a doctor has sufficient evidence to make
a diagnosis.
AGENT LEIA
SUBEVENTS
TRY: sufficient- grounds- to- diagnose-ok
EXPL “ Diagnosing [DISEASE] is clinically valid. The relevant feature val-
ues are [CONTRIBUTING- FEATURE- VALUES].”
TRY: no- sufficient- grounds- to- diagnose
EXPL “ Diagnosing [DISEASE] is not clinically valid. [CONTRIBUTING- FEATURE-
VALUES] contribute to making the diagnosis but [ABSENT- FEATURE-
VALUES] must also be known.”
This algorithm has two conditions. The first one detects situations
in which all of the necessary preconditions for diagnosing the disease,
which are recorded in the ontology, have been met, so the move is clini-
cally valid. When this condition holds, the agent explains its decision by
generating the content of the EXPL field, which includes two dynamically
populated variable slots: the name of the disease and the feature values
that made the diagnosis valid. The CONFIDENCE in this decision is 1 (fully
confident) because the decision involves simply comparing feature values
in the ontology with feature values in the dynamically populated patient
model.
The second condition covers cases in which necessary preconditions for
the diagnosis have not been met. The agent explains this decision as before:
by generating the content of the EXPL field, which has a dif fere nt set of
dynamically populated variable slots. The CONFIDENCE in this decision is also
1 for the same reason as above.
The final three features in the list above—R OLE- OF- ML, COMPARISON- OF-
OPTIONS, and IDIOSYNCRATIC- DECISION-T RACE— are not applicable for this part ic u-
lar decision function but they are needed for o thers, such as recommending
a par tic u lar treatment option.
8.5 An Example: LEIAs Serving as Tutors and Advisors Explain
Their Reasoning
Tutoring students and advising professionals have much in common. LEIAs
use the same knowledge and reasoning for both but package messages

Explaining 243
differently for the diff er ent audiences. For this overview, we w ill disregard
minor differences between tutoring and advising and treat them as a single
capability. But before getting into how LEIAs tutor and advise, we need
some background about an impor tant source of errors in human decision-
making: cognitive biases.
Cognitive bias is a term used by psychologists to describe distortions in
human reasoning that lead to empirically verified, replicable patterns of
faulty judgment (Kahneman, 2011). Cognitive biases result from the inad-
vertent misapplication of necessary human abilities: the ability to simplify
complex probl ems, make decisions despite incomplete information (i.e.,
decision- making under uncertainty), and generally function under the real-
world constraints of limited time, information, and cognitive capacity (cf.
Simon’s [1957] theory of bounded rationality). Factors that contribute to
cognitive biases include, non- exhaustively:5
• overreliance on one’s personal experience as heuristic evidence;
• the misinterpretation of statistics;
• overuse of intuition over analy sis;
• acting from emotion;
• the effects of fatigue;
• considering too few options or alternatives;
• the illusion that the decision-m aker has more control over how events
will unfold than he or she actually has;
• overestimation of the importance of information that is readily available
over information that is not;
• framing a probl em too narrowly; and
• not appreciating the interconnectedness of multiple decisions.
Even if one recognizes that cognitive biases could be affecting decision-
making, their effects can be difficult to counteract. As Heuer (1999) writes,
“Cognitive biases are similar to optical illusions in that the error remains
compelling even when one is fully aware of its nature. Awareness of the
bias, by itself, does not produce a more accurate perception. Cognitive
biases, therefore, are, exceedingly difficult to overcome” (112). When serv-
ing as tutors and advisors, LEIAs can offer objective assessments of when
a cognitive bias might be at play. This should be more useful than simply

244 Chapter 8
reporting potential user errors with no insight into where the persons’ rea-
soning might have gone wrong.
Returning to LEIAs, they know how to tutor and advise on the basis
of the ontological subtree headed by the concept TUTORING- AND- ADVISING.
This concept indicates that tutoring and advising comprise two kinds of
actions: (1) evaluating user moves and flagging prob lems, and (2) answer-
ing questions.
TUTORING- AND- ADVISING
DEFINITION Tutoring and advising involves evaluating user moves, flagging
errors, and answering questions.
AGENT HUMAN, LEIA
BENEFICIARY H UMAN, LEIA
SUBEVENTS
EVALUATE- FLAG- USER- MOVE
RESPOND- TO- REQUEST- INFO
TUTORING- AND- ADVISING is an intermediate node in the ontology that is
not ever instantiated as a script, but it contains the knowledge that allows
an agent to answer questions like What is involved in tutoring and advising?
The first subevent of TUTORING- AND- ADVISING, called EVALUATE-F LAG- USER-
MOVE, is a script that has its own subevents, which involve detecting both
plain errors and errors resulting from cognitive biases.6
EVALUATE- FLAG- USER- MOVE
DEFINITION This script evaluates user moves and detects dif fer ent kinds of
errors, including those that might result from cognitive biases.
AGENT LEIA
BENEFICIARY H UMAN
SUBEVENTS
TRY: DETECT- PLAIN- ERROR
TRY: DETECT- JUMPING- TO- CONCLUSIONS
TRY: DETECT- FRAMING- SWAY
TRY: DETECT- SMALL- SAMPLE- BIAS
TRY: DETECT- BASE- RATE- NEGLECT
TRY: DETECT- ILLUSION- OF- VALIDITY
TRY: DETECT- EXPOSURE- EFFECT
In teaching and advising applications, the LEIA evaluates each move
by the user to see if it reflects any known kind of mistake. Procedurally,
this means the LEIA tests whether each move fulfills the preconditions

Explaining 245
of any of the SUBEVENTS of EVALUATE- FLAG- USER- MOVE. If the preconditions for
detecting any of t hese error types are met, the agent issues an associated
message.
EVALUATE-F LAG- USER-M OVE is an intermediate node in the ontology whose
description is useful if someone asks an agent a metalevel question like
What do tutors do? or What kinds of mistakes do tutors look out for? However,
in order for the agent to perform as a tutor or advisor in an application,
it needs domain-s pecific knowledge, which is recorded in the appropriate
descendant of TUTORING- ADVISING-S CRIPT, for example:
TUTORING- ADVISING- SCRIPT
TUTORING- ADVISING- CLINICAL- MED
TUTORING- ADVISING- FURNITURE- ASSEMBLY
TUTORING- ADVISING- DRIVING- A- VEHICLE
Taking the example of clinical medicine, when a tutoring or advis-
ing session for clinical medicine begins, the agent places an instance
of TUTORING- ADVISING- CLINICAL- MED on its agenda. One of its subevents is
EVALUATE- FLAG- CLINICAL- MED- MOVE, which holds the knowledge about how to
respond specifically to actions in the domain of clinical medicine.
EVALUATE- FLAG- CLINICAL- MED- MOVE
DEFINITION This script evaluates user moves in the domain of clinical medi-
cine and detects dif fer ent classes of errors, including those that
might result from cognitive biases.
AGENT LEIA
BENEFICIARY H UMAN
SUBEVENTS
TRY: DETECT- PLAIN- ERROR- MED
TRY: DETECT- JUMPING- TO- CONCLUSIONS- MED
TRY: DETECT- FRAMING- SWAY- MED
TRY: DETECT- SMALL- SAMPLE- BIAS- MED
TRY: DETECT- BASE- RATE- NEGLECT- MED
TRY: DETECT- ILLUSION- OF- VALIDITY- MED
TRY: DETECT- EXPOSURE- EFFECT- MED
For purposes of illustration, we will describe two of these subevents: the
one that detects jumping to conclusions, which we introduced in passing
earlier; and the one that detects presenting information using a framing
sway, which involves phrasing it in a way that could subtly influence the
hearer’s response to it.

246 Chapter 8
Agents detect jumping to conclusions by comparing user moves against
the preconditions of good practice recorded in the ontology. Good practice
is encapsulated in guidelines, agreed upon by clinicians, that inform clinical
decision- making. For example, there are guidelines for determining when
there is enough evidence to hypothesize or diagnose a disease, and when
it is justified to recommend tests and interventions. T able 8.5 shows some
of the preconditions of good practice recorded in the ontological descrip-
tion of the disease achalasia. For readability, the fillers are described using
English strings rather than meaning repres en ta tions written in the ontologi-
cal metalanguage.
Using this information, agents functioning as tutors and advisors can
detect and flag if users are making moves that are not yet clinically justified,
and they can answer questions like Can a diagnosis be made yet?
A knowledge-e ngineering aside. Tables like 8.5 served as the common ground
between knowledge engineers and physician educators during development of
the Maryland Virtual Patient system, and they are useful in presenting cogni-
tive models to students, educators, and other stakeholders.
Although we already presented the algorithm for detecting jumping to
conclusions about diagnoses, we repeat it h ere for easy comparison with
table 8.5, in order to emphasize how agents leverage knowledge while eval-
uating decision functions.
Table 8.5
Some of the preconditions of good practice related to the disease achalasia.
Property English gloss of filler
SUFFICIENT- GROUNDS- TO- SUSPECT Dysphagia to solids and liquids or regurgitation
SUFFICIENT- GROUNDS- TO- DIAGNOSE All four of the following conditions:
1. either bird’s beak or lower esophageal
sphincter pressure > 45
2. aperistalsis
3. either dysphagia or regurgitation
4. negative EGD for cancer
SUFFICIENT- GROUNDS- TO- TREAT Definitive diagnosis of achalasia
PREFERRED- ACTION- WHEN- DIAGNOSED Pneumatic dilation or Heller myotomy
REASONABLE- ACTION-W HEN- DIAGNOSED Administer BoTox

Explaining 247
DETECT- JUMPING- TO- CONCLUSIONS- DIAGNOSIS
DEFINITION T his procedure detects if a doctor has sufficient evidence to
make a diagnosis.
AGENT LEIA
SUBEVENTS
TRY: sufficient- grounds- to- diagnose-ok
EXPL “Diagnosing [disease] is clinically valid. The relevant feature values
are [contributing- feature- values].”
TRY: no- sufficient- grounds- to- diagnose
EXPL “Diagnosing [disease] is not clinically valid. [contributing-f eature-
values] contribute to making the diagnosis but [absent- feature- values]
must also be known.”
If a user diagnoses a disease, the agent evaluates the move against its
knowledge of good clinical practices. If the move is valid, then the agent
simply rec ords it, including why it was justified, in case the agent is
asked about it later on. The justification is a trace of the preconditions
that were fulfilled in order to satisfy the conditions of the function
sufficient- grounds- to- diagnose-ok.
If, by contrast, a user move is incorrect, then the agent instantiates
the concept FLAG- CLINICAL- MOVE, which is the output of the function no-
sufficient- grounds- to- diagnose, and passes to that function the information
about which move was erroneous and why.
Consider the following example that shows how a LEIA playing the role
of a tutor responds when a clinician in training posits a diagnosis without
sufficient evidence.
• The student says to the virtual patient You have achalasia.
• The LEIA’s language understanding system understands this to mean
“DIAGNOSE- DISEASE-1 (THEME ACHALASIA-1 ) (ACHALASIA-1 (EXPERIENCER PATIENT- 1)).”
• Since TUTORING- ADVISING-C LINICAL-M ED is on the agent’s agenda, given the
agent’s role as a tutor, the agent tests every thing it perceives against all
of that plan’s SUBEVENTS, one of which is EVALUATE-F LAG- CLINICAL- MED- MOVE.
• We assume for this example that the diagnosis matches the second con-
dition, no- sufficient- grounds- to- diagnose, because although the first
three conditions of SUFFICIENT- GROUNDS- TO- DIAGNOSE in table 8.5 are ful-
filled, the fourth one is not: negative EGD for cancer.
• The LEIA reco rds relevant metadata associated with this decision:
– CONTRIBUTING- FEATURE- VALUES (in plain English): a bird’s beak, aperistal-
sis, and dysphagia.
– ABSENT-F EATURE- VALUES (in plain E nglish): negative EGD for cancer.

248 Chapter 8
• The LEIA instantiates FLAG- CLINICAL- MOVE, and its language generation
system outputs: “Diagnosing achalasia is not clinically valid. A bird’s
beak, aperistalsis, and dysphagia contribute to making the diagnosis but
a negative EGD for cancer must also be known.”7
Dedicated algorithms relying on ontological knowledge similar to that
in table 8.5 are available to the agent for evaluating w hether the precon-
ditions of good practice have been fulfilled for recommending tests and
procedures as well.
Which kind of warning the agent generates depends on the type of user,
student vs. professional, as well as user preferences about how much informa-
tion to provide when issuing warnings. For example, in the Maryland Virtual
Patient application, students could choose to see no tutoring messages, mini-
malistic messages (e.g., t here is insufficient evidence to diagnose a disease),
messages with context-s pecific information (e.g., what else must be known
in order to diagnose the disease in the given patient), or messages with exten-
sive additional information (e.g., all of the dif fer ent ways of fulfilling the
preconditions for diagnosing the given disease). The information- rich option
is illustrated by figure 8.4 in section 8.7, which shows all clinically justified
grounds for ordering the test called EGD as well as which preconditions were
already satisfied at the given point in the given simulation run.
The second example of a flaggable user move that we w ill consider
involves linguistic priming. In clinical scenarios, the way a doctor describes
interventions, pres ents options, and asks questions can impact patients’
impressions and their subsequent decision-m aking. For example,
• If the doctor asks “I imagine your throat hurts, right?,” the patient w ill
have a tendency to seek corroborating evidence, even if he or she had
not previously noticed any throat pain. This is the confirmation bias.
• If the doctor asks “Your pain is very bad, isn’t it?,” the patient is likely to
overestimate the perceived pain, having been primed with a high pain
level. This is the priming effect.
• If the doctor says, “ There is a 20% chance that this procedure will fail,”
the patient is likely to interpret the procedure more negatively than if the
doctor had said, “T here’s an 80% chance that this w ill succeed.” This is
the framing sway.
Agents can help doctors to be aware of, and learn to avoid, such formu-
lations by flagging potentially bias-i nducing utterances. The detection

Explaining 249
methods involve recognizing linguistic constructions as par tic u lar ontolog-
ical concepts, which are located in the DETECT-B IASED- LANGUAGE branch of the
SPEECH-A CTS subtree of the ontology. T able 8.6 provides examples.
Although the agent can detect utterances with a framing sway, it remains
a research issue when it should report them. For example, it is entirely appro-
priate, and an indication of compassion, for a doctor to say to a patient who
has asked for an increase in pain medi cation, “So, the pain is pretty bad?”
In addition to proactively responding to user moves, agents function-
ing as tutors and advisors can answer questions in the normal way. The
agent interprets the questions as instances of specific ontological concepts
using constructions in its lexicon and it looks up the adjacency pair of the
relevant concept to determine how to answer. T able 8.7 provides examples.
Table 8.6
Examples of constructions that can lead to biased decision- making.
Example Associated bias- detection function
I assume you d on’t eat before bed, right? DETECT- SEEK- CONFIRMATION- QU
Do you feel a sharp pain in your chest? DETECT- SUGGESTIVE- YES/NO- QU
Do you have heartburn between 10 and 20 DETECT- PRIME- WITH- RANGE-Q U
times a week?
There’s a 15% chance this procedure will fail. DETECT- NEGATIVE- FRAMING- SWAY
There’s an 85% chance this procedure will DETECT- POSITIVE- FRAMING- SWAY
succeed.
Table 8.7
Examples of the adjacency pairs for asking questions about clinical moves.
Sample Questions Concepts Reflecting the The Adjacency Pairs
Meaning of the Questions Guiding the Response
Can I diagnose achalasia yet? REQUEST- INFO- DIAGNOSIS- EVALUATE- DIAGNOSIS-
POTENTIAL POTENTIAL
Which diagnoses should I be REQUEST- INFO- DISEASE- EVALUATE- DISEASE-
thinking about? HYPOTHESIS- POTENTIAL HYPOTHESIS- POTENTIAL
Is it OK to order an EGD? REQUEST- INFO- TEST- EVALUATE- TEST- ORDERING-
ORDERING- POTENTIAL POTENTIAL
Would Heller Myotomy be a REQUEST- INFO- MED- EVALUATE- MED-
reasonable recommendation? INTERVENTION- POTENTIAL INTERVENTION- POTENTIAL

250 Chapter 8
All of the algorithms guiding the agent’s responses use the same kinds of
ontological knowledge as illustrated in the above t ables. For example, the
EVALUATE-D IAGNOSIS- POTENTIAL script evaluates and reports on w hether:
• the known feature values of a patient make it poss ib le to diagnose a dis-
ease; if so, which one or ones;
• the known feature values of a patient make it poss i ble to hypothesize an
as- yet not hypothesized disease;
• the known feature values of a patient are not sufficient to diagnose a
hypothesized disease; if so, which features values are missing; and
• the known feature values of a patient make it impossible to diagnose or
hypothesize any disease.
If users want more information than is provided by this algorithm, they
can ask for it. For example, if, at the given time, no disease can be diag-
nosed or hypothesized and the agent says so, the human can follow up with
a question about related ontological knowledge, such as “What is needed
to diagnose [some disease]?” The agent w ill answer using its methods for
explaining ontological knowledge, described in section 8.3.
8.6 How Empirical Contributions to LEIA Operation Affect Explainability
Data analytics and machine learning have impor tant roles to play in
explanation- capable systems. For example, visual object recognition,
speech recognition, and syntactic parsing can be performed using data-
driven methods, and data-d riven recommendation systems can inform
LEIA decision- making. The question is, how do the unexplainable contribu-
tions of data- driven systems affect the overall explainability of LEIA opera-
tion? The answer depends on the system module in question.
Perception Recognition is primarily handled by data- driven tools, such
as image and speech recognition systems. When an image recognition sys-
tem recognizes an image as a tree, or a speech recognition system recog-
nizes an utterance as His bicycle isn’t, those results cannot be explained.
In straightforward cases— when the signal is clear and the recognition is
confident— the lack of explainability is not a prob lem. However, when a
signal is unclear, incomplete, or ambiguous, Perception Recognition tools
perform worse than p eople. This is b ecause people can use the context and
their knowledge of the world to recognize a largely occluded object or a

Explaining 251
disrupted speech signal, and they can explain how they did it. For practical
purposes, the unexplainability of data-d riven Perception Recognition is not
a prob lem when the answer is right, but it is a big probl em when the answer
is not right. Of course, if agents are ever to achieve humanlike capabilities,
they need to be able to explain even high- confidence Perception Recogni-
tion in terms of feature values— for example, how to distinguish a dog from
a cat with reference to features that they can describe and point to.
Perception Interpretation—t hat is, translating raw recognition output
into ontologically grounded meaning representations— also incorporates
certain data- driven tools. For example, use of a statistical syntactic parser
means that the agent can say what the parse is but not why. This does not
seriously undermine the explainability of language understanding since
syntactic parsing plays only a supporting role in what is overwhelmingly a
semantic and pragmatic p rocess.
Data- driven tools can also inform the reasoning carried out in the
Deliberation module of the LEIA’s architecture. For example, LEIAs could
use LLMs to help them to estimate unknown feature values in decision
functions and to incorporate population-l evel statistical evidence into their
decision- making. However, since the output of LLMs is not explainable,
LEIAs must be prepared to incorporate into their own explanations the
role and relative weight of such evidence in their overall decision- making.
Hybrid decision-m aking of this type is a practical approach to getting the
best from knowledge- based and data- driven approaches; and making the sta-
tus of the resulting decisions maximally explainable is key to gaining the trust
of human decision- makers.
8.7 Visualizations for Explanation in the Maryland
Virtual Patient System
The model of explanation described in this chapter reflects our first attempt
at a broad- coverage microtheory of explanation, but this is not the first
time that explanation has been a part of LEIA modeling. For the Maryland
Virtual Patient (MVP) clinician- training application, a core requirement was
explainability to a variety of stakeholders—t eachers, non- teaching domain
experts, students, developers, and funders. A core strategy for fulfilling this
requirement was the use of visualizations, three examples of which we pre-
sent below by way of illustration.

252 Chapter 8
Visualization as Explanation. The goal of explanation is to provide insight into
what is being explained. Language is one way of providing such insight, and
visualizations are another. Visualizations are a useful method of explaining
knowledge bases, cognitive models, and algorithms, and they are indispens-
able for providing traces of system proc essing that are accessible to developers
and non-d evelopers alike.
Visualizing the physiological models underl ying virtual patients Modeling
human physiology to support dynamic, interactive virtual- patient simula-
tions is not about trying to replicate a human in the box. Instead, a knowl-
edge engineer leads physicians serving as subject matter experts through the
process of distilling their extensive knowledge about physiology and clini-
cal practices into the most relevant subset and expressing it in sufficiently
formal terms. Not infrequently, specialists are also called on to hypothesize
about the unknowable, such as the preclinical (i.e., pre-s ymptomatic) stage
of a disease and the values of physiological properties between the times
when tests are run to m easure them. Such hypotheses are, by nature, impre-
cise. However, rather than permit this imprecision to grind agent building
to a halt, we proceed in the same way as live clinicians do: by developing a
model that is reasonable and useful, with no claims that it is the only model
pos si ble or that it precisely replicates h uman functioning.8
Certain kinds of diseases can be con ve niently divided into conceptual
stages, with disease progression being represented as changes to part ic-
u lar physiological properties and patient symptoms over time. T able 8.8
illustrates this using a model of the disease achalasia.9 Achalasia makes a
person’s lower esophageal sphincter (LES) hypertensive and reduces the
efficacy of esophageal peristalsis, which results in difficulty swallowing and
vari ous other symptoms.
The top portion of the table shows how physiological property values
change over time (the stages labeled t0–t 4) if the disease is left untreated,
and the lower portion shows patient symptoms given a par tic u lar physi-
ological state. In this model, some features have diff er ent values across
patients (default values are shown in square brackets, and legal ranges are
shown when they are constrained), whereas other features play out the
same across patients. The latter does not imply that all h uman patients
are the same with res pect to t hese features. Instead, it reflects the fact that
this is a model—by necessity, a simplification—t hat aims to serve part ic u lar

8.8
elbaT
.detaertnu
tfel
si
esaesid
eht
fi
smotpmys
tneitap
detaicossa
dna
seulav
erutaef
lacigoloisyhp
ni
segnahc
swohs
taht
aisalahca
fo
ledom
eht
fo
noitrop
ehT
4t
3t
2t
1t
0t
tratS
]21[
]21[
]21[
]21[
]21[
)shtnom
ni(
noitarud
egatS
seitreporP
lacigoloisyhP
001/01
001/02
001/04
001/06
001/08
001/001
eht
ni
snoruen
gnitcartnoc
ot
gnixaler
fo
oitaR
sugahpose
latsid
04+
]eulav
-trats[
23+
]eulav
-trats[
42+
]eulav
-trats[
61
+
]eulav
-trats[
8
+
]eulav
-trats[
]52[
04–0
)rrot(
erusserp
SEL
lasaB
04
23
42
61
8
0
)rrot(
erusserp
SEL laudiseR
0
0
5.
0.1
5.1
2
)mc(
retem
aid
SEL laudiseR
01
02
03
04
56
08
sislatsirep
gnirud
noitcartnoc
fo edutilpmA
sislatsirepa
sislatsirepa
tnettimretni
lamron
lamron
lamron
sislatsirep
fo ycaciffE
sislatsirep
6
5
2.4
6.3
8.2
2
)mc(
sugahpose
latsid
fo retem
aiD
1
1–7.
7.–4.
4.–2.
2.–0
0
)}1,0{
elacs
eht
no(
tnetnoc
laegahpose
deniateR
]58.[
]55.[
]3.[
]1.[
01000,53
03
01
5
1
0
)setunim(
yaled
gniytpmE smotpmyS
4–3
3–2
2–1
1–5.
1.
0
)}4,1{
elacs
eht
no(
latsid
gniwollaws
ytluciffiD
]4[
]3[
]2[
]1[
sey
sey
sey
sey
on
on
?gniwollaws
elihw
kcits
sdilos
oD
sey
sey
sey
on
on
on
?kcits
sdiuqil
oD
2.–50.
51.–0
1.–0
50.–0
0
0
)}1,0{
elacs
eht
no(
ssol thgieW
]2.[
]1.[
]0[
]0[
1–5.
8.–3.
5.–0
3.–0
0
0
)}1,0{
elacs
eht
no(
niap
tsehC
]7.[
]5.[
]3.[
]1.[
001–02
05–02
02–0
4–0
0
0
)htnom
rep
semit(
noitatigrugeR
]07[
]04[
]01[
]0[

254 Chapter 8
pedagogical purposes defined by the physician- educators who collaborated
on building the system. They did not believe that adding additional vari-
ability to the model would improve the educational experience.
Whereas t able 8.8 reflects how achalasia unfolds if t here are no interven-
tions, clinical medicine is all about interventions. Interventions are also mod-
eled using t ables, but ones with a diff er ent semantics. T able 8.9 shows how
BoTox injected into the LES works as an intervention for achalasia. BoTox is
not a cure for the disease, but it can reduce symptoms for up to a year.
Intervention tables cover both the case when the treatment is given to a
previously untreated patient and to a patient whose LES pressure has been
changed by other interventions. This highlights the fact that MVP simula-
tions are open- ended, not fixed paths in the style of decision trees.
Table 8.10 shows an example of how treatment plays out in a simulation
run of a par tic u lar virtual patient, Gladys. Gladys is given BoTox when her
LES pressure is 52. The BoTox injection brings her LES pressure down to 32
which, as the basic disease table 8.8 shows, is a normal pressure that does
not evoke symptoms. However, the effect of BoTox will wear off over six
months, returning Gladys to her original LES pressure of 52.
Table 8.9
The model of how BoTox works as an intervention for achalasia, which allows for
great variability across patients.
If a patient is given BoTox when his 33–40 41–48 49–56 57–64 65+
or her basal LES pressure is
Then his or her basal LES pressure 4–24 12–30 18–36 24–42 30–48
will initially go down to [15] [21] [27] [33] [39]
And the effect will wear off over # 6–18 6–18 6–18 6–18 6–18
months [12] [12] [12] [12] [12]
Table 8.10
An example of how a part ic u lar virtual patient, Gladys, will respond to BoTox if it
is injected when her LES pressure is 52.
If a patient is given BoTox when his or 33–40 41–48 52 57–64 65+
her basal LES pressure is
Then his or her basal LES pressure will 4–24 12–30 32 24–42 30–48
initially go down to [15] [21] [33] [39]
And the effect w ill wear off over # 6–18 6–18 6 6–18 6–18
months [12] [12] [12] [12]

Explaining 255
Since all values in the treatment table are variables, and since the vari-
ability covers large scales, virtual patients can play out very differently with
re spect to their response to BoTox if a user should decide to use it as a treat-
ment in a simulation run. Other available treatments for this disease—t he
surgical procedure called Heller myotomy and the endoscopic procedure
called pneumatic dilation— are modeled using similar tables.
The main point of this discussion is not what, exactly, all of this means
medically. The import ant thing is that this relatively simple model: (a) is
fully transparent and, therefore, explainable; (b) is easily extensible and
modifiable—t hat is, it can be augmented to reflect new findings in medi-
cine or dif fer ent opinions of dif fer ent domain experts; and (c) is able to
generate great variability across the population of virtual patients, thus ful-
filling the pedagogical goals for which it was developed.
Visualizing system operation using under-t he- hood panes Another exam-
ple of visualization- based explanation in the MVP system involves display-
ing dynamic traces of system operation in what we call under-t he- hood
panes. The inventory of panes includes the following:
Physiology: A list of disease-r elevant property value pairs, with
values being highlighted e very time they change dur-
ing the simulation. This reflects an omniscient view
of the patient’s physiology.
Interoception: A list of the virtual patient’s perceived symptoms as
property- value pairs. Every time a symptom appears
or changes, a new entry is posted.
Thoughts: Dynamically populated traces of the patient’s deci-
sion functions, rendered in plain E nglish for read-
ability; for example, “I don’t know the risks of EGD.
I’d better ask about them.”
Knowledge Learned: T races of words, ontological concepts, and property
values of concepts learned through dialog.
TMRs: Text meaning repre sen ta tions of the virtual patient’s
interpretations of the user’s inputs during the simu-
lated doctor- patient interactions.
In the proof- of- concept MVP system, these panes were presented as side-
by- side columns in the lower portion of the computer screen during simu-
lation runs. Screenshots from two relatively self- explanatory panes during
a par tic u lar simulation run are shown in figure 8.1.11

256 Chapter 8
Thoughts Knowledge Learned
I am feeling bad but not EGD-n1
enough to go to a doctor syn-struc (root $var0)
yet. sem-struc EGD
I am feeling worse. EGD
I’d better make an IS-A MEDICAL-PROCEDURE
appointment to see the
doctor.
EGD
IS-A DIAGNOSTIC-PROCEDURE
I never blindly follow
doctors’ suggestions.
EGD
I need to think a little
PAIN 0
before I do the EGD.
EGD
I don’t know the risks of RISK 0
EGD. I’d better ask about
them.
I don’t know the side
effects of EGD. I’d better
ask about them.
Figure 8.1
Two of the under- the- hood panes of the MVP system during a simulation run.
The Thoughts pane shows traces of the patient’s decision-m aking that
were generated at diff ere nt points in the simulation. First it had to decide
about going to see the doctor, then about w hether to agree to the interven-
tion called EGD. Its decision- making is influenced by its lack of knowledge
about the procedure as well as its character traits, which include not blindly
trusting doctors and wanting to know specific t hings about procedures
before agreeing to them. The Knowledge Learned pane shows traces of what
the agent learns about EGD at sequential steps of the interaction. First it
recognizes that EGD is a noun that must be added to its lexicon and maps
it to a new concept called EGD, which it assumes must be some kind of
MEDICAL- PROCEDURE. Then, after asking the doctor (the system user) for more
information about the procedure, it learns that it is actually a DIAGNOSTIC-
PROCEDURE that is not painful and carries no risk.

Explaining 257
The under-t he- hood panes of MVP not only show exactly what is hap-
pening during the simulation; they also show that the simulation system,
although a prototype, is real: its components are modeled in such a way as
to be extensible into a deployable system.
Visualizing tutoring content The third kind of explanatory visualization
in MVP involves tutoring. The system offers vario us options regarding when
to provide tutoring messages and what to display in them. Tutoring mes-
sages can be provided only when the user is about to make a m istake, every
time the user makes a major move (o rders a test or procedure, hypothesizes
a disease, or diagnoses a disease), or not at all. As concerns what to show,
the messages range from a minimal right/wrong indicator to full informa-
tion about the preconditions of good practice related to the move, includ-
ing which preconditions are currently fulfilled with re spect to the given
patient. This latter strategy aims to teach by repetition, reinforcing the full
cluster of related knowledge each time a move is made. Figure 8.2 shows an
example of a tutoring message that appeared in a pop-up wind ow when a
user ordered the test called EDG during a simulation run. In the system, the
messages w ere color- coded using green to indicate fulfilled preconditions
Preconditions for EGD
ONE OF:
Suspicion of a mechanical obstruction
Suspicion of GERD
Suspicion of Barrett’s esophagus
Suspicion of achalasia (to rule out pseudoachalasia)
ONE OF:
Dysphagia
10% weight loss
Figure 8.2
An example of a tutoring message. Boldface shows preconditions that have been
satisfied. The preconditions are conceptually grouped into suspicions about diseases
and disorders (the first four) and individual symptoms (the last two). Dysphagia is
enough to warrant ordering an EGD.

258 Chapter 8
and red to indicate unfulfilled ones. H ere we use boldface for the green ones
and plain Latin for the red ones.
To wrap up this discussion of explanation in MVP, a variety of visualiza-
tion techniques are used to explain both the medical model and system
functioning. The goals of these visualizations are to ensure that the sys-
tem is functioning correctly, to gain the trust of medical educators, and
to explain to users and the outside world both the model itself and how it
plays out in simulation.
8.8 Explanation as Part of Overall Agent Operation
Although this chapter has focused on explanation, it has not been exclu-
sively about explanation. It has been about how explanation plays into the
overall operation of LEIAs. The kinds of explanations LEIAs will be called
on to provide depend on what role they are playing in a given application.
The content of the explanations depends on the LEIAs’ static knowledge,
their situational knowledge, and the algorithms driving their operation.
How they determine what needs to be explained and how to generate an
explanation derives from their microtheory of explanation itself.
An impor tant aspect of this microtheory is the acknowledgement that
agents need to be prepared to recognize and reason about dif fer ent kinds of
requests for information. T here is not, nor can t here be, a single question-
answering capability since questions like What do you think I said? and Why
is it too early to posit this diagnosis? require completely dif fer ent reasoning.
One question that might come to mind is, C ouldn’t the agent look directly
at its codebase to explain what it is doing? To some degree, yes. Decision func-
tions use ontological property values, and so, at a minimum, the agent
can extract t hose and report that they affected the decision. However, two
impor tant points must be kept in mind. First, end users do not need code-
level explanations and developers can track down system pro cessing in
more efficient ways, such as by using the DEKADE environment or looking
at the code itself. Second, in the big picture of developing reasoning algo-
rithms for cognitive systems, the additional work of decorating them with
select kinds of explanation- oriented metadata is so minimal as to hardly be
worth mentioning. So, creating a generic code-e xplanation functionality is
currently not on agenda.
