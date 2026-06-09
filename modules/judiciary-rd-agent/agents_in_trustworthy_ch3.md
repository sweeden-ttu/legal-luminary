3 Knowledge Bases
A distinguishing feature of LEIAs is their reliance on a large amount of
stored knowledge. Their core knowledge bases are the ontology; the lexi-
con; lexicon analogues for nonlinguistic channels of perception, such as
an opticon for the interpretation of visual stimuli; and episodic memory.
The theoretical and methodological princip les under lying the content and
organization of these knowledge bases are detailed in Nirenburg and Raskin
(2004) and McShane and Nirenburg (2021). This chapter recaps the basics
and describes how two microtheories— involving complex properties and
scripts— have recently evolved to account for the demands of learning and
explaining by LEIAs. But first it is import ant to show why well-k nown, large
“knowledge” resources are not sufficient.
3.1 Why Preexisting Resources Don’t Fill the Bill
There are many human-c urated repositories of information about language
and the world— lexicons, thesauri, wordnets, grammars, ontologies— but
they do not contain knowledge in a LEIA’s sense of the word and, therefore,
are not directly useful to them. This is unfortunate b ecause they reflect a lot
of human analy sis, and one cannot help but feel that they should be more
useful for developing intelligent systems.1
Human-o riented lexicons When human- oriented lexicons were digitized
in the 1980s, there was a surge of interest in automatically converting them
into machine-o riented knowledge bases.2 Developers expected that systems
could learn an ontological subsumption hierarchy from the hypernyms
that introduce most dictionary definitions (a dog is a domesticated carnivo-
rous mammal) and extract other salient properties as well (. . . that typically
has a long snout). But t here w ere snags:

42 Chapter 3
1. Senses are often split too finely for even a person to understand why.
2. Definitions regularly contain ambiguous words or idiomatic expressions.
3. Sense discrimination is often left to examples, meaning that the user
must infer the generalization illustrated by the example.
4. The hypernym that typically begins a definition can be of any level of spec-
ificity— a dog is a(n) animal / carnivore / domesticated carnivore / mammal—
which confounds the automatic learning of a semantic hierarchy.
5. The choice of what counts as a salient descriptor is variable across entries:
a dog is a domesticated carnivorous mammal; a turtle is a slow- moving reptile.
6. Definitions can be circular: a tool is an implement; an implement is a tool.
After more than a d ecade’s work attempting to automatically adapt
machine- readable dictionaries for use in natu ral language pro cessing, by
the early 1990s, that community concluded that this line of research had
little direct utility: machine- readable dictionaries simply required too much
human- level interpretation to be useful to machines in the ways originally
hoped (Ide & Véronis, 1993). Unfortunately, t hese prob lems do not go away
even if we ask LEIAs to semantically analyze the definitions. It’s a chicken-
and- egg probl em: LEIAs need to learn the very kind of knowledge that is
needed to disambiguate the dictionary’s descriptions.
Thesauri Most thesauri list clusters of words without explaining what dis-
tinguishes them, their main use being to remind native speakers of a word
they could not recall. If you have ever tried to use a thesaurus for a language
you don’t know very well, you realize the probl em facing agent systems.
Moreover, thesauri can group semantically diverse meanings together—n ot
only synonyms and near- synonyms but also rather distant hyponyms and
troponyms. There do exist explanatory thesauri, such as Hayakawa (1994),
which provide explanations of the distinctions between word usages; how-
ever, these descriptions pres ent the same ambiguity challenges as the defi-
nitions in standard dictionaries.3
WordNets The original WordNet (Miller, 1995), from which wordnets in
other languages followed suit, is a lexical database of English whose initial
goal was to model human lexical knowledge. It is organized as a semantic
network of four directed acyclic graphs, one for each of the major parts
of speech: noun, verb, adjective, and adverb. Words are grouped into sets
of synonyms called synsets. Synsets within a part- of- speech network are

Knowledge Bases 43
connected by a small number of relations. For nouns, the main ones are
subsumption (“is a”) and meronymy (“has as part”); for adjectives, anton-
ymy; and for verbs, troponymy, which is subsumption involving the man-
ner of the action.
Although WordNet was not originally developed for computational aims,
it has been widely used by the natu ral language pro cessing community for
a similar reason as machine-r eadable dictionaries: It is large, containing
155,287 unique strings and 206,941 word- sense pairs, and it is freely avail-
able.4 However, as a potential resource for learning by LEIAs, WordNet is as
unwieldy as regular large dictionaries:
• Its definitions are in plain E nglish, so they can be ambiguous or idiomatic.
• It exhaustively lists attested word usages, no matter how rare or narrowly
applicable. For example, t here are ten senses of heart, ten of cat (eight
nominal and two verbal), and eight of beaver (seven nominal and one
verbal).5 Although LEIAs are designed to treat lexical ambiguity, t hese
large inventories, which include rare senses, pres ent a serious obstacle
for making practical pro gress on computational semantics.
• The relative frequency of senses is not indicated. For example, two of
WordNet’s nominal senses of dog are “a hinged catch that fits into a notch
of a ratchet” and “metal supports of logs in a fireplace.” Similarly, there
are two verbal senses of cat meaning to beat with a cat-o ’- nine- tails and
to vomit. Even an impressionistic indication of rare or specialist-d omain
senses would have increased the potential utility of this resource for LEIA
learning.
• Multiword expressions are listed as if they were regular senses of one of
their constituent words, with no indication that the entire collocation
is needed to convey the meaning. Examples are to play house (listed as a
sense of house), to have a change of heart (listed as a sense of heart), and to
do something by the book (listed as a sense of book).
• Syntactic and semantic information about the arguments of verbs is not
provided, which means that, even in the best case, a LEIA could only
learn which verbs might be synonyms or troponyms of other verbs, not
all of the dependency- based information needed to process them.
• The results of productive linguistic pro cesses are recorded as word senses,
which runs c ounter to a LEIA’s model of h uman language proc essing,

44 Chapter 3
which distinguishes stored knowledge from productive pro cesses. For
example:
– Metonymies can be listed as regular word senses. For example, one
sense of house refers to the f amily living there, in contexts like “I waited
until the w hole house was asleep.” But any object can be used met-
onymically to refer to someone associated with it: The backpack <uni-
cycle, blue shirt> just waved at us.
– Regular personifications can be listed as senses. For example, t here is
a separate sense of teacher whose examples include “books were his
teachers” and “experience is a demanding teacher.”
The probl em with listing the results of productive linguistic pro cesses as
word senses in a LEIA’s lexicon is that e very time the agent encountered the
given word, it would have to consider all of the listed senses. For example,
if the lexicon contained a sense of house meaning “the people in a house,”
then every input with house would result in a candidate analys is using this
interpretation. Not only is this hardly likely to model human lexical stor-
age but it also unnecessarily complicates language analys is. A much better
solution to treating productive linguistic pro cesses is the one that LEIAs
actually use: they consider nonliteral meanings of words only if the senses
recorded in the lexicon do not semantically fit the context. For example,
since a house cannot be asleep, when a LEIA analyzes I waited until the whole
house was asleep, it will engage in recovery procedures that consider, among
other things, the possibility that house is being used metonymically. This
is a normal part of its language understanding process (cf. section 4.2.1).
• The classification of verbs is often imprecise. For example, all of the fol-
lowing verbs are considered to be troponyms of kill but they do not
actually mean to kill—t hey indicate methods of injuring someone that
may or may not result in death: poison, stone, brain, impale, shed blood,
electrocute, flight (to shoot a bird in flight), pick off, shoot, saber, tomahawk,
strangle.
• Definitions are often idiomatic or include vocabulary that is more com-
plicated than the word being described. In the following examples, the
tricky parts are italicized:6
– lynch: kill without legal sanction
– murder, slay, hit, dispatch, bump off, off, polish off, remove: kill
intentionally and with premeditation

Knowledge Bases 45
– burke: murder without leaving a trace on the body
– execute, put to death: kill as a means of socially sanctioned punishment
– neutralize, neutralise, liquidate, waste, knock off, do in: get rid of
(someone who may be a threat) by killing
• Notes about semantic constraints do not specify which participant is being
referred to. For example, from the definition of assassinate— “murder;
especially of socially prominent persons”— one must figure out that the
socially prominent people are the theme, not the agents, of the action.
Like any resource, WordNet reflects a large number of choices by its devel-
opers, who had par tic u lar goals and priorities in mind— none of which was
to support learning by intelligent agents like LEIAs. So, our assessment is
not of WordNet in the abstract. Instead, the question for us is whether this
resource, which reflects a significant societal investment, can contribute to
LEIA development. The answer is “yes,” but not as a source of automatic
learning by LEIAs. Instead, it can be used to jog the memories of knowledge
engineers, who can skim it for useful content.
FrameNet FrameNet is a lexical knowledge base inspired by the theory
of frame semantics (Fillmore & Baker, 2009), which is a precursor of con-
struction grammar (Hoffmann & Trousdale, 2013). Frame semantics sug-
gests that the meaning of many words and multiword expressions is best
described using semantic frames that indicate a type of event and the types
of entities that participate in it. For example, an Apply_heat event involves
a Cook, Food, and a Heating_instrument. A frame thus described can be
evoked by par tic u lar lexical units (i.e., words and phrases), such as fry and
bake. FrameNet includes frame descriptions, associated lexical units, and
annotated sentences featuring those lexical units. Frame semantics cap-
tures observations about language and meaning similar to t hose made by
the theory of Ontological Semantics that underpins LEIAs’ language pro-
cessing. However, frame semantics mixes lexical and ontological knowl-
edge in a way that diverges from our approach.
Because of the high lexicographic quality of FrameNet, we tried to make
use of it— specifically, to give LEIAs practice in (a) learning new words and
multiword expressions and (b) analyzing sentences from the open domain.
Although the experiment that explored this potential was not as fruitful as
we had hoped, it was instructive, helping us to clarify what constitutes the
kind of learning material that will help LEIAs to walk before they can run.

46 Chapter 3
In order for LEIAs to use FrameNet as a resource, the first requirement is
to automatically align FrameNet frames with concepts in the LEIA’s ontol-
ogy. An alignment is hypothesized if two or more FrameNet lexical units
are attested in the LEIA’s lexicon and mapped to the same or proximate
concepts in the same line of inheritance in the LEIA’s ontology. According
to this heuristic, FrameNet’s Ingestion frame aligns with the LEIA’s concept
INGEST based on the evidence summarized in t able 3.1.
For each concept- level alignment, two opportunities open up: the LEIA
can learn new lexemes and analyze annotated sentences.
Learning new lexemes FrameNet frames contain words and multiword
expressions that the LEIA does not yet know and can learn—s uch as the
verbs down, feed, gobble and guzzle and the noun gulp in t able 3.1. Besides
the concept mapping, LEIAs need to learn the syntactic d ependency
structures in which each word can participate, which is illustrated by the
frame’s examples. For instance, the verb gobble can take a direct object
(“ Don’t gobble yer food so fast”) or it can be used with vario us particles
in phrasal verb constructions (“I gobbled them down,” “This year . . . four
tons of fresh strawberries w ill be gobbled up”). Similarly, the noun gulp
Table 3.1
A sampling of alignments between FrameNet and a LEIA’s ontology and lexicon.
FrameNet concept Ingestion LEIA concept INGEST
breakfast.v breakfast- v1
consume.v consume- v1
devour.v devour- v1
dine.v dine- v1
down.v –
drink.v drink- v1
eat.v eat- v1
feast.v feast- v1
feed.v –
gobble.v –
gulp.n –
gulp.v gulp- v1
guzzle.v –
have.v have- v5

Knowledge Bases 47
can take a prepositional phrase with of that indicates what is drunk (“She
drank a good gulp of whiskey”).
Analyzing sentences that use the word in the known meaning One of the
main offerings of FrameNet is its large repository of annotated sentences,
which can be used to test the quality of language understanding by LEIAs.
These annotations provide (a) a key lexical disambiguation decision— that
is, the meaning of the word whose use is illustrated by the example, and (b)
the fillers of that word’s case roles. The FrameNet examples can, in princi-
ple, also support lexicon learning through bootstrapping. For example, one
of FrameNet’s examples of drink is “They drank hot sake from tiny porcelain
cups, . . . ,” from which the LEIA can learn that sake is a type of BEVERAGE (to
understand how it does this, see chapter 7).
Naturally, we manually analyzed FrameNet to some degree before
designing our learning experiment, and it was our analy sis of frames like
the following that gave us reason to believe that the approach might work:
Absorb_heat, Arrest, Bragging, Cogitation, Communication_manner, Inges-
tion, Self_motion. However, when we launched the program on FrameNet
overall, the results were much less clean than we had expected. Reasons
include the following:
• FrameNet uses both generic and frame- specific case role labels, whereas
a LEIA’s knowledge bases use only generic ones. For example, FrameNet’s
Ingestion frame includes an Ingestor and Ingestibles as case roles,
whereas a LEIA’s concept INGEST uses a generic AGENT and THEME. So, LEIAs
have to hypothesize the FrameNet- to-L EIA alignment in each case.
• Some FrameNet frames group entities in ways that our semantic theory
does not permit, as by bunching words and their antonyms. For exam-
ple, the Accompaniment frame includes the words alone and together.
LEIAs cannot automatically distinguish synonyms from antonyms, at
least not without consulting additional resources.
• FrameNet frames can cover broader semantic territory than the LEIA
concepts to which associated words would link. For example, the frame
Cause_to_experience covers amuse and entertain as well as terrorize and
torment.
• FrameNet bunches literal and meta phorical uses, which is something we
strictly avoid. For example, the FrameNet lexical unit devour.v belongs

48 Chapter 3
to the frame Ingestion but includes the examples, “On rainy days he
devoured books, . . .” and “The houses looked like shambling tents of
black straw, their terraces devoured by the glutton of rot . . .”
• Generalizing from the last point, since FrameNet developers w ere not
orienting around the needs of agent systems, some of the examples
they chose to annotate are worst cases for automatic analys is. Given the
example “ We’re not talking about children eating deadly nightshade,” a
LEIA has no way of knowing that deadly nightshade should not be learned
as an INGESTIBLE (the LEIA’s ontology asserts that THEMEs of INGEST must be
INGESTIBLEs). Of course, the agent could be configured to carry out addi-
tional work to vet e very candidate learnable; however, that kind of work
is exactly what we w ere trying to avoid by using a curated resource like
FrameNet as a source for learning.
• All of FrameNet’s definitions are in plain English, thus presenting all
of the ambiguity challenges of the definitions in human-o riented lexi-
cons and WordNet. For example, amble (part of the Self_motion frame)
is described as “walk or move at a leisurely pace”; and bop is described as
“to go quickly or unceremoniously; shuffle along as if to bop music.” A
LEIA could not automatically learn how t hese words differ from the core
meaning of the frame without knowing the meanings of leisurely pace,
unceremoniously, and bop music.
• FrameNet’s example annotations provide less added value to LEIAs than
they might to other computer systems because our language understand-
ing system identifies case roles as part of its normal operation.
In the spirit of not giving up on using existing resources, we could man-
ually prune FrameNet in order to make it more useful to LEIAs. This would
involve removing all metap horical and unreasonably difficult examples,
splitting or removing frames that bunch antonyms, reformulating defini-
tions to be more useful, and the like. We could also try to automate the
pruning, at least partially. However, this would make sense only if the
methods developed had broader applicability—t hat is, if they w ere able
to detect learning-s uitable material in any text repository. FrameNet is too
small to make narrowly focused manual work cost- effective.
To reiterate, the reason we spent effort on exploring the potential utility
of FrameNet is because we thought it might offer LEIAs useful practice in
learning new words and analyzing open-d omain sentences in a setup that
included hints based on manual curation. However, since no small amount

Knowledge Bases 49
of manual work is needed to prepare for such a process, further exploration
of this resource goes on the list of potential but not imminent knowledge-
acquisition methodologies. Our experimentation with FrameNet under-
scores our main claim about knowledge acquisition for LEIA- like intelligent
systems: it is best done in conjunction with system-b uilding. Even with
optimal bootstrapping knowledge, automatic semantic analy sis and learn-
ing are challenging. With resources that are not entirely suited to the task,
challenging quickly morphs into impossible.
Cyc Cyc is one of the oldest ontology-b uilding efforts to date, described
by its developers as a “high-r isk high- labor long- term proje ct” (Lenat et al.,
1990). Its proj ect leader, Doug Lenat, started the proj ect with the goal of
recording a sufficient amount of commonsense knowledge to support any
task requiring AI. He writes: “[F]or the last 35 years that Manhattan-P roject-
like effort has occupied a team of over a hundred knowledge engineers
(whom I dubbed ‘ontologists’ back then)—t hat’s millions of person-
hours of writing and testing and debugging IF/THEN rules” (Lenat, 2019).
Although initially configured using the frame-l ike architecture typical of
most ontologies, the knowledge repre sen ta tion strategy shifted to a “sea
of logical assertions,” such that each assertion is equally about each of the
terms used in it (Mahesh et al., 1996, p. 21).
In a published debate with Lenat (Lenat et al., 1995), George Miller artic-
ulates some of the controversial assumptions of the Cyc approach: that
commonsense knowledge is propositional; that a large but finite number of
factual assertions, supplemented by machine learning of an as-y et undeter-
mined type, can cover all necessary commonsense knowledge; that genera-
tive devices are unnecessary; and that a single inventory of commonsense
knowledge can be compiled to suit any and all AI applications. Additional
points of concern include how p eople can be expected to manipulate—
find, keep track of, detect lacunae in— a knowledge base containing mil-
lions of assertions, and the ever- present prob lem of lexical ambiguity. Yuret
(1996) offers a fair- minded explanatory review of Cyc in the context of AI.
Although we give Lenat and the ontologists at Cyc a lot of credit for tak-
ing on the challenge of building such a large knowledge base, we do not use
it. As previously mentioned, our experience shows that knowledge bases
and pro cessors need to be developed together. We do not exclude that Cyc
might be useful in some way as LEIAs evolve over time, but assessing how it
might be employed would be a large program of work in itself.

50 Chapter 3
It is plain common sense that reusing existing resources has the poten-
tial to save effort. It was, therefore, impor tant to spend time here describing
our lessons learned from attempting to use available knowledge resources
and explaining why the current offerings do not directly fulfill the needs of
LEIAs. Now we will turn to the resources that LEIAs actually need in order
to implement the computational cognitive models under lying them.
3.2 Ontology
A computational ontology is a model of the world designed to foster reason-
ing by agent systems. The ontology used by LEIAs is o rganized as a multiple-
inheritance hierarchical graph of concepts—O BJECTs and EVENTs— each of
which is described using PROPERTYs. Concepts are named using language-
independent labels, written in small caps, that resemble E nglish words only
for the benefit of English- speaking developers. The actual meaning of a
concept is its inventory of property- facet-f iller triples.
Facets permit the ontology to include an extra level of detail about prop-
erty fillers, such as the fact that the most typical colors of a car are white,
black, silver, and gray; other normal, but less common, colors are red, blue,
brown, and yellow; and rare colors are green and purple. The inventory of
facets includes: default, which represents the most restricted, highly typi-
cal subset of fillers; sem, which represents typical selectional restrictions;
relaxable- to, which represents what is, in princip le, poss i ble although not
typical; and value, which represents not a constraint but an a ctual, non-
overridable value. Value is used primarily in episodic memory but applies
to a select few properties in the ontology, such as DEFINITION, IS- A, and SUB-
CLASSES. A sampling of properties from the ontological frame for the event
SURGERY illustrates the use of facets.
SURGERY
DEFINITION value performing a medical procedure that
involves cutting into tissue
IS- A value INVASIVE- PROCEDURE
AGENT default SURGEON
sem MEDICAL- PERSONNEL
relaxable-to HUMAN
THEME default HUMAN
sem ANIMAL

Knowledge Bases 51
INSTRUMENT sem SURGICAL- INSTRUMENT
LOCATION default OPERATING- ROOM
sem MEDICAL- BUILDING
relaxable-to PLACE
The main benefits of writing an ontology in a knowledge repres en ta tion
language rather than a natu ral language are (a) the absence of ambiguity in
the knowledge repres ent a tion language, which makes the knowledge suit-
able for automatic reasoning, and (b) the ontology’s reusability across natur al
languages.
The ontology covers both general and specific domains and currently
contains around nine thousand concepts. The bulk of it was compiled
some twenty- five years ago, and, in keeping with our lab’s focus on cogni-
tive modeling research rather than application development, only modest
enhancements have been made since. We use the ontology as a research
tool and enhance it to test the ever-g rowing inventory of microtheories—
including the hypothesis that LEIAs can acquire ontology in de pen dently
through dialog, experience, and reading.
The example of SURGERY illustrates the simplest kind of ontological
structure. The expressive power of the ontology is actually far greater, and
its content far richer, since the ontology is intended to support multiple
agent functionalities including simulation, reasoning, learning, teaching,
explaining, and beyond.
3.2.1 Properties
Every OBJECT and EVENT is described using PROPERTYs. The inventory of PROP-
ERTYs essentially supplies the axiomatic layer of the ontology’s repres en ta-
tional system. PROPERTYs are characterized by their DOMAIN (constraints on
the sets of concepts for which they are defined) and their RANGE (their value
sets). The LEIA ontology includes several types of PROPERTYs:
• IS- A and SUBCLASSES indicate the concept’s placement in the inheritance
hierarchy. Multiple inheritance is permitted but not overused, and rarely
does a concept have more than two parents.
• RELATIONs indicate relationships among OBJECTs and EVENTs. The DOMAIN
and RANGE of RELATIONs are, therefore, filled by OBJECTs and/or EVENTs.
Examples include the case roles (e.g, AGENT, THEME7), spatial relations (e.g.,
ABOVE, NEXT- TO), HAS- OBJECT- AS- PART, CAUSED- BY, and so on. All RELATIONs have

52 Chapter 3
inverses: for example, the inverse of AGENT is AGENT- OF, the inverse of ABOVE-
AND- TOUCHING is BELOW- AND- TOUCHING, and the inverse of CAUSED- BY is EFFECT.
• SCALAR- ATTRIBUTEs are properties of OBJECTs and EVENTs that can be expressed
by numbers or ranges of numbers, such as COST, VELOCITY, and WEIGHT.
Values can be a ctual— for example, 180 pounds is “WEIGHT (180 MEASURED-
IN POUND)”—or they can be expressed on the abstract scale {0,1}— for
example, heavy is “WEIGHT .8” and light is “WEIGHT .2.”
• LITERAL- ATTRIBUTEs are properties of OBJECTs and EVENTs whose fillers are
represented by uninterpreted literals. For example, the property MARITAL-
STATUS has the literal fillers single, married, divorced, and widowed.
• SUBEVENTS holds ontological scripts, also known as complex events
(section 3.2.4).
• SEMANTIC-E XPANSION holds concept-b ased descriptions of complex proper-
ties (section 3.2.1).
• The DEFINITION field holds a natu ral language string that explains the con-
cept. Definitions are used by developers as well as by LEIAs for purposes
of explanation.
Ontological PROPERTYs can also function as ABSTRACT-O BJECTs: Friendli-
ness is impor tant; Color livens up a house. Property- based abstract nouns are
recorded in the lexicon as an ABSTRACT-O BJECT with a RELATION to the meaning
of the adjective. Since the adjective friendly is described as “FRIENDLINESS .8,”
the noun friendliness is described as:
ABSTRACT- OBJECT
RELATION FRIENDLINESS-1
FRIENDLINESS-1
RANGE .8
Treating nominal uses of properties as ABSTRACT-O BJECTs allows them to par-
ticipate in larger propositions in the normal way—t hey can be modified,
evaluated as case-r ole fillers, and so on. For example, the meaning repres en-
ta tion for Friendliness is impor tant is:
ABSTRACT- OBJECT-1
RELATION FRIENDLINESS- 1
IMPORTANCE .8
FRIENDLINESS-1
RANGE .8

Knowledge Bases 53
Properties can be s imple or complex. S imple properties, like WEIGHT and
VELOCITY, can be directly grounded in the real world, without further onto-
logical decomposition. Complex properties, by contrast, can be explained
in terms of other OBJECTs, EVENTs, and PROPERTYs. For example, a salient fea-
ture of people is who they are married to, which is expressed by the RELATION
called HAS- SPOUSE. This is not a primitive; it can be explained as the state that
is the EFFECT of a MARRY event. If you know about the MARRY event, you can
infer the HAS- SPOUSE relation and vice versa.
Complex properties are essential for cognitive modeling because they
capture how people think about the world—a nd, in turn, how they talk,
teach, learn, and reason about it. Recording the semantic interpretations
of complex properties in the ontology enables agents to make inferences
and understand implicatures like people do—an essential capability that
has largely eluded AI to date.8 For example, if an agent hears Jan and Paul
are married, which is semantically analyzed using the HAS- SPOUSE relation, it
must also understand that they w ere both AGENTs of the same MARRY event.
Similarly, if an agent hears that something is large, which is semantically
analyzed as “SIZE .8,” it must understand (a) that this implies a high value of
one or more of the primitive properties LENGTH, WIDTH, DEPTH, HEIGHT, and/
or WEIGHT, and (b) what the ballpark size of the given object is, since a large
beetle is much smaller than a large oak tree.
Philosophical analy sis of the nature and classification of properties is
beyond the scope of book.9 H ere, we focus on how LEIAs are being prepared
to interpret complex properties and make property- related inferences so that
they can communicate, reason, and learn about the world like p eople do.
For orientation, the property-r elated phenomena we will describe are as
follows:
– Complex properties can be states resulting from an event.
– Complex properties can generalize over repeated events.
– Complex properties can be shortcuts for an event- based chain.
– Complex properties can generalize over other properties.
– Abstract values of scalar properties can be calculated.
– Complex properties can have indirect semantic expansions.
– Qualitative properties can be used with quantitative implications.

54 Chapter 3
Complex Properties Can Be States Resulting from an Event Typical exam-
ples of states that result from events involve familial relations. Consider
again the example of getting married. Below is an excerpt from the onto-
logical description of the event MARRY that shows its relation to the state
HAS- SPOUSE. The numerical indices represent ontological instances, which
allow for coreference and disambiguation within multi-f rame ontological
structures (see section 3.2.2).
MARRY
AGENT HUMAN-1 , HUMAN-2
EFFECT HAS- SPOUSE-1 , HAS- SPOUSE-2
HAS- SPOUSE-1
DOMAIN HUMAN-1
RANGE HUMAN-2
HAS- SPOUSE-2
DOMAIN HUMAN-2
RANGE HUMAN-1
This says that when two p eople are the AGENTs of MARRY, the EFFECT is
that they are in a HAS- SPOUSE relationship. The connection between MARRY
and HAS- SPOUSE is also recorded in the SEMANTIC-E XPANSION field of HAS- SPOUSE’s
property definition, as shown below. Explanatory comments are provided
a fter semicolons.
HAS- SPOUSE
DOMAIN HUMAN-1
RANGE HUMAN-2
INVERSE SPOUSE- OF
SEMANTIC- EXPANSION
PRECONDITION MARRY-1 , MODALITY-1 ; they were married and not divorced
MARRY-1 ; they w ere married
AGENT HUMAN- 1, HUMAN-2
MODALITY-1 ; there was no divorce
TYPE EPISTEMIC
VALUE 0
SCOPE DIVORCE- 1
DIVORCE-1
AGENT HUMAN- 1, HUMAN-2 ; by these same people
TIME > MARRY-1 .TIME ; since their marriage
The SEMANTIC-E XPANSION of HAS- SPOUSE includes more information than the
MARRY script—n amely, that the individuals w ere not subsequently divorced.

Knowledge Bases 55
To recap: the reason why the ontology includes the relationship HAS-
SPOUSE is that people think and talk about the world in terms of kinship
relations. The relationship between HAS- SPOUSE and MARRY must be explic itly
recorded in the ontology to support the bidirectional inferencing between
getting married, which is an EVENT, and being married, which is a state
expressed as a RELATION.
Complex Properties Can Generalize over Repeated Events Athletes have
coaches, people have dentists, and kids have babysitters. T hese social
relations—H AS-C OACH, HAS-D ENTIST, HAS-B ABYSITTER— imply repeating events
and, in some cases, a formal process of establishing the relationship, such
as filling out paperwork to become a dentist’s patient. Seeing a dentist for
an emergency treatment while traveling does not make that person one’s
dentist.
The correlation between such properties and the event sequences that
they imply can be expressed in two ways in the ontology. On the one hand,
it can be appended to the event description as a conditional statement. If
we assume that more than one instance of coaching is needed to infer a
HAS- COACH relationship (the actual number can be understood differently by
dif fer ent people), then it will look as follows:
COACHING- EVENT-1
AGENT COACH- 1
BENEFICIARY ATHLETE- 1
SEMANTIC- EXPANSION
If ; If
SET ; there is more than one coaching event
MEMBER- TYPE COACHING- EVENT- 1
CARDINALITY >1
COACHING- EVENT-1 ; in which
AGENT COACH- 1 ; a part ic u lar coach coaches
BENEFICIARY ATHLETE- 1 ; a par tic u lar athlete
Then ; Then
HAS- COACH-1 ; that athlete has that coach
DOMAIN ATHLETE- 1
RANGE COACH- 1
This information is also stored in the SEMANTIC-E XPANSION field of the descrip-
tion of HAS- COACH, which also lists another way of establishing the relation-
ship: by hiring the coach.

56 Chapter 3
HAS- COACH-1 ; A par tic u lar athlete has a par tic u lar coach
DOMAIN ATHLETE- 1
RANGE COACH- 1
INVERSE COACH- OF
SEMANTIC- EXPANSION
If ; If
Either ; the coach has coached the athlete more than once
SET
MEMBER- TYPE COACHING- EVENT- 1
CARDINALITY >1
COACHING- EVENT-1
AGENT COACH-1
BENEFICIARY ATHLETE-1
Or ; or
HIRE-C OACH ; the athlete hired the coach
AGENT ATHLETE- 1
THEME COACH- 1
Then ; Then
HAS- COACH-1 ; the athlete has the coach
DOMAIN ATHLETE- 1
RANGE COACH- 1
For an example that does not involve social relations, we can look at
the Maryland Virtual Patient clinician training system (section 8.5), where
patient symptoms were modeled as properties whose values changed
throughout the interactive simulation. For example, DIFFICULTY- SWALLOWING
had the patient as its DOMAIN and the abstract values {0,1} as its RANGE. At the
beginning of a simulation run, before the patient experienced any symp-
toms, the value for DIFFICULTY- SWALLOWING was 0; but if the patient had a dis-
ease that caused difficulty swallowing, as the disease progressed, the value
for this property would increase. This property captured how physicians
think, talk, and reason about this symptom. In a word, they generalize—
they do not think in terms of the innumerable times a patient swallows in
a given day, month, or year. However, in order for the property DIFFICULTY-
SWALLOWING to have meaning, it must be described in the ontology with
reference to the implied large set of SWALLOW events:
DIFFICULTY-S WALLOWING-1
DOMAIN HUMAN-1 ; A part ic u lar person has
RANGE {0,1} ; a par tic u lar value for DIFFICULTY- SWALLOWING
SEMANTIC- EXPANSION
If ; If

Knowledge Bases 57
DIFFICULTY-A TTRIBUTE-1 ; difficulty-a ttribute applies
DOMAIN SET- 1 ; to a set of swallow events
RANGE var1 ; and has a part ic u lar value
SET-1 ; and that set
MEMBER- TYPE SWALLOW- 1 ; of swallow events
QUANT .8 ; is large
SWALLOW-1
AGENT HUMAN- 1 ; and is carried out by this person
Then ; Then
DIFFICULTY-S WALLOWING-1 ; the value of difficulty- swallowing is the
DOMAIN HUMAN- 1 ; range of difficulty- attribute- 1— that is,
RANGE var1 ; how difficult the swallowing is
This says, “If the value of DIFFICULTY- ATTRIBUTE for a large number of SWALLOW
events by a part ic u lar person is [some value], then the value of DIFFICULTY-
SWALLOWING for that person is [that same value].”
Complex Properties Can Be Shortcuts for an Event- Based Chain Con-
tinuing to draw examples from the medical domain, when clinicians
think, talk, and teach about DISEASEs, properties like the following are use-
ful: HAS- TYPICAL- SYMPTOM, HAS- DIAGNOSTIC- TEST, SUFFICIENT- GROUNDS- TO- SUSPECT,
SUFFICIENT- GROUNDS- TO- DIAGNOSE, SUFFICIENT- GROUNDS- TO- TREAT, and PREFERRED-
ACTION- WHEN- DIAGNOSED. These, in fact, were included in the Maryland
Virtual Patient system mentioned e arlier, and they are conceptual short-
cuts for what is actually going on. Whereas HAS- TYPICAL- SYMPTOM links a
disease to a symptom, in reali ty diseases are not directly associated with
symptoms: PATIENTs who are experiencing a DISEASE also likely experience
the given SYMPTOM (both DISEASEs and SYMPTOMs are EVENTs). This expla-
nation is recorded in the SEMANTIC- EXPANSION zone of the property called
HAS- TYPICAL- SYMPTOM:
HAS- TYPICAL- SYMPTOM
DOMAIN DISEASE-1
RANGE SYMPTOM- 1
SEMANTIC- EXPANSION
If
ANIMAL-1
EXPERIENCER-OF DISEASE-1
Then
ANIMAL-1
EXPERIENCER-OF SYMPTOM-1
SYMPTOM-1
LIKELIHOOD .8

58 Chapter 3
Recording the likelihood of the symptom as .8 (on the abstract scale {0,1})
conveys the notion of typical. For each par tic u lar disease, each par tic u lar
symptom has a population- based likelihood, which will be recorded if the
agent has learned that information.
Complex Properties Can Generalize over Other Properties When think-
ing about families, one thinks about grandparents, great-g randparents,
cousins, aunts, siblings, and the rest. However, all of these can be explained
in terms of the more primitive properties HAS- OFFPSRING and HAS- SPOUSE. The
property HAS- GREAT-G RANDCHILD illustrates how properties can, and need to
be, explained in terms of more primitive properties.
HAS- GREAT-G RANDCHILD
DOMAIN HUMAN
RANGE HUMAN
INVERSE GREAT- GRANDCHILD- OF
SEMANTIC- EXPANSION
If HUMAN-1 (HAS- GREAT- GRANDCHILD HUMAN-4 )
Then HUMAN-1 (HAS- OFFSPRING HUMAN-2 )
And HUMAN-2 (HAS- OFFSPRING HUMAN-3 )
And HUMAN-3 (HAS- OFFSPRING HUMAN-4 )
In addition, since HAS- OFFSPRING is, itself, semantically expanded using the
events BEAR- OFFSPRING and MARRY, the agent has the knowledge to reason
about these events if needed.
Abstract Values of Scalar Properties Can Be Calculated It is natu ral to think
and talk about the world in an underspecified way: a tall person, a fast race,
an inexpensive meal. Abstract values of scalar attributes allow us to represent
correspondingly imprecise meanings: a tall person— “ HUMAN (HEIGHT .8),” a fast
race— “RACE (VELOCITY .8),” a moderately-p riced meal— “MEAL (COST .5).” However,
in some cases, underspecified descriptions need to be concretized in order
to serve the needs of agent reasoning. For example, if we ask a robotic LEIA
to dig a hole the size of a large packing box, it needs to convert that descrip-
tion into some actual LENGTH, WIDTH, and DEPTH. For the agent to make such
calculations, it must know the actual size of the object referred to. For exam-
ple, packing boxes sold by one US comp any10 range from 6 × 6 × 6 inches to
24 × 24 × 24 inches, which informs the following ontological description:
PACKING- BOX
LENGTH sem 6– 24 (MEASURED-IN INCH)
WIDTH sem 6– 24 (MEASURED-IN INCH)
HEIGHT sem 6– 24 (MEASURED-IN INCH)

Knowledge Bases 59
Calculations of actual sizes from relative ones, which are always understood
to be approximate, are straightforward:11
A large box (abstract value .8) is around 20.4 inches L, W, H
A small box (abstract value .2) is around 9.6 inches L, W, H
The function for calculating a ctual values from abstract ones is recorded
as a SEMANTIC-E XPANSION attached to the SIZE property, which is the source
of such generalizations. We can see that this works pretty well in a com-
pletely diff er ent domain—p eople’s heights. If we say that the typical range
of heights for p eople is 4′10″ (58″) to 6′4″ (76″), then a tall person (.8 on the
scale) is around 6′ and a short person is around 5′1″.
Although generic formulas are useful, they do not work well in all cases,
as when extreme high and/or low values are substantially distant from the
normal range.12 Consider cars: a Rolls-R oyce Boat Tail car costs $28 million,
whereas the cheapest new Kia is u nder $17,000, and you can buy an old
junker for a couple hundred bucks.13 The ontology permits recording such
values explic itly using facets: sem for the normal values and relaxable- to for
the extreme ones, which can improve the relative calculations by orient-
ing around the sem range of values. But if agents need to be able to reason
more precisely about such values—in a way similar to people— then it is
also pos si ble to explic itly list understood values as semantic expansions of
the given property.
Complex Properties Can Have Indirect Semantic Expansions A repeating
theme in this section is that the ontology should rec ord how people think
about the world, which is clear from how they talk about it. Imagine that a
doctor is teaching students about the disease achalasia and says, “Patients
with achalasia complain of difficulty swallowing.” What the students w ill
glean from this is that a typical symptom of achalasia is difficulty swallow-
ing. In ontological terms, this is:
ACHALASIA
HAS- TYPICAL- SYMPTOM DYSPHAGIA
But how do the students extract the intended meaning from what is actu-
ally said?
• They know that the linguistic construction “Patients with NP com-
DISEASE
plain of NP ” means that patients report a symptom, not that they
SYMPTOM
whine about it. (The subscripts in the presentation of constructions indi-
cate ontological constraints on the meaning of the constituents.)

60 Chapter 3
• They know how to reason about generics: if patients with a given disease
report a symptom, then the symptom is typical of the disease.
The question is, how best to prepare an agent to do this reasoning? The
fastest and most reliable way is to rec ord typical ways of thinking and talking
about property values as formal repre sen ta tions in the SEMANTIC-E XPANSION
zone of the PROPERTY. Typical ways of expressing HAS- TYPICAL- SYMPTOM include
the following, among others.
• Patients with NP complain of NP
DISEASE SYMPTOM
• NP suggests NP
SYMPTOM DISEASE
• NP is suggestive of NP
SYMPTOM DISEASE
• NP is key to diagnosing NP
SYMPTOM DISEASE
The SEMANTIC-E XPANSION zone of HAS- TYPICAL- SYMPTOM lists the formal meaning
repre sen ta tions of such formulations, which are recorded in the agent’s lex-
icon as well so that agents can link language inputs to ontological knowl-
edge. Taking the first one as an example:
HAS- TYPICAL- SYMPTOM
SEMANTIC- EXPANSION
If ; If
DECLARATIVE- SPEECH- ACT-1
AGENT PATIENT-1 ; patients say
THEME SYMPTOM-1 ; that t here is a symptom
SYMPTOM-1
EXPERIENCER PATIENT- 1 ; that they are experiencing
PATIENT-1 ; and the same patients
CARDINALITY > 114 ; (indicates plurality)
EXPERIENCER-OF DISEASE- 1 ; have a part ic u lar disease
Then ; Then
DISEASE-1 ; the disease
HAS- TYPICAL- SYMPTOM SYMPTOM- 1 ; has this as a typical symptom
We reco rd semantic expansions like this because, at the current state of
the art, t here is no other way for agents to predict all of the diff er ent ways
that people think and talk about properties, and recording them is a time-
efficient way of making systems work reliably in the near term. For example,
if we want a LEIA to learn about a large number of diseases by reading texts
and listening to teaching physicians, it makes sense to do the small amount
of knowledge acquisition that prepares for common eventualities like the
ones above b ecause it promises a good payoff across hundreds of diseases.

Knowledge Bases 61
Returning to the issue of hybridization, data- driven tools could be used
to collect examples for the agent to learn from by identifying and clus-
tering excerpts that include symptoms and diseases. Then the LEIA could
semantically analyze them into text meaning repre sen ta tions, cluster those
meaning repre sen ta tions based on the concepts they use, and pres ent the
results to a knowledge engineer to vet as candidate values for the SEMANTIC-
EXPANSION zone of HAS- TYPICAL- SYMPTOM. And so on, for other properties of
interest.
Qualitative Properties Can Be Used with Quantitative Implications Quali-
tative properties such as SPATIAL- RELATIONS (e.g., ABOVE, BELOW, ADJACENT- TO)
can carry quantitative implications that an agent needs to understand.15
For example, the property NEAR is a relation that compares the locations of
two physical objects. Although it does not assert any par tic u lar distance
between them, the implied distance depends on the sizes of the objects
in question. In the following examples, the distances implied would be
best measured in inches, feet, small numbers of miles, and tens of miles,
respectively.
(3.1) The pencil is near the notebook.
(3.2) The car is near the stop sign.
(3.3) Her house is near her high school.
(3.4) My hometown is near yours.
It can be impor tant for agents to understand such calculations for similar
reasons as for our hole-d igging robotic LEIA. If a robotic LEIA is told to
stand near the door, does that mean a c ouple of inches away or a dozen
yards away? The way to prepare the robot to make this calculation is to for-
mulate the semantics of nearness.16 The following is a first approximation:
For each of the OBJECTs being compared
Take whichever values of LENGTH, WIDTH, DEPTH, HEIGHT are known.17
Average them together.
NEAR is <= 1.5 * average.
This calculation is a model—a simplistic one, to be sure—t hat produces
reasonable results for three of the four examples above: A pencil near a
notebook is <= 13.8 inches away; A car near a stop sign is <= 13.8 feet away;
and a hometown near another hometown is <= 17.5 miles away.18 For the
house near the high school example, however, this formula does not work:
a house that is near a high school is much farther away than 1.5 times

62 Chapter 3
their average size, even if one counts their grounds. P eople have, and
agents need, additional knowledge about what it means for a building to
be located near another building. Moreover, there are subclasses: buildings
that are near each other on a college campus are likely to be closer to each
other than homes that are near each other in suburbia. The importance of
reasoning about actual distances is illustrated using the example of a LEIA
learning rules of the road in section 7.1.5.
Recapping Why Properties Are So Import ant— And No Simple Matter The
expressive power of the property apparatus in the LEIA ontology is key
to modeling agents that learn, reason, and communicate like people. It
allows for the formalization of an in ter est ing analogy between complex
properties and habitual or reflexive actions. When an action is habitual or
reflexive, people don’t think about it anymore— unless something about
the situation triggers special attention. Thus, we take the same route home
from work e very day u nless a traffic jam c auses us to replan, and we drive
a stick shift car automatically until somebody asks us to teach them how
to do it. Similarly, we use complex properties as shortcuts for learning and
reasoning but can explain them if need be. For example, we think about
our grandm other without thinking about a sequence of birthing and mar-
riage events, but we could explain the relationship in terms of those events
if asked to. Since cognitive modeling involves hypothesizing about what
people seem to know and how they seem to reason, there is ample justi-
fication for including in the ontology whichever properties p eople orient
around and explaining them in ways that prepare agents to reason about
them in same ways as people do.
3.2.2 Ontological Instances
Ontological instances are remembered occurrences of ontological con-
cepts that are used for coreference and reification within larger ontological
descriptions. (Reification is filling a property’s slot with a complex struc-
ture.) For example, whereas it is correct to say that CARs have TIRE as their
part, it is more informative to specify that there are four of them.
CAR
HAS- OBJECT- AS- PART sem TIRE-1
TIRE-1
CARDINALITY value 4

Knowledge Bases 63
Another example of the use of ontological instances involves typical
sequences of events. For example, a fter someone asks a yes-no question,
the other person typically answers it. This question- answer combination is
an example of an adjacency pair—a topic that w ill be further discussed in
chapter 6.
REQUEST- INFO- YN
AGENT sem HUMAN
coref RESPOND- TO-R EQUEST- INFO- YN-1 .BENEFICIARY
BENEFICIARY sem HUMAN
coref RESPOND- TO-R EQUEST- INFO- YN-1 .AGENT
ADJACENCY- PAIR default RESPOND- TO-R EQUEST- INFO- YN
coref RESPOND- TO-R EQUEST- INFO- YN-1
RESPOND- TO-R EQUEST- INFO- YN
AGENT sem HUMAN
coref REQUEST- INFO- YN-1 .BENEFICIARY
BENEFICIARY sem HUMAN
coref REQUEST- INFO- YN-1 .AGENT
ADJACENCY- PAIR- OF default REQUEST- INFO- YN
coref REQUEST- INFO- YN-1
We call semantically linked pairs of events like the one above scriptlets—
small, script- like structures— and they have some noteworthy features.
First, since people know such pairs of events, so, too, must LEIAs: X asks Y
a question → Y answers it; X tells Y a joke → Y laughs; X waves to Y → Y waves
back. Second, these event sequences are domain independent: no m atter
when or where somebody asks a question, the likely next move is for the
other person to answer it. Third, from the point of view of knowledge engi-
neering, it is useful to model typical sequences of events that are reusable
across domains and applications.
3.2.3 Proto- Instances
Proto- instances are a hybrid between an ontological concept and a con-
cept instance. Like concepts, they are generic and are a proper part of
the ontology. Like instances, they are more specific than basic ontologi-
cal descriptions in that certain property values are asserted. The need for
proto- instances becomes clear when we consider some of the applications
that agents can participate in. For example, simulation-b ased training sys-
tems offer trainees a large variety of practice cases that differ with res pect

64 Chapter 3
to salient feature values. Each case thus defined is a proto-i nstance that
can be instantiated time and time again by diff er ent trainees in diff er ent
simulation runs. As a concrete example, our M aryland Virtual Patient cli-
nician training application featured an inventory of virtual patients, each
of which was a proto- instance. In training systems, proto- instances allow
teachers to encapsulate dif fere nt teaching scenarios, such as a GERD patient
who will pro gress to adenocarcinoma if left untreated.
3.2.4 Scripts
Ontological scripts reco rd complex events along with their participants
and props.19 They can reflect knowledge in any domain— what happens
at a doctor’s appointment, how to build a chair, what to do at a four-w ay
stop; and they can be at any level of specificity—f rom a basic sequence
of events to the level of detail needed to generate a computer simulation.
Their descriptions include more expressive means than the simple frame
illustrated by SURGERY above. For example, scripts can require the corefer-
encing of arguments across events, they can have optional and variously
ordered events, they can require time management, and so on. Scripts can
be recorded by knowledge engineers, or they can be acquired by agents on
the fly.20
Scripts both guide agent operation and support their reasoning about
the world. Example (3.5) illustrates how script- based knowledge is needed
for making implicatures during language understanding.
(3.5) “How was your doctor’s appointment?” “ Great! The scale was broken!”
Why does the second speaker say the scale? What licenses the use of the,
considering that this object was not previously introduced into the dis-
course? The mention of a doctor’s appointment prepares the listener to
mentally access objects, like scale, and events, like getting weighed, that are
typically associated with a doctor’s appointment, making t hose objects and
events primed for inclusion in the situation model. In fact, the linguistic
licensing of the with scale is evidence that such script activation actually
takes place. Of course, it is script- based knowledge that also explains why
the person is happy— and it further allows us to infer the body type of the
speaker. If we want LEIAs to be able to reason at this level as well, then
scripts are the place to store the associated knowledge.

Knowledge Bases 65
When the knowledge in a script is used to guide agent action, the agent
must create an instance of it, which is called a plan. A plan differs from
a script in that (a) it selects a par ticu lar path through the often- variable
sequence of events permitted by the script and (b) it fills the events’ case
roles in par tic u lar ways.
The events and objects referred to in a script are, themselves, concepts
that are recorded in appropriate branches of the ontology. This means that
scripts are organized like well-c onstructed computer programs— not as a
massive main function but, rather, as hierarchically organized drilldowns of
scripts that ultimately end in singleton events or function calls.
We will describe scripts using the example of the AGENT- FUNCTIONING- FLOW
script that implements the agent’s cognitive architecture and makes the
agent self- aware so that it can explain its own functioning (cf. section 2.1).
This script uses the EVENTs and OBJECTs shown in the ontological subtrees
in t able 3.2, which we provide as a crib to be consulted when reading the
scripts themselves. This description of AGENT- FUNCTIONING- FLOW serves the
double duty of presenting an example of a script as an ontological entity
and describing an impor tant aspect of LEIA operation.
The top level of the AGENT- FUNCTIONING- FLOW script has five ordered subev-
ents that correlate with the architecture diagram in figure 2.1.21
AGENT- FUNCTIONING- FLOW
DEFINITION This script implements the LEIA’s cognitive architecture.
AGENT LEIA- 1
SUBEVENTS
1. PERCEPTION- RECOGNITION
2. PERCEPTION- INTERPRETATION
3. DELIBERATION
4. ACTION- SPECIFICATION
5. ACTION- RENDERING
All of the subevents are, themselves, scripts, which we w ill describe in turn.
The first one is PERCEPTION- RECOGNITION, whose function is described in its
definition field.
PERCEPTION- RECOGNITION
DEFINITION The agent determines which recognizer is needed to process a sig-
nal, runs it, and stores the resulting data.
AGENT LEIA
INPUT PERCEPTION- INPUT
OUTPUT PERCEIVED- DATA

66 Chapter 3
SUBEVENTS
TRY: recognize- text- input
EXPL “text input is recognized and stored as data”
TRY: recognize- speech
EXPL “speech input is recognized and stored as data”
TRY: recognize- visual- input
EXPL “visual input is recognized and stored as data”
TRY: recognize- interoception
EXPL “interoceptive input is recognized and stored as data”
The input to PERCEPTION- RECOGNITION is any kind of PERCEPTION- INPUT which,
as indicated by that concept’s subclasses in t able 3.2, currently includes
Table 3.2
The ontological subtrees of EVENTs and OBJECTs that are used in the AGENT- FUNCTIONING-
FLOW script.
EVENTs OBJECTs
AGENT- FUNCTIONING AGENT- SPECIFIC- OBJECTS
AGENT- FUNCTIONING- FLOW AGENT- COGNITION- TOOL
AGENT- PERCEPTION- EVENT INTEROCEPTION- PROCESSOR
PERCEPTION- RECOGNITION NLU- SYSTEM
PERCEPTION- INTERPRETATION VISION- PROCESSOR
INTEROCEPTION PERCEPTION- INPUT
NATURAL- LANGUAGE- UNDERSTANDING INTEROCEPTION- SIGNAL
VISION- INTERPRETATION SPEECH- SIGNAL
AGENT- REASONING- EVENT TEXT- INPUT
AGENT- PLANNING VISION- INPUT
MEMORY- MANAGEMENT PERCEIVED- DATA
DELIBERATION INTEROCEPTION- DATA
PROCESS- DAEMONS SPEECH- DATA
AGENT- ACTION- EVENT TEXT- DATA
ACTION- SPECIFICATION VISION- DATA
CONVERT- MMR- TO- GMR XMR ; meaning representation
CONVERT- MMR- TO- AMR AMR ; robotic action MR
CONVERT- MMR- TO- SMR GMR ; generation MR
RENDERING IMR ; interoception MR
GENERATE- GMR MMR ; mental MR
LAUNCH- ROBOTIC- EFFECTOR SMR ; simulated action MR
SIMULATE- PHYSICAL- ACTION TMR ; text MR
VMR ; vision MR

Knowledge Bases 67
interoception, speech, text, and vision. The output is the associated kind of
PERCEIVED- DATA, whose subclasses are also shown in the t able.
There are four subevents, which are actually conditions with diff er ent
preconditions that are evaluated in turn; this is the semantics of “TRY.” The
SUBEVENTS field says, “If this is text input, then do text-i nput recognition;
Else if this is speech input, then do speech- input recognition,” and so on.
These subevents are not concepts, they are pointers to code that carries out
the associated functions. Their status as pointers to code is indicated by the
lowercase font. Since they are not concepts, the agent cannot look up their
definitions to know what they mean and what they do. So, to enable the
agent to explain these actions, a metadata field called “EXPL” (explanation)
provides a short description.
Using concepts vs. procedure calls as subevents of scripts
A subevent of a script is recorded as a concept if:
a. it is, itself, a script; or
b. it is a non-d ecomposable event that has a freestanding status in the
ontology.
By contrast, a subevent of a script is recorded as a procedure call if:
a. it implements a procedure that is below the threshold of what the agent
needs to understand;
b. it implements a procedure that is not explainable because it is grounded in
machine learning; or
c. it implements a procedure that should eventually be described using a con-
cept but is temporarily being treated as an opaque function in order to
speed up the implementation of a par tic u lar system.
It is impor tant, methodologically, not to attempt to make every line of code
needed to implement LEIAs fully understood and explainable by them. This
would be an inefficient use of resources. Instead, agents should be self- aware
to a useful degree, and they should be prepared to explain their be hav ior in
useful ways.
When the agent instantiates PERCEPTION- RECOGNITION as a plan, that plan
reflects a specific path through the script, depending on which type of input
was recognized. If a language input was recognized, the agent launches
NATURAL-L ANGUAGE-U NDERSTANDING; if a visual input was recognized, the agent
launches VISION- INTERPRETATION; if a bodily sensation was recognized, the

68 Chapter 3
agent launches INTEROCEPTION; and so on for other perception modalities
that could be implemented.
PERCEPTION- INTERPRETATION
DEFINITION T he agent analyzes data into the appropriate type
of XMR.
AGENT LEIA
INPUT PERCEIVED- DATA from PERCEPTION- RECOGNITION.OUTPUT
OUTPUT XMR
INSTRUMENT AGENT- COGNITION- TOOL
SUBEVENTS
TRY: NATURAL-L ANGUAGE- UNDERSTANDING
TRY: VISION- INTERPRETATION
TRY: INTEROCEPTION
The OUTPUT of PERCEPTION- INTERPRETATION is some type of meaning repres en-
ta tion, an XMR, but the a ctual type depends on the channel of perception:
it might be a TMR, a VMR, an IMR, and so on. In describing the rest of the
script, we will not continue to highlight the distinction between the static
script descriptions that populate the ontology and the plans that an agent
dynamically generates, but this distinction should be kept in mind.
Once the agent has understood an input, it needs to decide what to do
in response to it. That is handled by the DELIBERATION script, which takes the
just- generated XMR (e.g., TMR, VMR) as input and outputs a m ental meaning
repre sen ta tion (MMR) that reco rds its decision about what to do.
DELIBERATION
DEFINITION The agent decides how to respond to an input.
AGENT LEIA
INPUT XMR from PERCEPTION- INTERPRETATION.OUTPUT
OUTPUT MMR
SUBEVENTS
TRY: r un- procedure-f rom- concept- in- XMR
EXPL “ The XMR contains a concept that, when instantiated, triggers a
par tic u lar response.”
EX “If someone yells ‘Fire!,’ the triggered response is to exit
the building.”
TRY: a ct- on- adjacency- pair
EXPL “ The XMR contains a concept that has an adjacency pair, which
indicates the default response type.”
EX “If the TMR includes REQUEST- INFO- WH, the adjacency pair is
RESPOND- TO-R EQUEST- INFO- WH; that is, the default response to a wh-
question is to answer it.”

Knowledge Bases 69
TRY: PROCESS- DAEMONS
TRY: c ontinue- plan-o n-a genda
EXPL “ The plan currently on agenda is continued.”
The first condition checks to see if the XMR contains any concepts whose
ontological descriptions indicate a necessary event in response. For exam-
ple, if a TMR includes the speech act WARN- OF- FIRE— which will be generated,
for example, by someone yelling “Fire!”— then this triggers the agent to exit
the building.
The second condition exploits the adjacency pairs recorded in the ontol-
ogy. As mentioned e arlier, adjacency pairs reflect typical sequences of events
that serve as an agent’s default response. For example, if X asks a question,
Y answers it; if X holds out his hand, Y shakes it; and so on. Adjacency pairs
drive dialog interactions, as illustrated in chapters 6–8.
The third condition is a script that checks if any of the agent’s daemons
are triggered by the XMR. A daemon is a procedure that is on agenda and is
available to be run any time its preconditions are fulfilled. If a daemon is
triggered, the agent decides what to do in response. For example, say the
agent is asked to decide whether to agree to a medical procedure and it
has a daemon on its agenda that requires it to know about the associated
pain of procedures before agreeing to them. If the agent does not know
how painful the procedure is, then it must find that out before making a
decision. This bit of pro cessing is formulated as a script (PROCESS- DAEMONS)
rather than a procedure call b ecause it has its own subevents and decision
functions.
The last condition covers the situation in which the latest input does not
require action. In this case, the agent continues to pursue whatever goal it
was pursuing prior to the last perceptual input.
DELIBERATION results in a m ental meaning repres ent at ion (MMR) that con-
tains the agent’s decision about what to do next but not yet how. For exam-
ple, if it was asked a yes-no question, the MMR might represent its intention
to convey a negative response, but there are vari ous ways it can do that, as
by speech, text, or body language. And, for each of t hese modalities, t here
are subsequent decisions to be made. For example, if the agent chooses
speech, how polite will the response be, and will the agent provide the
reason for it? If the agent chooses body language, then which gesture w ill it
use, and how emphatically will it enact that gesture? All of this is de cided in
the script called ACTION- SPECIFICATION, whose subevents refer to the specific

70 Chapter 3
types of target repres en ta tions that can be generated: GMRs for language
generation, AMRs for robotic action, or SMRs for simulated physical action.
ACTION- SPECIFICATION
DEFINITION The agent decides which type of action to use to convey the
MMR and carries out the reasoning to convert the MMR into
the associated type of XMR.
EXAMPLE If the agent wants to respond negatively to a yes/no question, it
has to decide whether to use language, body language, or both;
and once it has de cided, it has to rec ord that meaning/inten-
tion in a generation meaning repre sen tat ion (GMR), an action
meaning repre sen ta tion (AMR), or a simulated action meaning
repre sen ta tion (SMR).
AGENT LEIA
INPUT MMR from DELIBERATION.OUTPUT
OUTPUT XMR
SUBEVENTS
TRY: CONVERT- MMR- TO- GMR ; for language generation
TRY: CONVERT- MMR- TO- AMR ; for robotic action
TRY: CONVERT- MMR- TO- SMR ; for simulated action
The final stage of AGENT- FUNCTIONING- FLOW is ACTION- RENDERING, in which the
agent actually generates text, speech, physical action, or simulated action.
ACTION- RENDERING
DEFINITION The agent carries out the action represented in the action-
oriented XMR.
EXAMPLE If the agent decides to respond positively to a yes/no question
using language, it has to create a sentence to reflect the mean-
ing of the GMR.
AGENT LEIA
INPUT XMR from ACTION- SPECIFICATION.OUTPUT
OUTPUT EVENT
SUBEVENTS
TRY: LANGUAGE- GENERATION
TRY: ROBOTIC-A CTION
TRY: SIMULATED- ACTION
When the action involves language, ACTION- RENDERING includes creating the
actual sentence that will realize the meaning that was fully specified in
the GMR (see section 4.3 for details). When the action involves robotic or
simulated action, ACTION- RENDERING involves creating the signals to pass to
the associated effectors.

Knowledge Bases 71
Let us recap some import ant points about scripts.
• Scripts can be recorded by knowledge engineers, or they can be learned
by agents during their operation.
• Scripts neatly open up into subscripts, which o rganizes knowledge
repre sen ta tion.
• Scripts are as concept- based and explainable as pos si ble but as stream-
lined and program-b ased as necessary. It would be a poor use of time to
attempt to make every line of code that implements agent action fully
explainable by the agent.
• When a script is instantiated as a plan, it reflects a specific path through
the script and requires such t hings as handling coreferences of partici-
pants and props across multiple events.
• Like all of the agent’s knowledge, scripts are fully inspectable and modi-
fiable over time.
• When scripts are acquired by knowledge engineers, this can involve col-
laboration by system engineers (cf. section 2.5.2). This is particularly
impor tant for scripts that contain a significant amount of unexplainable
code, such as those involving time management in simulation.
• Whereas more straightforward scripts can be learned by agents, t hose that
reflect the mental models of domain experts are most efficiently modeled
by knowledge engineers collaborating with t hose experts (see section 9.2).
However, agents can automatically update such models, as by learning
about new therapies for an already- modeled disease from the lit er a ture.22
• Agents can explain scripts based on:
– their understanding of the basic shapes of scripts:
Numbered events occur in order, conditions (introduced by TRY)
are ordered if- then statements, and so on. We did not pres ent all
script- related conventions here since that would be excessive detail
for non- developers;
– the natur al language definitions of the concepts that comprise a script:
Agents can use definitions directly in explanations or they can
semantically analyze them as part of a more reasoning-h eavy expla-
nation process. Definitions might be missing for scripts that agents
learn without the involvement of language;

72 Chapter 3
– if applicable, the natural- language examples in the EXAMPLE field of
the concepts that comprise a script; and
– the “EXPL” and/or “EX” fields of procedure calls in scripts.
Later chapters w ill provide more examples of scripts.
3.3 The Lexicon
The lexicon contains linked syntactic and ontological-s emantic descrip-
tions of words and constructions, with the latter covering any combination
of words and/or linguistically constrained variables. To start with a s imple
example, the construction someone feeds someone—in the meaning “some-
one gives food to someone”—is recorded in the LEIA’s lexicon as the first
verbal sense of feed, called feed-v 1.
feed- v1
definition Someone gives food to someone
example Jane fed Fido.
comments A dif fere nt sense covers the ditransitive construction:
Jane fed Fido a steak.
syntax- type v- trans
output- syntax CL
syn- struc
subject $var1
v $var0
directobject $var2
sem- struc
FEED
AGENT ^$var1
BENEFICIARY ^$var2
The definition, example, and comments zones of lexical senses contain
human- oriented annotations. The syntax- type zone indicates the syntactic
construction used in the entry: here, a transitive verb. The output- syntax
zone indicates the syntactic function of the construction overall: h ere, a
clause.
The syntactic structure (syn- struc) zone lists the minimal syntactic require-
ments of the given construction, including the d ependency structure, mor-
phological constraints on constituents, and required lexemes, such as the
required words in idiomatic expressions. Since feed-v 1 is a transitive verb

Knowledge Bases 73
sense, its minimal requirements are the subject, the verb, and the direct
object. They are listed in the correct order for the most basic syntactic
realization— the active voice.
The semantic structure (sem- struc) zone expresses the meaning of the con-
struction in terms of ontological concepts, which are written in small caps.
This sem- struc is headed by the concept FEED. The carets (^) indicate “the
meaning of.” So, the AGENT slot is filled by the meaning of the subject, and
the BENEFICIARY slot is filled by the meaning of the direct object. The mean-
ing of t hese arguments can only be computed when an actual input sen-
tence offers words or phrases to fill the variables $var1 and $var2.
Lexical senses can also include synonyms and hyponyms zones. It is func-
tionally equivalent to reco rd a synonym in its own entry or in the syn-
onyms zone of a dif fer ent entry. As for hyponyms, it is more informative to
rec ord a word in the hyponyms zone of another word than as its own entry
because this asserts that the word refers to a subtype of the listed concept.
For example, if pug is recorded as a hyponym in dog-n 1, this makes it clear
that pug is a kind of dog. If, by contrast, pug were to be recorded in its own
sense— pug- n1 mapped to DOG— then there would be no way for the agent
to know that pug is not a generic term for DOG.
The final zone that is needed for some lexical senses is called meaning-
procedures. It contains calls to procedural semantic routines that e ither
supplement sem- struc descriptions or are fully responsible for the semantic
interpretation. An example for which a meaning procedure supplements a
sem-s truc description is the pronoun she. The sem-s truc says that she means
“ HUMAN (GENDER female),” and the meaning procedure is needed to identify
which female human in the context is being referred to. An example for
which a meaning procedure is wholly responsible for the semantic analy sis is
the adverb respectively, as used in Bears and horses like honey and carrots, respec-
tively. This meaning procedure must account for the fact that what actually
needs to be semantically analyzed is Bears like honey and horses like carrots.
Below is the text meaning repres en ta tion (TMR) for the sentence Grand-
father fed the dog, which is analyzed using feed- v1.
FEED-1
AGENT GRANDPARENT-1
BENEFICIARY DOG-1
TIME < find- anchor- time
lex- sense feed- v1

74 Chapter 3
GRANDPARENT-1
HAS- GENDER
male23
lex- sense grandfather- n1
DOG-1
COREF seek- sponsor
lex- sense dog- n1
uses- sense the- det1
The first frame of the meaning repres en ta tion naturally looks very similar
to the sem-s truc of feed-v 1, which served as the scaffolding for this analys is.
Table 3.3 illustrates this parallelism.
Lexical senses for the other words similarly account for their mean-
ings: grand father and dog are plain nouns that are described as “GRANDPAR-
ENT (HAS- GENDER male)” in the sense grandfather- n1 and “DOG” in the sense
dog-n 1. The sense for the determiner the indicates that, syntactically, it col-
locates with a noun and, semantically, it does not have any static meaning;
instead, it triggers the procedural semantic routine seek- sponsor, which will
later attempt to track down its function in the context.24 The inclusion of
a function call indicates that this is not a final TMR; it is the result of an
intermediate stage of proc essing.
Although lexical senses can describe constructions of any form and
complexity, the majority reflect standard shapes on both the syntactic and
semantic sides. Beginning with syntax, over ninety standard syntactic tem-
plates are currently used, whose names fill the syntax- type zone of lexical
senses. In feed- v1, the syntax-t ype is v-t rans. T able 3.4 shows some addi-
tional examples, and the full current list is available in the online appendix.
There are two benefits to asserting syntax types in lexical senses. First, sys-
tem testing can be selective. If random examples of a part ic u lar syntax type
are proc essed correctly, then all examples of that type are expected to work
properly—a part from idiosyncratic errors thrown by the data- driven parser.
Table 3.3
The sem- struc descriptions in lexical senses provide the scaffolding for TMRs.
Lexicon TMR
FEED FEED-1
AGENT ^$var1 AGENT GRANDPARENT- 1
BENEFICIARY ^$var2 BENEFICIARY DOG-1

Knowledge Bases 75
Table 3.4
Examples of standard syntax types used in a LEIA’s lexicon.
Output
Sense Syntax Type Constituents Syntax Example
refrigerator- n1 n- bare Noun N refrigerator
sleep- v1 v- intrans Subj sleep CL Lulu slept.
V
give- v2 v- ditrans Subj give IndirectObj CL Lulu gave her
V
DirectObj dog a treat.
nice- adj2 adj- plain nice Noun N nice weather
ADJ
Second, the named syntax types can be used as parameters in rules for pro-
cessing syntactic transformations such as passivization (see section 4.2.2).
All lexical senses are also labeled with their output- syntax, which is the
type of constituent they create. For example, since adjectives are described
in conjunction with the noun they modify, their output-s yntax is N (noun);
and since verbs are described with their arguments, their output-s yntax is
CL (clause). The value of output- syntax asserts how the given lexical sense
can participate in larger constructions.
Many standard constructions include optional ele ments such as optional
arguments (e.g., the direct object of read) and adjuncts. Adjuncts are listed
in lexical senses when they are particularly common and when listing them
will help in disambiguation. For example, many adjuncts are headed by
prepositions, which are multiply ambiguous. Asserting what they mean in
a par tic ul ar construction is not only helpful; we think it mimics p eople’s
knowledge of constructions. For example, the “fasten” sense of the verb
secure is often used with a prepositional phrase headed by with to express
the INSTRUMENT: Fred secured the tent with stakes.25 Adding such information
to lexical senses boosts the agent’s power of disambiguation. This is a good
example of a low- cost, high- payoff strategy in the overall process of knowl-
edge acquisition (cf. chapter 9).
There are also nonstandard constructions, whose value for output-
syntax is atypical. They can include any number and type of ordered con-
stituents. For example, the semantically vacuous expression “The thing is,
is that Clause” is recorded in the lexicon as this specific sequence of words
followed by a clause of any shape. Nonstandard syntactic constructions can
have many diff er ent kinds of output-s yntax. They need to be tested sepa-
rately to determine how they will be treated by the parser.

76 Chapter 3
The tidy inventory of syntactic construction types in the lexicon belies
the massive complexity of language that must be handled during language
understanding. For example, any construction that includes a noun phrase
needs to accommodate any shape of noun phrase, such as:
• a car
• a nice, expensive car
• my friend’s nice, expensive car
• my friend’s nice, expensive car that she got from her parents as a gradu-
ation pre sent
• my friend’s nice, expensive car that she got from her parents as a gradu-
ate pre sent and has been driving to the beach every day all summer.
The lexicon includes only most basic uses of words, such as the active
forms of verbs and the attributive uses of adjectives. This is sufficient b ecause
the language analyzer can h andle generativity using a model of transfor-
mation pro cessing that is psychologically plausible and computationally
practical—as explained in section 4.2.2. This generative approach offers
practical benefits in terms of knowledge acquisition and maintenance:
• Most words have multiple senses, defined as part ic u lar correlations of syn-
tactic and semantic ele ments. Light verbs, such as have, take, and make,
have dozens of senses each. If all of t hese senses were listed in all of their
pos si ble shapes— including passive, imperative, and participating in every
type of question— the size of the lexicon would increase dramatically.
• Non- basic uses of constructions can combine, leading to further com-
binatorial explosion. For example, Fido, he was fed by the girl who was
recently hired as his dog sitter involves subject dislocation, passivization,
and a relative clause construction.
• If all of these non- basic uses and combinations thereof were listed
explic itly, then every time a lexical sense was edited, all of the associ-
ated senses would need to be edited. This w ill not be a rare occurrence
as the ontology grows over time. For example, if a knowledge engineer
decides to split a more coarse- grained concept, like RUN, into multiple
children, like JOG and SPRINT, then all associated lexical senses w ill need
to be remapped: jog-v 1 will remap from RUN to JOG, sprint- v1 will remap
from RUN to SPRINT, and so on.

Knowledge Bases 77
So far, we have discussed the syntactic side of lexical descriptions. Turn-
ing to semantics, descriptions of word senses also have more and less typi-
cal forms. T able 3.5 shows some typical forms of sem- strucs.
Although there are many typical shapes of sem- strucs, it is not prac-
tical to try to list them, nor is it needed. (Recall that the main reasons
for formally classifying syn- strucs were (a) to align them with the possibly
unpredictable output of the external parser and (b) to anticipate how con-
structions can interact with each other.) Instead, it is better to conceptual-
ize semantic descriptions as a generative process. At the highest level, the
legal form and content of sem- struc descriptions is as follows:
• They can include any number of frames.
• Each frame can be headed by a concept, a variable, or a set indicator.26
• Each frame can include any properties that are appropriate for its head
type.
• Property fillers can, themselves, be frames; that is, constituents can be
nested.
• The sem- struc zone of a lexical sense can be empty. In some cases, this
is because a word has no meaning—as for the disfluency markers uh and
Table 3.5
Examples of typical sem- struc zones of lexical senses in a LEIA’s lexicon.
Description Sense Example of Sem- Struc
Concept refrigerator- n1 REFRIGERATOR
Concept with one property sleep- v1 SLEEP
EXPERIENCER ^$var1
Concept with two properties throw- v1 THROW
AGENT ^$var1
THEME ^$var2
Variable with one property blue- adj1 ^$var1
COLOR blue
Multiple frames of the any type must- v1 MODALITY
TYPE OBLIGATIVE
VALUE 1
SCOPE ^$var2
^$var2
AGENT ^$var1

78 Chapter 3
er. In other cases, an empty sem-s truc reflects the fact that the entity has
no static meaning. As mentioned e arlier, the adverb respectively in inputs
like Bears and horses like honey and carrots, respectively triggers a procedure
that recasts the sentence as the meaning of Bears like honey and horses like
carrots. So, the entire semantic interpretation of the word respectively is
procedural.
The LEIA’s English lexicon currently contains around fifteen thousand
senses using the simplest counting method: the number of listed senses
(e.g., feed- v1, perform- v6). However, the actual coverage of the lexicon is
much greater because simple counting does not account for:
• the large number of synonyms and hyponyms recorded in lexical senses;
• the se lection or non- selection of optional elem ents;
• transformations, and combinations thereof, that make the lexicon
generative;
• the productive handling of numbers and named entities; and
• lexicon- wide pro cesses of derivational morphology.
Our point in citing a number at all is to show that we are trying to funda-
mentally solve the probl ems of natur al language understanding and gen-
eration, and this requires handling lexical ambiguity and paraphrase. So,
although the LEIA’s lexicon currently contains nowhere near human-l evel
lexical knowledge, it includes extensive polysemy and synonymy, which
creates a rigorous testbed for the agent’s natu ral language understanding
and generation systems.27
Although most of our recent work has involved English, both the
approach and much of the knowledge substrate— even the lion’s share of
the lexicon— are language- independent. The reason why LEIA-s tyle lexi-
cons can be ported across languages is because the most difficult part of
lexical acquisition is describing semantics, both static (recorded in the
sem- struc zone) and procedural (recorded as function calls in the meaning-
procedures zone). So, creating a lexicon of French or R ussian from the exist-
ing English one primarily involves changing the words used to convey the
given meaning. If any syntactic or semantic tweaks are needed, they are
typically quick and s imple.28 It is noteworthy, in this regard, that the the-
ory of Ontological Semantics that underpins LEIA language pro cessing has
its roots in interlingual machine translation.29 Section 5.4 gives a taste of

Knowledge Bases 79
the crosslinguistic applicability of our approach to language understanding
using evidence from Russian.
3.4 The Opticon and Analogous [Sense]icons
Just as the lexicon supports the translation of language inputs into onto-
logical concepts, so, too, must analogous knowledge bases for other chan-
nels of perception. To date, we have worked only with an opticon, but it is
straightforward to apply the approach to a hapticon (for touch), olfacticon
(for smells), physiocon (for sensor- detectable features of human physiol-
ogy), and so on.30 Focusing on the opticon, the entry for any object, event,
or scene includes:
• a head that is a set of one or more visual repre sen ta tions (static images or
video clips) that serve as exemplars;
• a visual repre sen ta tion of the components of the object, event, or scene,
along with their spatial relations and links to the components’ own opti-
con entries;
• a meaning procedure that helps the agent to recognize the object, event,
or scene and its parts; and
• a meaning procedure that helps the agent to recognize the individual
optical features that distinguish the object, event or scene.31
Whereas it is self- evident why an embodied agent would need to be
able to detect things like a stop sign (using vision), a red-h ot surface (using
touch), or something burning (using smell), the utility of physiological fea-
ture detection deserves further comment.
Human p erformance on a task can be affected by the person’s physi-
cal, emotional, and cognitive states. When h umans collaborate with each
other, they naturally respond to behavioral manifestations of such states:
for example, teachers give hints to students who are frustrated, workers
lend a hand to teammates who are exhausted, and supervisors offer reas-
surance to subordinates who are overwhelmed. In order for agents to serve
as reliable collaborators, they, too, must be able to detect and appropriately
respond to people’s physical, emotional, and cognitive states.
Human be hav ior research has discovered correlations between measurable
physiological features— such as heart rate variability, electrodermal activity,
pupil size, and eye movements— and states such as arousal, engagement,

80 Chapter 3
stress, fear, m ental effort, and physical exertion.32 Making use of such fea-
tures in cognitive systems involves:
• developing a physicon that maps sensor outputs to ontologically grounded
feature values;
• developing a dedicated recognition module that perceives physiological
inputs and interprets them according to the physiocon;
• developing a dedicated interpretation module that contextually inter-
prets physiological features in terms of people’s physical, emotional, and
cognitive states: for example, in a given context, increased heart rate
might be explained by stress, physical exertion, or exposure to heat; and
• developing reasoning functions that guide the agent in responding to
dif fer ent human states depending on a large number of features of the
context including the respective roles that the human and agent are
playing, the type of application, the application domain, and so on.
Returning to the overall topic of this section, just as LEIAs need a lexicon
to map between language and ontologically grounded meanings, they need
analogous knowledge bases to map between other channels of input and
ontologically grounded meanings. It is these meanings that agents use as
input for reasoning about action.
3.5 Episodic Memory
Episodic memory includes stored information about instances (exemplars)
of ontological concepts as well as meaning repre sent at ions that the agent
generates during its operation. Episodic knowledge structures include time-
stamps, provenance, and other relevant metadata.
The agent’s episodic memory is divided into spaces, which is a com-
mon practice in memory management. Memory spaces allow the agent to
rapidly access sets of known instances that share a common category or
purpose. For example, one part of an agent’s episodic memory contains a
fact repository of the agent’s beliefs about entities it knows—f or example,
the capital of Belgium and the hair color of its h uman collaborator Ben.
Another part of the agent’s episodic memory contains information about
its past successes and failures at carryi ng out a part ic u lar kind of plan (recall
that plans are instances of ontological scripts). Memories of plans allow
the agent to, in certain cases, bypass detailed decision-m aking about action

Knowledge Bases 81
and, instead, carry out a reflexive action. Specifically, when the agent needs
to decide which plan to use to achieve a goal, it can search its episodic
memory for past cases when par tic u lar plans successfully achieved the goal.
It can then compare its current situation model to the situation models
associated with the successful plans and select the best match. The agent
can then instantiate another copy of that plan in anticipation that it w ill
work as well as the last time. This kind of operation is an example of case-
based reasoning.
The content of the agent’s episodic memory is made available to all
reasoning heuristics throughout the system, allowing any algorithm to
inspect what the agent knows, what it has recently encountered, what it
is currently thinking about, and what is on its agenda. As with ontological
knowledge, episodic memory is indexed in a variety of ways—by relevant
domain space, but also by type, timestamp, and more. Operations devoted
to consolidation and other updates of the episodic memory, as well as the
way the agents model forgetting, are outside the scope of this book.
