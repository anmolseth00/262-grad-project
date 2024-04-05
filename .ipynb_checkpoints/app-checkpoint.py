import streamlit as st
from openai import OpenAI
import requests
import re
import os
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import ArxivRetriever

# OpenAI.api_key = st.secrets["OPENAI_API_KEY"]
# OpenAI.api_key = os.getenv("OPENAI_API_KEY")

#for hardcoding
OpenAI.api_key = ''

client = OpenAI(api_key=OpenAI.api_key)

def enhance_query(original_query):
    prompt = f"""
    Given a natural language query, convert it into a structured search query for the arXiv API. The arXiv API query format uses field prefixes like 'au' for author, 'ti' for title, 'cat' for category, and logical operators like 'AND', 'OR'. Below are examples of converting natural language queries into structured arXiv API queries:

    Here are a few examples:
    
    Natural Language Query: Papers by Albert Einstein about relativity
    Structured arXiv API Query: au:Albert Einstein AND all:relativity

    Natural Language Query: Quantum computing research after 2015
    Structured arXiv API Query: all:quantum computing AND submittedDate:[2015 TO *]

    Natural Language Query: Machine learning applications in finance
    Structured arXiv API Query: all:machine learning AND all:finance

    Now, convert the following natural language query into a structured arXiv API query:
    '{original_query}'
    Structured arXiv API Query:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    # Extracting the structured query from the response
    arxiv_query = response.choices[0].message.content.strip()
    return arxiv_query

def search_arxiv(query):
    url = f'http://export.arxiv.org/api/query?search_query={query}&start=0&max_results=5'
    response = requests.get(url)
    return response.text

def extract_titles_and_summaries(xml_response):
    # Regex patterns to match titles and summaries
    title_pattern = re.compile(r'<title>(.*?)<\/title>')
    summary_pattern = re.compile(r'<summary>(.*?)<\/summary>', re.DOTALL)  # re.DOTALL to match across newlines

    titles = title_pattern.findall(xml_response)
    summaries = summary_pattern.findall(xml_response)

    # The first 'title' match is always "ArXiv Query: ..." so we skip it
    titles = titles[1:]

    # Pairing titles with summaries
    papers_info = [{"title": title, "summary": summary.strip()} for title, summary in zip(titles, summaries)]

    return papers_info

def summarize(initial_query, papers_info):
    prompt = f"The user asked: '{initial_query}'. Based on the following titles and summaries from academic papers, provide a detailed and accessible explanation of the topic:\n\n"
    
    for paper in papers_info:
        prompt += f"Title: {paper['title']}\nSummary: {paper['summary']}\n\n"
    
    prompt += "Please review the titles and summaries to provide a thoughtful response to the user's question."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
    )
    
    thoughtful_response = response.choices[0].message.content.strip()
    return thoughtful_response

def initialize_conversational_chain():
    retriever = ArxivRetriever(load_max_docs=8)
    model = ChatOpenAI(model_name="gpt-3.5-turbo")
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
    return qa

def main():
    st.title("arXiv Summarizer")

    user_query = st.text_input("Enter your search query:", "")
    if user_query:
        arxiv_query = enhance_query(user_query)
        st.write(f"Structured arXiv Query: {arxiv_query}")

        st.write("Fetching papers from arXiv...")
        arxiv_results = search_arxiv(arxiv_query)
        extracted_information = extract_titles_and_summaries(arxiv_results)

        thoughtful_response = summarize(user_query, extracted_information)
        st.write("Summary of Findings:")
        st.write(thoughtful_response)


if __name__ == "__main__":
    main()
