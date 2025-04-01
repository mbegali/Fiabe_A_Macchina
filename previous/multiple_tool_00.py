from typing import List
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool, tool
from langchain.agents import initialize_agent, AgentType

# Load environment variables (for example, your OpenAI API key)
load_dotenv()

# Define Tool 1: Get Text Length
@tool
def get_text_length(text: str) -> int:
    """Returns the number of characters in a given text."""
    print(f"get_text_length was called with text={text!r}")
    return len(text)

# Define Tool 2: Count Words
@tool
def count_words(text: str) -> int:
    """Returns the number of words in a given text."""
    print(f"count_words was called with text={text!r}")
    return len(text.split())

# Define Tool 3: Reverse Text
@tool
def reverse_text(text: str) -> str:
    """Reverses the given text."""
    print(f"reverse_text was called with text={text!r}")
    return text[::-1]

if __name__ == "__main__":
    print("Hello, Multi-Tool Agent!")

    # 1) Create the language model
    llm = ChatOpenAI(temperature=0)

    # 2) Register the tools
    tools = [get_text_length, count_words, reverse_text]

    # 3) Initialize the agent with multiple tools
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True  # Show the agent's thought process
    )

    # 4) Ask a question (the agent will choose the correct tool)
    questions = [
        
        "write the reverse of Langchain'"
    ]

    for question in questions:
        print("\nUser Question:", question)
        result = agent.run(question)
        print("Final Answer:", result)
