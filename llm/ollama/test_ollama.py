from langchain_community.llms import Ollama

llm = Ollama(
    model="calebfahlgren/natural-functions"
)  # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `

print(llm.invoke("Tell me a joke"))

