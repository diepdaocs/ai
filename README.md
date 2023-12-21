# AI / ML

Play around the latest AI technologies

# Run LLM local server

- Download model into `data/models`: https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF#provided-files
- Start the model Api: `sh llm/server.sh`

# Web

- Get the OpenAI key (if you are not running the model locally): https://platform.openai.com/api-keys
- Open `web/index.html`: fill in the `chatGPTKey` or without key by
  uncomment `const OPEN_AI_ENDPOINT = 'http://localhost:8000/v1'`
- Run: `python -m http.server 8000`
- Open: http://localhost:8000
