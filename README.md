Installation
pip install -r requirements.txt

Environment Variables
Create a ".env" file and set one or more of the following API Keys.
MISTRAL_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

Launch Server
python manage.py runserver

Launch client on browser
http://127.0.0.1:8000

Evaluate Language Models
python evaluate.py

Output of "python evaluate.py" is saved to "report.txt"