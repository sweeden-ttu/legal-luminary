9 Knowledge Acquisition
As should already be clear, for LEIAs to operate with understanding across
many domains, they need knowledge—a nd a lot of it. By knowledge, we
mean data that has been translated into the unambiguous, ontologically
grounded metalanguage of the LEIA’s knowledge bases. Previous chapters
have shown how agents can acquire knowledge through learning. This
chapter describes manual and semiautomatic methods of knowledge acqui-
sition within the DEKADE infrastructure. T hese methods facilitate the
acquisition of the bootstrapping knowledge that is needed to enable LEIAs
to learn automatically with good results. The focus is on efficient method-
ologies that take the complexity of language and the world seriously.
Before we begin, a common misconception must be addressed. The need
for manual work on knowledge in AI is not unique to knowledge- based
systems. Data- driven systems also rely heavi ly on manual labor in the form
of annotating and cleaning training datasets, tweaking parameters, and
even recording application- specific responses, such as answers to typical
questions. According to The Economist, as of January 2020, data preparation
still claimed over three quarters of the time allocated to machine learning
proj ects.1 And according to Stasha (2021), Alexa Smart Assistant and Echo
products perform so well because thousands of employees are working on
optimizing these specific products. Similarly impressive h uman workforce
outlays were needed to prepare IBM’s Watson to play Jeopardy! However,
despite Watson’s spectacular win, it could not h andle the ambitious fol-
low-up applications it was set to (Lohr, 2021). In short, if one chooses to
think of knowledge as a prob lem, then data- driven approaches to AI share
the prob lem. However, since LEIAs are on a diff er ent path t oward artificial
intelligence than the data-d riven majority, it stands to reason that the focus
of manual labor is dif fer ent as well.

260 Chapter 9
This chapter, like the book overall, focuses on work that is e ither imple-
mented in a computer program or well- specified by algorithms. This
material does not exhaust all needs of LEIAs. As discussed in section 7.3,
collaboration with colleagues working on modeling a variety of percep-
tion and action modalities is needed to enhance the knowledge substrate
of LEIAs with multimodal, ontologically grounded descriptions that will
enable agents to interpret sensory inputs in a way analogous to their cur-
rent interpretation of language inputs. This knowledge will include such
things as static images, video clips, and links to programs that operational-
ize concept detection. The LEIA knowledge infrastructure is prepared to
receive such knowledge, since it is similar in kind to the procedural knowl-
edge that supports language understanding and reasoning.
9.1 Introduction
The need for extensive high- quality knowledge and the perceived impracti-
cality of amassing it—w hich has been referred to by some as the knowledge
bottleneck— contributed to the demise of so- called good old- fashioned AI in
the 1990s. It also fueled the paradigmatic turn t oward data-d riven methods,
which were already gaining momentum at that time due to the spectacular
technological advances in data availability, pro cessing speed, and storage
capacity. However, failing to address the knowledge probl em in the spirit
of cognitive modeling—by building ontologies, lexicons, explainable rule
bases, and so on— has left a big hole in the AI landscape. Data- driven AI
has, by necessity, avoided applications that require anything beyond ana-
logical reasoning.
Whereas data- driven AI operates over uninterpreted big data, developers
of cognitive systems typically assume that high-q uality interpreted knowl-
edge is available to support agent reasoning, and that cognitive agents w ill
somehow translate perceived data into interpreted knowledge. However,
as discussed in Section 2.8.3, few cognitive systems developers are work-
ing toward actually fulfilling these requirements, concentrating instead on
general theories, specific engineering issues, or small- domain applications.
The prob lem with focusing on small- domain applications is that they
obscure the need to account for many kinds of phenomena that are essen-
tial for scaling up. Take as an example polysemy— the fact that most words
have multiple meanings, only one of which fits any given context. A

Knowledge Acquisition 261
typical cognitive system will include only one of the word’s meanings in
the agent’s lexicon, as if the ambiguity probl em didn’t exist. Such simpli-
fications mean that each time a system’s coverage is extended beyond the
original example set, the original solutions need to be thrown away. After
all, a system that knows nothing about polysemy cannot spontaneously
carry out disambiguation if placed in a context where words suddenly have
more than one meaning. Forcing people to use controlled languages is also
not viable, though the field has amply explored this option.2 It is more
efficient—in fact, imperative—to address real-w orld challenges more holis-
tically from the outset, using the kinds of explanatory, evolving microtheo-
ries described in e arlier chapters.
Much has changed since the early days of AI, when manual acquisition
of knowledge was tried and found to be slow and cumbersome. In those
days, every thing about computing was slow and cumbersome. Now it’s a com-
pletely dif fere nt world with res pect to pro cessing speed, storage space, user
interfaces, tools for building interfaces, and the availability of large corpora
and online knowledge bases. Moreover, the newly available large language
models can be used to configure vario us kinds of support tools. All of this fun-
damentally changes the prospects of manual and semiautomatic knowledge
acquisition, which is a necessary complement to the ideal, but not immi-
nent, state of affairs in which agents can learn every thing automatically.
On the human front, it is becoming ever clearer what and how much
to expect of knowledge workers. Typically, knowledge workers are not pro-
ductive for the entire duration of a standard eight-h our workday; they are
productive for only about three to six hours a day, depending on the task
(Hakes, 2021). In addition, they cannot concentrate when they are bored.
A stark example of the consequences of boredom-i nduced inattention is
the fatal accident caused by an Uber autonomous vehicle, whose h uman
operator was supposed to be vigilant enough to prevent accidents despite
having nothing to do almost all the time (Smiley, 2022). Our own, more
mundane experience in developing knowledge- based systems has shown
that it is difficult to motivate workers to carry out knowledge acquisition
unless it is divided up into small, precisely defined tasks punctuated by
frequent, satisfying milestones.
It is also impor tant to have an efficient, pleasant knowledge- engineering
environment. All knowledge bases need to be easily accessible, viewable,
and editable, e ither as a freestanding task or in conjunction with assessing

262 Chapter 9
agent operation. In fact, folding knowledge acquisition into a workflow
that involves LEIA proc essing is exactly the kind of goal-o riented method-
ology that can keep knowledge workers engaged (see section 9.4).
This chapter discusses knowledge acquisition from three perspectives:
the ontology, the lexicon, and a workflow that interleaves knowledge
acquisition with agent functioning. These dovetail with the agent’s learn-
ing through dialog and reading, which w ere described in previous chapters.
9.2 Acquiring Ontology
Ontology development involves cognitive modeling, since a LEIA’s ontol-
ogy must capture how people understand and reason about the world. No
LEIAs are expected to be omniscient. Most of them w ill need highly special-
ized knowledge only about a part ic u lar domain, or none at all. But they
all need general knowledge. For example, all dialog agents have to know
the inventory of speech acts (asking a question, issuing a command, pro-
posing a plan, and so on), and they need to know the dozens of ways of
expressing each one in language. So, knowledge of this type is a high prior-
ity with a high return across applications. By contrast, many utterances and
situations cannot be fully understood without domain- specific knowledge.
For example, the sentence “Golfers have always walked in competitive
tournaments” implies that they d on’t ride in golf carts—s omething
(COCA)
that might not be obvious to all readers, even t hose living in societ ies where
golf is played. Specific knowledge like this is recorded in scripts.
Scripts can reflect knowledge in any domain—w hat happens at a doc-
tor’s appointment, how to make pizza, how to prune an apple tree; and
they can be at any level of granularity—f rom a basic sequence of events
to the level of detail needed to generate interactive computer simulations.
For general domains, knowledge engineers can double as domain experts,
whereas for specialized domains, they must consult outside experts. In both
cases, text sources can be useful for reference.
Ontological scripts can require expressive means beyond the simple
property- facet- value descriptions of basic ontological frames. Taking exam-
ples from the domain of doctors’ appointments, scripts require:
• The coreferencing of arguments. In a given appointment, the same
instance of DOCTOR will carry out many actions, such as asking questions,

Knowledge Acquisition 263
answering questions, and recommending interventions; and the same
instance of PATIENT w ill carry out many actions, such as answering ques-
tions, asking questions, and deciding about interventions.
• Loops. There can be many instances of event sequences, such as ask/
answer a question and propose/discuss an intervention.
• Variations in ordering. A doctor can get vital signs before or after the
patient interview and can provide lifestyle recommendations before or
after discussing medical interventions.
• Optional components. A doctor may or may not engage in small talk
and may or may not recommend tests or interventions.
• Time management. For simulation- oriented scripts, the script must
include information about what happens when, how fast, and for how
long.
Whereas it should be poss i ble for agents to automatically learn some
aspects of some kinds of scripts from texts, full automation is unlikely to
ever be the full answer to the prob lem. There are several reasons why.
1. Books and other texts intended for people do not describe how everyday
life works, they provide happenstance snippets. And people do not learn
how everyday life works from books, they live.
2. As concerns more specialized knowledge, aspects of scripts are recorded
in technical manuals and textbooks, but the quality, depth, and com-
prehensiveness of the descriptions varies dramatically. To see an exam-
ple, pull out the manual for your car or some appliance and look at the
troubleshooting instructions. Do they make perfect sense—or any sense
at all? It is difficult to formulate procedural knowledge because it needs
to address the needs of readers with diff ere nt amounts of background
knowledge. Moreover, manuals intended to be used by p eople do not
include the kinds of details that agent systems need in order to learn
to operate optimally, such as all of the impor tant subevents of scripts,
constraints on their players and props, indications of required versus
optional components and steps, reasons why things should be done in a
par tic u lar order, allowable variations in the ordering of subevents, event
preconditions and effects, and so on.
3. Scripts need to cover not only what people do but also how they think
about t hings. This includes their abstract understanding of how life

264 Chapter 9
works, how to make decisions in complex contexts, how to teach the
next generation their hard-w on knowledge, and so on. Although experts
clearly operate with such models, they are implicit and must be made
explicit through the process of knowledge engineering.3
To sum up, texts practically never contain anywhere near the complete
script- based information that agents need to operate intelligently, even if
agents could analyze all of the world’s texts automatically and with perfect
precision. So, manually acquiring ontology, with as much automatic sup-
port as is practicable, is a necessity.
Figure 9.1 shows some workflow options for ontology acquisition, which
we will describe in turn. Lexicon acquisition typically piggybacks on ontol-
ogy acquisition so that the agent can talk about the new concepts it has
learned.
Knowledge engineers model general domains For knowledge in the gen-
eral domain, knowledge engineers can double as subject matter experts.
Vari ous methodologies can be followed, but in all cases the knowledge
engineer must have a specific, application-o riented goal in mind. Without
such a goal,
1. it would be impossible to decide what to work on: negotiation strategies,
how to play baseball, or the food preferences of the world’s animals;
2. it would be impossible to know the necessary and sufficient amount of
detail; and
General
Data-driven system Knowledge engineer
extracts & clusters texts enhances ontology
domain
in selected domain and lexicon
Lexicon
Subject matter expert Knowledge engineer &
Specialist uses OntoElicit to subject matter expert
domain compile candidate collaborate to enhance
knowledge ontology and lexicon
Ontology
Knowledge engineer
Any domain : Data-driven system (with subject matter
property extracts property values expert) vets candidate
values from corpus property-value
enhancements
Figure 9.1
Sample knowledge- acquisition strategies that focus on ontology. Boldface indicates
automatic systems, and dotted lines indicate that the modules are optional.

Knowledge Acquisition 265
3. it would be impossible to validate whether the information was actually
useful— that is, whether it was of the type and grain- size needed to sup-
port automatic reasoning.
Once they have identified an ontology-a cquisition objective, knowledge
engineers can consult a variety of knowledge sources, compiled either man-
ually or with the help of a data- driven system that extracts and organizes
texts about the given topic.
Adding new ontological concepts can necessitate adding new lexicon
entries or modifying existing ones. For example, at a given time the ontol-
ogy might contain only the generic concept for DOG, with the words referring
to dif fer ent breeds of dogs being listed as hyponyms of dog- n1. If an acquirer
decides to expand DOG into a subtree of breeds in order to describe each one
more precisely, then the words for each breed need to be removed from the
hyponyms field of dog- n1 and be promoted to their own lexical senses: poo-
dle- n1 mapping to POODLE, dachshund- n1 mapping to DACHSHUND, and so on.
Knowledge engineers collaborate with subject m atter experts To model
specialist domains, knowledge engineers need to collaborate with subject
matter experts. Consider again the domain of clinical medicine (see sec-
tion 8.8). The se lection of properties to be included in a disease model is
guided by practical considerations. Properties are included if they can
be measured by tests, if they can be affected by medi cations or treat-
ments, and/or if they are necessary components of a physician’s mental
model of the disease. In addition to using directly measurable properties,
models also include abstract properties. For example, when the property
PRECLINICAL- IRRITATION-P ERCENTAGE is used in scripts describing esophageal
diseases, it captures how irritated a person’s esophagus is before the per-
son starts to experience symptoms. Preclinical disease states are not subject
to measurement by tests b ecause people do not go to the doctor before
they have symptoms. However, physicians know that each disease process
has a preclinical stage, which must be accounted for in an end-t o-e nd,
simulation-o riented model. Coming up with useful, appropriate abstract
properties reflects one of the creative aspects of computational modeling.
The abstract features used for cognitive modeling are similar to the inter-
mediate (non-l eaf) categories in ontologies. Although regular people might
not think of WHEELED- LAND- VEHICLE as a category, this can still be a useful
node in an ontology.

266 Chapter 9
Once an approach to modeling a disease has been devised and all requi-
site details have been elicited from experts, the disease- related events and
their participants are encoded in ontologically grounded scripts written in
the metalanguage of the LEIA’s ontology.
Because knowledge engineering is expensive, it is well worth developing
tools and automated support for the p rocess. We developed the prototype
for a tool called OntoElicit, which helps subject m atter experts to reco rd
key building blocks of models before interacting with knowledge engineers.
This tool encapsulates a theory and methodology of knowledge elicitation
developed during two quite dif fer ent proje cts: the Maryland Virtual Patient
system and the Boas system for eliciting knowledge about low-d ensity lan-
guages in s ervice of machine translation (McShane et al., 2002). We use
examples from the former in this thumbnail overview.
In OntoElicit, subject matter experts are led through a sequence of inter-
actions with the system in order to complete the following tasks:
• Divide each disease into any number of conceptual stages correlating
with impor tant events, findings, symptoms, or the divergence of disease
paths across patients.
• Indicate the typical duration of each stage as a range with a default
value.
• List the relevant physiological and symptom- related properties, along
with their typical value ranges and default values during each stage.
• List the tests that might be performed and the clinical guidelines for
ordering them.
• For each test, if it is carried out at each conceptual stage, list the expected
raw results and specialists’ interpretations, with the latter including per-
tinent negatives, diagnoses, “suggestive of [disease]” statements, and so
on.
• List interventions that might be performed, the clinical guidelines for
ordering them, how property values are affected by the intervention if
it is carried out at each conceptual stage, the pos si ble outcomes of the
intervention, poss i ble side effects, and, if known, the percentage of the
population expected to have each outcome and side effect.
The result of working with OntoElicit is the skeleton of what will become a
disease model like the model of achalasia shown in tables 8.8 and 8.9.

Knowledge Acquisition 267
Some kinds of agent capabilities are easier to model than o thers. For
example, it is straightforward to prepare a tutoring agent to check if the
preconditions for a move have been met, but it is more difficult to model
how to select among multiple moves, all of whose preconditions have been
met. In the case of clinical medicine, models of decision- making must
incorporate the possibly diverging preferences of a variety of stakeholders
(e.g., the patient, the physician, the insurance com pany), differing cost-
benefit analyses for dif fer ent options, and the potential need for decision-
making under uncertainty since it is not unusual for some key information
to be unavailable at the time a decision must be made. In order to manage
this complexity, we have experimented with the use of Bayesian networks.
The idea was to establish priors by asking subject m atter experts to assess,
for dif fer ent combinations of property values, the “goodness” of dif fer ent
available decisions. Our experience suggests that this method of knowledge
acquisition and associated reasoning merits further exploration.
Knowledge engineers use a data- driven system to suggest property values
An insufficiency in the LEIA’s current ontology is that some property values
that should be locally specified for a concept are not; instead, an overly
generic value is inherited from the parent. For example, the weight range
for adult dogs (DOG) is 2–200 pounds, but the weight ranges of chihuahuas
(CHIHUAHUA) and mastiffs (MASTIFF), which are children of DOG, are much
narrower. Knowledge engineers can improve concept descriptions with the
help of vari ous types of automation. For example, they can use the LEIA’s
automatic property-l earning mechanism, described in sections 7.1.3 and
7.2.2, to suggest property values, or they can use large language models
(LLMs) by feeding them appropriate prompts. The main difference between
the methods is that the LEIA’s automatic property-l earning mechanism
includes a trace back to the source material, whereas LLM-b ased responses
do not; and, in fact, the latter cannot be fully trusted. This means that LLMs
are best used in cases where the acquirer has a notion of the right answer
and is asking the LLM for a reminder.
9.3 Acquiring Lexicon
Another way to approach knowledge acquisition is by focusing on the lexi-
con and then supplementing the ontology as needed. There are many pos-
sib le workflows, including t hose shown in figure 9.2.

268 Chapter 9
Data-driven
system
identifies Knowledge
Data-driven LEIA analyzes
learnables system extracts the examples; engineer vets, Lexicon
edits, creates
& clusters creates
lexical senses;
Knowledge examples with candidate lexical might add/modify Ontology
engineer the word senses concepts
identifies
a nest of
near-synonyms
Figure 9.2
Sample knowledge- acquisition strategies that focus on lexicon. Boldface indicates
automatic systems, and dotted lines indicate that the modules are optional.
The first question is how to identify which words and expressions to
learn. This can be done either using a data- driven tool or by knowledge
engineers working with linguistic resources such as thesauri and WordNet.
Using data-d riven tools to identify learnable words and expressions The
princi ples of the data-d riven approach to learning w ere explained in sec-
tion 7.1.3. Here we focus on matters of content.
In language, frequency of occurrence m atters— a truism being explored
in theoretical, computational, and corpus- based linguistics. For example,
in the theoretical paradigm called the usage- based model, “language is seen
as a probabilistic system of emergent structures and fluid constraints that
are grounded in the language user’s experience with concrete words and
utterances” (Diessel, 2016). In other words, in h uman language proc essing,
there is no stark boundary between abstract syntactic constructions and the
words that can populate them. Instead, linguistic constructions are most
appropriately defined at multiple levels of abstraction, including using par-
tic u lar words in par tic u lar syntactic structures.
For agent modeling, the following aspects of linguistic frequency are par-
ticularly impor tant.
1. Agents need to become competent language users in the general domain
as quickly as pos si ble so that they can turn to automatically learning
about specialized domains. For this, they first need to accumulate a large
store of frequent expressions paired with their meanings. For example,
people often make a request by saying, I’d appreciate it if you’d VP, so
agents need to recognize this as an expression and know that it maps to

Knowledge Acquisition 269
the concept REQUEST- ACTION. The corpus-a ttested frequency of such multi-
word expressions can help to prioritize knowledge acquisition.
2. It is both useful and theoretically motivated to rec ord the meanings of at
least some very frequent multiword expressions even if they are semanti-
cally compositional. For example, I’m hungry occurs 1,794 times in the
COCA corpus. Enabling agents to directly access language-t o- meaning
couplings for multiword expressions results in high-c onfidence analy-
ses, enhances proc essing efficiency, and models our understanding of
human memory and information access.
3. Identifying high- frequency constructions that include par ticu l ar words
can inform the learning of more abstract constructions. For instance, if
a part icu lar complete sentence occurs multiple times in a corpus, it is
a candidate for being listed in the lexicon. If the LEIA uses the COCA
corpus as a search space, it w ill find that the following full sentences,
among many others, are attested multiple times:
Dinner is served.
Breakfast is served.
Lunch is served.
Tea is served.
Justice is served.
Having extracted the full set of frequent sentences in a corpus, the agent
can then cluster them and determine whether minimal pairs differ in
an ontologically significant way. In the examples above, four of the five
sentences involve a MEAL (tea can refer to a small after noon meal), so the
agent can hypothesize that Subj is served is a construction.4 However,
MEAL
the agent has no way of knowing that this construction does not simply
assert that a meal has been served. Instead, it is an invitation to come
and eat, so its semantic description should be headed by INVITE. This is a
good example of why p eople need to remain in the loop of knowledge
acquisition.
4. It would be ill- advised to indiscriminately rec ord fully compositional
multiword expressions that are only moderately frequent, such as (some-
one) had a burger. Not only would this likely not align with p eople’s lexi-
cal knowledge, it would also make the lexicon unnecessarily large—in a
similar way as explici tly listing the passive voice of all verbal senses (cf.
section 4.2.2).

270 Chapter 9
5. In order for automatic pro cessing to actually help, rather than hinder,
knowledge engineering, knowledge engineers and system engineers need
to work together to identify useful search strategies. Continuing with the
case of multiword expressions, some rule- out conditions are clear. For
example, pronoun- rich collocations like He did it cannot be associated
with a static semantic interpretation, so there is no benefit to recording
it as a multiword expression.
6. Further investigation is needed to determine in which ways frequently
met- with sequences of words can vary while still having high potential
for being multiword expressions whose meaning is worth recording.
For example, can the words vary in morphological features? Can they
be freely modified? Can they occur within larger sentences? Can any
of the slots in the candidate expression be filled by a variable? If the
search criteria are too strict, they will miss useful candidate expres-
sions; if they are too loose, they will overwhelm the human who must
evaluate the hypotheses.
7. T here are expressions, both single- word and multi- word, that are
extremely common and have a privileged status in a given type of con-
text. For example, when customers in a restaurant or coffee shop say
“Large latte,” they are placing an order. Similarly, when surgeons in an
operating room say “Scalpel,” they are asking to be handed a scalpel. It
would be useful for an automatic system to identify frequent utterances
like these to remind knowledge engineers that they must be covered.
Once such utterances are identified, t here are several options for prepar-
ing LEIAs to correctly interpret them. On the one hand, a lexical sense
can be added that asserts the given form-t o- meaning correlation, but
it must be appended with a meaning procedure that ensures that the
context is appropriate. On the other hand, the ontological script for the
given domain, such as SURGERY, can include the knowledge that when a
surgeon, during a surgical procedure, names a tool, it is a request to be
given that tool.
Frequency-d riven knowledge acquisition is wide open territory for
exploring how data- driven methods with vario us kinds of h uman guid-
ance can speed up the acquisition of language expressions that will help
LEIAs achieve basic language competency that is useful across domains and
applications.

Knowledge Acquisition 271
Knowledge engineers identify learnable words and expressions Human-
oriented linguistic resources— grammars, thesauri, classifications— can be
useful for jogging knowledge engineers’ memories and helping them to
organize acquisition efficiently. For example, Levin (1993) pre sents a clas-
sification of E nglish verbs according to their syntactic beh av ior, driven by
the hypothesis that verbs that are similar in syntactic be hav ior have seman-
tic affinity. For example, Levin’s grow verbs— which include grow, develop,
evolve, hatch, and mature— are similar in that they permit an alternation
between into and from (9.1) as well as a causative alternation (9.2).
(9.1) a. That acorn will grow into an oak tree.
b. A n oak tree will grow from that acorn. ( Levin, 1993, p. 174, #395)
(9.2) a. The gardener grew that acorn into an oak tree.
b. The gardener grew an oak tree from that acorn. ( Levin, 1993, p. 174, #397)
Levin’s verb classification can help to speed up the acquisition of verbs that
have similar syntactic beh av ior and, often, map to the same or relatively
proximate concepts.
Another example of a useful classification involves paraphrases, for
which vari ous classifications have been proposed.5 LEIAs handle many
classes of paraphrase as a m atter of course: lexical synonyms, diff er ent
forms of referring expressions, full and elliptical utterances, active and pas-
sive alternations, and so on. But additional phenomena must also be cov-
ered by a LEIA’s knowledge bases and reasoners.
• Paraphrases can show alternations between events and social roles:
Stuart teaches our kids chemistry versus Stuart is our kids’ chemistry
teacher.
• They can express an event or its converse: Stuart called up Beth versus Beth
got a call from Stuart.
• They can express something directly or as a double negation: Stuart
wants to go versus Stuart doesn’t not want to go.
• They can use direct quotes or narrative: Stuart said, sure he’d come versus
Stuart said, “Sure, I’ll come.”
• They can use light verb constructions or semantically specific verbs: Stu-
art did the dishes versus Stuart washed the dishes.
• They can use metonymy or a direct reference: The red hat just smiled at
Stuart versus The girl with the red hat just smiled at Stuart.

272 Chapter 9
LEIAs handle some of t hese using lexical constructions (e.g., X called Y and
Y got a call from X), and others using reasoning pro cesses (e.g., metonymy
resolution). But knowledge engineers have to remember that such phenom-
ena can occur— and that’s where classifications come in handy.
Another way to approach lexicon acquisition is for people to identify,
using a thesaurus or WordNet, nests of near-s ynonyms that are worth
acquiring and then acquire them either manually or with vari ous kinds
of automatic support.6 Table 9.1 shows some examples of near-s ynonyms
that should map to the listed concepts—n aturally, within fully specified
lexical senses that include all of the necessary syntactic and semantic
dependencies.
In looking at this list, one might think that compiling lists of near-
synonyms should be automatable. However, as explained in section 3.1, a
lot of entities listed in thesauri are not even near-s ynonyms. Consider some
examples:
• One thesaurus lists all of the following as synonyms of help but they are
better treated in other ways in the LEIA’s knowledge bases:
○ buck up and root for should map to ENCOURAGE;
○ stand by and stick up for should map to DEFEND; and
○ take under one’s wing and open doors are so specific that they need to be
described using multiple concepts linked by properties.
• The WordNet synset (synonym set) for scream includes the following:
○ useful synonyms: shout, shout out, yell, holler
○ detrimental synonyms because they have other main meanings or are
too rare in this meaning: cry, call, hollo, squall
○ useful direct troponyms: whoop, shriek, screech, howl
Table 9.1
Near- synonyms that map to a known concept.
HELP ALLOCATE WALK
do a favor divvy up hoof it
do a service dole out wend one’s way
lend a hand pass out go on foot
COMPLAIN ASSAULT HIDE (oneself)
kick up a fuss slap around go into hiding
make a fuss let have it go under ground
sound off work over lie low

Knowledge Acquisition 273
○ direct troponyms that could be added to the lexicon but w ill be of
little use because they are so rare; and, if added, they must be flagged
as rare so that they will not be used in generation: ululate, yawp, yaup
○ detrimental direct troponyms, which are too rare or too diff ere nt to
be acquired at all: screak, skread, skreigh, halloo, pipe up, pipe
So, if data- driven tools are used specifically to identify near-s ynonyms—
rather than, for example, to identify frequent words or multiword expres-
sions in a corpus— their results need to be inspected by a knowledge
engineer. At the time of writing, we are experimenting with using LLMs to
suggest synonym- based enhancements to the lexicon.
Pro cessing candidate additions to the lexicon Once words and expres-
sions have been selected for acquisition, the p rocess can unfold in vari-
ous ways (cf. figure 9.2). Optionally, a data-d riven system can be used to
extract and cluster examples containing the word or expression. This is use-
ful to jog acquirers’ memories about meanings and usages that are not the
first to come to mind. Next— also, optionally—t hose examples can be sent
through a LEIA’s language understanding and learning proc esses, resulting
in candidate senses for the new words and expressions. Fin ally, knowledge
engineers create—or review and edit automatically created—l exical senses,
which might involve adding or modifying ontological concepts as well.
Although it might seem like automation should always prove useful,
the fact is that machine- generated lists and clusters do not always speed
up humans’ work, as became clear in the early days of machine-a ssisted
translation. Fully manual approaches can actually be faster and/or less frus-
trating, depending on both the quality of the automatic results and the
preferences of individual workers.
For acquiring LEIA-s tyle lexical senses, we expect automation to be
useful mostly with re spect to syntax— for example, selecting a transitive
verb template based on corpus examples. Acquirers will still be responsible
for vetting the semantic mapping and adding additional property values
if needed, since ontological concepts are, by design, more coarse- grained
than the meanings of many of the words of any language. For example,
POLITENESS and FORMALITY are features that primarily apply to language, not
ontology; so, values for these features are recorded in lexicon entries for the
corresponding words and expressions. For example, I would really appreciate
it if you would VP is a REQUEST- ACTION with the feature values “FORMALITY .7”
and “POLITENESS 1.” As with any abstract scalar properties, assigning values

274 Chapter 9
to par tic u lar lexemes is aimed at supporting useful reasoning, with no claim
that the values reflect any precise or provable real ity. The goal is for LEIAs
to be as sophisticated as pos si ble while still being developed on a fast time
scale to offer near- term utility.
Some of the semantic features that distinguish near- synonyms involve
the core meaning, rather than the style, of the message. For example, rush
off can be described in any of the following ways:
– EXIT (URGENCY .8)
– EXIT (VELOCITY .8)
– EXIT (URGENCY .8) (VELOCITY .8)
The reason for the options is that this expression can imply physical speed,
urgency, or both. Additional examples of an appropriate grain-s ize of
description for the LEIA’s lexicon are as follows:
– do a favor: HELP (FORMALITY .4)
– do a service: HELP (FORMALITY .8)
– lend a hand: HELP (FORMALITY .2)
– kick up a fuss: COMPLAIN (FORMALITY .1)
– sound off: COMPLAIN (FORMALITY .4)
– slap around: ASSAULT (INSTRUMENT PALM-OF-HAND)
– let have it: ASSAULT (FORMALITY .2)
– work over: ASSAULT (FORMALITY .2)
These examples show just the skeleton of the semantic side of entries. Each
construction needs to be described using a full lexical sense of the type pre-
sented in e arlier chapters.
To wrap up this section on acquiring lexicon, it is worth noting that it
can be difficult even for people to describe certain kinds of abstract objects
and events in a way that is r eally useful for machine reasoning: privacy,
capitulation, endearment. Technically, it would be easy to have the agent cre-
ate a new lexical sense and associated concept for each such notion without
attempting to describe its distinguishing property values, but that would
be kicking the can down the road and would run c ounter to the princip les
of content-c entric computational cognitive modeling. We do not exclude
the possibility of automatically learning some abstract notions; however,
this will be most successful if they are related in some obvious way to a

Knowledge Acquisition 275
well- described existing concept. For example, if the ontology includes LOVE-
EVENT, and the lexicon maps the verb love to it, then the agent can learn the
meaning of the verb adore from the definition “to love intensely”: that is,
LOVE- EVENT (INTENSITY .9). However, expecting the agent to learn a concept
like LOVE or ADORE from scratch, simply from its usage in vario us contexts,
seems unrealistic. Thus, the impor tant role of human acquirers in compil-
ing bootstrapping- worthy knowledge bases.
9.4 Threading Knowledge Acquisition with System Operation
Knowledge acquisition can be threaded with system operation in vari ous
ways. We already saw in chapter 7 how LEIAs can learn lexicon and ontol-
ogy while operating in vari ous modes. And we saw in the previous subsec-
tions how p eople can acquire lexicon and ontology with vario us levels of
participation by LEIAs. In addition, people can acquire knowledge while
carryi ng out system testing and debugging. That is, they can run sentences
through the agent’s language understanding system, inspect the results
using the DEKADE environment, and then enhance the knowledge bases as
needed to result in a correct analy sis. This enhancement can invoke vari ous
levels of automatic pro cessing by the LEIA.
There are four reasons to thread knowledge acquisition with system
operation.
1. All acquired knowledge needs to actually serve proc essing, and r unning
sentences while acquiring resources is a good way of making sure that
it does. For example, a word like respectively cannot be described using
ontological concepts; it requires procedural semantic analys is provided
by a custom program. If an acquirer tried to add this word to the lexicon
without both specifying a meaning procedure and ensuring that it was
implemented properly, then the sense could not be used by the system.
Similarly, if acquirers fail to provide sufficient information in the lexicon
to permit dif fer ent senses of words to be disambiguated, then they are
setting the agent up to face residual ambiguity e very time it encounters
the given word.7
2. Knowledge engineering is mentally tough: it is open-e nded, it imposes
a heavy cognitive load, and it does not offer any inherent milestones
akin to a programmer’s opportunity to run a program and watch it work.

276 Chapter 9
Orienting acquisition around making a given input work correctly offers
frequent and concrete milestones.
3. LEIAs can automatically generate certain aspects of candidate knowl-
edge, which can speed up knowledge acquisition. For example, they can
posit templates for new lexical senses that match the syntactic use of the
word or phrase that is attested in the input.
4. When knowledge engineering is threaded with system operation, a side
effect is creating a repository of correctly analyzed texts, that is, pairs
of sentences and their correct TMRs. Such a repository, when viewed as
a component of the agent’s episodic memory, facilitates language pro-
cessing through reasoning by analogy. This can be implemented using
knowledge- based methods or machine learning. Using knowledge-b ased
methods, the agent can consult previous correct TMRs for guidance
about how to handle difficult analys is decisions in a new input. For
example, many expressions have both literal and meta phorical mean-
ings. If the agent’s stored TMRs overwhelmingly prefer one over the
other— given that both options are available in the given context— then
that is a vote for the choosing the more frequently attested meaning. To
give a concrete example, if most stored analyses of sentences of the form
X is gonna kill Y! refer to being angry at, not killing, someone, then the
angry interpretation will be the default hypothesis for future inputs of
this form. However, “of this form” can be tricky to automatically com-
pute. In this example, it is import ant that the verb be in the f uture tense
because the meta phorical meaning is rarely if ever used in the past tense.
The other option for implementing reasoning by analogy uses machine
learning, which requires creating a large enough repository of sentence-
to- TMR mappings to serve as training material.
Figure 9.3 illustrates a human- inclusive workflow that threads knowl-
edge acquisition with system testing and enhancement. This workflow
breaks the p rocess of knowledge acquisition into small chunks with a mile-
stone at the end of each one.
The knowledge engineer selects sentences to analyze and works on
them until the analys is is correct, resulting in what is called a golden or
gold- standard TMR that can be stored to episodic memory.8 The workflow
can involve lexical acquisition, ontology acquisition, and/or the improve-
ment of analy sis algorithms themselves (jointly with a software engineer).

Knowledge Acquisition 277
Data-driven system
extracts candidate
texts in a target
domain. LOOP
Lexicon
Knowledge engineer
Data-drive n system edits text or acquires
automatically word sense(s) Ontology
simplifies text.
NLU by LEIA
Knowledge engineer
identifies text worth Knowledge engineer
processing. Pastes Knowledge engineer sends golden TMRs Episodic
into DEKADE. reviews TMR to episodic memory. memory
LEIA highlights
unknown words.
Figure 9.3
A sample human-i nclusive knowledge-a cquisition strategy that incorporates lan-
guage pro cessing by LEIAs. Boldface indicates automatic systems, and dotted lines
indicate that the modules are optional.
Essential to this methodology is giving knowledge engineers full freedom to
decide what to work on, what to postpone, and which kinds of automation
to use. We will work through figure 9.3.
• Identify a text to work on either automatically or manually. A potential
benefit of automatic extraction is that similar texts can be clustered, offer-
ing better coverage of both content and linguistic expressions at one go.
• Simplify the text if needed, automatically and/or manually. As Steven
Pinker has pointed out, much of academic writing stinks (his term;
Pinker, 2014). He attributes this, for the most part, not to the ill will
of scholars or a desire to obfuscate but, rather, to the fact that writing
well is hard. Moreover, as long as bad writing continues to be published,
and those publications continue to advance p eople’s careers, it must be
accepted as the norm (Albert, 2004). A long history of work on auto-
matic text simplification has resulted in potentially useful tools,9 and
our recent experimentation using LLMs for this purpose shows promise.
In addition, manual simplification is actually quite fast and s imple. In
figure 9.3, the option of manual simplification is folded into the task of
identifying text worth pro cessing.

278 Chapter 9
• Identify unknown words. This is done automatically by the LEIA running
the first two stages of natur al language understanding: Basic Syntax and
OntoSyntax.
• Loop through knowledge acquisition and text analys is until either (a)
the system produces a golden TMR, which can then optionally be stored
to episodic memory, or (b) the knowledge engineer decides to abandon
the text, possibly having acquired useful linguistic and/or ontological
knowledge by working on it. It is import ant to allow knowledge engi-
neers to discontinue working on texts that prove to be more difficult
than expected—f or example, texts whose proc essing requires develop-
ment work by a software engineer, such as programming a procedural
semantic routine.
Minor edits to a text can dramatically improve a LEIA’s ability to under-
stand it. The following is how a subject matter expert, gastroenterologist
George Fantry, explained, in a personal correspondence, what is m easured
by esophageal motility tests:
Key measurements are Distal Latency (DL) and Distal Contractile Integral (DCI).
DL is the time interval in seconds from UES relaxation to where propagation of
peristalsis slows (m easured in seconds). DCI is a m easure of the vigor of the con-
traction, measured as Amplitude × duration × length (mmHg- s-cm) of the distal
esophageal contraction (previously utilized only amplitude).
Thanks to past collaboration with Dr. Fantry, we fully understood this
explanation, but LEIAs will face numerous challenges in interpreting this
passage. To start, it shows four diff er ent uses of parentheses, whose mean-
ings must be made manifest in the TMR. Parentheses can:
• introduce an abbreviation: (DL)
• explic itly provide a measuring unit: ( measured in seconds)
• implicitly provide a measuring unit: (mmHg-s -cm)
• signal an aside: (previously utilized only amplitude).
Other complexities include:
• Ellipsis: “Key m easurements [of esophageal motility tests]” and “([the
measurement of DCI] previously utilized only amplitude).”
• An informal turn of phrase: “from UES relaxation to where propagation. . . .”
• Instances of non- coreferential the that must be interpreted appropri-
ately: the time interval, the vigor, the distal esophageal contraction.10
• The mathematical use of x.

Knowledge Acquisition 279
A LEIA would be better able to derive the meaning if the input w ere simpli-
fied. Table 9.2 shows one such possibility.
This rewrite preserves most of the content of the original text but using
a simpler writing style. We must emphasize that we are not absolving LEIAs
of the need to p rocess difficult texts. In fact, we spend a lot of time prepar-
ing them to deal with inputs that include phenomena that are outside of
their current capabilities.11 However, building agent systems requires sober
practicality: it doesn’t make sense to ask a LEIA to semantically analyze seri-
ously challenging texts.
The above text simplification methodology is supported by interface
functionalities in the DEKADE development environment. Additionally, as
mentioned earlier, text simplification tools can be used to at least partially
automate this process.
We conclude this chapter on manual and semiautomatic acquisition by reit-
erating the main point: if one argues for the necessity of developing explain-
able cognitive systems, one must have a realistic plan for endowing agents
with knowledge that is of a size and complexity that makes them useful col-
laborators. Our plan comprises two parts. Knowledge engineers, supported by
well- designed automation, work on compiling lexical and ontological knowl-
edge that serves as a foundation. At the same time, LEIAs are being designed to
learn automatically, bootstrapping from that foundation and adding knowl-
edge at the fringes of what they know. This approach is no more l abor inten-
sive than the data- driven approaches that dominate mainstream AI.
Table 9.2
An example of text simplification.
Original Text Simplified Version
Key measurements are Distal Latency Esophageal motility tests measure
(DL) and Distal Contractile Integral (DCI) Distal Latency and Distal Contractile
Integral.
DL is the time interval in seconds from Distal Latency is the time interval
UES relaxation to where propagation of between the relaxation of the upper
peristalsis slows ( measured in seconds). esophageal sphincter and the slowing
of peristalsis. It is measured in seconds.
DCI is a m easure of the vigor of the con- Distal Contractile Integral measures
traction, measured as Amplitude × dura- the intensity of the contraction of
tion × length (mmHg- s-cm) of the distal the distal esophagus. The measuring
esophageal contraction (previously unit for Distal Contractile Integral is
utilized only amplitude) mmHg- s-cm.

