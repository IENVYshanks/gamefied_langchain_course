from langchain.agents import create_agent

agent = create_agent(model='ollama:Qwen2.5:0.5b',system_prompt="You are a helpful assistant. Be concise and accurate.")
query = "what is the capital of india ?"
result = agent.invoke(
    {"messages": [{"role": "user", "content": query}]},
    
)
response = result["messages"][-1].content
print(response)