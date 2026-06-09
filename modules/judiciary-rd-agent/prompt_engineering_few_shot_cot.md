Few-shot Learning and Chain of Thought
58
6.3 - Approaches to Few-Shot Learning
There are different approaches to few-shot learning, and they include
using:
6.3.1 - Prior Knowledge about Similarity
During training, we develop embeddings that can distinguish between
different classes, even if they haven’t been seen before.
Think of this like teaching an AI to recognize the difference between cats
and dogs by showing it many pictures. Even if later it sees a breed of cat or
dog it hasn’t seen before, it can still guess correctly because it has learned
the general idea of what makes a cat different from a dog. This is a bit like
a game where you match similar items, and the AI gets better at it over
time.
6.3.2 - Prior Knowledge about Learning
We leverage pre-existing knowledge to guide the learning algorithm in
selecting parameters that not only fit the data well but also generalize
effectively. This helps in preventing overfitting, especially when working
with limited data.
Imagine you’re teaching someone to ride a scooter. Instead of starting from
scratch, if they’ve ridden a bike before, you’d use that knowledge to help
them learn faster. Similarly, when teaching an AI, we use what it already
knows to help it learn new things without making common mistakes.
6.3.3 - Prior Knowledge of Data
By harnessing our understanding of the data’s inherent structure and
variations, we can effectively train AI even when provided with only
a handful of examples. This knowledge acts as a foundation for more
efficient learning.


Few-shot Learning and Chain of Thought
59
Let’s say you’re trying to teach someone about different types of fruits. If
they already know about apples and oranges, you can use that knowledge
to explain a tangerine (it’s like a small orange!). Similarly, when teaching
an AI, if it knows a bit about the type of information (or data) you’re giving
it, it can learn new things more easily.
6.4 - Examples of Few-Shot Learning
Let’s start with this simple example:
import os
import openai
import click
openai.api_key = os.getenv("OPENAI_API_KEY")
@click.command()
def chat_with_felix():
"""Chat with Felix, the chatbot."""
print("Felix: Hi there. I am Felix, the chatbot. Let's play a game.\
Give me a number and I'll tell you if it's even or odd.")
while True:
message = input("You: ")
if message.lower() in ['exit', 'quit']:
print("Felix: Goodbye!")
break
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a smart and help\
ful assistant."},


Few-shot Learning and Chain of Thought
60
{"role": "user", "content": "1"},
{"role": "assistant", "content": "1 is an odd number be\
cause it is not divisible by 2."},
{"role": "user", "content": "2"},
{"role": "assistant", "content": "2 is an even number b\
ecause it is divisible by 2."},
{"role": "user", "content": "3"},
{"role": "assistant", "content": "3 is an odd number be\
cause it is not divisible by 2."},
{"role": "user", "content": f"{message}"},
],
temperature=1,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
try:
print("Felix:", response.choices[0].message.content)
except:
print("Felix: Sorry, a problem occurred. Please try again l\
ater.")
if __name__ == '__main__':
chat_with_felix()
Interacting with the AI:


Few-shot Learning and Chain of Thought
61
Felix: Hi there. I am Felix, the chatbot. Let's play a game. Give me a \
number and I'll tell you if it's even or odd.
You: 6
exitFelix: 6 is an even number because it is divisible by 2.
You:
Felix: Goodbye!
In this example, we are using a few-shot learning technique to teach the AI
to recognize even and odd numbers and answer accordingly in a custom
way.
Another example is the following:
import os
import openai
import click
openai.api_key = os.getenv("OPENAI_API_KEY")
@click.command()
def chat_with_felix():
"""Chat with Felix, the chatbot."""
print("Felix: Hi there. I am Felix, the chatbot. Let's play a game.\
Name an animal, and I'll tell you if it's a mammal or not.")
while True:
message = input("You: ")
if message.lower() in ['exit', 'quit']:
print("Felix: Goodbye!")
break
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a smart and help\


Few-shot Learning and Chain of Thought
62
ful assistant."},
{"role": "user", "content": "dog"},
{"role": "assistant", "content": "A dog is a mammal bec\
ause it gives birth to live young and has fur."},
{"role": "user", "content": "fish"},
{"role": "assistant", "content": "A fish is not a mamma\
l because it lays eggs and lives in water."},
{"role": "user", "content": f"{message}"},
],
temperature=1,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
try:
print("Felix:", response.choices[0].message.content)
except:
print("Felix: Sorry, a problem occurred. Please try again l\
ater.")
if __name__ == '__main__':
chat_with_felix()
Interacting with the AI:


Few-shot Learning and Chain of Thought
63
Felix: Hi there. I am Felix, the chatbot. Let's play a game. Name an an\
imal, and I'll tell you if it's a mammal or not.
You: cow
Felix: A cow is also a mammal. It is a large domesticated ungulate anim\
al that is raised as livestock for meat, milk, and other dairy products
. Cows give birth to live young and produce milk to feed their offsprin
g.
You: Exit
Felix: Goodbye!
6.5 - Limitations of Few-Shot Learning
Let’s consider an example where we want the AI to answer with “X” if the
input is an odd number and “Y” if the input is an even number. We can use
the following code that uses a few-shot learning technique:
import os
import openai
import click
openai.api_key = os.getenv("OPENAI_API_KEY")
@click.command()
def chat_with_felix():
"""Chat with Felix, the chatbot."""
print("Felix: Hi there. I am Felix, the chatbot. Let's play a game.\
")
while True:
message = input("You: ")
if message.lower() in ['exit', 'quit']:
print("Felix: Goodbye!")
break


Few-shot Learning and Chain of Thought
64
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a smart and help\
ful assistant."},
{"role": "user", "content": "1"},
{"role": "assistant", "content": "X"},
{"role": "user", "content": "2"},
{"role": "assistant", "content": "Y"},
{"role": "user", "content": f"{message}"},
],
temperature=1,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
try:
print("Felix:", response.choices[0].message.content)
except:
print("Felix: Sorry, a problem occurred. Please try again l\
ater.")
if __name__ == '__main__':
chat_with_felix()
This is an execution example:


Few-shot Learning and Chain of Thought
65
Felix: Hi there. I am Felix, the chatbot. Let's play a game.
You: 1
Felix: X
You: 2
Felix: I'm sorry, but I'm not sure what you're referring to with "2." C\
ould you please provide more context or clarify your question?
You: 3
Felix: Z
You: 4
Felix: Z
You: 5
Felix: Z
This is not the expected behavior! In order to solve this problem, we can
use a different prompt, such as the following:
import os
import openai
import click
openai.api_key = os.getenv("OPENAI_API_KEY")
@click.command()
def chat_with_felix():
"""Chat with Felix, the chatbot."""
print("Felix: Hi there. I am Felix, the chatbot. Let's play a game.\
")
while True:
message = input("You: ")
if message.lower() in ['exit', 'quit']:
print("Felix: Goodbye!")
break
response = openai.ChatCompletion.create(


Few-shot Learning and Chain of Thought
66
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a smart and help\
ful assistant."},
{"role": "user", "content": "1"},
{"role": "assistant", "content": "1 is an odd number so\
the answer is X."},
{"role": "user", "content": "2"},
{"role": "assistant", "content": "2 is an even number s\
o the answer is Y."},
{"role": "user", "content": "3"},
{"role": "assistant", "content": "3 is an odd number so\
the answer is X."},
{"role": "user", "content": f"{message}"},
],
temperature=1,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
try:
print("Felix:", response.choices[0].message.content)
except:
print("Felix: Sorry, a problem occurred. Please try again l\
ater.")
if __name__ == '__main__':
chat_with_felix()
This is an execution example:


Few-shot Learning and Chain of Thought
67
Felix: Hi there. I am Felix, the chatbot. Let's play a game.
You: 10
Felix: 10 is an even number so the answer is Y.
You: 22
Felix: 22 is an even number so the answer is Y.
You: 44
Felix: 44 is an even number so the answer is Y.
You: 12
Felix: 12 is an even number so the answer is Y.
You: 13
Felix: 13 is an odd number so the answer is X.
You: 19
Felix: 19 is an odd number so the answer is X.
This is the expected behavior.
What we did to solve the problem was to provide a reasoning for the
answer. This is a common technique used in few-shot learning to bypass
some of the few-shot learning limitations. The few-shot learning technique
can return incorrect answers if the prompt is complex. By providing a
reasoning for the answer, or what we call a “Chain of Thoughts”, we can
help the AI to understand the problem better and provide the correct
answer.


7 - Chain of Thought (CoT)
According to “When do you need Chain-of-Thought Prompting for
ChatGPT?31” (Chen, J., Chen, L., Huang, H., & Zhou, T. (2023)), simply
adding a CoT instruction can improve GPT-3’s accuracy from 17.7% to
78.7%. This is a significant improvement, but not every query requires a
CoT instruction.
In fact, a CoT instruction is only necessary when the query is complex and
the AI needs more information to understand the problem.
CoT is a technique that allows us to provide reasoning for the answer. This
technique is used in combination with few-shot learning to bypass some of
the limitations of few-shot learning.
Consider this example:
import os
import openai
import click
openai.api_key = os.getenv("OPENAI_API_KEY")
@click.command()
def chat_with_felix():
"""Chat with Felix, the chatbot."""
print("Felix: Hi there. I am Felix, the chatbot. Let's play a game.\
")
while True:
message = input("You: ")
if message.lower() in ['exit', 'quit']:
31https://arxiv.org/abs/2304.03262


Chain of Thought (CoT)
69
print("Felix: Goodbye!")
break
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a smart and help\
ful assistant."},
{"role": "user", "content": f"{message}"},
],
temperature=1,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
try:
print("Felix:", response.choices[0].message.content)
except:
print("Felix: Sorry, a problem occurred. Please try again l\
ater.")
if __name__ == '__main__':
chat_with_felix()
Then ask the following question:
When James was 2 years old, his sister was 2*2 years old. James is now \
30 years old. How old is his sister?
This is how the dialog looks like:


Chain of Thought (CoT)
70
Felix: Hi there. I am Felix, the chatbot. Let's play a game.
You: When James was 2 years old, his sister was 2*2 years old. James is\
now 30 years old. How old is his sister?
Felix: If James was 2 years old, then his sister was 2*2 = 4 years old.
Since James is now 30 years old, his sister would be 30 - 2 = 28 years \
old.
As you can see, the answer is partially correct, which means that gpt-3.5-
turbo was able to understand the age difference but didn’t guess the correct
age of the sister.
Even after asking a different question, the answer is still incorrect:
Felix: Hi there. I am Felix, the chatbot. Let's play a game.
You: When Harry was 25 years old, his sister was 29 years old. Harry is\
now 30 years old. How old is his sister?
Felix: If Harry is now 30 years old, then his sister is 29 years old, a\
ssuming their age difference remains constant.
A CoT instruction should improve the answer.
import os
import openai
import click
openai.api_key = os.getenv("OPENAI_API_KEY")
@click.command()
def chat_with_felix():
"""Chat with Felix, the chatbot."""
print("Felix: Hi there. I am Felix, the chatbot. Let's play a game.\
")
while True:
message = input("You: ")


Chain of Thought (CoT)
71
if message.lower() in ['exit', 'quit']:
print("Felix: Goodbye!")
break
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a smart and help\
ful assistant."},
{"role": "user", "content": "When James was 2 years old\
, his sister was 2*2 years old. James is now 30 years old. How old is h
is sister?"},
{"role": "assistant", "content": "When James was 2 year\
s old, his sister was 4 years old. There's 2 year differences between t
hem and the sister is older than James. When James is 30 years old, his
sister should be 32 years old."},
{"role": "user", "content": "When Harry was 25 years ol\
d, his sister was 29 years old. Harry is now 30 years old. How old is h
is sister?"},
{"role": "assistant", "content": "When Harry was 25 yea\
rs old, his sister was 29 years old. There's 4 year differences between
them and the sister is older than Harry. When Harry is 30 years old, h
is sister should be 34 years old."},
{"role": "user", "content": f"{message}"},
],
temperature=1,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
try:
print("Felix:", response.choices[0].message.content)
except:
print("Felix: Sorry, a problem occurred. Please try again l\


Chain of Thought (CoT)
72
ater.")
if __name__ == '__main__':
chat_with_felix()
When asked the following question, the answer was correct:
Felix: Hi there. I am Felix, the chatbot. Let's play a game.
You: When James was 50 years old, his sister was 50/2 years old. James \
is now 100 years old. How old is his sister?
Felix: When James was 50 years old, his sister was 50/2 years old, whic\
h is 25 years old. There's a 25-year difference between them and the si
ster is younger than James.
Now that James is 100 years old, his sister would be 100 - 25 = 75 year\
s old.
Another question to test the CoT instruction:
Felix: Hi there. I am Felix, the chatbot. Let's play a game.
You: When James was 10 years old, his sister was 10*3 years old. James \
is now 30 years old. How old is his sister?
Felix: When James was 10 years old, his sister was 10*3 = 30 years old.
Since then, the age difference between them remains the same.
Therefore, if James is now 30 years old, his sister would be 30 + (30-1\
0) = 50 years old.
Asked without any CoT instruction, the answer was incorrect:
Felix: Hi there. I am Felix, the chatbot. Let's play a game.
You: When James was 10 years old, his sister was 10*3 years old. James \
is now 30 years old. How old is his sister?
Felix: When James was 10 years old, his sister was 10*3 = 30 years old.\
This age difference of 30 years remains constant over time. Since Jame
s is now 30 years old, his sister would be 30 + 30 = 60 years old.


Chain of Thought (CoT)
73
Certain problems, such as symbolic and arithmetic reasoning, are complex
for AI models like GPT. These problems often require a Chain-of-Thought
(CoT) instruction to assist the model in better understanding the problem.
This is because the model fundamentally lacks an understanding of the
problem’s nature and attempts to guess the answer based on its generative
capabilities, not logic.
In our example, the CoT allowed the model to break down a problem into
steps that are easier to understand. Think of this as a transparent box that
enables the model to see what’s inside and comprehend the reasoning
behind the answer.
The authors of “Chain-of-Thought Prompting Elicits Reasoning in Large
Language Models32” (Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter,
B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022)) explored the use of the CoT
method to improve the reasoning capabilities of large language models.
They showed that when large models are provided with a few examples of
this method, they naturally enhance their reasoning abilities. Tests on three
major language models revealed that this approach improves performance
in arithmetic, commonsense, and symbolic reasoning tasks. Notably, by us-
ing only eight examples of this method, a 540B-parameter language model
achieved top accuracy on the GSM8K33 math word problem benchmark,
surpassing even a specialized GPT-3 model.
32https://arxiv.org/abs/2201.11903
33https://paperswithcode.com/dataset/gsm8k


8 - Zero-shot CoT Prompting
Sometimes, you might not want or simply can’t provide examples for a CoT
instruction. In this case, zero-shot CoT prompting could be an alternative.
Let’s try this code where we don’t provide any examples for the CoT
instruction:
import os
import openai
import click
openai.api_key = os.getenv("OPENAI_API_KEY")
@click.command()
def chat_with_felix():
"""Chat with Felix, the chatbot."""
print("Felix: Hi there. I am Felix, the chatbot. Let's play a game.\
")
while True:
message = input("You: ")
if message.lower() in ['exit', 'quit']:
print("Felix: Goodbye!")
break
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a smart and help\
ful assistant."},
{"role": "user", "content": f"{message}"},


Zero-shot CoT Prompting
75
],
temperature=1,
max_tokens=256,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)
try:
print("Felix:", response.choices[0].message.content)
except:
print("Felix: Sorry, a problem occurred. Please try again l\
ater.")
if __name__ == '__main__':
chat_with_felix()
Now, this is the instruction that uses the zero-shot CoT prompting tech-
nique:
When James was 2 years old, his sister was 2*2 years old. James is now \
30 years old. How old is his sister? Think step by step (who's older, t
he age difference..etc)
As you can see, we added the following Think step by step (who's
older, the age difference, etc.) at the end of the question. This is
how the dialog looks like:


Zero-shot CoT Prompting
76
Felix: Hi there. I am Felix, the chatbot. Let's play a game.
You: When James was 2 years old, his sister was 2*2 years old. James is\
now 30 years old. How old is his sister? Think step by step (who's old
er, the age difference..etc)
Felix: To find out how old James's sister is, we can work through the p\
roblem step by step:
1. When James was 2 years old, his sister was 2 * 2 years old, which me\
ans his sister was 4 years old at that time.
2. This implies that James's sister is two years older than him, as she\
was 4 years old when he was 2 years old.
3. Since James is now 30 years old, we need to account for the age diff\
erence of two years between him and his sister.
4. To calculate his sister's current age, we add the age difference to \
James's age: 30 + 2 = 32.
Therefore, James's sister is 32 years old.
Surprisingly, the answer is correct, and the CoT instruction helped the
model to understand that breaking the problem into smaller steps while
taking into consideration the age difference is the right approach to solve
the problem.
This approach was introduced in the paper “Large Language Models are
Zero-Shot Reasoners34” (Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., &
Iwasawa, Y. (2022)). While LLMs are praised for their few-shot learning,
the authors of this paper discovered that these models can also reason
without any prior examples (zero-shot) by simply prompting them to
“think step by step.”
We show that LLMs are decent zero-shot reasoners by simply
adding “Let’s think step by step” before each answer.
34https://arxiv.org/abs/2205.11916


Zero-shot CoT Prompting
77
Their method, named Zero-shot-CoT, using just this single prompt, greatly
improved performance on various reasoning tasks. For instance, accuracy
on the MultiArith task (a collection of multi-step arithmetic problems)
jumped from 17.7% to 78.7%. The success of this approach across different
tasks suggests that LLMs have untapped potential for zero-shot reasoning.
They believe their findings emphasize the need to explore the vast knowl-
edge within LLMs before creating specific training datasets or examples.
While this approach could help you save some time and effort, it’s not
always accurate.


9 - Auto Chain of Thought
Prompting (AutoCoT)
Large Language Models can reason through problems by breaking them
down into smaller steps. This method, known as chain-of-thought (CoT)
prompting, has two main approaches. The first uses a straightforward
prompt like “Let’s think step by step” to guide the model’s thinking. The
second involves manually creating demonstrations that show a question
and its step-by-step reasoning. While the second approach performs better,
it relies heavily on crafting these demonstrations by hand.
The authors of “Automatic Chain of Thought Prompting in Large Language
Models35” (Zhang, Z., Zhang, A., Li, M., & Smola, A. (2022)) found that by
using the “Let’s think step by step” prompting approach, LLMs can generate
the reasoning steps themselves, though they sometimes make errors. To
improve the quality of these automatically generated steps, they stated
that it’s essential to have diverse questions. They introduced an automated
method, Auto-CoT, which selects diverse questions and then generates the
reasoning steps. In tests with GPT-3 on ten benchmark reasoning tasks,
Auto-CoT performed as well as, or better than, the manual CoT method.
Auto-CoT works using two primary steps to help a language model reason
through problems:
1. Question clustering:
• This stage organizes questions from a dataset36 into groups or “clus-
ters” based on their similarities.
• Each question is transformed into a vector using Sentence-BERT,
which captures its essence in a numerical form.
35https://arxiv.org/abs/2210.03493
36https://github.com/kojima-takeshi188/zero_shot_cot/tree/main/dataset


Auto Chain of Thought Prompting (AutoCoT)
79
• These vectors are then grouped using the k-means clustering algo-
rithm. Questions closer in meaning end up in the same cluster.
2. Demonstration sampling:
• For each cluster, a representative question is chosen.
• The model is then prompted to think step-by-step using the “Let’s
think step by step” prompt to generate a reasoning chain for that
question.
• The goal is to create a demonstration that combines the question with
its reasoning chain.
• There are certain criteria for selecting these demonstrations, such as
the question being short (no more than 60 tokens) and the reasoning
being concise (no more than 5 steps).
After these two primary stages, the demonstrations are utilized to assist
the model in answering test questions. The model is provided with all the
demonstrations and then a test question to answer, using the reasoning
methods it observed in the demonstrations.
Figure 4 from the paper37 illustrates the Auto-CoT process. In simpler
terms, Auto-CoT is akin to teaching the model by example, but instead of
humans creating these examples, the model generates them itself, learning
how to reason step-by-step.
37https://arxiv.org/pdf/2210.03493.pdf


10 - Self-Consistency
GPT-3.5 and similar NLP models are trained using vast text datasets,
enabling them to produce relevant and logical replies based on the training
examples. However, they don’t understand math and logic; they just use
recognized patterns to form answers. In other words, they can’t explain
their reasoning, they just “mix” words to form an eloquent answer. While
the Chain-of-Thought (CoT) method, which prompts the model to explain
its reasoning step-by-step, has shown promise in improving reasoning, it’s
not foolproof. Here’s why:
• Over-reliance on a single path: CoT typically uses a “greedy” ap-
proach, meaning it often sticks to the first, most obvious reasoning
path it finds. This can lead to errors if that path is flawed or if there’s
a better solution it hasn’t considered.
Imagine CoT as a hiker in a vast forest. The moment the hiker sees a path,
instead of exploring the entire forest or searching for alternative routes,
they immediately take the first and most obvious trail they come across.
This might get them to a destination quickly, but there’s no guarantee it’s
the best or most scenic route, and sometimes it might even lead to a dead
end.
• Lack of diversity: Since CoT tends to follow a single line of reasoning,
it might miss out on other valid ways to approach a problem. This
can be especially limiting for complex problems where multiple
perspectives are beneficial.
Still using the hiker metaphor - imagine the forest has many hidden beau-
tiful spots scattered in different areas. Since CoT, our hiker, consistently
chooses the first path they see, they might reach one spot quickly but


Self-Consistency
81
completely miss out on the others. For a hiker who wants to truly under-
stand and experience the richness of the forest’s spots, exploring multiple
trails would be far more beneficial than sticking to just one. Similarly, for
complex problems, considering a range of pathways or perspectives can
lead to more insightful answers.
• Not always optimal: Just because a model can explain its reasoning
doesn’t mean that reasoning is correct. CoT can sometimes lead
to verbose or roundabout explanations that sound logical but are
actually based on incorrect assumptions.
It’s like our hiker who, when asked why they chose a particular path, gives
a lengthy description of the trail markers, the condition of the path, and
the sounds of the birds they heard, making it sound like a well-thought-out
decision. However, they might have missed the clear sign at the trailhead
warning of a bridge out ahead, or the recommendation for a more scenic
route or a beautiful spot. Their explanation might sound detailed and
logical, but it’s rooted in overlooking critical information or misinterpreting
the signs they did see.
So while CoT helps models “show their work”, it doesn’t guarantee that the
work is always correct. Combining it with strategies like self-consistency
can help address some of these limitations. These observations were
presented in Self-consistency Improves Chain of Thought Reasoning in
Language Models38 (Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E.,
Narang, S., Chowdhery, A., & Zhou, D. (2022)).
Self-consistency is a strategy to enhance the model’s reasoning abilities.
Returning to the metaphor we used, our hiker stands at the crossroads of
several trails, each claiming to lead to the most scenic spot in the forest.
Instead of choosing one at random, the hiker consults different maps, asks
other experienced hikers, and even observes where the majority seem to
be headed. If all these sources point to the same trail, the hiker would feel
confident in choosing that path. This verification from multiple sources
embodies the idea of self-consistency in reasoning and decision-making.
38https://arxiv.org/pdf/2203.11171.pdf


Self-Consistency
82
Similarly, if you’re trying to solve a math problem, instead of just using
one method to find the answer, you use several different methods. If all
these methods lead to the same answer, you’d be pretty confident that your
answer is correct. That’s the simplified main idea behind self-consistency.
In technical terms, when a language model is given a problem, instead of
just rushing to the most obvious answer, it explores multiple reasoning
paths. Each path might suggest a different answer. The model then checks
which answer appears most consistently across these paths. Just as humans
have different ways of thinking and approaching problems, this diversity
can be simulated in language models.
The idea is that the more often an answer appears, the more likely it is to
be correct. Here’s how it works:
• Prompt the model: Start by giving the model a question and some
examples of how to reason through it.
• Generate multiple answers: Instead of just getting one answer, let the
model generate several possible reasoning paths.
• Pick the most consistent answer: From the multiple answers the
model comes up with, choose the one that appears most frequently.
When the model generates multiple solutions, it’s like sampling different
paths of reasoning. These paths are then weighed based on their likelihood.
The final answer is chosen based on which answer appears most frequently
among these paths.
When compared to other methods, self-consistency “consistently” per-
formed better. Even in situations where adding a step-by-step reasoning
process might not be beneficial, self-consistency still improved perfor-
mance. In addition, it proved to be better than other popular techniques
like beam search39 and ensemble-based approaches40.
The technique was tested on various tasks and models, and the results were
impressive. When combined with certain models like PaLM-540B or GPT-
3, self-consistency set new performance records on several reasoning tasks.
39https://en.wikipedia.org/wiki/Beam_search
40https://en.wikipedia.org/wiki/Ensemble_learning


Self-Consistency
83
For instance, on the GSM8K task, there was an improvement of 17.9% in
accuracy.
In practice, if we take this question:
If you have 5 apples and eat 2, how many are left?
The model using CoT might use the following reasoning path as a learning
example:
You start with 5 apples. You eat 2 of them. So, 5 minus 2 equals 3 appl\
es. The answer is 3 apples left.
On the other hand, a self-consistency model explores multiple ways of
thinking about a problem to ensure its answer is correct. For the same
question, the model might be prompted to think of different ways to solve
it, such as:
You had 5 apples and after eating 2, you have 3 left
and
Start with 5 apples, and if 2 are gone when eaten, that leaves 3 apples
and
If there were 5 apples and 2 are no longer there because you ate them, \
then 5 minus 2 equals 3 apples remaining.
Since all these different reasoning paths lead to the answer “3 apples”, the
model gains confidence that 3 is the correct answer. So, while CoT provides
a clear breakdown of the thought process, self-consistency cross-checks the
problem in various ways to ensure the reliability of the answer.
When implementing self-consistency, it’s recommended to provide as many
examples as possible. This helps the model explore more reasoning paths


Self-Consistency
84
and increases the chances of finding the correct answer. This file named
“test_socratic.jsonl41” on the OpenAI GitHub repository is a good example.
Let’s ask OpenAI text-davinci-002 the following question:
If there are 3 cars in the parking lot and 2 more cars arrive, 1 car le\
aves, 15 cars arrive and 8 leave, how many cars are in the parking?
This is the Python code:
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
prompt = """
Q: If there are 3 cars in the parking lot and 2 more cars arrive, 1 car\
leaves, 15 cars arrives and 8 leaves, how many cars are in the parking
?"
A:
"""
# the answer should be: 3 + 2 - 1 + 15 - 8 = 11
response = openai.Completion.create(
engine="text-davinci-002",
prompt=prompt,
temperature=0.5,
max_tokens=260
)
print(response.choices[0].text.strip())
The answer is incorrect as it returned:
41https://github.com/openai/grade-school-math/blob/master/grade_school_math/data/test_socratic.jsonl


Self-Consistency
85
There are 18 cars in the parking lot.
To improve the answer, we can use the few-shot examples provided in the
paper42:
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
# Few shot learning to improve the accuracy of the model
prompt = """
Q: There are 15 trees in the grove. Grove workers will plant trees in t\
he grove today. After they are done,
there will be 21 trees. How many trees did the grove workers plant toda\
y?
A: We start with 15 trees. Later we have 21 trees. The difference must \
be the number of trees they planted.
So, they must have planted 21 - 15 = 6 trees. The answer is 6.
Q: If there are 3 cars in the parking lot and 2 more cars arrive, how m\
any cars are in the parking lot?
A: There are 3 cars in the parking lot already. 2 more arrive. Now ther\
e are 3 + 2 = 5 cars. The answer is 5.
Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how ma\
ny pieces do they have left in total?
A: Leah had 32 chocolates and Leah’s sister had 42. That means there we\
re originally 32 + 42 = 74
chocolates. 35 have been eaten. So in total they still have 74 - 35 = 3\
9 chocolates. The answer is 39.
Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has \
12 lollipops. How many lollipops
did Jason give to Denny?
A: Jason had 20 lollipops. Since he only has 12 now, he must have given\
the rest to Denny. The number of
42https://arxiv.org/abs/2203.11171


Self-Consistency
86
lollipops he has given to Denny must have been 20 - 12 = 8 lollipops. T\
he answer is 8.
Q: Shawn has five toys. For Christmas, he got two toys each from his mo\
m and dad. How many toys does
he have now?
A: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toy\
s. Then he got 2 more from dad, so
in total he has 7 + 2 = 9 toys. The answer is 9.
Q: There were nine computers in the server room. Five more computers we\
re installed each day, from
monday to thursday. How many computers are now in the server room?
A: There are 4 days from monday to thursday. 5 computers were added eac\
h day. That means in total 4 * 5 =
20 computers were added. There were 9 computers in the beginning, so no\
w there are 9 + 20 = 29 computers.
The answer is 29.
Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wed\
nesday, he lost 2 more. How many
golf balls did he have at the end of wednesday?
A: Michael initially had 58 balls. He lost 23 on Tuesday, so after that\
he has 58 - 23 = 35 balls. On
Wednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is\
33.
Q: Olivia has $23. She bought five bagels for $3 each. How much money d\
oes she have left?
A: She bought 5 bagels for $3 each. This means she spent 5
Q: If there are 3 cars in the parking lot and 2 more cars arrive, 1 car\
leaves, 15 cars arrives and 8 leaves, how many cars are in the parking
?"
A:
"""
# the answer should be: 3 + 2 - 1 + 15 - 8 = 11
response = openai.Completion.create(
engine="text-davinci-002",
prompt=prompt,


Self-Consistency
87
temperature=0.5,
max_tokens=260
)
print(response.choices[0].text.strip())
The answer is now correct:
There are 3 cars in the parking lot already. 2 more arrive. Now there a\
re 3 + 2 = 5 cars. 1 car leaves. So now there are 5 - 1 = 4 cars. 15 mo
re cars arrive. So now there are 4 + 15 = 19 cars. 8 cars leave. So now
there are 19 - 8 = 11 cars. The answer is 11.


11 - Transfer Learning
11.1 - What Is Transfer Learning?
Transfer learning (TL), by definition, is the enhancement of learning in a
new task through the transfer of knowledge from a related task that has
already been learned. The related task is typically either a task from the
same domain or a task from a different domain that has shared concepts or
shared low-level features.
The concept of transfer learning is not new. In fact, it has been studied in
the field of psychology and behaviorism for over 100 years. It was also
used in pedagogy to teach children how to acquire new skills by building
on what they already know.
Here are some examples of transfer learning in the real world:
• If someone learned to play the piano, they might find it easier to learn
another keyboard instrument like the organ, due to the similarities
between the two instruments.
• A child who’s learned to be wary of a hot stove might also avoid
touching a barbecue grill without being explicitly taught.
• A child who learned to ride a tricycle might find it easier to learn to
ride a bicycle than a child who has never ridden a tricycle.
TL has only recently become a popular topic in the field of machine
learning.
For instance, when applied in image classification, transfer learning can
be used to reuse knowledge gained while solving a problem in one domain
(e.g., recognizing reptiles) to solve a problem in another domain (e.g.,
recognizing amphibians).
