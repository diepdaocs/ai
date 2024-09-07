import asyncio
import os

from langchain_community.tools import TavilySearchResults
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"

search = TavilySearchResults(max_results=3)
# search_results = search.invoke("What is the weather in Singapore?")
# print(search_results)

tools = [search]

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]
# ai_msg = llm.invoke(messages)
# print(ai_msg)

# Chain
# from langchain_core.prompts import ChatPromptTemplate
#
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful assistant that translates {input_language} to {output_language}.",
#         ),
#         ("human", "{input}"),
#     ]
# )
#
# chain = prompt | llm
# response = chain.invoke(
#     {
#         "input_language": "English",
#         "output_language": "German",
#         "input": "I love programming.",
#     }
# )
# print(response)

from langchain_core.messages import HumanMessage

# response = llm.invoke([HumanMessage(content="hi!")])
# print(response.content)

# model_with_tools = llm.bind_tools(tools)
# response = model_with_tools.invoke([HumanMessage(content="What is the weather in Singapore?")])
#
# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")

from langgraph.prebuilt import create_react_agent

memory = MemorySaver()
agent_executor = create_react_agent(model=llm, tools=tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}


# response = agent_executor.invoke({"messages": [HumanMessage(content="What is the weather in Singapore?")]})
# print(response["messages"])
# for chunk in agent_executor.stream({"messages": [HumanMessage(content="whats the weather in sf?")]}):
#     print(chunk)
#     print("----")

async def test_async():
    async for event in agent_executor.astream_events(
            input={"messages": [HumanMessage(content="whats the weather in Singapore?")]},
            version="v1",
            config=config
    ):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                    event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print(
                    f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                )
        elif kind == "on_chain_end":
            if (
                    event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print()
                print("--")
                print(
                    f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                )
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                print(content, end="|")
        elif kind == "on_tool_start":
            print("--")
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")


asyncio.run(test_async())
