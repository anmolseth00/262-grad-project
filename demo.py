#demo file to be run in command line, combining both files before it if possible
from openai import OpenAI
import requests
import re
import os

OpenAI.api_key = ''
#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

def suggest_research_directions(initial_query, thoughtful_response):
    """
    Generates novel research directions based on the user's feedback on a provided summary
    and their specific interests.

    Parameters:
    - initial_query: The original query posed by the user.
    - thoughtful_response: A comprehensive response to the initial query, summarizing relevant
      academic papers and insights.

    Returns:
    - A string containing suggestions for research trends, gaps, next steps, or future directions.
    """

    print("\n--- Research Direction Suggestion ---")
    user_feedback = input("What are your thoughts on the provided summary? Any specific areas of interest or questions that arise? ")

    research_interests = input("Could you specify any particular research interests or areas where you're seeking innovation? ")
    
    prompt = f"""
    Based on the initial inquiry about '{initial_query}' and the provided summary, the researcher shared their thoughts: '{user_feedback}'. They expressed a particular interest in '{research_interests}'.

    Considering the current state of research and potential future developments, identify emerging trends, and gaps in the literature, and suggest novel research directions or next steps that could significantly advance the field. Emphasize novelty and innovation in your suggestions.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
    )

    research_suggestions = response.choices[0].message.content.strip()
    return research_suggestions




def main():
    from langchain.chains import ConversationalRetrievalChain
    from langchain_openai import ChatOpenAI
    from langchain_community.retrievers import ArxivRetriever

    if OpenAI.api_key == '':
        print("OpenAI API key is currently empty, please code in your OpenAI API key at the top of demo.py")
        #OpenAI.api_key = input("Please enter your OpenAI API key: ")
   

    os.environ["OPENAI_API_KEY"] = OpenAI.api_key
        
    
    user_query = input("Enter your search query: ")
    print("Converting your query into an arXiv-friendly format...")
    arxiv_query = enhance_query(user_query)
    #inserrt langchain retriever here
    print(f"Here is the arXiv Query I am using: {arxiv_query}\nFetching papers from arXiv...")
    arxiv_results = search_arxiv(arxiv_query)
    extracted_information = extract_titles_and_summaries(arxiv_results)
    # print(extracted_information)
    retriever = ArxivRetriever(load_max_docs=8)
    docs = retriever.get_relevant_documents(query=arxiv_query)
    model = ChatOpenAI(model_name="gpt-3.5-turbo")  # switch to 'gpt-4'
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)


    thoughtful_response = summarize(user_query, extracted_information)
    print("Here's what I found:\n", thoughtful_response)
    #give choices to user to ask for suggestions, ask questions from langchain, or end the program
    next_step = input("Would you like to ask a question or receive research suggestions based on this summary? (Question/Research): ")
    if next_step.lower() == "question":
        b = False
        for i in range(4):
            if b:
                break
            print("Please ask your question:")
            question = input()
            # answer = qa(user_question)
            # print("Answer:", answer)
            chat_history = []
            result = qa({"question": question, "chat_history": chat_history})
            chat_history.append((question, result["answer"]))
            print(f"-> **Question**: {question} \n")
            print(f"**Answer**: {result['answer']} \n")
            if i == 2:
                print("You have reached the maximum number of questions for this query.")
            b = input("Do you have any more questions? (yes/no): ").lower() == "no"
    elif next_step.lower() == "research":
        research_suggestions = suggest_research_directions(user_query, thoughtful_response)
        print("Here are a few research ideas to inspire your work:\n", research_suggestions)
    else:
        print("Answer did not match, please run the program and try again!")
    #research_suggestions = suggest_research_directions(user_query, thoughtful_response)
    #print("Here are a few research ideas to inspire your work:\n", research_suggestions)

if __name__ == "__main__":
    main()
