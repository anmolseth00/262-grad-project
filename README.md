# 262-grad-project

## Files in this Repository:
demo.py: Python script combining the proof of concept and langchain conversation features into a script that can be run entirely from command line. Allows users to make queries and then either ask questions about the results or receive research suggestions or other insights from the GPT API.

MVP.ipynb: Proof of concept notebook for the arXiv API and using GPT to make queries based on user input


## Environment and Setup Details:
Python 3

A Python Environment (here a conda virtual environment)

streamlit

**REQUIRED:** An OpenAI API private key

* You can find / make an API key here: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
* A few tips on keeping your API key protected can be found [here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)

### Usage
* Create a venv: `python3 -m venv venv`
* Active the venv: `source venv/Scripts/activate`
* Install requirements: `pip install -r requirements.txt`

* Use this command: `streamlit run streamlit.py`

## References
* [arXiv API](https://info.arxiv.org/help/api/index.html)
* [langchain](https://python.langchain.com/docs/integrations/retrievers/arxiv/)
* [streamlit](https://streamlit.io/)
