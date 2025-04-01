from typing import List
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool, tool
from langchain.agents import initialize_agent, AgentType

# Load environment variables (for example, your OpenAI API key)
load_dotenv()

@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length was called with text={text!r}")
    text = text.strip("'\n").strip('"')  # strip away extra quotes/newlines
    return len(text)

if __name__ == "__main__":
    print("Hello ReAct LangChain!")

    # 1) Create the language model
    llm = ChatOpenAI(
        temperature=0,
        # You may need your OpenAI API key in your .env file, for example:
        # OPENAI_API_KEY=YOUR-KEY-HERE
    )

    # 2) Register your tools in a list (we have just one here)
    tools = [get_text_length]

    # 3) Initialize an agent that can use these tools using a ReAct approach
    #    (the "Zero Shot" agent with ReAct-style tool usage)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True  # prints out what the agent is "thinking" and doing
    )

    # 4) Ask your question. The agent will figure out it needs to call the tool.
    #    For example: "What is the length of the string 'Hello world'?"
    question = "What is the length of 'Hello world'?"
    result = agent.run(question)

    # 5) Print the final result
    print("Final Answer:", result)
