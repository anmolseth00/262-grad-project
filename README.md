# 262-grad-project

## Files in this Repository:
`demo.py`: Python script combining the proof of concept and langchain conversation features into a script that can be run entirely from the command line. Allows users to make queries and then either ask questions about the results or receive research suggestions or other insights from the GPT API.

`MVP.ipynb`: Proof of concept notebook for the arXiv API and using GPT to make queries based on user input

`app.py`: Proof of concept for a streamlit-based UI. It only has summarization capabilities at the moment.

## Environment and Setup Details:
Python 3

A Python Environment (here a conda virtual environment)

streamlit

**REQUIRED:** An OpenAI API private key

* You can find / make an API key here: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
* A few tips on keeping your API key protected can be found [here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)

### Usage
* Create a virtual environment called venv: `python3 -m venv venv`
* Active the virtual environment: `source venv/Scripts/activate`
* Install requirements: `pip install -r requirements.txt`

* Use this command: `streamlit run app.py`

## References
* [arXiv API](https://info.arxiv.org/help/api/index.html)
* [langchain](https://python.langchain.com/docs/integrations/retrievers/arxiv/)
* [streamlit](https://streamlit.io/)
