from typing import List

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool
def validate_user(user_id: int, addresses: List[str]) -> bool:
    """Validate user using historical addresses.

    Args:
        user_id (int): the user ID.
        addresses (List[str]): Previous addresses as a list of strings.
    """
    print("Validating user", user_id, "with addresses", addresses)
    return False


llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

llm_with_tools = llm.bind_tools([validate_user])

notool_result = llm.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX."
)
print(notool_result.tool_calls)
print(notool_result.content)

result = llm_with_tools.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX."
)

print(result.tool_calls)
print(result.content)

from langgraph.prebuilt import create_react_agent

tools = [validate_user]
agent_executor = create_react_agent(llm, tools)

response = agent_executor.invoke(
    {
        "messages": [HumanMessage(content=
                                  "Could you validate user 123? They previously lived at "
                                  "123 Fake St in Boston MA and 234 Pretend Boulevard in "
                                  "Houston TX.")
                     ]
    }
)

for message in response["messages"]:
    print(message)
