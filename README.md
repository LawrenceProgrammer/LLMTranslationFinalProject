**Documentation**

**Purpose of application**

Multilingual Machine Translation using LLM

**The LLM used and why it was chosen**

**GPT-4o and Mistral Large**: They were chosen because they are popular main stream LLMs
which boast good performance on language translation.

**GPT-4o-mini, GPT-3.5, Mistral Small**: This was chosen as a means of comparison with the larger LLMs.

**Dataset details and preprocessing steps**

**Christos-c corpus**

https://christos-c.com/bible/

https://github.com/christos-c/bible-corpus

Running the evaluation automatically downloads the dataset.

**How to use the application**

**Dependency Installation**

pip install -r requirements.txt

**Setting Environment Variables**

Create a ".env" file and set one or more of the following API Keys.

MISTRAL_API_KEY=

OPENAI_API_KEY=

ANTHROPIC_API_KEY=

**Launch Server**

python manage.py runserver

**Launch client on browser**

http://127.0.0.1:8000

**Evaluate Language Models**

python evaluate.py

Output of "python evaluate.py" is saved to "report.txt"

**Any known limitations or future improvements.**

Support for more undocumented/low-resource languages.

More corpus for under-represented languages.
