from langchain.chains import create_sql_query_chain
from langchain_community.chat_models import ChatOllama
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# llm = Ollama(
#     model="llama3",
# )  # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `

llm = ChatOllama(model="codellama", temperature=0)

chain = create_sql_query_chain(llm, db)
chain.get_prompts()[0].pretty_print()

print("---------------------------------------------------------------")
response = chain.invoke({"question": "How many employees are there"})
print(response)

# db.run(response) # some errors with Ollama model

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
print(chain.invoke({"question": "How many employees are there"}))

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

print(chain.invoke({"question": "How many employees are there"}))
