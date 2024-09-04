from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print(db.run(
    "SELECT COUNT(*) FROM Employee"
))
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm = ChatOllama(model="llama3", temperature=0)
agent_executor = create_sql_agent(llm, db=db, verbose=True)

agent_executor.invoke(
    {
        "input": "Describe the playlisttrack table"
    }
)
